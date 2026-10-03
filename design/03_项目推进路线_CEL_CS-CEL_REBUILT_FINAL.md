# 03_项目推进路线：CEL / CS-CEL 重构冻结执行协议

> 上游算法原语：`01_算法原语设计_CEL_CS-CEL.md`  
> 上游方法合同：`02_方法实现机制设计_CEL_CS-CEL_REBUILT_FINAL.md`  
> 文档职责：把冻结算法原语与重构后的方法合同转换为一套完整、可终止、抗 route-shopping、具有预注册 power 的执行协议。  
> 文档层级：**Project Execution Manual / Pre-registration Protocol / Evidence SOP**  
> 状态：**REBUILT-FINAL / 01-02-ALIGNED / STATE-CLOSED / POWER-LOCKED / EXECUTION-READY**

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
Stage 4P  Mechanism Power / Precision Lock
    ↓
Stage 4D  M2 / M3′ / M4 / M5 Development
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
    feature_to_output_grid: fixed_physical_time_linear_interpolation
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

P2/P3 的 formal screen comparator 为 O2/O3′/O4/O5。

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

primary CI / p-value 对 \(\bar\Delta_u\) 进行 source-utterance cluster bootstrap；REAL:MULTI 时额外按 family / platform stratified。

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

任何补样必须来自 Stage 0B 已预注册的 sealed reserve；只能因 minimum / CI-width precision 不足解封，不得根据 effect 方向决定是否补样。

## 7.15 Statistical constants

```yaml
statistics:
  ci_level: 0.95
  alpha: 0.05
  multiple_comparison: holm
  power_target: 0.80
  planning_alpha_rule: alpha_divided_by_3
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
```

## 7.17 CS selectivity scaling

```yaml
cs_selectivity:
  margin_m_rule: 0.10 * IQR(D_minus_CEL - D_plus_CEL)
  epsilon_sel_gain_rule: 0.10 * IQR(D_minus_CEL - D_plus_CEL)
  fallback_rule: 0.01 * median_nonzero_D_scale
```

两者只在 `D_cs-dev` 计算并在 Stage 6L 冻结。

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

若 precision 不足，只允许按第7.14节解封预注册 reserve；达到最大轮次仍不足则：

```text
PRECISION_INFEASIBLE
或
POWER_INFEASIBLE
```

并进入合法终点。

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

仅对未 SUPPORTED 的 \(F_k\) 执行：

\[
H_{0k}^{null}:\Delta_k\ge\epsilon_{main}.
\]

PRACTICAL_NULL：

```text
one-sided 95% upper CI < epsilon_main
AND
Holm-corrected equivalence p < alpha。
```

其它为 INCONCLUSIVE。

## 8.6 Stage 4 power planning

Stage 4P 在 `D_mech-dev` 上估计每个 source utterance 的 seed-averaged paired difference 标准差：

\[
\hat\sigma_k,\qquad k\in\{4,5,6\}.
\]

使用保守 planning level：

\[
\alpha_{plan}=\alpha/3,
\qquad
\beta=1-\texttt{power_target}.
\]

对目标 effect \(\epsilon_{main}\)，近似 required sample：

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

只对 mixed-partial utterance：

\[
0<\sum_kY_{u,k}<L_u
\]

计算 temporal AUPRC，再 macro average：

\[
\boxed{
AUPRC_{partial}
=
\frac{1}{|\mathcal U_{partial}|}
\sum_{u\in\mathcal U_{partial}}AUPRC_u.
}
\]

no-skill baseline：

\[
\boxed{
AUPRC_{noskill}
=
\frac{1}{|\mathcal U_{partial}|}
\sum_u\frac{1}{L_u}\sum_kY_{u,k}.
}
\]

Secondary localization metrics：Segment F1、Segment mIoU、Boundary MAE / P90、bona-fide temporal FPR、fully-manipulated coverage。

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

如果 primary F4 supported，但 `Delta4_common <= 0` 且增益主要来自 W-only support，则论文解释必须使用：

```text
coverage-mediated transport necessity
```

不得使用：

```text
common-support correspondence accuracy superiority。
```

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

若 O5 在全部 seeds 上相对 O3′ 或 O4 明确负向超过 \(\epsilon_{screen}\)，则 SCREEN_NONPROMISING；否则进入 P3。

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

Delta5_screen 随 achieved error 呈正向 Spearman trend，
且最高 achieved-error level Delta5_screen >= 0。
```

同时至少一个 nonzero level：

\[
\Delta_6^{screen}\ge-\epsilon_{screen}.
\]

SCREEN_NONPROMISING：全部 nonzero levels 均明确负向超过 \(\epsilon_{screen}\)。

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

从 occupancy field 提取 manipulation boundaries；按同 polarity、最大基数、保持时间顺序、最小总绝对时间差完成一一匹配。

定义 boundary displacement：

\[
BTD_p^{task}
=
\operatorname{median}\frac{|b_r-b_i|}{output\_grid\_ms}.
\]

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

pair task-active 当且仅当：

\[
BTD_p^{task}\ge\tau_B
\quad\lor\quad
U_{B,p}^{task}>0
\quad\lor\quad
U_p^{task}\ge\tau_U.
\]

family-level `q_active` 为 task-active pair fraction。

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

Sparse track 使用 independent landmarks 建立禁止 extrapolation 的 monotonic piecewise-linear map，使用同构的 boundary displacement 与 q_active 判据。

## 15.2 F2 — Manipulation Occupancy Is Transportable

禁止定义：

\[
Y_{x'}:=W^{ref}Y_x.
\]

target GT 必须来自 independent target provenance。

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
formal seeds。
```

然后才解封 `D_loc-test`。

## 16.3 Stage 2T

定义：

