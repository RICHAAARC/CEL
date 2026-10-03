# 02_方法实现机制设计：CEL / CS-CEL 重构冻结版

> 上游唯一算法原语：`01_算法原语设计_CEL_CS-CEL.md`  
> 下游唯一执行协议：`03_项目推进路线_CEL_CS-CEL_REBUILT_FINAL.md`  
> 文档职责：在不修改 01 冻结算法原语的前提下，完整定义 CEL / CS-CEL 的方法空间、数学合同、强对照、信息边界、独立 correspondence validation、失败路线以及 claim 解释。  
> 文档层级：**Method Contract / Mathematical Specification / Mechanism Identifiability Contract**  
> 状态：**REBUILT-FINAL / 01-ALIGNED / CONTROL-CLOSED / METHOD-SPACE-CLOSED**

> 修订：2026-10-03，实施前修订 v1.2。保留01原语，明确监督权重与有效batch归约；主指标、网格实例和失败后的新版本研究流程由03落实。实际运行就绪状态以数据、配置和阶段记录为准。

---

# 0. 权威链、设计目标与重构原则

本项目唯一权威链为：

\[
\boxed{
01\ \text{Algorithm Primitive}
\rightarrow
02\ \text{Method Contract}
\rightarrow
03\ \text{Execution Protocol}
}
\]

## 0.1 01 唯一拥有

```text
研究问题；
CEL / CS-CEL 核心算法语义；
F1–F7 原语级含义；
创新边界；
原语偏离条件。
```

本文不得修改上述内容。

## 0.2 02 唯一拥有

本文唯一、完整地定义：

```text
基础符号与网格合同；
base supervision；
M0–M6 与 formal control family；
Localizer / W / R / N 方法族；
Grid Adapter；
d / d_W / d_Y；
独立 correspondence validation 接口；
G-A formal topology；
F4 / F5 / F6 的可辨识对照结构；
correspondence uncertainty 的两层检验语义；
CS informative gate；
CS-CEL objective；
route order / exhaustion；
object status；
claim interpretation；
隐藏假设与依赖边。
```

## 0.3 03 唯一拥有

03 唯一定义：

```text
Stage / phase；
partition；
sample size；
数值 threshold；
统计检验与 power；
seed；
search budget；
seal / lock；
Colab / GPU 执行；
artifact；
合法项目终点。
```

## 0.4 本次重构的四条方法学原则

本文不采用“补丁式 control”。所有 formal mechanism controls 统一遵循：

1. **单变量原则**：formal comparator 与 M5 只允许在待检验机制维度上发生必要差异；
2. **同信息预算原则**：M2 / M3′ / M4 / M5 使用相同 source supervision、相同 paired data、相同 operational W/R 信息预算；
3. **事前唯一化原则**：会显著影响 F4/F5/F6 方向的对象必须在 formal test 前唯一冻结；
4. **解释分解原则**：当一个 formal effect 可能由不同机制来源产生时，必须同时报告其机制分解，不得把总效应自动解释为单一机制。

---

# 1. 科学状态与对象层级

CEL 当前状态固定为：

\[
\boxed{\text{Candidate Primary Mechanism}}
\]

CS-CEL 当前状态固定为：

\[
\boxed{\text{Candidate Strong Extension}}
\]

W / R / Grid Adapter 统一定位为：

\[
\boxed{\text{Enabling Infrastructure}}
\]

只有同一 claim scope 下：

\[
F4=F5=F6=\mathrm{SUPPORTED}
\]

才允许将 CEL 升级为：

\[
\boxed{\text{Validated Mechanism Contribution}}
\]

只有进一步满足：

\[
F7=\mathrm{SUPPORTED}
\]

才允许将 CS-CEL 升级为：

\[
\boxed{\text{Validated Strong Extension}}
\]

---

# 2. 基础符号与全局合同

对 paired sample：

