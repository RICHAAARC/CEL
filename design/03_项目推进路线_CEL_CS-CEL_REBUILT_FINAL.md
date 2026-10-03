# 03_项目推进路线：CEL / CS-CEL 重构冻结执行协议

> 上游算法原语：`01_算法原语设计_CEL_CS-CEL.md`  
> 上游方法合同：`02_方法实现机制设计_CEL_CS-CEL_REBUILT_FINAL.md`  
> 文档职责：把冻结算法原语与重构后的方法合同转换为一套完整、可终止、抗 route-shopping、具有预注册 power 的执行协议。  
> 文档层级：**Project Execution Manual / Pre-registration Protocol / Evidence SOP**  
> 状态：**REBUILT-FINAL / 01-02-ALIGNED / PRE-RUN-CONFIGURATION-REQUIRED**

> 修订：2026-10-03，实施前修订 v1.2。落实独立审计发现的指标、网格、统计与判决缺口，并增加失败账本、文献驱动的新路线及版本隔离流程。正式研究尚未运行；真实数据、模型revision和所属阶段配置落实后才具备运行条件。

---

# 0. 执行总原则

本协议不采用“线性跑完所有模块再看结果”的工程路线，而采用：

\[
\boxed{
\text{Cheap Screen}
\rightarrow
\text{Premise}
\rightarrow
\text{Parallel Feasibility Tracks}
\rightarrow
\text{Power-Locked Mechanism Test}
\rightarrow
\text{Real Strength}
\rightarrow
\text{CS Extension}.
}
\]

其中：

1. Stage P 只负责资源筛查，不产生 F1–F7 formal claim；
2. F1 / F2 先证明算法语义前提；
3. Localizer 与 W/R 在 premise 之后允许并行，W/R 作为最高风险 gate 可优先；
4. F4/F5/F6 前必须完成 formal power lock；
5. formal test 解封后禁止为了结果切 route、换 comparator、换 feature tap、改 threshold；
6. 每个失败状态必须有合法终点，不允许出现“既不能继续、又没有 Outcome”的死路；
7. `OPERATIONAL_SCOPE_REFUTED` 与“某个 locked realization 外部失败”严格区分。

---

# 1. 单一真值源

唯一权威关系：

```text
01 → F1–F7 semantic；
02 → M0–M6、M3′、O2/O3′/O4/O5、L/W/R/N、exact math、control semantics；
03 → stages、data、numbers、statistics、power、decisions、locks、execution。
```

formal implementation 必须记录：

```text
01 primitive hash；
02 method-contract hash；
03 protocol hash。
```

任何文档或代码不得重新定义上游对象。

---

# 2. Canonical Status Registry

全文不得使用未登记 scientific / route status。

## 2.1 Screen verdict

```text
SCREEN_PROMISING
SCREEN_INCONCLUSIVE
SCREEN_NONPROMISING
```

## 2.2 F1 / F2 verdict

```text
SUPPORTED
INCONCLUSIVE
PREMISE_REFUTED
```

## 2.3 F3 verdict

```text
SUPPORTED
INCONCLUSIVE
OPERATIONAL_REALIZATION_FAILED
OPERATIONAL_SCOPE_REFUTED
```

语义区别：

```text
OPERATIONAL_REALIZATION_FAILED：
  已锁定并通过双层 qualification 的具体 W/R realization 在正式独立 Corr-Test 上明确失败；
  当前 protocol 终止，不允许在同一 formal evidence 版本中切换 route；
  不声称所有可能 W/R route 已被证伪。

OPERATIONAL_SCOPE_REFUTED：
  W-A/B/C/D 按冻结顺序在 formal lock 前全部被独立 qualification 明确 REJECTED；
  对当前预注册 operational family，F3 scope 被证伪。
```

## 2.4 F4 / F5 / F6 / F7 verdict

```text
SUPPORTED
INCONCLUSIVE
PRACTICAL_NULL
```

## 2.5 Route / W-R candidate verdict

```text
QUALIFIED
INCONCLUSIVE
REJECTED
REJECTED_EXTERNAL
```

其中 `REJECTED_EXTERNAL` 只允许用于 formal Corr-Test 尚未解封前的第二层 qualification。

## 2.6 R-0 eligibility

```text
ELIGIBLE
INELIGIBLE
INCONCLUSIVE
```

## 2.7 Localizer verdict

```text
LOCALIZER_SUPPORTED
LOCALIZER_INCONCLUSIVE
LOCALIZER_UNUSABLE
```

## 2.8 Guardrail verdict

```text
PASS
FAIL
INCONCLUSIVE
```

## 2.9 Protocol / run status

```text
VALID
INVALID_FOR_FORMAL_EVIDENCE
INVALID_IMPLEMENTATION
POWER_INFEASIBLE
PRECISION_INFEASIBLE
```

---

# 3. Scope Registry 与继承规则

每个 formal scientific verdict 必须绑定：

```text
CTRL
REAL:<family>
REAL:MULTI:<family-set-hash>
```

定义：

\[
\mathrm{Scope}(F_k).
\]

禁止跨 scope 拼接。

Strong Real CEL 必须：

\[
\boxed{
\mathrm{Scope}(F1)
=
\mathrm{Scope}(F2)
=
\mathrm{Scope}(F3)
=
\mathrm{Scope}(F4)
=
\mathrm{Scope}(F5)
=
\mathrm{Scope}(F6)
=
\mathrm{Scope}(Stage5).
}
\]

若 F4/F5/F6 仅在 CTRL scope 支持，则只能形成 Controlled Mechanism CEL；real-chain 结果最多作为 exploratory transfer。

---

# 4. 重构后的项目状态机

```text
Stage P0  Controlled Transport Sanity
    ↓
Stage P1  Minimal Localizer
    ↓
Stage P2  Oracle O2/O3′/O4/O5 Screen
    ↓
Stage P3  U-REF Admissible Error Sweep
    ↓
──────── PRE-FORMAL RESOURCE GATE ────────
    ↓ only if SCREEN_PROMISING
Stage 0A  Real Reference Feasibility + Early Collection Checkpoint
    ↓
Stage 0B  Global Formal Protocol Freeze
    ↓
Stage 1   Formal F1 / F2 Premise Audit
    ↓
┌───────────────────────────────┬────────────────────────────────┐
│ Track L — Localizer           │ Track C — Correspondence       │
│ Stage 2D → 2L → 2T            │ Stage 3D → 3Q-A → 3Q-B → 3L → 3T │
└───────────────────────────────┴────────────────────────────────┘
    ↓ merge only if LOCALIZER_SUPPORTED AND F3=SUPPORTED
Stage 4D  M2 / M3′ / M4 / M5 Development
    ↓
Stage 4P  Mechanism Power / Precision Lock
    ↓
Stage 4L  Mechanism Lock
    ↓
Stage 4T  F4 / F5 / F6 Formal Test
    ↓
────────── NOVELTY KILL GATE ──────────
    ↓ only if F4=F5=F6 SUPPORTED
Stage 5T  Frozen Real-Chain Evaluation
    ↓
Stage 6D  CS Development
    ↓
Stage 6L  CS Lock
    ↓
Stage 6T  F7
    ↓
Stage 7   Frozen Evidence Package
```

## 4.1 并行原则

Stage 2 与 Stage 3 在 F1/F2 同 scope 支持后可以并行。

优先级上，Stage 3 是高风险 critical path；资源受限时允许先执行 Stage 3。LOCALIZER_UNUSABLE 不应使已经启动的 Stage 3 自动失效，但会阻断 Stage 4。

## 4.2 Formal Corr-Test 的唯一位置

W/R route switching 只允许发生在 Stage 3Q-A / 3Q-B，且 Corr-Test 尚未解封时。

一旦 Stage 3L 锁定并解封 Stage 3T：

\[
\boxed{\text{禁止切换 W/R route}.}
\]

这保证 route selection 与 final external validation 分离。

---

# 5. 数据 Partition

## 5.1 Stage P

\[
D_{\mathrm{screen-train}},
\qquad
D_{\mathrm{screen-dev}}.
\]

screen source identity 永远不得进入 formal test。

## 5.2 Premise

\[
D_{\mathrm{premise-ctrl}},
\qquad
D_{\mathrm{premise-real}}.
\]

## 5.3 Localizer

\[
D_{\mathrm{loc-train}},
\quad
D_{\mathrm{loc-dev}},
\quad
D_{\mathrm{loc-test}}.
\]

## 5.4 Correspondence

\[
D_{\mathrm{corr-dev}},
\quad
D_{\mathrm{corr-qual-A}},
\quad
D_{\mathrm{corr-qual-B}},
\quad
D_{\mathrm{corr-test}}.
\]

A/B 必须 source-identity disjoint。

## 5.5 Mechanism

\[
D_{\mathrm{mech-train}},
\quad
D_{\mathrm{mech-dev}},
\quad
D_{\mathrm{mech-test}}.
\]

Stage 4P 只使用 `D_mech-dev` 估计 variance / required n；不得读取 `D_mech-test` effect。

## 5.6 Real-chain

```text
D_real-train；
D_real-dev；
D_real-formal-seen；
D_real-formal-unseen。
```

## 5.7 CS

\[
D_{\mathrm{cs-dev}},
\quad
D_{\mathrm{cs-test}}.
\]

另登记 \(D_{\mathrm{cs-train}}\)。默认继承同scope的 \(D_{\mathrm{mech-train}}\) 身份清单，不能使用任何dev、qualification或test身份作CS训练；cs-dev / cs-test分别与训练身份隔离，且不复用已读取效果的formal test。CEL控制和CS分支共用同一cs-train清单。

## 5.8 Source-identity leakage

同一 source utterance 的 codec、noise、RTC、re-recording、speed、deletion、jitter、augmentation、perturbation realization 必须继承同一上层 split identity。

---

# 6. Seal / Lock

formal partitions 必须 seal：

```text
configs/seals/
├── premise_ctrl.seal.json
├── premise_real.seal.json
├── loc_test.seal.json
├── corr_qual_A.seal.json
├── corr_qual_B.seal.json
├── corr_test.seal.json
├── mech_test.seal.json
├── real_formal.seal.json
└── cs_test.seal.json
```

locks：

```text
configs/locks/
├── stage0_protocol.lock.yaml
├── stage2_localizer.lock.yaml
├── stage3_correspondence.lock.yaml
├── stage4_power.lock.yaml
├── stage4_mechanism.lock.yaml
└── stage6_cs.lock.yaml
```

任何 formal partition 提前读取：

\[
\boxed{\text{INVALID_FOR_FORMAL_EVIDENCE}.}
\]

---

# 7. Global Numeric Registry

所有正式数值只在：

```text
configs/protocol_vFINAL_global.yaml
```

出现一次。

## 7.1 Output grid 与数值稳定

```yaml
output_grid_ms: 20

numerical:
  epsilon_D: 1.0e-8
  epsilon_h: 1.0e-8
  smooth_l1_beta: 1.0
```

## 7.2 Stage P 固定模型配置

```yaml
screen_model:
  backbone_model_id: microsoft/wavlm-base-plus
  backbone_frozen: true
  feature_cache_required: true
  head:
    type: tcn
    hidden_dim: 256
    input_projection: linear_to_hidden_dim
    feature_to_output_grid: physical_center_linear_with_endpoint_clamp_before_head
    kernel_size: 3
    dilations: [1, 2, 4]
    blocks: 3
    activation: gelu
    dropout: 0.10
    output: sigmoid_scalar_per_time_cell
  optimizer:
    type: adamw
    learning_rate: 1.0e-4
    weight_decay: 1.0e-2
  effective_batch_size: 32
  p1_train_steps: 1500
  variant_train_steps: 1000
  lambda_BCE: 1.0
  lambda_Dice: 1.0
  lambda_id: 1.0
  lambda_AS_match: 1.0
  lambda_feat: 1.0
  lambda_CEL: 1.0
  initialization:
    variants_from_same_seed_P1_checkpoint: true
```

Stage P frozen backbone 必须预提取并缓存 feature；缓存只属于算力优化，不改变科学语义。

## 7.3 Stage P budget

```yaml
screen:
  min_pairs_per_family: 48
  localizer_min_mixed_partial: 96
  screen_seeds: 2
  localizer_auprc_excess_min: 0.05
  correspondence_error_levels_ms: [0, 20, 40, 80]
  perturbation_target_tolerance_ms: 2
  epsilon_screen: 0.005
  max_total_screen_model_runs: 28
```

P2/P3 的 formal screen comparator 为 O2/O3′/O4/O5。`localizer_min_mixed_partial`指screen-dev中至少96个独立source utterance的mixed-partial可评价实例；`min_pairs_per_family`指每family至少48个usable dev pairs，同一母音频的多个窗口不增加独立身份数。训练规模单独记录，不能与dev数量相加凑下限。

## 7.4 C0 time-preserving baseline

```yaml
c0_time_preserving:
  max_label_grid_error_cells: 1.0
  max_unmatched_fraction: 0.0
```

## 7.5 Main effect sizes

```yaml
effect_sizes:
  epsilon_main: 0.01
  epsilon_real: 0.01
  epsilon_cs: 0.005
```

## 7.6 Reference feasibility

```yaml
reference:
  dense:
    uncertainty_p50_ms: 10
    uncertainty_p90_ms: 20
    coverage_min: 0.95
  sparse:
    uncertainty_p50_ms: 40
    uncertainty_p90_ms: 100
    min_landmarks_per_pair: 5
    min_temporal_span_fraction: 0.60
    min_usable_pair_fraction_per_family: 0.80
  early_checkpoint_pairs_per_family: 150
```

Stage 0A 必须先完成 early checkpoint，reference quality 未达标时不得直接投入 Stage 5 大规模采集。

## 7.7 F1 / F2 constants

```yaml
premise:
  occupancy_boundary_threshold: 0.50

premise_f1:
  boundary_displacement_cells: 1.0
  task_unmatched_fraction: 0.05
  meaningful_pair_fraction: 0.20
  min_supported_real_families_for_multi_claim: 2

premise_f2:
  dense:
    median_occupancy_error_max: 0.03
    p90_occupancy_error_max: 0.10
    median_segment_iou_min: 0.95
  sparse:
    median_segment_iou_min: 0.90
```

## 7.8 Localizer

```yaml
localizer_dev:
  auprc_partial_min: 0.80
  segment_f1_min: 0.65
  boundary_mae_ms_max: 100

localizer_formal:
  auprc_excess_supported: 0.10
  auprc_excess_refuted: 0.05
  segment_f1_supported: 0.40
  segment_f1_refuted: 0.30
  boundary_mae_supported_ms: 250
  boundary_mae_refuted_ms: 300
```

## 7.9 W qualification