\[
G_{loc}=AUPRC_{partial}-AUPRC_{noskill}.
\]

LOCALIZER_SUPPORTED 需同时满足 formal thresholds。

LOCALIZER_UNUSABLE 为明确达到 refutation thresholds。

其它为 LOCALIZER_INCONCLUSIVE。

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

若仅 precision 不足，允许解封预注册 reserve；达到 cap 仍不足则 route INCONCLUSIVE。

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

R-0 仅在 dense evidence 下按 Q95 error eligibility 判定；sparse-only 永远 INELIGIBLE。

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
先按 precision-only reserve escalation；
达到 cap 仍 INCONCLUSIVE → F3=INCONCLUSIVE；
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

才允许进入 Stage 4。

因此：

```text
Stage 2 成功但 Stage 3 失败 → 不进入 Stage 4；
Stage 3 成功但 Localizer unusable → 不进入 Stage 4；
二者都成功 → 进入 Stage 4P。
```

---

# 19. Stage 4P — Mechanism Power / Precision Lock

这是正式 Stage 4 的必要前置，不是可选 sanity check。

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

# 20. Stage 4D — M2 / M3′ / M4 / M5 Development

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
coverage-mediated / accuracy-mediated attribution label。
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

且全部属于同一 REAL target scope。

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

Stage 5 必须在 formal test 解封前检查 expected CI width。若 initial 2000 不足，只能按第7.14节 precision-only 解封预注册 reserve，最多到 `real_formal_cap`。

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

后进入。

negative route：

\[
N\text{-A}\rightarrow N\text{-B}\rightarrow N\text{-C}.
\]

执行顺序：

```text
1. 固定 W/R；
2. 按 N route 构造合法 negative bank；
3. 通过 02 negative contract；
4. 冻结 bank hash；
5. 之后才读取 Y_x；
6. 计算 informative gate；
7. 训练 CS。
```

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
delta_W；
delta_Y_op；
lambda_sel；
epsilon_cs；
formal seeds；
guardrails；
informative-pair rule；
exact informative-pair count plan。
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
CEL = frozen M5；
CS-CEL = same frozen M5 + selectivity。
```

## 27.1 Discrimination

定义：

\[
S(M)
=
\operatorname{median}_p[D_M^-(p)-D_M^+(p)].
\]

\[
\Gamma_{sel}=S(CS)-S(CEL).
\]

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
bona-fide guardrail PASS；
fully-manipulated guardrail PASS。
```

才：

\[
\boxed{F7=SUPPORTED.}
\]

任一 component PRACTICAL_NULL 或 guardrail FAIL：

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
4P / 4D / 4L / 4T 分离；
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

Stage P的 `effective_batch_size: 32` 保持不变。显存不足时可采用micro-batch与梯度累积，在单卡下使每次optimizer更新对应32个有效训练样本；1500 / 1000训练步仍按optimizer更新计。累积时保持既定loss归约，尤其不得把跨样本Dice改成不同的逐micro-batch目标。优先在optimizer更新边界保存checkpoint。

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

本地验收时尚未建立Git仓库，环境检查记录脚本内容hash；后续正式实验仍按原协议冻结可核验的代码版本。本节不要求为环境安装提前建立未来阶段的锁。

---

# 33. Run Manifest

```json
{
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
| 4P | statistical feasibility | power lock | POWER_INFEASIBLE |
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
| CS selectivity adds value | F7 |
| authenticity-label-agnostic estimator | structural audit |
| cross-authenticity fidelity stability | stratified Stage 3 evidence，不等价于 structural audit |

---

# 37. 合法项目终点

本节覆盖所有可能的 terminal states，不允许出现“无法继续但没有 Outcome”。

## Outcome A — Strong Real CS-CEL

同一 real scope：

```text
F1–F6 SUPPORTED；
Stage 5 SUPPORTED；
F7 SUPPORTED；
guardrails PASS。
```

允许主张：

\[
\boxed{\text{Strong Real CS-CEL}.}
\]

## Outcome B — Strong Real CEL

同一 real scope：

```text
F1–F6 SUPPORTED；
Stage 5 SUPPORTED；
F7 PRACTICAL_NULL / INCONCLUSIVE；
或 NEGATIVE_BANK_UNAVAILABLE。
```

允许主张 Strong Real CEL，不再主张 CS extension。

## Outcome C — Controlled CS-CEL

CTRL scope：

```text
F1–F6 SUPPORTED；
F7 SUPPORTED；
real scope 不足、未支持或仅 exploratory。
```

允许主张 Controlled CS-CEL，不得升级为 Strong Real CS-CEL。

## Outcome D — Controlled Mechanism CEL

CTRL scope：

```text
F1–F6 SUPPORTED；
F7 未支持或未运行；
real scope insufficient / inconclusive / exploratory。
```

## Outcome E — Screen Non-Promising

```text
SCREEN_NONPROMISING。
```

停止 full formal CEL engineering。不是 F5 formal refutation。

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

只能修复工程 / protocol violation 后从受污染 stage 之前重新开始；污染 evidence 不得保留为 formal evidence。

---

# 38. Failure Routing Owner

为防止失败后职责不明，所有终点绑定默认 handoff owner。

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

**不得修改本 02/03 来“救结果”。**

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

工程修复不得改变算法语义、threshold、route order 或 comparator。

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
claim-evidence matrix。
```

最终论文表格不得只保留成功 run；所有 formal invalidation、route rejection 与 terminal evidence 都必须可追踪。

---

# 41. 最终闭合检查

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
[✓] 所有合法 terminal states 均可达；
[✓] 不再依赖“失败后再补一个条款”的循环返修模式。
```

---

# 42. 最终冻结声明

项目唯一推进逻辑自此固定为：

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
EXECUTION-READY
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