\[
p=(x,x'),
\]

source / target manipulation-output grid 长度分别为：

\[
N_p,\qquad M_p.
\]

模型输出：

\[
P_\theta(x)\in[0,1]^{N_p},
\qquad
P_\theta(x')\in[0,1]^{M_p}.
\]

source / target manipulation occupancy：

\[
Y_x\in[0,1]^{N_p},
\qquad
Y_{x'}\in[0,1]^{M_p}.
\]

operational correspondence：

\[
\hat W_p\in\mathbb R_{\ge0}^{M_p\times N_p}.
\]

reliability：

\[
\hat R_p\in[0,1]^{M_p}.
\]

## 2.1 Direct-supervision valid set

对任意直接监督音频 \(u\)，定义：

\[
\boxed{
\mathcal I_u^{sup}
=
\{i:\text{output cell }i\text{ 属于真实非 padding 音频支持}\}.
}
\]

因此：

```text
padding cell 不进入 direct supervision；
真实静音属于 direct supervision；
真实 bona-fide 区域属于 direct supervision；
只有 padding / batch-fill 被排除。
```

## 2.2 Output-grid correspondence semantics

对每个 target row：

\[
\sum_j\hat W_{p,ij}
=
\begin{cases}
1,&\text{valid correspondence},\\
0,&\text{correspondence unavailable}.
\end{cases}
\]

zero row 只表示：

\[
\boxed{\text{correspondence unavailable}}
\]

不得解释为 occupancy 0 或 manipulation probability 0。

## 2.3 Authenticity-isolation contract

构造 \((\hat W_p,\hat R_p)\) 时禁止读取：

```text
fake / real labels；
Y；
fake boundaries；
P_theta；
detector confidence；
detector gradients；
CEL / CS detector-side gradients。
```

允许三种 representation isolation。

### C1 — Frozen shared pretrained encoder

localizer 与 correspondence branch 可共享 pretrained representation，但共享 encoder 必须完全 frozen。

### C2 — Separate correspondence encoder

correspondence branch 使用独立 encoder，且仅允许 frozen 或 correspondence-only objective 更新。

### C3 — Detached correspondence copy

若 localizer backbone 接受 authenticity supervision，则 correspondence branch 必须使用 detached / independent copy。

禁止：

\[
\boxed{
\text{authenticity-trained trainable shared representation}
\rightarrow
(\hat W,\hat R).
}
\]

## 2.4 Partial / unmatched contract

所有 W 路线必须允许：

```text
null / skip state；
gap；
partial alignment；
insertion / deletion；
unmatched target row。
```

## 2.5 Operational-valid set

全文唯一使用：

\[
\boxed{
\mathcal I_p^+
=
\left\{
i:\hat R_{p,i}>0,\ \sum_j\hat W_{p,ij}>0
\right\}.
}
\]

若：

\[
\mathcal I_p^+=\varnothing,
\]

则该 pair 的 CEL / CS term 为：

\[
\boxed{\text{not applicable}}
\]

不得记为 zero loss。

## 2.6 训练与单音频推理接口

训练输入为paired \(x,x'\)、source标签及该阶段允许的W/R；formal primary仍按第4节只使用source直接监督。部署接口为单个待检音频 \(u\mapsto P_\theta(u)\)，输出与该音频自身物理时间网格绑定的manipulation field及真实音频有效mask。推理不需要原始source音频、通信链ID、W/R或negative bank；这些对象服务于训练和机制验证。阈值化区间、切窗合并及重采样时间映射按03事前固定，不能借用测试标签。

---

# 3. 显式假设与依赖边注册表

为避免隐藏假设在执行阶段被误当成已证明事实，本文显式注册以下方法级假设。

## A1 — Direction / confidence factorization

Grid Adapter 的 row normalization：

\[
\operatorname{RN}_0(\cdot)
\]

会丢弃原始 row mass。本文因此显式假设：

> correspondence 的“方向 / 分布形状”由 \(\hat W\) 表示，而被 row mass 丢弃的置信信息可以由独立 \(\hat R\) 恢复或近似补齐。

若某 W estimator 的 row mass 本身包含关键 uncertainty，则该信息必须在进入 \(\operatorname{RN}_0\) 前显式映射到 reliability evidence，不得静默丢弃。

## A2 — Physical-time grid compatibility

Grid Adapter 假设内部 alignment grid 可以被固定映射到 physical time。对 W-C（phoneme / CTC）尤其要求：

> phoneme / CTC position → physical-time 的映射必须来自独立 alignment / timing mechanism，且不得读取 authenticity label、Y 或 detector output。

若 W-C 无法形成可审计的 physical-time 映射，则 W-C 对 formal CEL 不具资格。

## A3 — Informative-gate inheritance

CS operational gate 使用 \(\hat W_pY_x\) 近似原语中的真实 transport 语义，因此：

\[
\boxed{
\text{informative-gate validity}
\Leftarrow
F3\ \text{correspondence fidelity}.
}
\]

F3 未通过时不得解释 CS informative gate 的科学含义。

## A4 — Admissible uncertainty scope

本文的 admissible perturbation 只描述保持预注册 monotonicity / locality / slope class 的 correspondence error。它不覆盖：

```text
完全错配；
非单调 catastrophic skip；
错误 transcript anchoring；
跨段重复映射；
reference 本身错误。
```

因此，oracle-centered ε-sweep 只回答“admissible local error sensitivity”，不得外推为全部 operational failure robustness。

---

# 4. Base Supervision 与基础模型

formal mechanism fairness family 的 base supervision 固定为：

\[
\boxed{
\mathcal S_{base}
=
\text{source-view direct localization supervision only}.
}
\]

即：

```text
source x 使用 Y_x；
target x' 不使用 Y_x' 作为 formal primary mechanism signal。
```

target direct supervision 仅可用于 secondary strong-supervision / oracle study。

## 4.1 Supervised localization functional

给定：

\[
P,Y\in[0,1]^L,
\qquad
\Omega_i\ge0,
\qquad
\mathcal I\neq\varnothing,
\]

定义：

\[
\mathcal L_{WBCE}
=
\frac{\sum_{i\in\mathcal I}\Omega_i\operatorname{BCE}(P_i,Y_i)}
{\sum_{i\in\mathcal I}\Omega_i},
\]

\[
\mathcal L_{WSoftDice}
=
1-
\frac{2\sum_{i\in\mathcal I}\Omega_iP_iY_i+\epsilon_D}
{\sum_{i\in\mathcal I}\Omega_iP_i+\sum_{i\in\mathcal I}\Omega_iY_i+\epsilon_D}.
\]

定义：

\[
\boxed{
\mathcal L_{sup}
=
\lambda_{BCE}\mathcal L_{WBCE}
+
\lambda_{Dice}\mathcal L_{WSoftDice}.
}
\]

source localization objective：

\[
\boxed{
\mathcal L_{loc}
=
\mathcal L_{sup}
(P_\theta(x),Y_x;\Omega_x,\mathcal I_x^{sup}).
}
\]

source权重唯一为 \(\Omega_{x,i}=|B_{x,i}\cap\operatorname{supp}(x)|\)，单位为秒，即该输出cell的真实音频时长；不按标签、类别频率或预测加权。padding权重为0，真实尾部不足整格按实际时长保留。\(\sum_{i\in\mathcal I}\Omega_i>0\) 是可计算前提；空支持或非有限输入属于无效样本，不以零损失掩盖。

### 4.1.1 有效batch与梯度累积

一个optimizer更新的有效batch记为 \(\mathcal B\)。先按上式分别计算每个source样本的BCE和Dice，再对全部监督有效样本等权平均：

\[
\mathcal L_{loc}^{batch}=\frac{1}{|\mathcal B|}\sum_{p\in\mathcal B}\mathcal L_{loc}(p).
\]

禁止先拼接不同样本的cell再计算一个pooled Dice。相同source出现于不同pair时，按冻结sampling清单中的样本条目计数，不在不同方法间临时去重。

对M2、M3′、M3 native、M4、M5、M6的每个辅助项，先计算各pair自己的R/支持加权标量，再对该项适用的pair集合 \(\mathcal A_t\subseteq\mathcal B\) 等权平均。CS按第17节保留gate乘数：\(\mathcal L_{sel}^{batch}=|\mathcal B|^{-1}\sum_{p\in\mathcal B,\ g_p^{CS}=1}\mathcal L_{sel}(p)\)；分母为完整监督有效batch大小，包含同batch中 \(g=0\) 的pairs，不能改成只按informative数量归一化。\(g=0\)不计算缺失bank的D-minus，仍参加相同loc/CEL基础目标。某辅助项没有适用pair时，不构造该项梯度贡献，日志记录not applicable及适用数0，不输出观测到的零损失；CS另外同时记录完整batch分母和informative数。全部batch均无有效source是实现失败。

micro-batch仅分割计算。每个source损失除以完整有效batch的样本数，每个辅助pair损失除以上述该项在完整有效batch内的分母；不能分别对各micro-batch求均值后机械相加。分母未知时先完成有效性判定或缓存必要统计，再反传；每个有效batch只进行一次optimizer/scheduler更新。该规则适用于CS、末尾batch及所有训练对照。

## 4.2 M0 — Base Localizer

\[
\boxed{\mathcal L_{M0}=\mathcal L_{loc}.}
\]

M0 用于 localizer 基线与 guardrail reference。

## 4.3 M1 — Time-Preserving Communication Augmentation

仅允许使用由 03 的 C0 gate 证明为 time-preserving 的 transforms。

M1 只作为 contextual robustness baseline，不属于 F4/F5/F6 fairness family。

## 4.4 M6 — Oracle-CEL

M6 以 independent：

\[
W_p^{ref},\qquad R_p^{ref}
\]

替代 operational \(\hat W_p,\hat R_p\)。

定义：

\[
\mathcal I_p^{ref}
=
\left\{i:R_{p,i}^{ref}>0,\ \sum_jW_{p,ij}^{ref}>0\right\},
\]

\[
\boxed{
\mathcal L_{OracleCEL}(p)
=
\frac{
\sum_{i\in\mathcal I_p^{ref}}R_{p,i}^{ref}
 d(P_\theta(x')_i,[W_p^{ref}\operatorname{sg}(P_\theta(x))]_i)
}
{\sum_{i\in\mathcal I_p^{ref}}R_{p,i}^{ref}}.
}
\]

\[
\boxed{
\mathcal L_{M6}
=
\mathcal L_{loc}
+
\lambda_{CEL}\mathcal L_{OracleCEL}.
}
\]

M6 仅用于 oracle upper bound、failure decomposition、screen 与 audit，不得作为 operational CEL claim。

---

# 5. Transport Grid Adapter

correspondence estimator 可在内部网格输出：

\[
\widetilde W_p\in\mathbb R_{\ge0}^{L_{t,p}\times L_{s,p}}.
\]

定义固定 physical-time interpolation operators：

\[
G_{s,p}^{o\rightarrow h}\in\mathbb R_{\ge0}^{L_{s,p}\times N_p},
\]

\[
G_{t,p}^{h\rightarrow o}\in\mathbb R_{\ge0}^{M_p\times L_{t,p}}.
\]

要求：

```text
fixed；
non-learned；
signal-independent；
physical-time based；
no extrapolation；
nonzero rows row-stochastic。
```

定义：

\[
A_p
=
G_{t,p}^{h\rightarrow o}\widetilde W_pG_{s,p}^{o\rightarrow h}.
\]

row normalization：

\[
\operatorname{RN}_0(A)_{i,:}
=
\begin{cases}
A_{i,:}/\sum_jA_{ij},&\sum_jA_{ij}>0,\\
0,&\sum_jA_{ij}=0.
\end{cases}
\]

最终：

\[
\boxed{\hat W_p=\operatorname{RN}_0(A_p).}
\]

内部 reliability：

\[
\widetilde R_p\in[0,1]^{L_{t,p}}
\]

通过同一 target-grid projection 得到：

\[
\boxed{
\hat R_{p,i}
=
\mathbf1[\sum_jA_{p,ij}>0]\cdot
[G_{t,p}^{h\rightarrow o}\widetilde R_p]_i.
}
\]

若 raw row mass 被 estimator 用作 confidence，则必须在 RN0 前记录为 reliability evidence，满足 A1。

---

# 6. Temporal Localizer 方法族与唯一 feature-tap 语义

formal route order：

\[
\boxed{L\text{-A}\rightarrow L\text{-B}\rightarrow L\text{-C}.}
\]

| 路线 | 机制 | 定位 |
|---|---|---|
| L-A | SSL encoder + lightweight temporal head | 首选 |
| L-B | segment-aware multi-scale head | 第一 fallback |
| L-C | boundary + segment dual-head with final fusion | 最终 fallback |

所有 route 最终都必须输出统一 dense manipulation field：

\[
P_\theta(u).
\]

## 6.1 L-A

候选 backbone：WavLM、wav2vec 2.0 / XLS-R、HuBERT 或同等级 speech SSL encoder。

候选 temporal head：TCN、lightweight Conformer、shallow Transformer、BiLSTM、Mamba-style temporal head。

## 6.2 L-B

允许联合利用 frame、short-segment 与 mid-segment context，但最终仍输出统一 temporal manipulation field。

## 6.3 L-C

boundary / segment 双分支必须在 detector 内部完成确定性融合，并输出一个统一 manipulation logit stream。不得把任务退化为纯 boundary detection。

## 6.4 Formal M4 的 canonical feature tap

为消除 F6 architecture-sensitive ambiguity，primary feature tap 唯一冻结为：

\[
\boxed{
H_\theta(u)
=
\text{the exact tensor immediately consumed by the unique final manipulation-logit projection}.
}
\]

具体规则：

```text
L-A / L-B：最后一个 temporal / fusion block 输出，且该 tensor 直接输入最终 manipulation-logit projection；
L-C：boundary / segment 分支完成融合后的 post-fusion tensor，且该 tensor 直接输入最终统一 manipulation-logit projection；
pre-branch tensor 禁止作为 formal M4 tap；
若一个架构不存在唯一 post-fusion pre-logit tensor，则该架构对 formal F6 不具资格，除非该 tensor 本来就是 detector 固有组成；
不得为 M4 额外增加 projector、adapter 或只为对照服务的 fusion layer。
```

03 只负责记录该 tensor 的 exact module path / shape hash，不得重新解释 tap 语义。

---

# 7. Operational Correspondence 方法族

formal operational family：

\[
\boxed{
\mathfrak R_W^{op}
=
\{W\text{-A},W\text{-B},W\text{-C},W\text{-D}\}.
}
\]

唯一 route order：

\[
\boxed{W\text{-A}\rightarrow W\text{-B}\rightarrow W\text{-C}\rightarrow W\text{-D}.}
\]

## 7.1 W-A — Semantic-Anchored Acoustic-Refined Monotonic Transport

semantic branch 产生 coarse corridor / prior，acoustic branch 使用 frozen / correspondence-only SSL representation。

允许：soft-DTW + gap / null、monotonic attention + unmatched state、forward-backward partial alignment、unbalanced monotonic OT。

## 7.2 W-B — Transcript-Free SSL Partial Alignment

使用 frozen correspondence SSL representation 与 partial monotonic alignment 构造 \(\hat W\)。

## 7.3 W-C — Phoneme / CTC-Only Partial Correspondence

允许 phoneme posterior、CTC posterior、forced-alignment-style posterior 与 null / skip / insertion / deletion state。

必须满足 A2 的 phoneme/CTC → physical-time 映射合同。

## 7.4 W-D — Learned Label-Agnostic Monotonic Transport

\[
F_\phi(x,x')\rightarrow\widetilde W.
\]

允许 cross-attention、monotonic attention、Sinkhorn / differentiable OT、path decoder、state-space matcher。

formal detector training 期间：

\[
\boxed{F_\phi\text{ 不接受 detector gradient}.}
\]

## 7.5 W-E — Reference / Oracle / Audit Only

W-E 可使用 known transform、timestamps、packet/device timing、sync marker、manual independent landmark 产生 \(W^{ref}\)。

固定：

\[
\boxed{W\text{-E}\notin\mathfrak R_W^{op}.}
\]

W-E 永远不得升级为 operational rescue route。

---

# 8. Reliability 方法族

唯一顺序：

\[
\boxed{R\text{-A}\rightarrow R\text{-B}\rightarrow R\text{-C}\rightarrow R\text{-0}.}
\]

## 8.1 R-A — Analytic Multi-Evidence Reliability

允许 evidence：alignment entropy、bidirectional agreement、semantic/acoustic similarity、path plausibility，以及 A1 要求保留的 raw-row-mass confidence evidence。

## 8.2 R-B — Dual-Estimator Agreement

使用两个 label-agnostic correspondence estimators 的局部一致性构造 reliability。

## 8.3 R-C — Learned Label-Agnostic Uncertainty

\[
U_\psi(x,x',\hat W)\rightarrow\hat R.
\]

监督仅允许来自 synthetic known correspondence error、independent reference error、correspondence-only data。

formal CEL / CS training 前必须冻结。

## 8.4 R-0 — Support-Only Binary Reliability

只有 independent dense evidence 证明全部 nonzero support 满足 full-support fidelity 后，才允许：

\[
\hat R_{p,i}=\mathbf1[\sum_j\hat W_{p,ij}>0].
\]

Sparse-only evidence 不足以资格化 R-0。

---

# 9. Discrepancy Definitions

## 9.1 CEL point discrepancy

formal primary：

\[
\boxed{d(a,b)=\operatorname{SmoothL1}(a,b).}
\]

beta统一取03第7.1节的 `numerical.smooth_l1_beta`，M3′、M5及其screen对应项使用同一值。

其它 discrepancy 只允许 secondary ablation。

## 9.2 Correspondence discrepancy

对 normalized rows \(q,r\in\Delta_{N_p}\)，以 source physical time 为 ground cost，定义：

\[
\boxed{d_W^{row}(q,r)=W_1^{(t)}(q,r).}
\]

对同一source/target物理网格上的两个矩阵 \(W,V\)，令

\[
\mathcal J(W,V)=\{i:\sum_jW_{ij}>0,\ \sum_jV_{ij}>0,\ \omega_i>0\},
\qquad \omega_i=\text{target cell }i\text{与真实音频支持相交的时长}.
\]

只在 \(\mathcal J\ne\varnothing\) 上定义矩阵级标量：

\[
\boxed{d_W(W,V)=
\frac{\sum_{i\in\mathcal J}\omega_i
 d_W^{row}(\operatorname{RN}_0(W_{i,:}),\operatorname{RN}_0(V_{i,:}))}
{\sum_{i\in\mathcal J}\omega_i}.}
\]

source时间以毫秒计，因此 \(d_W\)、U-REF achieved error和 \(\delta_W\) 均以毫秒计。不同网格先按固定物理时间合同适配，不能直接比较矩阵下标。\(d_W\) 不使用 \(\hat R\) weighting，避免reliability self-masking；空共同支持为not applicable，不记零。该量不惩罚缺失覆盖，必须另报共同支持和coverage。U-REF与CS仍分别满足各自的same-support约束，不能删去困难行降低距离。

## 9.3 Occupancy discrepancy

对共同有效集合 \(\mathcal J\neq\varnothing\)：

\[
\boxed{
d_Y(a,b;\mathcal J)
=
\frac{\sum_{i\in\mathcal J}\omega_i|a_i-b_i|}
{\sum_{i\in\mathcal J}\omega_i}.
}
\]

\(\omega_i\) 同第9.2节，为实际有效cell时长；最后一个不足整格的真实cell按其实际时长计。空集合时为 not applicable。

---

# 10. Independent Correspondence Validation 接口

任何 operational W/R 在进入 formal CEL 前必须经过 independent reference track。

允许：

```text
known injected timing transform；
independent capture timestamps；
sync marker；
packet / device timing；
independent timing landmarks。
```

禁止：

```text
Y；
fake boundary；
P_theta；
detector confidence；
W_hat 自生成 reference。
```

## 10.1 Dense W fidelity

定义 jointly evaluable support：

\[
\mathcal I_p^{joint}
=
\left\{i:R_{p,i}^{ref}>0,\ \sum_jW_{p,ij}^{ref}>0,\ \sum_j\hat W_{p,ij}>0\right\}.
\]

定义：

\[
\boxed{
E_W^{ref}(p)
=
\frac{\sum_{i\in\mathcal I_p^{joint}}R_{p,i}^{ref}d_W^{row}(\hat W_{p,i,:},W_{p,i,:}^{ref})}
{\sum_{i\in\mathcal I_p^{joint}}R_{p,i}^{ref}}.
}
\]

coverage：

\[
\boxed{
\mathrm{Cov}_W(p)
=
\frac{|\mathcal I_p^{joint}|}{|\mathcal I_p^{ref}|}.
}
\]

禁止使用 \(\hat R\) mask correctness error。

## 10.2 Sparse W fidelity

对 independent landmarks \((t_{s,k}^{ref},t_{t,k}^{ref})\)，若对应 operational row 非零，则：

\[
\hat t_{s,k}=\sum_j\hat W_{p,i(k),j}t_{s,j},
\]

\[
\boxed{e_{p,k}^{sparse}=|\hat t_{s,k}-t_{s,k}^{ref}|.}
\]

zero row 记为 unrecovered，不得记为 error 0。

## 10.3 Reliability calibration

共同目标：

\[
\boxed{\hat R\uparrow\Rightarrow\text{independent correspondence error}\downarrow.}
\]

## 10.4 Authenticity-conditioned fidelity

结构隔离只能证明 estimator 未使用 authenticity supervision，不能证明其误差在所有 authenticity strata 上均稳定。因此 formal validation 必须额外分层报告：

```text
bona fide；
fully fake；
partial fake interior；
partial-fake boundary-crossing。
```

该分层遵循以下原则：

1. 分层标签只在 W/R 完全冻结后用于 evaluation；
2. 每个主张 scope 内的必要 strata 都必须满足 absolute W-fidelity floor，具体阈值由 03 冻结；
3. strata 之间误差差异本身只作为 diagnostic，不自动等价于“correspondence 读取了 authenticity”；
4. 若差异显著，必须额外报告 matched acoustic-difficulty analysis；
5. 未通过某一必要 stratum 的 absolute fidelity 时，只能缩小 F3 scope，不得把其它 strata 的结果拼接为全局 F3。

由此，“authenticity-label-agnostic”继续作为结构性信息边界；“authenticity-conditioned fidelity”作为部署稳定性证据，两者不混为同一命题。

---

# 11. Formal CEL Topology 与机制对照族

formal primary topology 唯一为：

\[
\boxed{G\text{-A}=\text{Stop-Gradient Source Teacher}.}
\]

G-B joint-gradient 与 G-C EMA teacher 仅作为 secondary diagnostic，不得 rescue formal result。

## 11.1 M5 — CEL

\[
\boxed{
\mathcal L_{CEL}^{sg}(p)
=
\frac{
\sum_{i\in\mathcal I_p^+}\hat R_{p,i}
 d(P_\theta(x')_i,[\hat W_p\operatorname{sg}(P_\theta(x))]_i)
}
{\sum_{i\in\mathcal I_p^+}\hat R_{p,i}}.
}
\]

\[
\boxed{
\mathcal L_{M5}
=
\mathcal L_{loc}
+
\lambda_{CEL}\mathcal L_{CEL}^{sg}.
}
\]

## 11.2 M2 — Strict Identity / No-Transport Control

构造 strict physical-time identity \(W_{id,p}\)。只允许相同 physical timestamp interpolation，禁止 offset、scale、drift、warp 与 duration-normalized correction。

定义：

\[
\mathcal I_p^{id}
=
\{i:\hat R_{p,i}>0,\ \sum_jW_{id,p,ij}>0\}.
\]

\[
\boxed{
\mathcal L_{IdCEL}(p)
=
\frac{
\sum_{i\in\mathcal I_p^{id}}\hat R_{p,i}
 d(P_\theta(x')_i,[W_{id,p}\operatorname{sg}(P_\theta(x))]_i)
}
{\sum_{i\in\mathcal I_p^{id}}\hat R_{p,i}}.
}
\]

\[
\boxed{
\mathcal L_{M2}=\mathcal L_{loc}+\lambda_{id}\mathcal L_{IdCEL}.
}
\]

F4 的 formal primary comparison 仍为：

\[
\boxed{M5>M2.}
\]

但必须同时执行第12节 coverage / common-support 分解。

## 11.3 M3′ — Matched Aligned-Supervision Control（F5 formal comparator）

这是 F5 唯一 formal comparator。

定义 transported occupancy：

\[
\widetilde Y_p^t=\hat W_pY_x.
\]

M3′ 与 M5 使用完全相同的：

```text
point discrepancy d = SmoothL1；
reliability R_hat；
valid set I_p^+；
source base supervision；
paired data；
optimizer / step budget；
source / target model architecture。
```

唯一核心差异为 transported object：

```text
M5：W_hat sg(P_theta(x))；
M3′：W_hat Y_x。
```

定义：

\[
\boxed{
\mathcal L_{AlignedSup}^{match}(p)
=
\frac{
\sum_{i\in\mathcal I_p^+}\hat R_{p,i}
 d(P_\theta(x')_i,[\hat W_pY_x]_i)
}
{\sum_{i\in\mathcal I_p^+}\hat R_{p,i}}.
}
\]

\[
\boxed{
\mathcal L_{M3'}
=
\mathcal L_{loc}
+
\lambda_{AS'}\mathcal L_{AlignedSup}^{match}.
}
\]

F5 唯一 formal claim：

\[
\boxed{M5>M3'.}
\]

因此 F5 只检验：

> 运输模型自身 source 软预测是否超出运输 source occupancy label 的价值。

## 11.4 M3 — Native Aligned-Supervision Control（secondary）

保留原生监督式 aligned-supervision 作为 secondary strong baseline：

\[
\mathcal L_{AlignedSup}^{native}(p)
=
\mathcal L_{sup}
(P_\theta(x'),\hat W_pY_x;\omega_p\hat R_p,\mathcal I_p^+).
\]

\[
\mathcal L_{M3}
=
\mathcal L_{loc}
+
\lambda_{AS}\mathcal L_{AlignedSup}^{native}.
\]

M3 可用于回答“工程上直接 transported-label supervision 是否更强”，但：

\[
\boxed{M5>M3\text{ 不产生 F5 formal verdict}.}
\]

## 11.5 M4 — Same-W Feature Control

primary feature 仅允许使用第6.4节 canonical tap：

\[
H_\theta(u)\in\mathbb R^{L_u^h\times D_h}.
\]

feature loss在M5使用的manipulation-output grid上评价。定义固定时间插值矩阵
\(\Pi_s\in\mathbb R^{N_p\times L_x^h}\)、\(\Pi_t\in\mathbb R^{M_p\times L_{x'}^h}\)：每个output cell中心在相邻native feature中心间作线性插值；恰好重合时为one-hot；超出feature中心凸包或涉及padding时该行无效，禁止extrapolation。两网格相同时取identity。这是固定时间适配，不是可学习的通道projector。

唯一执行顺序为：**时间插值 → 使用同一最终W传输未归一化source feature → 两侧分别L2归一化 → 计算差异**：

\[
\widetilde H_s=\Pi_s\operatorname{sg}(H_\theta(x)),\qquad
\widetilde H_t=\Pi_tH_\theta(x'),\qquad
\bar H_s=\hat W_p\widetilde H_s.
\]

不得另估feature-specific W，也不得改成“先归一化source各行再传输”。W、R和时间插值矩阵均不接收detector梯度。

row-wise L2 normalization：

\[
\nu(h)=\frac{h}{\|h\|_2+\varepsilon_h}.
\]

feature discrepancy：

\[
\boxed{d_h(a,b)=1-a^\top b.}
\]

令 \(\mathcal I_p^h\subseteq\mathcal I_p^+\) 为target插值有效、该W行所有正权重source列的插值均有效，且 \(\|\bar H_{s,i}\|_2>\varepsilon_h\)、\(\|\widetilde H_{t,i}\|_2>\varepsilon_h\) 的行。任何缺失项均不得以零feature补入；记录剔除原因与相对 \(\mathcal I_p^+\) 的覆盖率。

\[
\boxed{\mathcal L_{SameWFeat}(p)=
\frac{\sum_{i\in\mathcal I_p^h}\hat R_{p,i}
 d_h\!\left(\nu(\widetilde H_{t,i}),\nu(\bar H_{s,i})\right)}
{\sum_{i\in\mathcal I_p^h}\hat R_{p,i}}.}
\]

空 \(\mathcal I_p^h\) 为not applicable，不能记零。有效pair的feature项先逐pair计算，再对batch中适用pair等权平均；base supervision仍对全部监督有效source样本计算。该归约与M5一致；不得按各模型的结果改变paired data或采样顺序。

\[
\boxed{
\mathcal L_{M4}
=
\mathcal L_{loc}
+
\lambda_{feat}\mathcal L_{SameWFeat}.
}
\]

禁止：

```text
extra projector；
formal multi-layer ensemble；
feature-specific W；
pre-branch tap；
formal result 后更换 feature tap。
```

F6：

\[
\boxed{M5>M4.}
\]

---

# 12. F4 的覆盖效应与共同支持效应分解

F4 的原语问题是 sample-conditioned transport 是否优于 strict identity。由于 \(W_{id}\) 与 \(\hat W\) 可能具有不同 valid support，F4 必须显式分解。

定义：

\[
\boxed{
\mathcal I_p^{4,common}
=
\mathcal I_p^+\cap\mathcal I_p^{id}.
}
\]

定义 operational-only support：

\[
\boxed{
\mathcal I_p^{4,W-only}
=
\mathcal I_p^+\setminus\mathcal I_p^{id}.
}
\]

定义 identity-only support：

\[
\mathcal I_p^{4,id-only}
=
\mathcal I_p^{id}\setminus\mathcal I_p^+.
\]

formal F4 仍以完整 task-evaluable set 上的 M5 vs M2 为 primary effect，但 03 必须同步报告：

1. **Coverage decomposition**：\(|\mathcal I_p^+|\)、\(|\mathcal I_p^{id}|\)、\(|\mathcal I_p^{4,W-only}|\)；
2. **Common-support performance**：只在 \(\mathcal I_p^{4,common}\) 上比较 M5 与 M2；
3. **W-only region performance**：在 \(\mathcal I_p^{4,W-only}\) 可评价时单独报告 M5 与 M2 的 localization behavior。

解释纪律：

```text
若 F4 总效应为正且 common-support 也为正，报告“收益在共同有效区域仍可观察到”；
若收益主要集中在 W-only support，报告“收益主要出现在额外覆盖区域”；
不得仅凭上述区域分解断言 correspondence accuracy 的因果贡献，或排除训练coverage的间接影响。
```

F4仍检验01的transport相对identity是否有增益。两模型训练时的支持可能不同，共同区域上的评价不能消除这种训练差异；本节提供描述性分解，不单独证明中介或因果归因。若要作更强归因，须另行事前规定训练支持匹配的研究，不能由当前F4自动推出。

---

# 13. Correspondence Uncertainty：两层证据合同

本文区分两类不确定性研究，二者不得互相替代。

## 13.1 U-REF — Oracle-centered admissible perturbation

定义：

\[
\mathcal P_\varepsilon:\mathfrak W_p\rightarrow\mathfrak W_p,
\]

\[
W_{p,\varepsilon}=\mathcal P_\varepsilon(W_p^{ref}),
\]

并要求：

\[
d_W(W_{p,\varepsilon},W_p^{ref})\approx\varepsilon.
\]

必须保持 shape、support、row-normalization、预注册 monotonicity / locality / slope class。

U-REF 只用于：

```text
Stage P resource screen；
机制局部敏感性解释。
```

不得声称其等价于 operational \(\hat W\) 的真实错误分布。

## 13.2 U-OP — Operational-error-aligned analysis

只有 F3 后才定义。其误差来源必须来自：

```text
corr-test 上实测 W_hat vs independent reference 的 row / pair error；
或基于该实测误差分布预注册生成的 perturbation replay。
```

允许：

1. 按 independent operational error quantile 对 F5 effect 分层；
2. 从实测 error profile 采样 admissible perturbation 施加到 locked W；
3. 对比 U-REF 与 U-OP 的趋势一致性。

U-OP 固定为 secondary analysis，除非在 formal test 解封前由 03 预注册为独立 secondary family；它永远不得事后升级为 F5 主 verdict。

---

# 14. Pre-Formal Oracle Screen Objects

Stage P 只用于 resource decision，不产生 F4/F5/F6 formal verdict。

Oracle Screen objects：

\[
\boxed{O2,O3',O4,O5.}
\]

其中：

```text
O2 对应 M2；
O3′ 对应 formal M3′；
O4 对应 M4；
O5 对应 M5；
均将 operational W/R 替换为 W_ref/R_ref 或 W_e/R_ref。
```

原生监督式 M3 的 oracle 版本可作为 secondary screen，但不得影响 screen gate。

固定：

\[
\boxed{\text{Stage P Screen}\not\Rightarrow F4/F5/F6.}
\]

Stage P 不得用于选择 formal W/R route、改变 feature tap、改变 M3′ 定义、改变 formal threshold。

---

# 15. CS-CEL Negative Contract 与方法族

negative：

\[
W_p^-\in\mathfrak W_p.
\]

必须满足：

```text
same shape；
same valid target support as W_hat；
same row-normalization semantics；
same reliability source；
same admissibility class；
label-blind；
detector-output-blind；
no detector gradient。
```

并要求：

\[
\boxed{d_W(W_p^-,\hat W_p)\ge\delta_W.}
\]

negative set：

\[
\boxed{
\mathcal N_p(\delta_W)
=
\{W_p^-\in\mathfrak W_p:d_W(W_p^-,\hat W_p)\ge\delta_W\}.
}
\]

若为空，该 pair 可参与 CEL，但不可参与 CS。

上述 \(\mathcal N_p\) 是抽象admissible集合。实际训练和评价使用预注册、有限、去重后的bank

\[
\boxed{\mathcal B_p=\{W_{p,1}^-,\ldots,W_{p,K_p}^-\}\subseteq\mathcal N_p(\delta_W).}
\]

generator family、参数、候选数上限、确定性seed规则、去重与合法性检查均在读取该partition的Y前冻结。train/dev保存实际bank hash；test只在相应数据解封后按锁定生成器实例化，先保存bank hash再读取test Y。不得按标签或detector loss补采、删选bank；训练可在冻结bank内按第17节取hardest negative，但不更新bank。

第16–17节的可实现最小值均取自 \(\mathcal B_p\)。空bank使CS项不适用，CEL仍可适用。F7结论限定于登记的有限候选族和scope：一般有 \(\min_{\mathcal B_p}\ge\inf_{\mathcal N_p}\)，bank上通过informative gate不能推出对所有admissible alternatives均可辨识。01的抽象原语保留，该bank是本次方法实例的操作性范围。

negative route order：

\[
\boxed{N\text{-A}\rightarrow N\text{-B}\rightarrow N\text{-C}.}
\]

N-A 为 structured path perturbation；N-B 为 distribution-matched negatives；N-C 为 learned label-blind generator。

formal F7 后不得重新选择 negative family。

---

# 16. Correspondence-Informative Operational Gate

只有 \(\mathcal I_p^+\neq\varnothing\) 且 \(\mathcal B_p\neq\varnothing\) 时定义。

执行顺序必须为：

```text
1. W/R 完全冻结；
2. negative bank 完全冻结；
3. F3 已在对应 scope 支持；
4. 之后才允许读取 Y_x；
5. 计算 informative gate。
```

定义：

\[
\widehat{\operatorname{Sep}}_p
=
\min_{W_p^-\in\mathcal B_p}
 d_Y(\hat W_pY_x,W_p^-Y_x;\mathcal I_p^+).
\]

定义：

\[
\boxed{
g_p^{CS}
=
\mathbf1[\widehat{\operatorname{Sep}}_p\ge\delta_Y^{op}].
}
\]

若前置集合为空，则 \(g_p^{CS}=0\)。

该 gate 是 **label-conditioned applicability gate**，不是 label-free gate。它不得反向更新 W/R/negative bank。

---

# 17. CS-CEL Objective

formal source：

\[
P_{src}(x)=\operatorname{sg}(P_\theta(x)).
\]

对 negative：

\[
D_\theta(p;W_p^-)
=
\frac{
\sum_{i\in\mathcal I_p^+}\hat R_{p,i}
 d(P_\theta(x')_i,[W_p^-P_{src}(x)]_i)
}
{\sum_{i\in\mathcal I_p^+}\hat R_{p,i}}.
\]

positive：

\[
D_\theta^+(p)=D_\theta(p;\hat W_p).
\]

hardest negative：

\[
D_\theta^-(p)
=
\min_{W_p^-\in\mathcal B_p}D_\theta(p;W_p^-).
\]

selectivity loss：

\[
\boxed{
\mathcal L_{sel}(p)
=[m+D_\theta^+(p)-D_\theta^-(p)]_+.
}
\]

formal CS-CEL：

\[
\boxed{
\mathcal L_{CS-CEL}
=
\mathcal L_{loc}
+
\lambda_{CEL}\mathcal L_{CEL}^{sg}
+
\lambda_{sel}g_p^{CS}\mathcal L_{sel}.
}
\]

formal source topology 仍唯一为 G-A。

F7比较的CEL控制与CS-CEL必须从同一seed的同一M5 checkpoint出发，使用相同追加训练数据、采样次序、optimizer、共享超参数及optimizer更新步数。CEL控制只优化 \(\mathcal L_{loc}+\lambda_{CEL}\mathcal L_{CEL}^{sg}\)，CS分支增加上述selectivity项；CS参数的dev搜索范围与预算由03事前固定。所谓“冻结M5”指冻结起点身份、方法配置及W/R，不是用未继续训练的旧checkpoint对比额外训练后的CS模型。

---

# 18. Route Order、Exhaustion 与冻结语义

本节及第21、23节的路线封闭和冻结要求作用于对应method/protocol/evidence版本。当前版本失败按03判决；保持01原语的后续新路线按03第39节主动检索、查重、建立独立版本并验证，不能作为旧版formal rescue，也不受旧版候选名称数量的永久限制。

## 18.1 Localizer

\[
\boxed{L\text{-A}\rightarrow L\text{-B}\rightarrow L\text{-C}.}
\]

first-qualified wins。

## 18.2 Correspondence

\[
\boxed{W\text{-A}\rightarrow W\text{-B}\rightarrow W\text{-C}\rightarrow W\text{-D}.}
\]

每个 W 内：

\[
\boxed{R\text{-A}\rightarrow R\text{-B}\rightarrow R\text{-C}\rightarrow R\text{-0}.}
\]

first-qualified W/R wins。

W-E 不参与 fallback。

## 18.3 CEL topology

formal：

\[
\boxed{G\text{-A only}.}
\]

G-B / G-C 不能 rescue。

## 18.4 CS

\[
\boxed{N\text{-A}\rightarrow N\text{-B}\rightarrow N\text{-C}.}
\]

N-route 全部无法构造合法 negative bank 时，只能形成 F7 insufficient-negative evidence，不得新增 N-D。

---

# 19. Object Status Registry

## 19.1 FORMAL-PRIMARY

```text
M2；
M3′；
M4；
M5；
formal CS-CEL。
```

## 19.2 CONTEXTUAL-BASELINE

```text
M0；
M1。
```

## 19.3 SECONDARY-DIAGNOSTIC

```text
M3 native aligned-supervision；
G-B；
G-C；
alternative d ablations；
F4 coverage/common-support decomposition；
U-OP uncertainty analysis；
strong target-supervision study。
```

## 19.4 ORACLE / AUDIT / SCREEN

```text
M6；
O2；
O3′；
O4；
O5；
W-E；
W_ref；
U-REF Stage P perturbation。
```

---

# 20. Claim Interpretation

| 条件 | 唯一允许解释 |
|---|---|
| F1–F3 supported | operational premise 可进入 mechanism validation |
| F4 supported | sample-conditioned transport necessity 有证据；必须附 coverage/common-support 分解 |
| F5 supported | paired prediction transport 超出 matched transported-label supervision |
| F6 supported | output-space action 超出 same-W feature action |
| F4–F6 同 scope 全 supported | CEL = Validated Mechanism Contribution at that scope |
| F7 supported | CS-CEL = Validated Strong Extension within registered finite negative family and scope |
| F5 practical-null | 不再主张 prediction transport 的独立必要性 |
| F6 practical-null | 不再主张 output-space action 的独立必要性 |
| F4 practical-null | 不再主张 sample-conditioned transport necessity |
| F7 practical-null / inconclusive | 删除 strong CS claim，保留 CEL supported scope |

F5 的正式结论只允许来自：

\[
\boxed{M5>M3'.}
\]

M5>M3 只能作为 secondary engineering comparison。

Strong Real CEL 必须满足：

\[
\boxed{
\mathrm{Scope}(F1)=\cdots=\mathrm{Scope}(F6)=\mathrm{REAL\ target\ scope}.
}
\]

---

# 21. 明确禁止

禁止：

```text
只做 augmentation 冒充 CEL；
只做 feature alignment 冒充 CEL；
W/R 读取 authenticity labels / Y / detector outputs；
W_ref 代替 formal operational W；
detector loss 更新 W/R；
formal 失败后新增 W/R/G/N route；
formal 失败后更换 M4 canonical tap；
formal 失败后把 M3 native 替代 M3′ 作为 F5 comparator；
Stage P 结果替代 F4/F5/F6；
Stage P 结果用于选择有利 formal method definition；
用 CTRL 的 F4–F6 与 REAL 的 F1–F3 拼接 Strong Real CEL；
把 authenticity-stratified error difference 自动解释为 label leakage；
把 oracle-centered U-REF 当作 operational error distribution；
仅凭F4区域分解宣称排除了训练coverage影响或证明了common-support correspondence accuracy的因果贡献。
```

---

# 22. 与 03 的唯一接口

03 必须从本文直接引用，而不得重新定义：

```text
M2 / M3′ / M3 / M4 / M5 / M6；
O2 / O3′ / O4 / O5；
canonical M4 tap 语义；
F4 decomposition sets；
U-REF / U-OP 身份；
W/R/N route order；
CS informative gate；
object status。
```

03 只负责：

```text
exact module path；
threshold；
minimum；
power；
partition；
lock；
state transition；
execution artifact；
合法项目终点。
```

任何实现若引入新的 loss、route、state 或 verdict，而在 01/02/03 中无唯一 owner，则：

\[
\boxed{\text{INVALID IMPLEMENTATION}.}
\]

---

# 23. 最终冻结声明

本文已从整体结构上闭合：

```text
基础 supervision；
M0–M6；
formal M3′ single-variable control；
M4 canonical pre-logit tap；
F4 coverage/common-support decomposition；
Localizer / W / R / N route；
Grid Adapter；
RN0 confidence assumption；
W-C physical-time assumption；
Independent W/R validation；
authenticity-conditioned fidelity；
U-REF / U-OP uncertainty semantics；
CS informative gate 的 F3 dependency；
CS objective；
object status；
claim interpretation。
```

因此本文件自此冻结为：

\[
\boxed{
\textbf{
02 METHOD CONTRACT:
REBUILT-FINAL
/
01-ALIGNED
/
CONTROL-CLOSED
/
METHOD-SPACE-CLOSED
}
}
\]

冻结后，普通实验失败、某 route 表现差、某工程细节需要调整，均不得反向修改本文；只能按照 03 的 frozen state machine 输出 verdict、claim downgrade，或启动与当前 evidence 隔离的新研究版本。