```yaml
w_controlled:
  p50_ms: 20
  p90_ms: 60
  coverage: 0.90

w_real_floor:
  p50_ms: 40
  p90_ms: 100
  coverage: 0.80

corr_precision:
  p50_ci_halfwidth_max_ms: 10
  p90_ci_halfwidth_max_ms: 20
  coverage_ci_halfwidth_max: 0.05
```

real dense / sparse thresholds 仍由 reference uncertainty 派生：

\[
T_{50}^{real}=\max(40ms,2U_{50}^{ref}),
\]

\[
T_{90}^{real}=\max(100ms,2U_{90}^{ref}).
\]

## 7.10 Reliability / R-0

```yaml
reliability:
  spearman_point_max: -0.30
  top_quartile_gain_point_min: 0.25

r0:
  controlled_q95_ms: 60
  sparse_only_strong_trust: forbidden
```

## 7.11 Formal minimums 与 caps

```yaml
minimums:
  premise_pairs_per_family: 100
  loc_test_mixed_partial: 300
  loc_test_bona_fide_if_available: 100
  loc_test_fully_manipulated_if_available: 100

  corr_qual_A_total: 300
  corr_qual_B_total: 300
  corr_test_controlled_total: 600
  corr_real_pairs_per_family_initial: 200
  corr_authenticity_stratum_min: 50
  corr_pairs_per_family_cap: 400

  mech_test_initial: 300
  mech_test_major_family_min: 100
  mech_test_cap: 1500

  real_formal_initial: 2000
  real_formal_per_major_family: 300
  real_formal_cap: 3000

  cs_test_initial_informative_pairs: 100
  cs_test_cap_informative_pairs: 500
```

## 7.12 Formal seeds 与 inference hierarchy

```yaml
formal:
  seeds: 5
  bootstrap_replicates: 10000
  primary_resampling_unit: source_utterance
  seed_handling: fixed_strata_then_seed_average
```

主 inference 不对 5 个 seed 做 bootstrap。

对每个 source utterance \(u\) 与 mechanism difference \(\Delta\)，先计算固定 5 seeds 的平均 paired difference：

\[
\bar\Delta_u
=
\frac{1}{S}\sum_{s=1}^{S}\Delta_{u,s}.
\]

线性primary差量的CI/p-value对 \(\bar\Delta_u\) 作source-utterance cluster bootstrap；REAL:MULTI按第8.9节的source membership分层，跨family的同一source共用抽样次数。F7 discrimination按第27.1节非线性统计量完整重算，不将其中位数之差替换为上述均值。

seed variability 单独报告：

```text
5 个 seed-level aggregate effect；
seed SD；
可选 mixed-effects sensitivity analysis。
```

不得声称 10000 bootstrap replicates 提高了 seed-level 独立信息量。

## 7.13 Search budgets

```yaml
search_budget:
  localizer_per_route: 12
  W_A_B_C_per_route: 12
  W_D: 16
  R_A_B_C_per_route: 6
  mechanism_lambda_candidates_each: 3
  CS_per_negative_route: 12
```

## 7.14 Supplement / escalation discipline

```yaml
escalation:
  max_precision_only_rounds: 2
  no_effect_driven_optional_stopping: true
  formal_test_effect_seen_then_expand: forbidden
```

任何补样必须来自Stage 0B预注册的sealed reserve。正式effect或实际test CI被读取前，可仅根据dev功效/精度规划增加计划样本，最多两轮且受cap限制；正式评价只作一次。解封后只允许预声明、与effect无关的数据损坏/缺失替换，不得按已观察test CI宽度反复补样。qualification阶段亦按此一次评价规则；不同已登记候选可依路线规则使用qualification集合，不能对同一候选边看CI边加样。

## 7.15 Statistical constants

```yaml
statistics:
  ci_level: 0.95
  alpha: 0.05
  multiple_comparison: holm
  power_target: 0.80
  planning_alpha_rule: alpha_divided_by_3
  bootstrap_rng: PCG64
  bootstrap_seed: 20261003
  ci_method: percentile
  quantile_method: linear_type7
  p_method: centered_bootstrap_error
  undefined_replicate_policy: inconclusive_no_drop_no_redraw

precision:
  stage4_effect_halfwidth_max: 0.005
  stage5_effect_halfwidth_max: 0.005
  stage6_localization_halfwidth_max: 0.0025
  stage6_selectivity_halfwidth_rule: 0.5 * epsilon_sel_gain
  guardrail_halfwidth_rule: 0.5 * corresponding_tolerance
```

Stage 4 power planning 使用保守：

\[
\alpha_{plan}=\alpha/3.
\]

## 7.16 Guardrails

```yaml
guardrails:
  mixed_partial_clean_auprc_drop_max: 0.01
  bona_fide_fpr:
    absolute_increase_floor: 0.005
    relative_increase_fraction: 0.20
  fully_manipulated_coverage:
    absolute_drop_floor: 0.01
    relative_drop_fraction: 0.10
  min_source_per_subset: 100
  max_source_per_subset: 500
  prediction_threshold: 0.50
  segment_iou_match_min: 0.50
```

保护性检查的每个子集最低100个独立source，适用于各正式评价阶段；不能用informative pair数抵扣。阈值化、时长及空集合规则见第8.7、28节。新增最低量用于独立评价三类退化风险，不替代primary的更高样本量要求。

## 7.17 CS selectivity scaling

```yaml
cs_selectivity:
  margin_m_rule: 0.10 * IQR(D_minus_CEL - D_plus_CEL)
  epsilon_sel_gain_rule: 0.10 * IQR(D_minus_CEL - D_plus_CEL)
  fallback_rule: 0.01 * median_nonzero_D_scale
```

两者只使用追加训练前固定M5在 `D_cs-dev` 的预测，在CS参数搜索前计算并于Stage6L冻结。采用与第27.1节相同的mixed-partial informative eligibility、source/family/realization权重及固定seed清单；不能按M5 gap大小选pair。

每个seed先独立计算 \(z=D^-_{M5}-D^+_{M5}\) 的weighted IQR。分位数唯一采用加权inverse-CDF：合并相同值、递增累积归一权重，首次累计达到或超过q的值为Q_w(q)；IQR_s=Q_w(.75)-Q_w(.25)。先对各seed的IQR等权平均，再乘0.10，同时得到m与epsilon_sel_gain；禁止先pool seeds再算IQR。

若平均IQR严格为0，fallback的D_scale明确取这些固定pairs上全部seed的D+及D-（每个seed等权、每对正负项各占一半，第(seed,u,f,r,+/−)项初始权重为 \(w_{ufr}/(2S)\)）；仅保留严格大于0的有限D值后全局重新归一，按第27.1节的weighted-median规则计算尺度，再乘0.01。没有正D值、无informative pair或有必须值缺失时，尺度不可识别，记录F7=INCONCLUSIVE、reason=CS_SCALE_UNIDENTIFIABLE；不启动依赖m的CS训练、不计算零precision目标；不得以m=0或epsilon=0继续、不得为取得非零尺度按detector结果补换bank。该诊断不否定先前CEL，后续新路线遵循第39节。上述两个乘数仍引用本节registry。

## 7.18 Secondary metric registry

```yaml
secondary_metrics:
  range_based_eer:
    enabled: true
    tolerance_ms: 100
    verdict_role: secondary_only
    implementation_hash_required: true
```

RB-EER 的 threshold sweep 只属于 metric computation，不是 protocol threshold tuning；不得改变 F4/F5/F6/F7/Stage5 verdict。

---

## 7.19 Stage P 启动实例与待落实字段

以下实例在首次读取screen模型效果前固定。`null`表示尚未取得的信息，不表示可跳过；数据集、release、路径、身份/标签及train/dev清单、不可变模型revision与文件hash全部落实后，才可启动使用预训练特征的P1–P3。当前本地环境验收不填补这些数据条件。

```yaml
screen_instance:
  dataset:
    dataset_id: null
    release: null
    audio_root: null
    source_interval_manifest: null
    source_identity_manifest: null
    screen_train_manifest: null
    screen_dev_manifest: null
    label_intervals: half_open_seconds
    split_unit: parent_source_utterance
  audio:
    sample_rate_hz: 16000
    channels: mono
    multichannel_rule: arithmetic_mean
    decode_dtype: float32
    resampler: torchaudio.functional.resample
    window_seconds: 10
    minimum_window_seconds: 3
    window_rule: deterministic_nonoverlap
    final_partial_cell: keep_with_actual_duration
  identity:
    data_seed: 20261003
    screen_seed_ids: [17, 29]
    pair_seed_rule: sha256_of_data_seed_parent_id_window_id_family
    model_id: microsoft/wavlm-base-plus
    model_revision: null
    model_file_hashes: null
    processor_revision: null
    feature_layer: last_hidden_state
    feature_extraction_mode: eval_no_grad
    feature_extraction_dtype: float32
    cache_dtype: float32
  controlled_families:
    prefix_crop:
      removal_ms: [80, 160, 320]
    interior_delete:
      removal_ms: [80, 160, 320]
      start_fraction: [0.25, 0.50, 0.75]
      minimum_retained_side_ms: 400
    boundary_grid: output_grid_ms
    parameter_selection: deterministic_label_blind
    pairs_per_window_per_family: 1
    crossfade: false
  u_ref:
    family: endpoint_fixed_source_time_sine_warp
    max_point_displacement_ms: 160
    derivative_relative_to_reference_range: [0.75, 1.25]
    amplitude_bisection_iterations: 40
  p0_numeric:
    row_sum_abs_tolerance: 1.0e-6
    occupancy_max_abs_tolerance: 1.0e-6
    timing_map_tolerance_samples: 1
  runtime:
    python: /home/richar/project/CEL/.venv/bin/python
    environment_lock: requirements/local-cu128.lock.txt
    device: cuda:0
    feature_microbatch_initial: 1
    head_microbatch_initial: 4
    accumulation_steps_initial: 8
    dataloader_workers_initial: 2
    model_cache: .cache/models
    feature_cache: .cache/features
    artifacts: artifacts/stageP_screen
```

构造与执行口径：

