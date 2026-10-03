#!/usr/bin/env python3
"""Check the local audio/CUDA environment using synthetic inputs, without downloads.

This is an installation check, not a CEL implementation or a research experiment.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import traceback


ROOT = Path(__file__).resolve().parents[1]


def command(*args):
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT).strip()


def check(report):
    import librosa
    import numpy as np
    import soundfile as sf
    import torch
    import torchaudio
    from sklearn.metrics import average_precision_score
    from transformers import WavLMConfig, WavLMModel

    packages = [
        "torch", "torchaudio", "transformers", "numpy", "scipy",
        "scikit-learn", "pandas", "matplotlib", "librosa", "soundfile",
        "PyYAML", "tqdm", "pytest", "ipykernel", "huggingface-hub",
    ]
    report["packages"] = {p: importlib.metadata.version(p) for p in packages}
    report["ffmpeg"] = command("ffmpeg", "-version").splitlines()[0]
    report["ffprobe"] = command("ffprobe", "-version").splitlines()[0]
    report["nvidia_smi"] = command(
        "nvidia-smi", "--query-gpu=name,driver_version,memory.total,memory.free",
        "--format=csv,noheader",
    )
    report["checks"]["dependency_consistency"] = command(
        sys.executable, "-m", "pip", "check"
    )
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is unavailable in this Python environment")

    torch.set_num_threads(4)
    torch.manual_seed(0)
    device = torch.device("cuda:0")
    props = torch.cuda.get_device_properties(device)
    report["cuda"] = {
        "torch_cuda_runtime": torch.version.cuda,
        "device": props.name,
        "compute_capability": list(torch.cuda.get_device_capability(device)),
        "total_memory_bytes": props.total_memory,
        "cudnn": torch.backends.cudnn.version(),
    }
    a = torch.ones(128, 128, device=device)
    if not torch.equal(a @ a, torch.full_like(a, 128)):
        raise RuntimeError("CUDA matrix multiplication returned an incorrect result")
    report["checks"]["cuda_matmul"] = "PASS"
    del a

    with tempfile.TemporaryDirectory(prefix="cel-env-") as tmp:
        tmp = Path(tmp)
        rate = 16000
        signal = (0.1 * np.sin(2 * np.pi * 440 * np.arange(rate) / rate)).astype(np.float32)
        wav = tmp / "synthetic.wav"
        sf.write(wav, signal, rate, subtype="PCM_16")
        restored, sr = sf.read(wav, dtype="float32")
        if sr != rate or len(restored) != rate or np.max(np.abs(restored - signal)) > 1e-4:
            raise RuntimeError("SoundFile WAV round-trip failed")
        opus = tmp / "synthetic.opus"
        command("ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(wav),
                "-c:a", "libopus", "-b:a", "32k", str(opus))
        decoded = tmp / "decoded.wav"
        command("ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(opus),
                "-ar", str(rate), "-ac", "1", str(decoded))
        decoded_audio, decoded_sr = sf.read(decoded)
        if decoded_sr != rate or len(decoded_audio) != rate or not np.isfinite(decoded_audio).all():
            raise RuntimeError("FFmpeg Opus round-trip failed")
        probe = json.loads(command("ffprobe", "-v", "error", "-show_entries",
                                  "stream=codec_name,sample_rate,channels", "-of", "json", str(opus)))
        ta = torchaudio.functional.resample(torch.from_numpy(signal), rate, 8000)
        lb = librosa.resample(signal, orig_sr=rate, target_sr=8000)
        if ta.numel() != 8000 or len(lb) != 8000:
            raise RuntimeError("Audio resampling length check failed")
        report["checks"]["audio_io_and_resampling"] = {
            "status": "PASS", "wav_samples": rate, "opus": probe["streams"],
            "torchaudio_samples": ta.numel(), "librosa_samples": len(lb),
        }

    # Base architecture, random weights: validates WavLM code/CUDA, not pretrained quality.
    config = WavLMConfig(
        hidden_size=768, num_hidden_layers=12, num_attention_heads=12,
        intermediate_size=3072, apply_spec_augment=False,
    )
    model = WavLMModel(config).eval().requires_grad_(False).to(device)
    waveform = torch.randn(1, 32000, device=device) * 0.01
    torch.cuda.reset_peak_memory_stats(device)
    torch.cuda.synchronize()
    start = time.perf_counter()
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.float16):
        features = model(waveform).last_hidden_state
    torch.cuda.synchronize()
    if features.shape[0] != 1 or features.shape[-1] != 768 or not torch.isfinite(features).all():
        raise RuntimeError("WavLM synthetic forward check failed")
    report["checks"]["wavlm_random_weight_forward"] = {
        "status": "PASS", "pretrained_weights": False, "input_seconds": 2,
        "batch_size": 1, "parameter_count": sum(p.numel() for p in model.parameters()),
        "feature_shape": list(features.shape),
        "forward_seconds_including_first_call_overhead": time.perf_counter() - start,
        "peak_allocated_bytes": torch.cuda.max_memory_allocated(device),
        "peak_reserved_bytes": torch.cuda.max_memory_reserved(device),
    }
    del model, waveform, features
    torch.cuda.empty_cache()

    # A small convolutional head exercises AMP/backprop/AdamW only; not the formal TCN.
    layers = [torch.nn.Conv1d(768, 256, 1)]
    for dilation in (1, 2, 4):
        layers += [torch.nn.Conv1d(256, 256, 3, padding=dilation, dilation=dilation),
                   torch.nn.GELU(), torch.nn.Dropout(0.1)]
    layers.append(torch.nn.Conv1d(256, 1, 1))
    head = torch.nn.Sequential(*layers).to(device)
    optimizer = torch.optim.AdamW(head.parameters(), lr=1e-4, weight_decay=1e-2)
    scaler = torch.amp.GradScaler("cuda")
    x = torch.randn(2, 768, 250, device=device)
    target = torch.rand(2, 1, 250, device=device)
    before = head[-1].weight.detach().clone()
    torch.cuda.reset_peak_memory_stats(device)
    with torch.autocast("cuda", dtype=torch.float16):
        loss = torch.nn.functional.binary_cross_entropy_with_logits(head(x), target)
    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    if not torch.isfinite(loss) or not all(
        p.grad is not None and torch.isfinite(p.grad).all() for p in head.parameters()
    ):
        raise RuntimeError("Synthetic head training produced non-finite loss/gradients")
    scaler.step(optimizer)
    scaler.update()
    torch.cuda.synchronize()
    if torch.equal(before, head[-1].weight):
        raise RuntimeError("Optimizer did not update the head parameters")
    report["checks"]["synthetic_head_amp_backward_adamw"] = {
        "status": "PASS", "optimizer_steps": 1, "micro_batch": 2,
        "feature_frames": 250, "loss": loss.item(),
        "peak_allocated_bytes": torch.cuda.max_memory_allocated(device),
        "peak_reserved_bytes": torch.cuda.max_memory_reserved(device),
    }
    if average_precision_score([0, 1, 0, 1], [0.1, 0.9, 0.2, 0.8]) != 1.0:
        raise RuntimeError("Scikit-learn binary AP smoke check failed")
    report["checks"]["binary_ap_library_smoke"] = "PASS"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/environment/local_environment.json")
    args = parser.parse_args()
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "synthetic installation check; no dataset or pretrained model download",
        "status": "RUNNING", "python": sys.version, "executable": sys.executable,
        "platform": platform.platform(), "project_root": str(ROOT),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checks": {},
    }
    lock = ROOT / "requirements/local-cu128.lock.txt"
    report["environment_lock_sha256"] = (
        hashlib.sha256(lock.read_bytes()).hexdigest() if lock.exists() else None
    )
    try:
        check(report)
        report["status"] = "PASS"
    except Exception:
        report["status"] = "FAIL"
        report["error"] = traceback.format_exc()
    report["disk_free_bytes"] = {
        str(p): shutil.disk_usage(p).free for p in (ROOT, Path("/mnt/d")) if p.exists()
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