1. 先按母source身份划分数据，再确定性切窗；尾部不足minimum window的窗口按预声明规则排除并记账，保留窗口内不足一个output cell的真实尾部。不得按伪造边界或效果挑选窗口、删除位置或强度。先由SHA-256所得整数对合法参数笛卡尔积取模选一个组合，再执行；没有合法组合记不可构造，不换seed重抽。
2. waveform编辑器保存target sample→source sample的整数索引映射。reference构造器只读取该timing记录生成一热 \(W^{ref}\) 与有效行 \(R^{ref}=1\)；另一路直接编辑原始source区间provenance并独立binning得到 \(Y_{x'}\)，不得读取W或离散化的 \(Y_x\) 生成目标标签。两路可共享已知编辑操作，但不声称统计独立。
3. 前缀裁剪检验整体偏移，内部删除检验局部跳跃；全部编辑边界对齐output grid，不加入crossfade、codec或noise混合。该实例只代表这两个controlled families，不自动代表真实RTC链。
4. U-REF对参考source-time路径 \(s_i\) 使用 \(\tilde s_i=s_i+\sigma a\sin(\pi(s_i-s_{min})/(s_{max}-s_{min}))\)，其中符号由pair seed固定。幅度在最大点位移和相对参考路径导数范围内二分搜索，以02第9.2节矩阵距离达到第7.3节误差levels；相邻source cell中心线性插值生成W，端点与target support保持不变。参考路径中的合法skip保留，导数约束针对对参考路径的扰动。不可达按P3的INCONCLUSIVE处理，不换扰动族。
5. P1在source清单上训练；P2/P3所有变体共用按source及family等权的预先固定pooled pair清单，不为每个family另建一套28-run模型矩阵。micro-batch和累积可按显存调整，但有效batch、loss归约及optimizer步数按第7.2和32.5节保持一致。SmoothL1的beta取第7.1节。
6. source/target特征分别缓存，key按第32.1节。首次获取模型时将远端revision解析为commit SHA并记录文件hash；不能以可变的`main`充当锁定revision。训练集规模和时长分布由实际数据盘点填写，不虚构已满足下限。

### 7.19.1 Stage P 特征与输出时间网格实例

16 kHz输入的第n个样本登记于时间n/16000秒；输出cell为 `[i*0.02, min((i+1)*0.02,T))`，时间中心取该实际区间中点，最后不足整格仍为真实支持。WavLM卷积前端的局部输入支持宽度为400 samples（不表示最终contextual token仅依赖这400个样本）、步长320 samples；第j个native特征的时间中心为 `(320*j+199.5)/16000` 秒，长度为 `floor((N-400)/320)+1`。模型revision的卷积配置必须与该实例一致，否则先修订并冻结实例，不能仅按长度缩放时间。

在输入linear projection及TCN之前，冻结的native backbone特征按物理中心线性插值到完整output grid；超出首/尾native中心但仍在真实音频内的cell固定夹持到最近端点特征。该端点延拓只属于localizer输入适配，不构造额外音频、不读取标签，不扩展W的对应支持；Grid Adapter与M4自身的禁止外推合同保持不变。无native特征为无效输入。TCN的3个block各使用一个stride=1、kernel=3、对应dilation的Conv1d，再GELU及dropout；每层两侧padding=dilation保持输出长度，无额外归一化、残差或第二卷积。padding位置在每层后清零；最终逐cell linear→sigmoid。所有模型共用该实例。

因此canonical pre-logit H已位于output grid，Stage P的M4取Pi=identity。监督mask只排除batch padding，真实首尾格均保留。native feature提取逐条真实长度进行，禁止把batch-fill算进真实尾部；较长音频先按第7.19节固定窗口处理，再恢复原时间坐标。

验收例：N=160000时native长度499、output长度500、有效时长10秒；N=160080时native长度500、output长度501，最后格时长5 ms、中心10002.5 ms，全部501格属于真实支持。两例均检查时间原点、首尾夹持及padding隔离。配置依据：[Microsoft WavLM配置](https://huggingface.co/microsoft/wavlm-base-plus/blob/main/config.json)；运行时保存实际revision与配置hash。


---

# 8. Global Statistical Rules

## 8.1 Minimum-first rule

任何 formal Gate 在 decision function 前必须先检查唯一 minimum。

若：

\[
n<n_{\min},
\]

则：

\[
\boxed{\text{verdict}=\text{INCONCLUSIVE}.}
\]

minimum 未满足时不得输出 SUPPORTED、PRACTICAL_NULL、PREMISE_REFUTED、QUALIFIED、REJECTED 或 scope refutation。

## 8.2 Precision-first rule

F3、Stage 4、Stage 5、Stage 6 在读取 scientific effect verdict 前必须满足预注册 CI-width / power 条件。

若dev规划的precision不足，只允许在effect解封前按第7.14节扩充预注册计划；达到最大轮次仍不可行则：

```text
PRECISION_INFEASIBLE
或
POWER_INFEASIBLE
```

并进入合法终点。实际formal CI宽度超出已冻结门槛时为终局INCONCLUSIVE，保留区间和失败原因，不把规划通过当作实际precision已通过。

## 8.3 Practical-null discipline

禁止：

```text
p >= .05
→ PRACTICAL_NULL。
```

必须满足：

\[
\boxed{
U_{95}^{one-sided}(\Delta)<\epsilon.
}
\]

## 8.4 F4/F5/F6 support family

定义 primary differences：

\[
\Delta_4
=
AUPRC(M5)-AUPRC(M2),
\]

\[
\boxed{
\Delta_5
=
AUPRC(M5)-AUPRC(M3')
}
\]

\[
\Delta_6
=
AUPRC(M5)-AUPRC(M4).
\]

Support family：

\[
H_{0k}^{sup}:\Delta_k\le0.
\]

使用 Holm correction。

SUPPORTED：

```text
point Delta_k >= epsilon_main
AND
95% paired source-utterance bootstrap CI lower > 0
AND
Holm-corrected support p < alpha。
```

## 8.5 F4/F5/F6 practical-null family

固定对 \(k\in\{4,5,6\}\) 的三个假设共同计算并执行Holm correction：

\[
H_{0k}^{null}:\Delta_k\ge\epsilon_{main}.
\]

PRACTICAL_NULL：

```text
one-sided 95% upper CI < epsilon_main
AND
Holm-corrected equivalence p < alpha。
```

判决顺序为：先按第8.4节判断SUPPORTED；仅对未SUPPORTED的项采用本节经固定三项family校正后的PRACTICAL_NULL结论；其它为INCONCLUSIVE。不得根据同批support结果删除假设、缩小null family后重新校正。两组family分别报告其三个原始p值及校正值。

## 8.6 Stage 4 power planning

Stage 4D先在mech-train训练、mech-dev选择并固定M2/M3′/M4/M5的候选与checkpoint；随后Stage 4P使用这些固定模型在 `D_mech-dev` 上的预测，估计每个source utterance的seed-averaged paired difference标准差：

\[
\hat\sigma_k,\qquad k\in\{4,5,6\}.
\]

使用保守 planning level：

\[
\alpha_{plan}=\alpha/3,
\qquad
\beta=1-\texttt{power_target}.
\]

`power_target`唯一指：真实效应为 \(\epsilon_{main}\) 时，单个 \(H_{0k}^{sup}:\Delta_k\le0\) 在保守 \(\alpha/3\) 水平下的近似检验功效。它不是完整SUPPORTED复合条件、也不是F4/F5/F6同时通过的概率。以该planning alternative估计required sample：

\[
\boxed{
n_k^{req}
=
\left\lceil
\left[
\frac{
(z_{1-\alpha_{plan}}+z_{1-\beta})\hat\sigma_k
}{
\epsilon_{main}
}
\right]^2
\right\rceil.
}
\]

最终：

\[
n_{lock}
=
\max(
n_{initial},
n_4^{req},
n_5^{req},
n_6^{req}
).
\]

还须满足各major family的预注册最低数量，整数分配在读取test effect前固定。若将来要以“完整SUPPORTED通过概率”为设计目标，需在test解封前另行规定大于 \(\epsilon_{main}\) 的planning alternative，并模拟完整判决；本版本不作该功效保证。在真实效应恰等于 \(\epsilon_{main}\) 且估计近似对称时，点估计过该阈值的概率约为一半，不能由上式声称整体通过率为80%。dev方差只是规划估计，其来源、样本量与不确定性随power lock保存。

若：

\[
n_{lock}>n_{cap},
\]

则：

\[
\boxed{\text{POWER_INFEASIBLE}.}
\]

不得解封 `D_mech-test` 后再凭 effect 方向增加样本。

## 8.7 Canonical primary metric

primary唯一采用 **duration-weighted soft-occupancy grouped step AP**，本文继续记为temporal AUPRC。Y保持01的分数occupancy语义，不以0.5二值化后计算主指标；不采用梯形面积。AP与梯形PR面积并非同一算法，常规AP接口也不直接接受连续标签，参见[scikit-learn定义](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html)。下面公式是本项目针对occupancy的明确操作性定义。

对同一音频realization的真实、预声明可评价cells，令 \(w_i\) 为实际cell秒数，\(a_i=w_iY_i\)、\(b_i=w_i(1-Y_i)\)。只在 \(A=\sum_i a_i>0\) 且 \(B=\sum_i b_i>0\) 时计算primary。按预测分数从高到低将**完全相同的分数整体分组**，不得按标签拆分ties，不加jitter或近似合并；累计使用float64，所有Y/P须有限且属于[0,1]。到第g个分组为止：

\[
T_g=\sum_{i:P_i\ge q_g}a_i,\quad F_g=\sum_{i:P_i\ge q_g}b_i,\quad
\pi_g=\frac{T_g}{T_g+F_g},\quad r_g=\frac{T_g}{A},
\qquad AP=\sum_g(r_g-r_{g-1})\pi_g,\quad r_0=0.
\]

常数预测的no-skill参照为 \(A/(A+B)\)，与同一时长和soft标签定义一致；这不是有限样本随机排序AP的精确期望。Y为0/1时该公式退化为相同时长权重的grouped step AP。全真/全假音频的primary为not applicable，分别进入FPR/coverage保护性检查；缺失预测、非有限值或真实cell被静默删除属于实现失败，不能以0/1填入。

同一母source切出的窗口先恢复到各自realization的物理时间轴并汇集其所有预声明窗口cells，再计算该realization的AP，不把窗口当独立样本、不对窗口AP简单平均。所有窗口共用固定切窗及不足minimum-window尾部的记录规则。每个source内部先在同family的可评价realizations间等权平均，再在登记的family间等权平均，最后对source等权macro average。所需family无可评价realization时记该source不适用并报告覆盖；source/family清单不能随模型改变。多seed先按第7.12节汇总paired差量；no-skill使用完全相同的层级、支持和分母。

该指标定义适用于P1–P3、Localizer、F4–F7、Stage5及clean regression。boundary用的0.5阈值不能回流改变primary。最低量按独立母source计；多个family或窗口不增加独立样本数。

### 8.7.1 阈值化定位与保护性指标

预测 \(P\ge\texttt{guardrails.prediction_threshold}\)、GT occupancy \(Y\ge\texttt{premise.occupancy_boundary_threshold}\) 分别形成最大连续区间，不跨padding、未观察支持或窗口间隙连段；阈值和后处理对全部模型/seed相同，不作test调优。Segment F1按IoU不低于第7.16节阈值的最大基数一一匹配，再以最大总IoU、时间索引字典序打破并列，计 \(2TP/(|A|+|B|)\)。只有一侧无区间时为0；两侧皆无时不适用并报告数量。

Boundary MAE/P90使用同polarity、保持顺序、最大基数后最小总距离的匹配，ties按时间索引；每个未匹配GT或预测边界记该realization的可观察时长为误差，不能因漏检删掉该样本。真实区间内真假切换才是边界，padding/未知支持边缘不算。匹配误差和未匹配惩罚一起求MAE/P90；全部无边界时不适用。Segment mIoU沿用第15.2节公式。指标先逐realization计算，再按上述source/family层级汇总；正式CI重采样source。局部指标不适用数及最低量单列，不能借primary样本量宣称其它指标已够量。

Bona-fide FPR是全真音频上预测为假的真实时长比例；fully-manipulated coverage是全假音频上预测为假的真实时长比例。两者不要求informative gate，沿用source/family汇总和同一阈值。全真/全假指原始provenance在评价支持上分别全0/全1，不能将mixed-partial按平均标签改归类。

## 8.8 F4 mandatory decomposition

除了 primary \(\Delta_4\)，Stage 4T 必须报告：

```text
support_common = I_p^+ ∩ I_p^id；
support_W_only = I_p^+ \ I_p^id；
support_id_only = I_p^id \ I_p^+；
coverage ratio / duration；
Delta4_common；
W-only localization behavior。
```

按02第12节作描述性区域分解：common-support上的正收益说明收益在共同区域仍可观察到；W-only集中收益说明收益主要位于额外覆盖区域。两模型训练支持可能不同，不能据此排除训练coverage的间接效应，也不能单独主张对齐精度的因果贡献。

## 8.9 唯一重采样、CI与p值实现

在固定source registry上，按其预登记family/platform membership signature建立互不重叠的strata；每层有放回抽取原数量的parent sources。同一source的bootstrap multiplicity由所有方法、seeds、family、realization及保护性子集共用，不独立抽seed、窗口、frame或同一source的另一个family。每次抽样重算该指标规定的聚合，使用重复source的抽样次数作为权重；不改变冻结的family汇总规则。两模型先在相同评价清单形成配对，预测失败不是改用不同分母的理由。

使用第7.15节的RNG、seed与10000次重采样；每个有定义的统计量T，默认双侧95%区间为 \([Q_{.025}(T^*),Q_{.975}(T^*)]\)，单侧95%上/下界分别为 \(Q_{.95}(T^*)\)、\(Q_{.05}(T^*)\)，quantile使用linear/type-7。未标one-sided的L95/U95统一指双侧端点；半宽为(U-L)/2。重采样中统计量无定义时记录原因为INCONCLUSIVE，不静默丢弃或重抽；实际minimum、eligibility与coverage先于推断。

F4–F6令 \(E_b=T_b^*-\hat T\)。检验 \(H_0:T\le0\) 的support原始p值与检验 \(H_0:T\ge\epsilon_{main}\) 的practical-null原始p值分别固定为：

\[
p_{sup}=\frac{1+\sum_{b=1}^{B}\mathbf1[E_b\ge\hat T]}{B+1},\qquad
p_{null}=\frac{1+\sum_{b=1}^{B}\mathbf1[E_b\le\hat T-\epsilon_{main}]}{B+1}.
\]

尾部ties计入，执行plus-one校正；两组各对固定三项作Holm，排序ties按F4/F5/F6顺序，adj-p按累积最大值并截断至1。percentile CI与centered-error p不宣称精确互为反演，仍按第8.4–8.5节同时核验CI和校正p条件。F7、reference及其它非线性指标直接重算其完整统计量来取CI，不套用F4–F6的差量均值。

这些是条件于固定训练seeds的近似source-population推断，不是有限样本精确检验，也不保证多个阶段/指标联合95%覆盖。退化bootstrap分布、罕见事件和过小strata必须报告；零宽区间不意味着总体无不确定性。实现参考：[SciPy paired bootstrap与区间定义](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)；实现必须显式指定本文方法，不能使用库的其它默认CI。

## 8.10 精度规划与一次正式评价

Stage3保持第7.9节precision阈值；Stage4/5/6与各guardrail使用第7.15节新增半宽目标。相同固定模型的dev source-bootstrap半宽为h_dev、独立source数n_dev时，使用 \(n_{precision}=\lceil n_{dev}(h_{dev}/h_{max})^2\rceil\) 作规划近似，与该阶段最低量、power要求和family配额共同取最大；dev退化/不可估计时不能用h_dev=0宣称所需样本为0，应以预登记最大计划样本或新独立dev证据完成规划。上述平方根缩放不是对formal宽度的保证。

Stage4第8.6节n_lock还须覆盖三项effect的precision需求；Stage5沿用2000–3000 cap；Stage6 informative沿用100–500 cap。三类guardrail各至少100个source、每类最多500个source，分别规划并预封存；一类样本不能替另一类凑数。样本不足或计划超cap即停止该阶段并记录INCONCLUSIVE/PRECISION_INFEASIBLE。读到正式结果后，实际precision不足只报告终局INCONCLUSIVE，不按结果反复扩样。


---

# 9. Stage P0 — Controlled Transport Sanity

P0 不更新模型参数，只使用 `D_screen-dev` construction records。

每个 transform 必须保存：

```text
known transform record；
W_ref；
R_ref；
independent target occupancy Y_x'；
source / target physical-time map。
```

验证：

\[
W^{ref}\neq W_{id}
\]

以及：

\[
Y_{x'}\approx W^{ref}Y_x.
\]

对第7.19节的整格精确编辑实例，`≈`唯一指有效target cells上的最大绝对occupancy差不超过 `p0_numeric.occupancy_max_abs_tolerance`；同时检查W非负、有效行和为1（容差见registry）、无效行和为0、timing映射误差不超过登记的sample容差。无有效支持、错误shape或非有限值属于construction failure，不能以零误差通过。该构造容差不替代formal F2阈值。

usable pairs 未达到 `screen.min_pairs_per_family`：

\[
\boxed{SCREEN_INCONCLUSIVE.}
\]

若 construction / reference 错误：

\[
\boxed{INVALID_IMPLEMENTATION.}
\]

修复纯工程问题后允许重跑 P0，但不得改变科学 transform family。

---

# 10. Stage P1 — Minimal Localizer

训练 `D_screen-train`，评价 `D_screen-dev`。

定义：

\[
G_{screen}
=
AUPRC_{partial}-AUPRC_{noskill}.
\]

P1 通过：

```text
mixed-partial >= screen.localizer_min_mixed_partial；
全部 screen seeds 的 G_screen > 0；
seed mean(G_screen) >= screen.localizer_auprc_excess_min；
无 NaN / constant-output / optimization collapse。
```

数据不足 → SCREEN_INCONCLUSIVE。

性能不满足 → SCREEN_NONPROMISING。

---

# 11. Stage P2 — Oracle O2 / O3′ / O4 / O5 Screen

同一 seed 的 variants 必须来自同一 P1 checkpoint。

此处：

\[
W_0=W^{ref}.
\]

计算：

\[
\Delta_5^{screen}(0)
=
AUPRC(O5_0)-AUPRC(O3'_0),
\]

\[
\Delta_6^{screen}(0)
=
AUPRC(O5_0)-AUPRC(O4_0).
\]

若存在同一个固定对照（O3′或O4），使O5在全部screen seeds上对该对照的差量均严格小于 \(-\epsilon_{screen}\)，则SCREEN_NONPROMISING；否则进入P3。不能把不同seed各自最不利的对照拼成停止条件。

---

# 12. Stage P3 — U-REF Admissible Error Sweep

P3 只检验 02 的 U-REF，不声称覆盖 operational error。

对每个预注册 nonzero level \(e\)：

\[
W_e=\mathcal P_e(W^{ref}).
\]

保存 achieved error：

\[
e_{achieved}=d_W(W_e,W^{ref}).
\]

误差按02第9.2节逐pair计算，bank在读取模型效果前生成并固定，所有方法与seed共用。三个nonzero levels必须在同一预先固定的train/dev pair清单上都达到目标±`perturbation_target_tolerance_ms`，保持原target support和admissibility；任一级不可达、缺失或跨level achieved error重复时，记录原因并判SCREEN_INCONCLUSIVE。不得删除不利pair、临时换样本或删level来获得趋势。

每个level的横坐标是固定dev清单上先按source utterance汇总、再等权平均的achieved error。每个seed独立计算各模型AUPRC，先取paired difference，再对两个固定seed等权平均；本节无seed下标的 \(\Delta_5^{screen}(e)\)、\(\Delta_6^{screen}(e)\) 均指该seed均值，同时保存两个seed各自结果。多个realization先在同一source内部等权汇总。

训练 / 评价：

\[
O3',\ O4,\ O5.
\]

计算：

\[
\Delta_5^{screen}(e)
=
AUPRC(O5_e)-AUPRC(O3'_e),
\]

\[
\Delta_6^{screen}(e)
=
AUPRC(O5_e)-AUPRC(O4_e).
\]

SCREEN_PROMISING 满足以下任一：

```text
至少一个 nonzero level 的 Delta5_screen >= epsilon_screen，
且最高 achieved-error level Delta5_screen >= 0；

或

三个nonzero levels的seed-mean Delta5_screen对achieved error的Spearman rho > 0，
且最高 achieved-error level Delta5_screen >= 0。
```

同时至少一个 nonzero level：

\[
\Delta_6^{screen}\ge-\epsilon_{screen}.
\]

Spearman使用average ranks；这是三个level上的描述性筛查规则，不作显著性检验。若三个差量相同使rho未定义，则趋势分支不成立，仍可按绝对增益分支判断。“最高level”按实际横坐标确定。

SCREEN_NONPROMISING：三个nonzero levels、两个seed各自的 \(\Delta_{5,s}^{screen}(e)\) 全部严格小于 \(-\epsilon_{screen}\)。

其它：SCREEN_INCONCLUSIVE。

Stage P 完成后不得新增 screen model variants。

---

# 13. Stage 0A — Real Reference Feasibility + Early Collection Checkpoint

只有 SCREEN_PROMISING 默认进入。

对每个 candidate real family 先采集：

```text
reference.early_checkpoint_pairs_per_family
```

用于验证：

```text
independent reference uncertainty；
reference coverage；
landmark density；
family acquisition throughput；
provenance completeness。
```

输出：

```text
R-Dense；
R-Sparse；
R-None。
```

R-Dense 不满足可降级 R-Sparse；R-Sparse 不满足则 R-None。

R-None：

```text
不支持 strong real F2/F3；
允许 CTRL scope 或 exploratory real transfer；
不得继续盲采 real_formal_initial 规模。
```

---

# 14. Stage 0B — Global Formal Protocol Freeze

必须冻结：

```text
formal partitions 与 reserves；
source identity registry；
all seals；
scope registry；
01/02 hashes；
global numeric registry；
statistics；
route order；
search budget；
canonical M4 feature-tap rule；
Stage 4 power formula；
claim rules；
artifact schemas；
secondary metric implementation hashes；
OOD dataset/version/split hash（若启用）。
```

生成：

```text
configs/protocol_vFINAL_global.yaml
configs/locks/stage0_protocol.lock.yaml
```

Stage 0B 后：

\[
\boxed{\text{formal scientific protocol immutable}.}
\]

---

# 15. Stage 1 — Formal F1 / F2 Premise Audit

所有 verdict 先执行 minimum-first rule。

## 15.1 F1 — Task-Relevant Communication Transport Exists

Dense track：

定义 reference transported occupancy：

\[
Y_p^{ref}=W_p^{ref}Y_x,
\]

strict identity occupancy：

\[
Y_p^{id}=W_{id,p}Y_x.
\]

以 `premise.occupancy_boundary_threshold` 将occupancy field二值化，在各自有效连续支持内部提取manipulation boundaries；padding及未知支持边缘不当作真假切换。记两组边界为 \(B_r,B_i\)，按同polarity、最大基数、保持时间顺序、最小总绝对时间差完成一一匹配 \(\mathcal M_p\)，仍并列时按边界时间索引字典序确定。

定义 boundary displacement：

\[
BTD_p^{task}
=
\operatorname{median}\frac{|b_r-b_i|}{output\_grid\_ms}.
\]

median仅遍历 \(\mathcal M_p\)；无匹配时BTD为not applicable。未匹配边界比例定义为：

\[
\boxed{U_{B,p}^{task}=\frac{|B_r|+|B_i|-2|\mathcal M_p|}{|B_r|+|B_i|}.}
\]

两组都为空时该量not applicable；只有一组非空时为1。\(\tau_B\)、\(\tau_U\)、\(q_{min}\)分别引用第7.7节的boundary displacement、task unmatched fraction、meaningful pair fraction。

定义 source manipulated unmatched mass：

\[
U_p^{task}
=
\frac{
\sum_j\omega_jY_{x,j}\mathbf1[\sum_iW_{p,ij}^{ref}=0]
}{
\sum_j\omega_jY_{x,j}
}.
\]

这里 \(\omega_j\) 为source cell实际时长；source manipulated mass为0时该量not applicable，不作除零计算。

pair task-active 当且仅当：

\[
BTD_p^{task}\ge\tau_B
\quad\lor\quad
U_{B,p}^{task}>0
\quad\lor\quad
U_p^{task}\ge\tau_U.
\]

family-level `q_active` 为至少一个上述量可定义的预注册可评价pairs中的task-active比例。not applicable项不参与逻辑或；全部不适用的pair单列原因，不计为inactive，也不进入该比例分母。eligible pair数必须满足premise最低量，并报告原始数、有效数、缺失及coverage；有效数不足为INCONCLUSIVE。BTD的family median仅使用有匹配的pairs；没有任何BTD时其条件为不适用，仍可按有效的q_active判断。

F1 SUPPORTED：

\[
L_{95}(median\ BTD^{task})\ge\tau_B
\]

或：

\[
L_{95}(q_{active})\ge q_{min}.
\]

F1 PREMISE_REFUTED：`q_active` 上界低于 \(q_{min}\)，且 boundary displacement 也明确低于 threshold 或完全 not-applicable。

其它：INCONCLUSIVE。

Sparse track使用independent landmarks建立禁止extrapolation的monotonic piecewise-linear map；仅在其覆盖的时间区间计算上述边界量。未观察区间不推断为删除或零occupancy；没有独立删除依据时source unmatched mass项为not applicable。采用相同的边界匹配与q_active判据，结论限定于登记的可观察支持。

## 15.2 F2 — Manipulation Occupancy Is Transportable

禁止定义：

\[
Y_{x'}:=W^{ref}Y_x.
\]

target GT 必须来自 independent target provenance。

segment mIoU统一按pair计算：将两侧被比较的occupancy/区间provenance在共同参考有效支持内裁切，并按第7.7节阈值取最大连续manipulated区间。设区间集合为A、B，使用最大总IoU的一一匹配，未匹配项记0，pair分数为匹配IoU之和除以 \(\max(|A|,|B|)\)。两集合都为空时该指标not applicable；只一侧为空时为0。禁止用裁切支持边界产生额外虚假切换。family统计只使用该指标可评价的pairs，须满足最低量，并同时报告不适用比例。

Dense：

\[
E_Y=d_Y(Y_{x'},W^{ref}Y_x;\mathcal I^{ref}).
\]

同时评价：

```text
median(E_Y)；
P90(E_Y)；
median pair-level segment mIoU。
```

SUPPORTED 需全部满足 dense thresholds 的 CI 条件；任一明确反向越界则 PREMISE_REFUTED；其它 INCONCLUSIVE。

Sparse 必须同时具有 independent timing landmarks 与 independent target manipulation provenance；否则：

\[
\boxed{F2=INCONCLUSIVE.}
\]

条件齐备时，使用通过第7.6节质量检查的landmarks构造固定source→target分段线性单调映射。将source manipulation区间裁切到landmark覆盖范围后映射其端点；target区间由独立provenance给出，并裁切到同一target可观察范围。按上面的pair segment mIoU计算 \(J_p^{sparse}\)，对source utterance重采样得到其family median的CI：

\[
\begin{aligned}
L_{95}(\operatorname{median}_p J_p^{sparse})\ge
\texttt{premise\_f2.sparse.median\_segment\_iou\_min}
&\Rightarrow SUPPORTED,\\
U_{95}(\operatorname{median}_p J_p^{sparse})<
\texttt{premise\_f2.sparse.median\_segment\_iou\_min}
&\Rightarrow PREMISE\_REFUTED.
\end{aligned}
\]

其余为INCONCLUSIVE。最小样本、reference覆盖与误差要求先于该判决；不能将landmark之间未确认的插入/删除区间强行插值为可靠支持。无法界定可靠映射段时，该pair缺失并保留原因。Sparse结论不外推至未观察区间，也不以Sparse W fidelity代替本项occupancy验证。

## 15.3 Scope coupling

后续同一 scope 必须：

\[
\boxed{
F1[\mathrm{scope}]
=
F2[\mathrm{scope}]
=
SUPPORTED.
}
\]

---

# 16. Track L：Stage 2D / 2L / 2T — Localizer

## 16.1 Stage 2D

只读：

\[
D_{\mathrm{loc-train}},
\quad
D_{\mathrm{loc-dev}}.
\]

route order：

\[
L\text{-A}\rightarrow L\text{-B}\rightarrow L\text{-C}.
\]

每 route 不超过 search budget。

第一条同时满足 dev AUPRC、Segment F1、Boundary MAE thresholds 的 route 被选中。

全部 route 在 dev 明确失败：

\[
\boxed{LOCALIZER_UNUSABLE.}
\]

## 16.2 Stage 2L

冻结：

```text
L route；
backbone / head；
optimizer；
base augmentation；
lambda_BCE / lambda_Dice；
checkpoint selection；
02 canonical feature tap 的 exact module path；
tap shape hash；
formal seeds及各seed被选M0 checkpoint hash。
```

然后才解封 `D_loc-test`。

## 16.3 Stage 2T

定义：

\[
G_{loc}=AUPRC_{partial}-AUPRC_{noskill}.
\]

先检查第7.11节minimum及三项指标的可估计性；G_loc、Segment F1和Boundary MAE各自的可评价mixed-partial source数均须达到loc_test_mixed_partial，不能相互抵扣。以第8.9节CI，SUPPORTED当且仅当：

\[
L_{95}(G_{loc})\ge0.10\ \land\ L_{95}(SegmentF1)\ge0.40\ \land\ U_{95}(BoundaryMAE)\le250\text{ ms}.
\]

UNUSABLE当且仅当至少一项明确失败：

\[
U_{95}(G_{loc})\le0.05\ \lor\ U_{95}(SegmentF1)\le0.30\ \lor\ L_{95}(BoundaryMAE)\ge300\text{ ms}.
\]

上式数值引用第7.8节，不维护第二份配置。其余（含必要指标缺失、最低量不足）为LOCALIZER_INCONCLUSIVE。不存在有效性缺口时先检查SUPPORTED，再检查UNUSABLE；两组条件因不同门槛不会同时成立。Stage2D的route选择仍使用固定dev点估计与dev thresholds；没有合格route且指标不可估计时为LOCALIZER_INCONCLUSIVE，不能当作全部明确失败。

Formal test 后不得切换 L route。

LOCALIZER_UNUSABLE 是合法项目终点，不再出现无 Outcome 状态。

---

# 17. Track C：Stage 3D / 3Q-A / 3Q-B / 3L / 3T — Operational W/R

Stage 3 是最高风险 premise-feasibility track。它不依赖 localizer，可与 Stage 2 并行。

## 17.1 Stage 3D — Development

只读：

\[
D_{\mathrm{corr-dev}}.
\]

W order：

\[
W\text{-A}
\rightarrow
W\text{-B}
\rightarrow
W\text{-C}
\rightarrow
W\text{-D}.
\]

对每个固定 W：

\[
R\text{-A}
\rightarrow
R\text{-B}
\rightarrow
R\text{-C}
\rightarrow
R\text{-0}.
\]

每个 route 只允许产生一个 candidate hash。

## 17.2 Stage 3Q-A — Primary Qualification

只读 sealed：

\[
D_{\mathrm{corr-qual-A}}.
\]

### W decision

评价：

```text
P50 independent error；
P90 independent error；
coverage。
```

QUALIFIED：

\[
U_{95}(P50)\le w_{50},
\]

\[
U_{95}(P90)\le w_{90},
\]

\[
L_{95}(Coverage)\ge c_W.
\]

REJECTED：任一指标的 CI 明确越过失败方向。

INCONCLUSIVE：其它。

### Precision condition

在给 route verdict 前还必须：

```text
P50 CI half-width <= corr_precision.p50_ci_halfwidth_max_ms；
P90 CI half-width <= corr_precision.p90_ci_halfwidth_max_ms；
Coverage CI half-width <= corr_precision.coverage_ci_halfwidth_max。
```

样本/precision计划按第8.10节在读取该候选qualification结果前固定。评价后precision不足为该route的INCONCLUSIVE，不按同一结果反复解封reserve。

### Reliability decision

计算：

\[
\rho_R=\rho(\hat R,e),
\]

\[
G_R
=
1-
\frac{median(e\mid R\in Q_{top})}{median(e)}.
\]

使用共同可评价的reference rows / landmarks，不按预测R屏蔽误差。Spearman使用average ranks；top quartile取R排序最高的 \(\lceil n/4\rceil\) 个点，并列按稳定的source/realization/时间索引打破。CI按source utterance cluster bootstrap计算。

QUALIFIED 必须满足：

\[
\rho_R\le-0.30,
\quad
U_{95}(\rho_R)<0,
\]

\[
G_R\ge0.25,
\quad
L_{95}(G_R)>0.
\]

R-A/B/C的判决顺序：满足以上全部条件为QUALIFIED；否则若 \(L_{95}(\rho_R)>-0.30\) 或 \(U_{95}(G_R)<0.25\)，则REJECTED；其它为INCONCLUSIVE。若R或error为常数、median(error)=0，或有效数据不足，使rho/G未定义，则为INCONCLUSIVE并记录原因，不填零或默认通过。数值阈值均引用第7.10节。

R-0不经过Spearman/gain检验，只表示已验证的二值对应支持。它仅在dense reference下评价同一W的independent row-error Q95：\(U_{95}(Q95)\le\texttt{r0.controlled\_q95\_ms}\)时ELIGIBLE并映射为该W的R=QUALIFIED；\(L_{95}(Q95)\)严格大于阈值时INELIGIBLE并映射为REJECTED；跨越阈值则INCONCLUSIVE。此严格Q95上限也适用于REAL dense，不随REAL的W阈值放宽。sparse-only永远INELIGIBLE，作为结构上不适用的候选跳过，不能冒充一次统计失败。

仅有以下预登记例外：若independent error恒定，或median(error)=0导致gain无定义，可检查同一W的R-0；必须dense reference、W整体及全部mandatory strata的minimum/precision/absolute fidelity均合格，且整体与每个mandatory stratum的 \(U_{95}(Q95)\le60\text{ ms}\)。通过时选择R-0并记录reason `RANK_UNIDENTIFIABLE_HIGH_FIDELITY`，不将R-A/B/C无定义的值填成通过。仅R恒定而error非退化、数据/precision不足或普通CI跨阈值不能触发该出口；R-0未通过则保持原INCONCLUSIVE。Q-B及Corr-Test只能验证已选定的同一W/R-0，独立重复相同资格检查，不在test改R。

固定W内先核验W及必要strata，再按R-A→R-B→R-C→R-0处理（仅上述高保真退化例外可直达R-0）：只有明确REJECTED或结构INELIGIBLE才进入下一R；任何终局INCONCLUSIVE保持sticky。W明确失败则不靠换R挽救。所有适用R明确失败且没有INCONCLUSIVE时，该W/R路线整体REJECTED，方可尝试下一W；W、R及必要strata全部合格才得到W/R candidate QUALIFIED。Q-B使用同一合并规则，不能仅确认W而忽略R。

### Authenticity-conditioned absolute fidelity

对 scope 中预注册的必要 strata：

```text
bona fide；
fully fake；
partial fake interior；
boundary-crossing。
```

在每个达到 `corr_authenticity_stratum_min` 的 stratum 上重复 W absolute fidelity 检查。

Strong scope qualification 要求所有 mandatory strata 均达到 absolute W floor。

strata 间差异本身只输出 diagnostic flag：

```text
AUTHENTICITY_STABILITY_OK
AUTHENTICITY_STABILITY_FLAG
```

不得把该 flag 自动解释为 label leakage。

## 17.3 Stage 3Q-B — Independent Confirmation Before Lock

只有 Stage 3Q-A 的 W/R candidate QUALIFIED 才允许读取：

\[
D_{\mathrm{corr-qual-B}}.
\]

使用完全相同的 W、R、threshold 与 decision function。

### Q-B QUALIFIED

candidate 进入 first-qualified selection，可锁定。

### Q-B REJECTED

记：

```text
REJECTED_EXTERNAL
```

因为 formal Corr-Test 尚未解封，所以允许继续下一个预注册 W/R route。

### Q-B INCONCLUSIVE

INCONCLUSIVE 是 sticky：

```text
结果读取前可按dev precision规划使用reserve；
读取Q-B后仍 INCONCLUSIVE → F3=INCONCLUSIVE；
不得静默跳到下一 route。
```

其目的在于防止“某 route 不确定就换一条更容易过的 route”。

## 17.4 Route exhaustion

按 W-A→W-B→W-C→W-D 顺序：

```text
first candidate 同时通过 Q-A 与 Q-B → first-qualified wins；
全部 routes 明确 REJECTED / REJECTED_EXTERNAL → F3=OPERATIONAL_SCOPE_REFUTED；
任一路线达到终局 INCONCLUSIVE → F3=INCONCLUSIVE；
W-E 永远不得 rescue。
```

这里的 `OPERATIONAL_SCOPE_REFUTED` 才表示 01 F3 中预注册 operational family 全部失败。

## 17.5 Stage 3L — Correspondence Lock

冻结：

```text
W route / params；
R route / params；
Grid Adapter；
support rule；
reference mode；
claim scope；
candidate hash；
Q-A / Q-B qualification artifact hashes；
authenticity-strata registry；
U-OP analysis plan。
```

生成：

```text
stage3_correspondence.lock.yaml
```

然后才解封：

\[
D_{\mathrm{corr-test}}.
\]

## 17.6 Stage 3T — Final Corr-Test / F3

只验证 locked realization，重复完全相同 decision functions。

若 W 与 R 均 QUALIFIED，必要 authenticity strata 均满足 absolute fidelity floor，且 precision gate 通过：

\[
\boxed{F3[\mathrm{scope}]=SUPPORTED.}
\]

若仅 precision / sample size 不足：

\[
\boxed{F3=INCONCLUSIVE.}
\]

若 locked realization 在 Corr-Test 上明确 REJECTED：

\[
\boxed{F3=OPERATIONAL\_REALIZATION\_FAILED.}
\]

并记录：

```text
external_validation_failure: true
route_switch_in_current_protocol: forbidden
```

该状态是合法终点。它**不**等价于 `OPERATIONAL_SCOPE_REFUTED`。

若研究者希望之后尝试其它 W/R route，必须新建 evidence-isolated protocol version，不得与本次 formal evidence 合并。

---

# 18. Merge Gate：进入机制验证的必要条件

只有同一 scope：

\[
\boxed{
F1=F2=F3=SUPPORTED
}
\]

且：

\[
\boxed{
LOCALIZER\_SUPPORTED
}
\]

才允许进入 Stage4；从Stage4进入Stage5/6还须满足第28.4节M5三类保护性检查。

因此：

```text
Stage 2 成功但 Stage 3 失败 → 不进入 Stage 4；
Stage 3 成功但 Localizer unusable → 不进入 Stage 4；
二者都成功 → 进入 Stage 4D，再进入4P。
```

---

# 19. Stage 4D — M2 / M3′ / M4 / M5 Development

只读：

\[
D_{\mathrm{mech-train}},
\quad
D_{\mathrm{mech-dev}}.
\]

formal fairness family 唯一为：

\[
\boxed{M2,M3',M4,M5.}
\]

共享：

```text
same localizer；
same source base supervision；
same source identities；
same paired task-transport-active realizations；
same W/R；
same optimizer family；
same training-step budget；
same formal seed IDs；
same output grid。
```

只允许在 dev 选择：

```text
lambda_id；
lambda_AS_match；
lambda_feat；
lambda_CEL。
```

M3 native 可训练，但固定为 SECONDARY-DIAGNOSTIC，不参与 F5 formal tuning family。

---

# 20. Stage 4P — Mechanism Power / Precision Lock

这是Stage 4D之后、4L/4T之前的必要步骤。输入为4D已固定的四个模型及mech-dev预测；不得重新调参以降低方差或改变required n。若模型或训练配置发生合法的实施前修改，需重新生成4D预测并重新执行4P，然后才能4L。

只读：

\[
D_{\mathrm{mech-dev}}.
\]

使用与 formal architecture / data unit 相同的 paired metric 结构，估计：

\[
\hat\sigma_4,\hat\sigma_5,\hat\sigma_6.
\]

其中 F5 必须基于：

\[
M5-M3'.
\]

按第8.6节计算：

\[
n_{lock}.
\]

### PASS

若：

\[
n_{lock}\le\texttt{minimums.mech\_test\_cap},
\]

则将 exact `n_lock` 写入：

```text
stage4_power.lock.yaml
```

同时记录输入checkpoint hashes、dev source清单、固定seed IDs、三个方差估计、planning alternative、功效仅对应单项显著性检验的解释及family分配。4L核验这些模型身份与最终mechanism配置完全一致。

并从已 seal 的 `D_mech-test` 预注册池中固定抽取该数量 source identities。

### POWER_INFEASIBLE

若：

\[
n_{lock}>n_{cap},
\]

则：

\[
\boxed{POWER\_INFEASIBLE.}
\]

不得用 under-powered 300 pairs 强行运行并把 negative result 解释为 null。

---

# 21. Stage 4L — Mechanism Lock

冻结：

```text
M2 / M3′ / M4 / M5 02-contract hashes；
scope；
lambda values；
canonical M4 exact tap path + shape hash；
formal seeds；
training steps；
epsilon_main；
guardrails；
statistics；
Stage 4 n_lock；
F4 decomposition rules；
U-OP strata / replay plan；
secondary M3-native reporting rule。
```

然后才解封：

\[
D_{\mathrm{mech-test}}.
\]

---

# 22. Stage 4T — F4 / F5 / F6 Formal Mechanism Test

先验证 exact `n_lock` 与 source identities。

primary verdict：

\[
\Delta_4=AUPRC(M5)-AUPRC(M2),
\]

\[
\boxed{
\Delta_5=AUPRC(M5)-AUPRC(M3')
}
\]

\[
\Delta_6=AUPRC(M5)-AUPRC(M4).
\]

按第8.4–8.5节输出 F4/F5/F6。

## 22.1 F4 mandatory attribution report

同时输出：

```text
overall Delta4；
Delta4_common；
W-only duration / row fraction；
M5 vs M2 on W-only region；
共同区域 / 额外覆盖区域的描述性结果及训练支持差异限制。
```

该 attribution label 不改变 F4 verdict，但约束论文表述。

## 22.2 F5 secondary engineering comparator

额外报告：

\[
\Delta_5^{native}
=
AUPRC(M5)-AUPRC(M3).
\]

固定：

\[
\boxed{
\Delta_5^{native}\text{ 不改变 F5 verdict}.
}
\]

## 22.3 U-OP secondary analysis

只使用 Stage 3T 已获得的 independent operational error。

允许：

```text
按 W error quantile 分层 Delta5；
按 validated R quantile 分层 Delta5；
按 empirical error profile replay admissible perturbations。
```

禁止：

```text
按 M5-M3′ 自身 performance 反向定义 strata；
事后把 U-OP 升级为 F5 main evidence。
```

## 22.4 RB-EER

在相同 frozen predictions 上计算 secondary Range-Based EER。

其 threshold sweep 仅属于 metric computation，不修改任何 protocol threshold。

---

# 23. Novelty Kill Gate

## 23.1 PASS

只有：

\[
\boxed{
F4=F5=F6=SUPPORTED
}
\]

CEL 才升级为：

\[
\boxed{
\text{Validated Mechanism Contribution at the tested scope}.
}
\]

## 23.2 任一 PRACTICAL_NULL

\[
\boxed{\text{STOP FULL-SCALE CEL DEVELOPMENT}.}
\]

禁止：

```text
Stage 5 formal；
Stage 6；
新增 W/R route；
换 M3′；
更换 M4 tap；
新增 formal comparator；
加平台救结果。
```

允许 failure analysis、M6、secondary transfer。

## 23.3 任一 INCONCLUSIVE

formal effect 已读取后，不允许 effect-driven 补样。

若 Stage 4P power lock 正确而 formal test 仍 INCONCLUSIVE：

```text
该结果即终局 INCONCLUSIVE；
不得因为方向接近正向就追加样本。
```

只有预先声明的数据损坏 / 缺失替换可以使用 sealed reserve，且 replacement 规则必须与 effect 无关。

---

# 24. Stage 5T — Frozen Real-Chain Evaluation

formal Stage 5 前置：

\[
\boxed{
F1\text{--}F6=SUPPORTED
}
\]

且全部属于同一REAL target scope，Stage4的M5三类保护性检查均PASS。

否则 real evaluation 只能是 exploratory transfer。

## 24.1 Comparator

从：

\[
M2,M3',M4
\]

在 `D_mech-dev` 按 primary metric 选择：

\[
C^\star.
\]

tie-break：

\[
\boxed{M4>M3'>M2.}
\]

M3 native 仍为 secondary，不进入 primary comparator selection。

## 24.2 Primary

\[
\Delta_{real}
=
AUPRC(M5)-AUPRC(C^\star).
\]

Stage5在formal test解封前按第7.15、8.10节规划expected CI width；initial 2000不足时，在读取test效果前使用预注册reserve，最多到real_formal_cap，固定样本后只评价一次。实际precision不足为终局INCONCLUSIVE。primary verdict按以下公式，最终Stage5 verdict再按第28.4节合并三类保护性检查；只有保护性检查通过时，primary PRACTICAL_NULL才按Outcome M交付，保留原REAL机制证据。

SUPPORTED：

\[
\Delta_{real}\ge\epsilon_{real},
\]

\[
L_{95}(\Delta_{real})>0,
\]

并满足 multi-family consistency。

PRACTICAL_NULL：

\[
U_{95}^{one-sided}(\Delta_{real})<\epsilon_{real}.
\]

其它 INCONCLUSIVE。

## 24.3 Multi-family consistency

若 `REAL:MULTI`，要求：

```text
positive family 数 >= 2；
nonnegative family 比例 >= 0.50；
不存在 major family：
  point Delta <= -0.01
  AND U95(Delta) < 0。
```

不满足时 multi-family strong claim = INCONCLUSIVE，但允许报告 aggregate result。

## 24.4 OOD

OOD 固定为：

\[
\boxed{
\text{SECONDARY-DESCRIPTIVE GENERALIZATION EVIDENCE}.
}
\]

统一报告：

```text
AUPRC_partial；
Segment F1；
Boundary MAE / P90；
bona-fide FPR；
fully-manipulated coverage；
RB-EER。
```

OOD 不产生独立 formal verdict。

---

# 25. Stage 6D — CS Development

只有同一 scope：

\[
\boxed{
F1\text{--}F6=SUPPORTED
}
\]

且Stage4的M5三类保护性检查PASS后进入。

negative route：

\[
N\text{-A}\rightarrow N\text{-B}\rightarrow N\text{-C}.
\]

执行顺序：

```text
1. 固定 W/R；
2. 按 N route 构造合法 negative bank；
3. 通过 02 negative contract；
4. 冻结train/dev bank hashes及适用于test的generator/seed/合法性规则；
5. 之后才读取对应train/dev Y_x；test bank仅在6L后解封该partition时按固定规则生成，先保存hash再读Y；
6. 计算 informative gate；
7. 从同一M5起点追加训练CEL控制与CS分支。
```

两分支使用同一seed的M5 checkpoint、\(D_{cs-train}\)、paired sampling次序、optimizer、学习率/weight decay、\(\lambda_{CEL}\)、追加optimizer步数、有效batch及checkpoint选择规则。CEL控制继续优化loc+CEL，CS增加selectivity；g=0的pair仍以相同规则参与两侧基础目标，不能只给CS筛选更容易的数据。detector可按合同继续更新，W/R及negative bank不更新。CS新增参数仅在cs-dev和既有search budget内选择，共享配置不为某一侧单独调优。

第7.17节的margin及selectivity尺度用追加训练前的M5在cs-dev上的固定预测计算，先确定尺度再搜索CS参数，不使用test结果，也不以训练后CS输出定义门槛。追加训练步数、优化器配置和有效batch应在本阶段首次训练前登记，未落实时不能启动该阶段。

## 25.1 N-route exhaustion

若 N-A/B/C 全部无法在 dev 上产生满足：

```text
same support；
same admissibility；
d_W >= delta_W；
足够 informative pair coverage
```

的合法 negative bank，则：

\[
\boxed{
F7=\mathrm{INCONCLUSIVE}
}
\]

reason code：

```text
NEGATIVE_BANK_UNAVAILABLE
```

不得新增 N-D。

这不否定已支持的 CEL。

---

# 26. Stage 6L — CS Lock

在 `D_cs-dev` 上按第7.17节唯一规则计算并冻结：

```text
margin m；
epsilon_sel_gain。
```

同时冻结：

```text
scope；
N route；
negative-bank hash；
negative-generator / candidate-count / seed-rule hashes；
cs-train / cs-dev identity manifests；
paired CEL/CS start-checkpoint hashes；
shared optimizer / learning-rate / sampling / additional-update budget；
delta_W；
delta_Y_op；
lambda_sel；
epsilon_cs；
formal seeds；
guardrails；
informative-pair rule；
exact informative source-count plan；
clean/BF/fullfake未筛选子集identity manifests及各自minimum/precision计划；
M0 reference checkpoint hashes及dev-derived guardrail margins。
```

然后才解封：

\[
D_{\mathrm{cs-test}}.
\]

---

# 27. Stage 6T — F7

先执行 minimum / precision gate。

formal comparison：

```text
CEL = 从固定M5 checkpoint完成匹配追加训练的CEL控制；
CS-CEL = 从同一M5 checkpoint、同数据与更新预算追加selectivity训练的模型。
```

两个primary components在同一冻结test bank及同一mixed-partial informative pairs上评价；结论限定于登记的有限negative候选族和当前scope。三类guardrail分别在未经过informative筛选的独立登记子集上评价，见第28.4节。原始M5可作描述性参照，不替代匹配追加训练的CEL控制。

## 27.1 Discrimination

定义 \(z_{ufrs}^{M}=D_M^-(u,f,r,s)-D_M^+(u,f,r,s)\)。固定informative清单中共有U个parent sources，每个source有F_u个合格family、每个source/family有R_uf个合格realizations；pair权重为 \(w_{ufr}=1/(U F_u R_{uf})\)。清单和权重对两模型及所有seed一致；各family分别报告样本数和coverage，登记必要family无合格source时为INCONCLUSIVE。

\[
S_s(M)=\operatorname{wmedian}_{u,f,r}(z_{ufrs}^{M};w_{ufr}),\quad
S(M)=\frac1S\sum_{s=1}^S S_s(M),\quad
\Gamma_{sel}=S(CS)-S(CEL).
\]

Weighted median按值合并ties并递增累积权重；第一次超过0.5取该值，恰好0.5取该值与下一不同值的中点。等权时恢复通常样本中位数。先每seed算两个模型各自中位数，再作差并平均seed；禁止替换为逐pair差量的均值/中位数或先平均seed再取中位数。

每次第8.9节source-cluster bootstrap保留两模型和全部seed，按抽到的source multiplicity重新归一上述权重并重算S_s、S及Gamma。minimum按独立source而非窗口、realization数计算。Margin/epsilon_sel_gain仍由追加训练前固定M5的cs-dev预测计算，在6L冻结；重采样不重算这些门槛。

SUPPORTED：

\[
\Gamma_{sel}\ge\epsilon_{sel\_gain},
\]

\[
L_{95}(\Gamma_{sel})>0,
\]

且：

\[
S(CS)>0.
\]

PRACTICAL_NULL：

\[
U_{95}^{one-sided}(\Gamma_{sel})<\epsilon_{sel\_gain}.
\]

其它 INCONCLUSIVE。

## 27.2 Localization

\[
\Delta_7
=
AUPRC(CS)-AUPRC(CEL).
\]

SUPPORTED：

\[
\Delta_7\ge\epsilon_{cs},
\]

\[
L_{95}(\Delta_7)>0.
\]

PRACTICAL_NULL：

\[
U_{95}^{one-sided}(\Delta_7)<\epsilon_{cs}.
\]

其它 INCONCLUSIVE。

## 27.3 F7 final

只有：

```text
Discrimination SUPPORTED；
Localization SUPPORTED；
clean mixed-partial guardrail PASS；
bona-fide guardrail PASS；
fully-manipulated guardrail PASS。
```

才：

\[
\boxed{F7=SUPPORTED.}
\]

任一component PRACTICAL_NULL或三类guardrail中任一FAIL（分别记录PRIMARY_NULL或GUARDRAIL_FAIL，后者不冒称primary的效应上界）：

\[
\boxed{F7=PRACTICAL_NULL.}
\]

其它：

\[
\boxed{F7=INCONCLUSIVE.}
\]

---

# 28. Guardrail Decision Functions

## 28.1 Mixed-partial clean regression

\[
\Delta AUPRC_{clean}
=
AUPRC_{method,clean}-AUPRC_{M0,clean}.
\]

PASS：

\[
L_{95}(\Delta AUPRC_{clean})
\ge
-\epsilon_{clean}.
\]

FAIL：

\[
U_{95}(\Delta AUPRC_{clean})
<
-\epsilon_{clean}.
\]

其它 INCONCLUSIVE。

## 28.2 Bona-fide FPR

\[
\Delta FPR
=
FPR_{method}-FPR_{M0}.
\]

\[
\epsilon_{FPR}
=
\max(
0.005,\,
0.20\times FPR_{M0,dev}
).
\]

PASS：

\[
U_{95}(\Delta FPR)\le\epsilon_{FPR}.
\]

FAIL：

\[
L_{95}(\Delta FPR)>\epsilon_{FPR}.
\]

其它为INCONCLUSIVE。

## 28.3 Fully-manipulated coverage

\[
\Delta Coverage
=
Coverage_{M0}-Coverage_{method}.
\]

\[
\epsilon_{allfake}
=
\max(
0.01,\,
0.10\times Coverage_{M0,dev}
).
\]

PASS：

\[
U_{95}(\Delta Coverage)\le\epsilon_{allfake}.
\]

FAIL：

\[
L_{95}(\Delta Coverage)>\epsilon_{allfake}.
\]

其它为INCONCLUSIVE。

## 28.4 评价子集、reference与阶段合并

三项分别使用clean mixed-partial、bona-fide、fully-manipulated子集，全部与训练/dev身份隔离，在相应test seal中预登记，不按CS gate、negative-bank可用性或模型预测过滤。clean与informative可共享parent identity，其bootstrap multiplicity必须相同；纯真/纯假不需negative bank。三类各遵循第7.16、8.10节minimum/precision/cap，缺类或量不足为该guardrail INCONCLUSIVE，不默认PASS。CS的informative minimum不能抵扣这些子集。

M0是该版本Stage2L锁定、对应seed的source监督localizer checkpoint，整个版本不为某个方法另行重训。Stage4/5检查M5对M0，Stage6检查CS对同一M0；匹配追加训练CEL仍是F7 primary comparator。Bona-fide与fullfake容忍量由相应stage dev上固定M0计算，并在4L、Stage5解封前的plan、6L分别冻结，不用test计算门槛。第28.1节epsilon_clean引用第7.16节的clean容忍量。

组合guardrail：任一FAIL则FAIL；否则任一INCONCLUSIVE则INCONCLUSIVE；全部PASS才PASS。三项CI只代表各自marginal近似区间，不宣称联合95%覆盖。Stage4–6的主效果、guardrail状态、合并状态分别保存，不互相覆盖。

| 阶段 | 主效果之外的必需条件 | 未通过的结果与推进 |
|---|---|---|
| 4T | M5三类guardrail PASS | FAIL记Outcome N；INCONCLUSIVE记Outcome K；保留F4–F6效果判定，停止当前版本5/6，不主张可用CEL方法 |
| 5T | M5三类guardrail PASS | FAIL记Outcome N，Stage5合并verdict=INCONCLUSIVE并带GUARDRAIL_FAIL原因；INCONCLUSIVE记K；保留primary结果，不形成Strong Real CEL |
| 6T | CS三类guardrail PASS | FAIL使F7=PRACTICAL_NULL且reason=GUARDRAIL_FAIL；INCONCLUSIVE使F7=INCONCLUSIVE（若primary已明确NULL则仍NULL）；保留此前成立的CEL |

最低量/precision不足优先于对应项判定。Stage4若主效果已明确NULL仍记J；若主效果支持而guardrail失败记N，不把保护性失败当作机制效应小于epsilon。Stage5在guardrails PASS后才采用第24节primary/multi-family合并verdict；失败时不以primary上界解释guardrail。Stage6沿用第27.3节“明确NULL/FAIL优先，其余不确定”的组合。Outcome K/N可同时列原因，已成立的其它scope和旧版本证据保留各自身份。

---

# 29. Authenticity / Information-Boundary Audit

formal run 必须同时包含结构审计与经验稳定性审计。

## 29.1 Structural authenticity audit

必须确认：

```text
W/R 不读 Y；
W/R 不读 fake boundary；
W/R 不读 detector output；
detector loss 不更新 W/R；
shared representation 满足 02 C1/C2/C3；
CS gate 在 W/R/negative bank 冻结后才读 Y。
```

任一违反：

\[
\boxed{INVALID_IMPLEMENTATION.}
\]

## 29.2 Empirical authenticity-conditioned fidelity

Stage 3Q-A、3Q-B、3T 均保存：

```text
bona-fide W error / coverage；
fully-fake W error / coverage；
partial interior W error / coverage；
boundary-crossing W error / coverage。
```

若某 required stratum absolute fidelity 失败，则该 stratum 不得进入 F3 supported scope。

若 strata 之间差异显著但都满足 absolute floor，记录：

```text
AUTHENTICITY_STABILITY_FLAG
```

并执行 matched acoustic-difficulty diagnostic。

该 flag 不自动构成 structural leakage verdict。

---

# 30. Implementation Authenticity Audit

formal run 必须自动审计：

```text
A1  W/R 不读取 Y / detector；
A2  Grid Adapter fixed / no extrapolation；
A3  RN0 前 raw row-mass confidence 若存在已被显式保留到 R evidence；
A4  zero-row semantics 正确；
A5  formal G-A source gradient = 0；
A6  W_ref 仅 oracle / audit / screen；
A7  L/W/R/N route order；
A8  W-C 若启用，phoneme/CTC → physical-time mapping 可审计；
A9  M2 strict identity；
A10 M3′ 与 M5 使用相同 d / R / I_p^+，只改变 transported object；
A11 M3 native 不参与 F5 verdict；
A12 M4 使用 canonical post-fusion pre-logit tap；
A13 M4 无 projector / feature-specific realignment；
A14 Corr-Qual A/B 与 Corr-Test seals 未提前解封；
A15 Q-B INCONCLUSIVE sticky，不跳 route；
A16 formal Corr-Test 后不切 W/R route；
A17 F4 coverage/common-support decomposition 已保存；
A18 Stage P U-REF 未冒充 operational error；
A19 U-OP 仅使用 independent operational error；
A20 CS bank 先冻结后读 Y；
A21 informative gate 仅在 F3 supported scope 启用；
A22 Strong Real claim 满足 F1–F6 同 scope；
A23 source-identity leakage 检查通过；
A24 power lock 在 Stage 4T 前完成；
A25 primary inference 未对 5 seeds 做伪 bootstrap。
```

缺一项：

\[
\boxed{INVALID_FOR_FORMAL_EVIDENCE.}
\]

---

# 31. Canonical Entrypoint Contract

每个 Stage / Phase 必须有唯一 orchestration entrypoint。

强制边界：

```text
P0 / P1 / P2 / P3 相互独立；
0A / 0B 相互独立；
Stage 1 只做 premise；
2D / 2L / 2T 分离；
3D / 3Q-A / 3Q-B / 3L / 3T 分离；
4D / 4P / 4L / 4T 分离；
5T 单独；
6D / 6L / 6T 分离；
Stage 7 只打包 evidence。
```

任何 entrypoint 同时读取两个本应由 seal 隔离的 partition：

\[
\boxed{INVALID_IMPLEMENTATION.}
\]

---

# 32. 本地 WSL / Colab / GPU 执行规范

本地脚本与 Colab notebook 共用同一核心实现，每个入口只允许 orchestration：

```text
1. 打开本地项目目录，或在新环境 clone repo；
2. formal run checkout frozen commit；环境验收与开发记录当前源码快照；
3. 选择 artifact root；仅 Colab 使用 Drive 时执行 mount；
4. verify 01/02/03 hashes；
5. verify 当前阶段应已生成的 stage lock；
6. verify 当前阶段适用的 partition seal / data manifest；
7. 激活并验证项目环境；新环境按已记录版本安装；
8. load / build frozen feature cache；
9. run exactly one stage task；
10. save checkpoint；
11. save raw records；
12. save run_manifest.json；
13. save wall-clock / memory / retry metadata；
14. copy artifacts。
```

禁止：

```text
notebook 手改 threshold；
notebook 维护第二份算法；
不保存 raw records；
正式 test 中临时改变 batch sampling；
formal run 失败后换 seed 重跑直到满意；
因为本地或 Colab 中断而重置 optimizer history 却继续记为同一 run。
```

Stage P / Stage 0A 早于 Stage 0B，不要求未来 formal 阶段的锁；开发阶段也不要求尚未进入锁定阶段才会产生的 lock。记录实际使用的配置和数据 manifest。正式 test 仍必须验证对应已生成的 lock 与 seal；应有但缺失的文件不能标为“不适用”。

## 32.1 Frozen backbone caching

凡 backbone 完全 frozen 的阶段，feature extraction 默认一次性缓存。cache key 至少包含 source identity、实际输入波形及变换/预处理配置、backbone revision、特征层和数值精度；原音与不同通信 realization 分别校验，不得仅凭同一 source identity 复用特征。

缓存不属于模型可学习参数，不改变 formal semantics。

## 32.2 Checkpoint continuation

本地进程或 Colab session 中断只允许从同一 run manifest 与同一 optimizer / scheduler state 恢复。

无法恢复完整 training state 时，该 run 必须重启并保留原失败记录，不得把两段不同状态拼接为一个 formal run。

## 32.3 当前本地硬件与运行边界（2026-10-03 实测）

本节记录本地实施条件；研究门槛、数据隔离、模型对照与第7节数值配置仍按原协议执行。

| 项目 | 当前配置 / 实测结果 |
|---|---|
| Windows 主机 | Windows 11，版本 10.0.26300 |
| Linux 环境 | WSL2，Ubuntu 24.04.4 LTS，x86_64 |
| CPU | Intel Core i9-12900H，主机14核 / 20线程；WSL可用12个逻辑CPU |
| 物理内存 | 主机约32 GB；WSL配置上限12 GiB，swap 4 GiB |
| GPU | NVIDIA GeForce RTX 3060 Laptop GPU，6 GiB显存，compute capability 8.6 |
| NVIDIA Windows驱动 | 591.74；WSL CUDA Driver API初始化与设备枚举成功 |
| 存储 | ZHITAI TiPlus7100 2 TB NVMe SSD；WSL虚拟磁盘位于D盘 |
| 项目根目录 | `/home/richar/project/CEL` |
| 虚拟磁盘 | `D:\WSL_Space\Ubuntu\ext4.vhdx` |
| Python环境 | `/home/richar/project/CEL/.venv`，Python 3.12.3 |

检查时GPU空闲显存约4.5 GiB，WSL可用内存约10 GiB；这些是动态读数，不是可保证的运行配额。安装前D盘剩余约340 GiB；WSL内部报告约453 GiB可用，但虚拟磁盘继续增长受D盘实际剩余空间限制，两者不得相加。

当前适用范围：

- P0、音频预处理、标签/时间对应检查：适合本地执行。
- Stage P：按第7.2节冻结WavLM并缓存特征，训练256维、3-block TCN；预计适合本机，真实数据吞吐和最大长度需在首次运行时测定。
- 28次screen runs为可串行的总预算，不要求并行驻留；冻结特征的正式多seed实验也可按任务串行安排。
- 长音频、端到端解冻骨干、复杂多编码器或learned correspondence的可行性需单批实测；本节不承诺全套formal研究均能在6 GiB显存完成。

本机优先小批提取特征、按需加载缓存。每次运行记录峰值显存、内存和wall-clock，再决定是否需要调整运行资源。不得为适配硬件临时改变科学判据或删除困难样本。

## 32.4 本地软件环境与复验

2026-10-03已安装并通过本地验收的主要组件：

| 组件 | 实际版本 |
|---|---|
| Python | 3.12.3 |
| PyTorch / TorchAudio | 2.11.0+cu128 / 2.11.0+cu128 |
| PyTorch CUDA runtime | 12.8 |
| Transformers | 4.57.6 |
| librosa / SoundFile | 0.11.0 / 0.14.0 |
| FFmpeg / FFprobe | 6.1.1-3ubuntu5 |
| Notebook kernel | ipykernel 7.4.0，使用本项目 `.venv/bin/python` |

另已安装NumPy、SciPy、scikit-learn、pandas、Matplotlib、PyYAML、tqdm和pytest。项目使用独立 `.venv`；GPU版PyTorch与TorchAudio使用同一版本及CUDA构建。包含传递依赖的104个Python发行包版本统一保存为：

```text
requirements/local-cu128.lock.txt
```

直接依赖列表位于 `requirements/local.in`，用于维护软件依赖；重建当前环境以lock文件为准。系统音频工具使用Ubuntu软件包 `ffmpeg`、`libsndfile1`。音频读写采用SoundFile / FFmpeg，重采样可调用TorchAudio或librosa。

本地激活与复验：

```bash
cd /home/richar/project/CEL
source .venv/bin/activate
python -m pip check
python scripts/check_local_environment.py
```

在新的Ubuntu 24.04 / Python 3.12环境中重建：

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends ffmpeg libsndfile1 python3-venv
cd /home/richar/project/CEL
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements/local-cu128.lock.txt
.venv/bin/python scripts/check_local_environment.py
```

PyTorch CUDA wheels从[官方安装源](https://pytorch.org/get-started/previous-versions/)获取。本环境使用现有Windows NVIDIA驱动提供的WSL GPU通路；环境内CUDA依赖随PyTorch安装。`nvidia-smi`显示的CUDA上限、PyTorch实际CUDA runtime和独立CUDA编译工具链是不同信息，以复验报告记录为准。

复验脚本仅使用合成音频和随机权重，检查依赖、CUDA矩阵运算、WAV/Opus读写、重采样、WavLM Base结构前向以及小型卷积head的AMP反向和AdamW更新，不下载数据集或预训练权重。报告输出：

```text
artifacts/environment/local_environment.json
```

本次验收结果为 `PASS`：`pip check`无依赖冲突；CUDA矩阵运算、WAV/Opus编解码、TorchAudio/librosa重采样、随机权重WavLM Base前向、合成head的AMP反向与AdamW参数更新均成功。报告绑定复验脚本及依赖lock文件的SHA-256。

该报告中的耗时含首次调用开销，只用于软件安装验收；不代表预训练模型质量、真实数据吞吐、正式TCN实现或F1–F7证据，也不计入Stage P的28-run预算。首次正式使用WavLM前仍需获取并记录模型revision及特征配置。

## 32.5 本地显存、缓存与路径安排

Stage P的 `effective_batch_size: 32` 保持不变。显存不足时可采用micro-batch与梯度累积，使每次optimizer更新对应32个有效训练样本；1500 / 1000训练步按optimizer更新计。BCE/Dice逐样本计算后按完整有效batch平均，辅助项按02第4.1.1节各自分母归约；禁止改成pooled Dice或独立micro-batch均值。训练采样跨epoch持续组成32个条目的完整batch，不执行不足32的末尾optimizer更新。优先在optimizer更新边界保存checkpoint。

建议目录：

```text
/home/richar/project/CEL/
├── .venv/                 # 独立Python环境
├── .cache/                # 模型 / frozen features缓存，按需创建
├── data/                  # 数据及partition manifests，按需创建
├── artifacts/             # 环境检查、运行记录与checkpoint
├── requirements/          # 依赖列表与解析后的版本
└── scripts/               # 环境复验等入口
```

频繁读取的数据与缓存优先放在WSL的Linux文件系统；Windows挂载盘可存归档副本，符合[Microsoft的WSL文件存储建议](https://learn.microsoft.com/en-us/windows/wsl/filesystems)。特征按批读取，避免把全量特征和dense W装入12 GiB内存；实际稀疏/带状W可使用保持数学值不变的存储表示。

2026-10-03本地环境验收时尚未建立Git仓库，故该报告记录脚本内容hash。随后已初始化本目录Git仓库，修订前基线为`710ba11`；后续运行记录当时实际commit及未提交差异，正式实验按原协议冻结可核验的代码版本。本节不要求为环境安装提前建立未来阶段的锁。

---

# 33. Run Manifest

```json
{
  "research_version": "...",
  "route_fingerprint": "...",
  "parent_failure_event_ids": [],
  "experiment_plan_ref": "...",
  "budget_record_ref": "...",
  "git_commit": "...",
  "primitive_hash": "...",
  "method_contract_hash": "...",
  "global_protocol_hash": "...",
  "stage_lock_hash": "...",
  "stage": "...",
  "phase": "screen|dev|qualA|qualB|formal",
  "scope": "...",
  "route": "...",
  "seed": 0,
  "dataset_partition": "...",
  "dataset_manifest_hash": "...",
  "partition_seal_hash": "...",
  "candidate_hash": "...",
  "feature_cache_hash": "...",
  "checkpoint": "...",
  "records": ["..."],
  "wallclock_seconds": 0,
  "resume_count": 0,
  "execution_environment": "local-wsl|colab",
  "python_version": "...",
  "torch_version": "...",
  "cuda_runtime": "...",
  "device": "...",
  "environment_lock_hash": "...",
  "micro_batch_size": null,
  "gradient_accumulation_steps": null,
  "artifact_root": "..."
}
```

环境验收 / 开发尚无Git版本时，`git_commit`可为`null`，同时记录实际源码快照hash；不得伪造已冻结commit。只对当前阶段不适用的lock/seal字段使用`null`并注明原因；formal run仍须提供原协议要求的全部证据。

---

# 34. Artifact Structure

```text
artifacts/
├── versions/              # 后续版本隔离的运行产物与协议快照引用
├── stageP_screen/
│   ├── P0/
│   ├── P1/
│   ├── P2/
│   └── P3/
├── stage0_reference/
├── stage0_protocol/
├── stage1_premise/
├── stage2_localizer/
├── stage3_correspondence/
│   ├── dev/
│   ├── qual_A/
│   ├── qual_B/
│   └── corr_test/
├── stage4_mechanism/
│   ├── power_lock/
│   ├── dev/
│   └── formal/
├── stage5_real_chain/
├── stage6_cs/
└── final/
```

---

# 35. Stage Gate 总表

| Stage | 目标 | Gate | 未通过动作 |
|---|---|---|---|
| P0–P3 | cheap oracle mechanism signal | Screen verdict | stop / recorded deviation |
| 0A | reference feasibility | Dense / Sparse / None | downgrade / stop real claim |
| 0B | protocol freeze | hashes + seals | STOP |
| 1 | semantic premise | F1 / F2 | scope stop / inconclusive |
| 2 | localizer | localizer verdict |合法终点 LOCALIZER_UNUSABLE / inconclusive |
| 3Q-A/B | route qualification | W/R route verdict | frozen-order fallback / sticky inconclusive |
| 3T | operational feasibility | F3 | supported / realization failed / inconclusive |
| 4D | develop fixed comparators and M5 | dev selection + checkpoint identities | stop if required model unavailable |
| 4P | statistical feasibility after 4D | power lock | POWER_INFEASIBLE |
| 4T | mechanism necessity | F4/F5/F6 | Novelty Kill Gate |
| 5 | real-chain strength | real verdict | scope claim |
| 6 | selectivity | F7 | CS drop / controlled CS / appendix |
| 7 | evidence package | audit + hashes | no scientific changes |

---

# 36. Claim → Evidence Binding

| Claim | 必须证据 |
|---|---|
| Stage P mechanism promise | Screen only，不是论文 claim |
| task-relevant transport exists | F1 |
| occupancy transportable | F2 |
| operational W/R recoverable | F3 |
| sample-conditioned transport necessary | F4 + mandatory attribution decomposition |
| paired output transport non-redundant | F5 = M5 vs M3′ |
| output-space action independently useful | F6 = M5 vs canonical-tap M4 |
| CEL validated mechanism | same-scope F4+F5+F6 |
| Strong Real CEL | same REAL scope F1–F6 + Stage 5 |
| operational uncertainty robustness | U-OP secondary only |
| admissible local correspondence-error sensitivity | U-REF / Stage P only |
| OOD generalization | secondary descriptive only |
| CS selectivity adds value within registered negative family | F7 + matched CEL continuation |
| authenticity-label-agnostic estimator | structural audit |
| cross-authenticity fidelity stability | stratified Stage 3 evidence，不等价于 structural audit |

---

# 37. 合法项目终点

本节终点约束对应research version、scope及formal track。先保存原verdict、证据和claim边界；已授权研究任务随后按第39节主动诊断、检索并探索新路线。版本终止不等于整个研究任务永久停止，也不能将旧失败改写为成功。

## Outcome A — Strong Real CS-CEL

同一 real scope：

```text
F1–F6 SUPPORTED；
Stage5合并verdict SUPPORTED；
F7 SUPPORTED；
Stage4/5的M5及Stage6的CS三类guardrails均PASS。
```

允许主张：

\[
\boxed{\text{Strong Real CS-CEL}.}
\]

## Outcome B — Strong Real CEL

同一 real scope：

```text
F1–F6 SUPPORTED；
Stage4/5的M5三类guardrails均PASS，Stage5合并verdict SUPPORTED；
F7 PRACTICAL_NULL / INCONCLUSIVE；
或 NEGATIVE_BANK_UNAVAILABLE。
```

F7尚未运行时也可保留已成立的Strong Real CEL；没有F7支持时不主张CS extension。

## Outcome C — Controlled CS-CEL

CTRL scope：

```text
F1–F6 SUPPORTED且Stage4的M5三类guardrails PASS；
F7 SUPPORTED（含CS三类guardrails PASS）；
real scope 不足、未支持或仅 exploratory。
```

允许主张 Controlled CS-CEL，不得升级为 Strong Real CS-CEL。

## Outcome D — Controlled Mechanism CEL

CTRL scope：

```text
F1–F6 SUPPORTED且Stage4的M5三类guardrails PASS；
F7 未支持或未运行；
real scope insufficient / inconclusive / exploratory。
```

## Outcome E — Screen Non-Promising

```text
SCREEN_NONPROMISING。
```

停止当前版本的full formal CEL engineering；不是F5 formal refutation。研究任务按第39节转入失败分析与有依据的新版本探索。

## Outcome F — Premise Refuted

```text
F1 PREMISE_REFUTED；
或 F2 PREMISE_REFUTED。
```

停止对应 scope。

## Outcome G — Operational Scope Refuted

```text
Stage 3Q-A/B 中 W-A/B/C/D 全部明确 REJECTED / REJECTED_EXTERNAL。
```

因此：

\[
F3=OPERATIONAL\_SCOPE\_REFUTED.
\]

## Outcome H — Locked Operational Realization Failed

```text
已通过双层 qualification 并锁定的 W/R；
Stage 3T 独立 Corr-Test 明确 REJECTED。
```

因此：

\[
F3=OPERATIONAL\_REALIZATION\_FAILED.
\]

当前 protocol 终止，不切 route；不把该结果扩大解释为整个 operational family 全部被证伪。

## Outcome I — Localizer Unusable

```text
Stage 2D 全 route dev failure；
或 Stage 2T locked localizer formal failure。
```

机制验证 track 停止。

允许保留：

```text
F1/F2/F3 premise evidence；
detection-only contextual baseline；
failure analysis。
```

不得进入 Stage 4。

## Outcome J — Mechanism Partial Null

F4/F5/F6 任一：

```text
PRACTICAL_NULL。
```

停止 full-scale CEL；不进入 formal Stage 5/6。

## Outcome K — Terminal Inconclusive

包括：

```text
precision-only reserve 已耗尽；
POWER_INFEASIBLE；
PRECISION_INFEASIBLE；
formal effect test 本身 INCONCLUSIVE；
N-route exhaustion 导致 F7 INCONCLUSIVE。
```

必须如实报告，不允许继续无限补样。

## Outcome L — Protocol / Implementation Invalid

出现：

```text
seal violation；
oracle-as-operational；
W/R authenticity boundary violation；
M3′ comparator contract violation；
M4 tap violation；
source identity leakage；
formal test 后 route switching；
effect-driven optional stopping；
hash / provenance 不可恢复。
```

则：

\[
\boxed{INVALID\_FOR\_FORMAL\_EVIDENCE}
\]

或：

\[
\boxed{INVALID\_IMPLEMENTATION}.
\]

只能修复工程/protocol violation后从受污染stage之前恢复；污染evidence不得保留为formal evidence。若测试信息已经暴露，修复代码不能使该测试重新独立，须按第39.7节恢复数据隔离或建立新版本。

## Outcome M — REAL Scope Mechanism Supported, Real Strength Not Supported

同一REAL scope的F1–F6全部SUPPORTED且Stage4保护性检查通过，但Stage5 primary为PRACTICAL_NULL、Stage5保护性检查亦通过。允许报告该已测试REAL scope内的机制贡献及真实链效应上界；不主张Strong Real CEL，也不能在未独立验证CTRL时改称Controlled Mechanism CEL。

若按第25节另执行了F7，其结果作为该scope及登记negative族内的扩展证据单列，不把Stage 5未支持改写为Strong Real CS-CEL。若Stage 5为INCONCLUSIVE则使用Outcome K并同样保留已有机制证据。已有CTRL结论可按自己的独立证据同时保留，不能跨scope拼接。

---

## Outcome N — Guardrail Not Satisfied

当前版本Stage4或Stage5的必要guardrail明确FAIL。保留已得到的主效应、scope及失败维度，停止相应可用方法/Strong Real主张；不把该状态冒充PRACTICAL_NULL效应上界。三类guardrail有INCONCLUSIVE而无FAIL时使用K。CS阶段的guardrail失败按F7记录并保留先前合法CEL结论。

# 38. Failure Routing Owner

为防止失败后职责不明，所有终点绑定默认owner。owner负责完成动作：Research Scout核验文献与反证，Method Architect提出保持01的新假设，Research Planner选择有限候选与判别实验，Implementer执行授权内实现，Implementation Auditor核对失败身份、路线差异及证据隔离。职责可由同一协调者分阶段承担；必要独立复核按04执行。

| Outcome | 默认 owner | 下一动作 |
|---|---|---|
| E Screen Non-Promising | Method Architect + Research Scout | 判断是否放弃候选机制或启动新研究版本 |
| F Premise Refuted | Method Architect | 重新评估算法前提；不得改 01 适配结果 |
| G Operational Scope Refuted | Method Architect | 若继续，只能提出新的 operational family 并建立新版本 |
| H Locked Realization Failed | Method Architect + Research Planner | 分析 qualification-to-test shift；新版本方可尝试其它 route |
| I Localizer Unusable | Method Architect | 重选 localizer family 需新方法版本；当前 formal track 终止 |
| J Mechanism Partial Null | Research Scout + Method Architect | novelty downgrade / claim rewrite |
| K Terminal Inconclusive | Research Planner | 判断是否值得新版本扩大资源，不得在当前 protocol 内循环补样 |
| L Protocol Invalid | Implementer + Implementation Auditor | 修复真实性 / 工程问题并重跑受污染阶段 |
| M REAL Mechanism Only | Method Architect + Research Planner | 保留已测scope机制证据，报告真实强度未支持；新路线按第39节推进 |
| N Guardrail Not Satisfied | Method Architect + Research Scout | 记录退化维度及已有机制证据，检索并验证针对退化原因的新候选 |

---

# 39. 反循环返修纪律

本协议明确区分三类事件。

## 39.1 Scientific failure

例如：

```text
F3 failure；
F5 practical-null；
F6 practical-null；
F7 null。
```

处理方式：

```text
输出冻结 verdict；
降级 claim；
必要时新建 research version。
```

**不得改写已用于产生结果的02/03快照来救该结果。** 保持01原语的实质新路线由第39.4–39.7节进入新版本，不占用旧版成功名义。当前尚未开始实验的文档修订不构成事后救结果。

## 39.2 Statistical insufficiency

例如：

```text
power > cap；
precision reserve 耗尽；
formal CI 仍跨越 effect threshold。
```

处理方式：

```text
终局 INCONCLUSIVE / POWER_INFEASIBLE；
不得无限补样；
如需更大研究，建立新的预注册版本。
```

## 39.3 Engineering / authenticity failure

例如：

```text
shape bug；
scheduler state bug；
feature cache 错位；
seal 提前读取；
M3′ 实现并非 same-discrepancy；
M4 tap 实际取错层。
```

处理方式：

```text
标记 INVALID；
修复实现；
从受污染 stage 前重新运行。
```

工程修复不得改变算法语义、threshold、route order或comparator；此类变化属于新方法/协议版本，不能将科学失败改称工程错误。测试已暴露时，重跑必须满足第39.7节的独立性要求。


## 39.4 跨版本失败账本

每次run、候选开发/qualification失败、无效执行、资源中断及终局不确定都保存原始记录，并向项目共享的 `research/ledger/events.jsonl` 追加事件。账本目录由首次实际任务创建并纳入版本管理；目前没有研究run，不虚构失败条目。大型日志/checkpoint保存在artifact root，账本保存可解析引用及hash，并按项目备份安排保全。`research/routes/index.json`仅为从账本可重建的路线索引，不能替代原记录。

事件必须包含：

```json
{
  "event_id": "...",
  "timestamp_utc": "...",
  "event_type": "failure|interrupted|inapplicable|diagnosis_update|retry|closure",
  "parent_event_ids": [],
  "research_version": "...",
  "stage_scope": "...",
  "route_fingerprint": "...",
  "method_semantics_ref": "...",
  "run_manifest_ref": "...",
  "category": "scientific|statistical|engineering_authenticity",
  "verdict": null,
  "facts_and_artifact_refs": [],
  "applicability_conditions": "...",
  "affected_evidence_refs": [],
  "diagnosis_hypothesis": "...",
  "diagnosis_evidence_refs": [],
  "unresolved_questions": [],
  "dedup_matches": [],
  "material_change_and_retry_basis": "...",
  "literature_record_ref": null,
  "experiment_plan_ref": null,
  "data_exposure_record_ref": "...",
  "budget_record_ref": "...",
  "owner": "..."
}
```

已有run manifest提供代码/config/模型/数据/seed/环境身份，不重复存大对象。未运行、结构不适用、缺失数据与无有效科学评价的中断分别记录，verdict保持null并说明原因，不计成科学失败。观察事实、冻结verdict与原因假设分开；原因未知可以明确写unknown，不能编造诊断。

事件只追加。更正、重试、否定旧诊断、关闭问题均通过新event引用旧event完成；不得删除失败、覆盖旧分数或只留最好seed。每个新任务、新版本启动及训练前先读全项目路线索引和匹配事件，不能仅阅读当前版本目录。

## 39.5 路线查重与合法再试

`route_fingerprint`来自规范化、可读的机制说明：假设、表示与更新来源、W/R或localizer估计器、损失与teacher拓扑、信息/梯度边界、支持规则及必要对照。规范化规则/version与该说明一并保存。另以exact run identity记录具体代码、参数、模型revision、数据和seed；两种身份不能混用。

去重同时检查fingerprint和语义近似路线，并结合失败适用的scope、数据条件、资源与评价问题。相同机制改名称、换commit、改seed、换目录或换research version不会清除旧失败；配置变化必须解释其因果作用，不能仅凭hash不同声称新路线。相同hash但关键scope/条件变化也不能机械拒绝，要记录适用性判断。

重复执行只有以下可检验依据之一成立才允许：已定位且修复的工程缺陷；新证据直接针对失败原因支持机制/条件变化；预注册独立复现；原协议仍允许且未看正式effect的精度规划。每次再试关联旧failure ID、具体变化、预期可区别观察及停止条件。没有新依据时沿用旧结论并跳过，不花预算再次“试试看”。更换seed、无机制解释的调参、把终局不确定重新开run，都不是独立依据。独立复现保留全部预定seeds与结果，不挑成功run。

## 39.6 失败后主动文献检索与有限实验

失败后负责人持续完成以下动作，而非只提交一句“建议换路线”：

1. **定位失败机制。** 读取失败原始记录，区分科学、统计、工程、资源和数据适用性问题；能直接修复的工程问题先做最小修复核验，未知原因保留备选解释。
2. **检索一手证据。** 自主检索针对该机制的原论文、作者代码/数据、官方技术资料；同时查已知限制、反例和后续修正。保存检索日期、查询词、已读来源URL/DOI及版本、支持段落/公式定位、适用前提及与本项目的差异。预印本标明状态；仅有摘要/二手转述时标明未核验。论文事实与本项目推断分开，不把引用数量当作成功证据；无相关证据也记录，不伪造替代方案。
3. **选有限候选。** 每轮至多3条机制上有区别且未被相同条件失败覆盖的候选，按解释力、原语符合性、可判别性、数据合法性及资源成本排序。记录接受/拒绝理由与旧路线的实质差异，不要求预先枚举全部未来路线。
4. **先登记最小判别实验。** 记录假设、必要对照、允许读取的数据、唯一观察量、继续/拒绝/不确定规则、实现真实性检查、具体run/步数/时间或算力上限及累计已用预算，再实施。优先用工程反例、已有开发证据或小规模pilot区分机制；正式命题仍须完整协议。失败后pilot结果只有探索意义，不直接继承旧formal资格。
5. **按证据继续或结束本轮。** 在已有资源、数据与执行授权内，自主实现并验证所选路线，写入全部结果和下一动作。候选有支持才进入该版本后续阶段；失败则记账查重，进入剩余候选。没有新的非重复候选、独立数据或可判别实验，或本轮/任务预算到顶时，保存结论并说明具体限制，不无上限试到成功。

首次续行实验前，负责人须在既有授权范围内登记有限、数值化的任务/执行段总预算及每轮子预算；用户已有cap则沿用，未给具体数值则由负责人依据可用资源事前制定保守的有限cap，无需逐路线请示。所有候选、轮次、版本共同计入该总cap，失败、无效及中断执行也计入；每轮记录已用和剩余量。达到上限即结束该执行段并交付，不得通过换轮次、版本、任务标识或自行提高cap继续领取预算。超出原授权的新增投入须用户明确授权；可继续完成不依赖新增运行资源的分析。当前若只授权设计，则推进检索、方案和代码准备，不为纯文档任务虚设实验预算。新一轮还必须有新证据、实质候选或已解决外部条件，不能仅重新编号。记录保存在 `research/literature/`、`research/plans/` 并由账本相互引用。

## 39.7 原协议fallback与新research version

当前版本内仅执行已冻结的路线顺序、触发条件和预算；sticky不确定、test后不切路线等规则继续有效（第17节明确的R-0出口除外）。新的方法族、实质机制配置或研究问题使用新的research_version，先固定旧版Outcome、01/02/03/04快照hash、run/失败账本及数据暴露记录，再登记新版方法/协议与验证计划。Git commit或内容hash能够恢复每版完整快照；本目录可维护当前设计，但旧证据永远引用旧快照。

01原语保持不变时，已授权的失败后研究续行包括自主检索、候选选择、新版本设计、实现及授权预算内验证，不因“新路线/新版本”字样本身重复请示。改变01研究问题/核心算法关系、实际增加超授权资源或付费、取得新受限数据权限、外部发布/不可逆写入等超出原范围的动作，才提交具体待决定项，并继续完成不依赖它的工作。

凡旧test信息用于失败诊断、选路或新版设计，就属于已暴露信息：其对应parent sources不得再充当新版独立确认test，也不能通过换codec/window/seed重新变成未见测试。旧数据可登记为探索/dev用途；新版正式结果使用未参与选择且source-identity隔离的新test，重新完成受影响阶段的freeze/qualification。保留所有尝试与暴露历史；多轮结果分别报告，不跨版本择优拼接，也不声称多轮搜索后的单版本p值具有整个研究程序的统一错误率控制。

---

# 40. Stage 7 — Final Evidence Package

Stage 7 只允许从 frozen artifacts 生成结果包，不允许重新训练或修改科学配置。

必须包含：

```text
01 / 02 / 03 hashes；
git commit；
environment lock；
dataset split / seal hashes；
all run manifests；
F1–F7 verdict table；
scope table；
route qualification history；
Stage 3 authenticity-stratified fidelity；
Stage 4 power lock；
M3′ control-verification artifact；
M4 canonical-tap verification artifact；
F4 coverage/common-support decomposition；
U-REF vs U-OP distinction report；
guardrails；
secondary M3 native results；
RB-EER secondary table；
failure / invalid-run ledger；
检索记录、候选取舍、重试依据及跨版本关系；
数据暴露清单与轮次/任务累计预算；
claim-evidence matrix。
```

最终论文表格不得只保留成功 run；所有 formal invalidation、route rejection 与 terminal evidence 都必须可追踪。

---

# 41. 设计覆盖清单

以下项目记录文档中的设计约束，不表示代码、数据或科学验证已完成；实际完成度以所属阶段产物与审查为准。

```text
[✓] 01 的 F1–F7 语义未修改；
[✓] 02 的 M3′ 已成为 F5 唯一 formal comparator；
[✓] M3 native 已降为 secondary，不再污染 F5 attribution；
[✓] M4 feature tap 由 02 唯一化，03 只锁 exact path；
[✓] F4 强制 coverage / common-support 分解；
[✓] Stage P U-REF 与 operational U-OP 已拆分；
[✓] authenticity structural isolation 与 empirical stratified fidelity 已拆分；
[✓] F3 informative-gate dependency 已显式；
[✓] Stage 2 / 3 可并行，F3 critical path 不再被 localizer 线性阻塞；
[✓] Corr-Qual A/B 在 formal Corr-Test 前完成 route switching；
[✓] Corr-Test clear failure 有合法 OPERATIONAL_REALIZATION_FAILED 终点；
[✓] OPERATIONAL_SCOPE_REFUTED 只用于全 route exhaustion；
[✓] LOCALIZER_UNUSABLE 有合法项目终点；
[✓] F3 有 CI precision gate；
[✓] Stage 4 有 Holm-aware power lock；
[✓] 5-seed bootstrap 饱和问题已消除；
[✓] effect-driven optional stopping 被禁止；
[✓] supplement reserve 有上限；
[✓] N-route exhaustion 有 F7 INCONCLUSIVE 合法路径；
[✓] Controlled CS-CEL 有独立 Outcome；
[✓] margin m 有确定的 D_cs-dev 冻结规则；
[✓] frozen backbone feature caching 已显式；
[✓] Stage 0A 包含 real reference early checkpoint；
[✓] RB-EER 固定为 secondary，不改变 verdict；
[✓] failure routing owner 已定义；
[✓] 原版本终点、新版本续行与保护性失败分开记录；
[✓] 失败查重、文献检索、有限新路线与证据隔离有明确合同。
```

---

# 42. 最终冻结声明

本研究版本内的推进逻辑固定为下列顺序；失败后的项目级续行按第39节进入独立新版本，不改写本版结果：

\[
\boxed{
\text{Stage P}
\rightarrow
\text{F1/F2 Premise}
\rightarrow
\text{Parallel Localizer + W/R Feasibility}
\rightarrow
\text{Power-Locked F4/F5/F6}
\rightarrow
\text{Real Strength}
\rightarrow
\text{CS Extension}.
}
\]

其中：

\[
\boxed{
F5:
M5>M3'
}
\]

是 primary non-redundancy gate；

\[
\boxed{
F6:
M5>M4_{\text{canonical pre-logit tap}}
}
\]

是 output-action-space gate；

\[
\boxed{
F4
}
\]

必须伴随 coverage / common-support attribution decomposition；

而：

\[
\boxed{
Stage\ 4
}
\]

仍为 Formal Novelty Kill Gate。

本文件自此冻结为：

\[
\boxed{
\textbf{
03 EXECUTION PROTOCOL:
REBUILT-FINAL
/
01-02-ALIGNED
/
STATE-CLOSED
/
POWER-LOCKED
/
PRE-RUN-CONFIGURATION-REQUIRED
}
}
\]

以下情况不得重新打开本文：

```text
formal 结果不好；
某 route 失败；
换 feature tap 可能更强；
M3 native 比 M3′ 更强；
还可以增加 sanity check；
还可以继续补样；
可以增加一个新 W/N route。
```

这些情况只能触发：

```text
冻结 verdict；
claim downgrade；
terminal inconclusive；
纯工程修复；
或 evidence-isolated 新研究版本。
```
