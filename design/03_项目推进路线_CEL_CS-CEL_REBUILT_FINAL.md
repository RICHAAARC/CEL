# 03_项目推进路线：CEL / CS-CEL 方法研究与实验指南

> 上游算法原语：`01_算法原语设计_CEL_CS-CEL.md`
> 上游方法合同：`02_方法实现机制设计_CEL_CS-CEL_REBUILT_FINAL.md`
> 文档职责：将01/02的方法定义落实为可实现的起步配置、实验问题、指标、统计解释及失败后的自主研究路径。
> 状态：**方法优先 / 可迭代的研究基线**

> 修订：2026-10-03，v1.4.1。治理、可复现、防篡改、环境与协作信息全部作为记录，不设运行或继续研究的强制准入。当前尚无研究实验结果；真实数据和可用权重只影响依赖它们的运行，小构造例、损失和模块实现可以先行。

---

# 0. 执行总原则

首要任务是推进方法机制：实现实际计算路径、构造能区分解释的对照、运行并分析，再根据失败继续改进。Stage、F1–F7和Outcome用于组织问题与解释结果，不是一套必须逐项过关的工作审批。

1. 先用小构造例开发物理时间网格、occupancy、W/R、有效支持、CEL/CS损失及梯度，再接真实音频、模型和训练。
2. Localizer、operational W/R、对照损失和CS可按输入依赖并行开发，不等待F1–F6全部SUPPORTED。Stage P提供现成小规模实验配置，其结果不直接支持真实场景机制结论。
3. 同次比较保持方法对象、数据、训练投入与评价口径可比；真实的信息/梯度边界仍按02实现。数学错误或对照混淆会影响所声称的机制，缺少治理文件不会。
4. 后文formal、minimum、precision、power和guardrail定义完整评价的参考口径，用来判断证据能支持何种表述，不决定是否允许实现、调试、试验或换路线。样本不足、单seed或探索选择后的结果按其局限解释。
5. seal、lock、hash、manifest、完整环境复现、固定审查角色均不作为任何阶段的项目强要求；已有信息随手记录即可。文中的模型冻结、固定W/R、stop-gradient及同次比较使用固定配置是计算含义，不是行政锁定。
6. 失败后自主诊断、检索原论文和作者实现、提出有区别的候选并做最小判别实验。简记失败原因或未知点，回顾相关尝试，避免没有新问题的重复消耗。无需先建立新research version。
7. 继续使用已看过的test做探索是允许的；如实称为开发/探索数据。只有声称独立确认时才需要未参与选路调参的独立评价；编号、hash或重新切窗不能恢复独立性。

本文里的建议预算按实际资源调整；用户实际给出的时间、费用或资源限制仍按原意执行。

---

# 1. 文档分工

01描述研究问题与核心算法关系；02定义方法数学、控制比较和信息边界；03给出实现实例、数据用途、指标及结果解释；04说明方法优先的协作方式。

本次保留01原语。02/03可以随实现和认识更新；记录有用的代码版本、配置和修改原因，不要求保存文档hash或完成版本手续后才继续。旧结果按当时实际方法与数据解释。

---

# 2. Canonical Status Registry

下列状态是整理结果的常用词，可按实际问题补充原因或描述，不要求先注册状态才能开展研究。

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
  具体W/R realization在独立Corr-Test上明确失败；
  该具体实现的独立验证失败，可分析后换路线继续探索；
  不声称所有可能 W/R route 已被证伪。

OPERATIONAL_SCOPE_REFUTED：
  已评估的W-A/B/C/D候选均有明确失败证据；
  结论仅覆盖所评估的候选及其scope，不代表所有可能operational方法均失败。
```

## 2.4 F4 / F5 / F6 / F7 verdict

```text
SUPPORTED
INCONCLUSIVE
PRACTICAL_NULL
```

F7的合并结论另可为 `GUARDRAIL_FAILED`，表示保护性指标明确失败，不表示primary效应接近零。Discrimination、Localization与各guardrail仍分别保留实际判决；合并规则见第27.3节。

## 2.5 Route / W-R candidate verdict

```text
QUALIFIED
INCONCLUSIVE
REJECTED
REJECTED_EXTERNAL
```

其中 `REJECTED_EXTERNAL` 表示候选在第二组评价数据上的明确失败；数据若已参与选择，则说明该评价的探索性质。

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
REAL:MULTI:<family-list>
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

scope还包括实际reference支持、matched/unmatched状态与评价时间范围。Sparse F3应附“landmark位置”范围；它与同family的全时间轴F4–F7不是相同scope，不能单独拼成整段Strong Real CEL/CS-CEL。Dense结论同样说明reference覆盖及未观察部分，不能将缺失区间当作已证实。现有F3/R-0阈值针对已确认matched支持；若完整真实通信主张还涵盖unmatched区域，需要独立拒配/支持检测证据，不能仅凭matched误差通过形成完整partial-support或Strong Real主张。已确认误接受的位置不纳入可信作用域，未知区域不能默认可信。该区别限制结论范围，不限制后续实现或实验。

---

# 4. 方法推进路径与真实依赖

| 当前工作 | 实际需要 | 能回答的问题 |
|---|---|---|
| P0与各损失原型 | 构造的时间轴、标签、对应及tensor | 方向、网格、支持、归约和梯度是否正确 |
| Localizer路径（P1 / 2D） | 可读音频、区间标签、可加载backbone或明确标注的结构原型 | 定位头能否学习、输入输出是否正确 |
| Operational W/R（3D） | paired音频与估计器；评价误差另需独立reference | 能否恢复对应，reliability是否有信息 |
| 对照比较（P2/P3 / 4D） | 可训练localizer、共同pair、W/R、各项损失和同口径指标 | output transport相对标签/特征传输的观察收益 |
| CS原型与比较（6D） | 合法bank、gate及同起点匹配追加训练 | selectivity是否提供额外信息 |
| 更充分评价（1 / 2T / 3T / 4T / 5T / 6T） | 与目标结论相匹配的数据、对照和样本信息 | 哪些机制或适用范围得到支持，哪些仍不确定 |

## 4.1 并行与投入选择

W/R、localizer和损失原型可同时推进；CS可在已有可用CEL实例后直接比较，不以Stage5完成或F1–F6支持为开发门槛。若localizer完全不学习或W没有有效行，应先定位这些实际问题，不能从无信息比较判断机制优劣。资源受限时先做最能排除当前疑点的小实验。

## 4.2 选路与评价的解释

所有阶段均可根据失败调整路线。保留已观察结果，说明后续选择用了哪些数据。若要作独立确认，将候选选择与未参与选择的评价数据分开；如果目前只有开发数据，继续探索并报告限制，不因缺少独立测试或封存文件阻断实现。

---

# 5. 数据用途与独立评价建议

下列划分服务于完整独立评价，首轮方法探索可只使用小规模train/dev。数据可以重新用于探索，但不能同时冒充未参与训练或选择的独立test；实际source身份比manifest或seal格式重要。

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

# 6. 配置与来源的辅助记录

可在现有脚本、Notebook、配置或笔记中留下实际数据用途、模型来源、参数、seed和产物位置，便于理解差异。已有seal/lock/hash或manifest可保留为参考；不要求创建、验证或补齐它们，也不因缺项判定运行无效。

评价独立性取决于数据是否实际参与训练、调参或选路。发现这种使用时说明其对结论的影响，可继续开发，不能以补写seal恢复独立性。

---

# 7. 起步配置与完整评价参考数值

数值可以集中放在配置中减少重复，也可先使用函数参数或Notebook；实际代码与本次比较采用的口径一致即可，不指定唯一文件路径。

以下数值提供可直接实现的默认实例。网格与损失参数改变时同步核对公式和对照；预算、seed数和样本规划可随实际资源调整。未执行完整配置时报告实际规模，不用下列配置表作运行准入。

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
  feature_cache_recommended: true
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

Stage P的frozen backbone可预提取并缓存feature节省算力，也可在线提取；缓存不是运行条件。

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

建议先用小规模Stage 0A检查reference质量，再决定真实数据采集投入；reference不足时先处理测量问题，已有数据仍可用于有限探索。

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

dense采用02第10.1节逐row分布误差，sparse采用第10.2节相对于点reference的分布误差，不能使用重心误差代替。Reference uncertainty包括时钟/标注及point-to-grid误差，并在同一scope、同一参考可观察对象及第17.2.1节层级权重下求U50/U90；未量化的不确定度不填零。real dense / sparse thresholds由reference uncertainty派生：

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

## 7.14 样本追加与统计解释

完整评价建议先用dev做样本量和精度规划，再对固定候选作一次独立评价。可根据观察继续收集、调参和探索，记录实际选择；不能将反复看效果、补样直到显著的结果解释为原先单次检验的受控错误率。需要确认性推断时使用独立数据或适当的序贯统计设计。

参考规模与caps帮助估算成本，可按资源改变，不要求预封存reserve、登记轮次或先取得扩样批准。遵守用户实际资源限制，避免无信息重复。

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
    implementation_hash_required: false
```

RB-EER 的 threshold sweep 只属于 metric computation，不是 protocol threshold tuning；不得改变 F4/F5/F6/F7/Stage5 verdict。

---

## 7.19 Stage P 启动实例与待落实字段

以下为可直接起步的实例。`null`表示尚未取得的信息。真实P1–P3运行需要可读音频、正确区间标签、可区分的source及train/dev用途、可加载且时间网格兼容的模型权重；没有这些实际输入时先做构造例和模块实现。release、revision、文件hash或环境锁未补齐，不是停工理由；可用的模型来源/config随手记录。环境安装通过不等于真实数据或权重已经可用。

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
6. source/target可分别缓存，按第32.1节避免错用特征。模型来源、revision及配置已知时随运行记录，hash可选；训练集规模和时长分布按实际盘点说明，不虚构已满足参考下限。

### 7.19.1 Stage P 特征与输出时间网格实例

16 kHz输入的第n个样本登记于时间n/16000秒；输出cell为 `[i*0.02, min((i+1)*0.02,T))`，时间中心取该实际区间中点，最后不足整格仍为真实支持。WavLM卷积前端的局部输入支持宽度为400 samples（不表示最终contextual token仅依赖这400个样本）、步长320 samples；第j个native特征的时间中心为 `(320*j+199.5)/16000` 秒，长度为 `floor((N-400)/320)+1`。实际模型的卷积配置若与此实例不同，按真实配置重算网格并检查首尾，不能仅按长度缩放时间；不需要等待文档冻结。

在输入linear projection及TCN之前，冻结的native backbone特征按物理中心线性插值到完整output grid；超出首/尾native中心但仍在真实音频内的cell固定夹持到最近端点特征。该端点延拓只属于localizer输入适配，不构造额外音频、不读取标签，不扩展W的对应支持；Grid Adapter与M4自身的禁止外推合同保持不变。无native特征为无效输入。TCN的3个block各使用一个stride=1、kernel=3、对应dilation的Conv1d，再GELU及dropout；每层两侧padding=dilation保持输出长度，无额外归一化、残差或第二卷积。padding位置在每层后清零；最终逐cell linear→sigmoid。所有模型共用该实例。

因此canonical pre-logit H已位于output grid，Stage P的M4取Pi=identity。监督mask只排除batch padding，真实首尾格均保留。native feature提取逐条真实长度进行，禁止把batch-fill算进真实尾部；较长音频先按第7.19节固定窗口处理，再恢复原时间坐标。

验收例：N=160000时native长度499、output长度500、有效时长10秒；N=160080时native长度500、output长度501，最后格时长5 ms、中心10002.5 ms，全部501格属于真实支持。两例均检查时间原点、首尾夹持及padding隔离。配置依据：[Microsoft WavLM配置](https://huggingface.co/microsoft/wavlm-base-plus/blob/main/config.json)；运行时可记下实际模型来源与配置，hash可选。



### 7.19.2 Operational W-B / R-A起步实例

首轮可从无需转录的W-B开始；这是可计算的开发基线，尚无证据表明它在真实通信中够准。若现成W-A输入可用也可选W-A，不必按菜单逐项等待。

1. 使用与localizer相同来源但冻结、eval/no-grad的WavLM特征。对应估计器只在线性插值**不外推**的output cell中心上取特征，source/target网格外端点不借用localizer的夹持扩展。特征L2归一化；范数不大于epsilon_h的点不可匹配。特征可共享缓存，不能读取训练后的head或Y。真实支持外/不可匹配位置最终为零row。
2. 在有效时间顺序上，设source特征h_j、target特征h'_i，匹配代价 \(c_{ij}=\max(0,\min(2,1-\langle h'_i,h_j\rangle))\)。不可匹配点的c为无穷。以gap代价g=.30做全局单调edit alignment：

\[
 C_{i,j}=\min\{C_{i-1,j-1}+c_{ij},\ C_{i,j-1}+g,\ C_{i-1,j}+g\},
 \quad C_{0,j}=jg,\ C_{i,0}=ig.
\]

   从右下角回溯；完全相同代价优先match、再跳过source、再跳过target。对匹配(i,j)，raw \(A_{ij}=q_i=\exp(-c_{ij}/.20)\)，其它列为0；跳过target则整行0。保留q_i作为raw-mass证据，\(\hat W=\operatorname{RN}_0(A)\)，不会把置信质量在归一化时丢掉。物理网格已是output grid，后续Adapter为identity。算法不读known transform/reference，后者只用于评价；源/目标缺口在这个基线中由skip表达。
3. 交换source/target用相同规则独立计算反向path。若target i匹配source j，且反向j匹配target i'，循环误差 \(b_i=|t_{t,i'}-t_{t,i}|\)；以秒为单位取 \(\hat R_i=q_i\exp(-b_i/.060)\)。反向无对应或正向零row时R_i=0。这是R-A的相似度、raw mass与双向一致性实例，数值为开发初值；其校准是否有用由独立误差检验，不能仅因公式产出[0,1]就称为可靠。
4. 先在identity、prefix-crop、interior-delete的小特征/波形构造上检查方向、skip、零row、时间坐标与raw mass；再在corr-dev测row-error、coverage、reliability及耗时。错配重复内容或软时间漂移可促使改用soft/partial alignment、W-A或其它新实例。无需先训练detector，参数可以依据corr-dev调整；修改后的独立性按实际数据使用解释。

该硬路径只是一种单调运输实例。用于下面N-A比较的共同admissibility class定义为：相同target非零row集合，source时间均在可用source中心范围内，非零row为非负归一分布，按target次序的row source-time重心非降；允许合法source skip。W与negative均逐项满足此类。它不宣称涵盖所有真实通信的多对多关系。

### 7.19.3 N-A起步实例与首批落地步骤

对上述W-B的matched source中心s_i，在可用source中心范围[a,b]内使用端点固定warp：

\[
 f_\alpha(t)=t+\alpha\sin\!\left(\pi\frac{t-a}{b-a}\right),
 \qquad \alpha\in\{-160,-80,-40,40,80,160\}\ \mathrm{ms}.
\]

保留满足 \(|\alpha|\pi/(b-a)\le.25\) 的候选，使导数处于[.75,1.25]且单调；b=a时bank为空。将每个f_alpha(s_i)按相邻有效source中心的物理时间线性插值分配到至多两列，端点取自身，原zero rows保持zero，不wrap、不clip、不删困难row。检查上节共同admissibility、same support与02的d_W，首轮取delta_W=40 ms，只保留实际d_W≥40 ms的候选并去重。source/target输入不含Y或detector输出，候选参数也不因gate是否通过而补抽。该简单bank不适用其它W类时可重新选择相容的generator，说明实例差别。

bank取得后才按02第16节使用Y计算gate，首轮delta_Y_op=.05；阈值是开发初值，可依据研究问题修改，但不按当前pair的Y补选negative。空bank、全部gate=0或teacher退化均有可解释的不同原因：前两者诊断候选范围与数据是否提供可区分标签，第三者按02第17.1节检查预测与梯度；不能合并为CEL被证伪。

实际落地顺序是：先实现grid/occupancy/transport与各loss的构造例，再接上述path/R/bank及统计计算；随后盘点或检索能提供真实音频、区间provenance和source身份的数据，以及可用WavLM权重，优先接通一小批train/dev；最后按共同数据与起点比较M2/M3′/M4/M5和CEL/CS。数据/权重的读取、普通下载与兼容处理属于已授权研究中的实际工作；只有遇到具体受限权限或超范围费用才处理该问题，不把待落实字段变成逐项审批。轻量笔记记录实际输入和失败即可。首轮样本量及训练步数可随信息量和资源调整，不等待完整正式评价配置。

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

F3、Stage4/5/6的完整结论结合样本量、实际CI宽度和规划功效解释。规划不可行可记PRECISION_INFEASIBLE或POWER_INFEASIBLE；实际CI超出参考精度则为INCONCLUSIVE，不把规划通过当作精度已达到。

这些状态说明当前证据不足，可继续开发、诊断和有信息的试验。样本追加按第7.14节说明统计解释，不要求reserve、固定轮次或事先封存。

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

还须满足各major family的预注册最低数量，整数分配在读取test effect前固定。若将来要以“完整SUPPORTED通过概率”为设计目标，需在test解封前另行规定大于 \(\epsilon_{main}\) 的planning alternative，并模拟完整判决；本版本不作该功效保证。在真实效应恰等于 \(\epsilon_{main}\) 且估计近似对称时，点估计过该阈值的概率约为一半，不能由上式声称整体通过率为80%。dev方差只是规划估计，可随结果说明其来源、样本量与不确定性，无需power lock。

若：

\[
n_{lock}>n_{cap},
\]

则：

\[
\boxed{\text{POWER_INFEASIBLE}.}
\]

看过 `D_mech-test` effect后可以继续探索或补数据，但不能沿用原单次检验的独立确认解释；见第7.14节。

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

Stage4第8.6节n_lock还须覆盖三项effect的precision需求；Stage5沿用2000–3000 cap；Stage6 informative沿用100–500 cap。完整评价的三类guardrail各参考至少100个source、每类最多500个source，一类样本不能替另一类凑数。样本不足时报告INCONCLUSIVE/PRECISION_INFEASIBLE及实际区间，可继续探索或调整研究规模；追加与选择后的统计解释遵循第7.14节，无需封存手续。


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

修复后可重跑P0，也可探索其它transform family；说明实际改变及适用范围，不把变化后的结果替代旧构造失败。

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

Stage P之后可以新增有针对性的screen变体；报告新增原因与全部相关结果，不将探索性发现自动升级为正式机制结论。

---

# 13. Stage 0A — Real Reference Feasibility + Early Collection Checkpoint

可与方法开发并行检查真实reference，不以SCREEN_PROMISING作为进入条件。

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
优先改善reference，再按信息增益决定是否扩大采集。
```

---

# 14. Stage 0B — 汇总当前实验选择（辅助记录）

有需要时把目前使用的数据用途、scope、指标、配置、对照及统计口径汇总在现有笔记或配置中，便于后续阅读。可以边实现边补充或修订，不要求统一schema、协议快照、seal、lock或hash。

0B不是后续阶段的前置步骤；缺少此整理不影响运行和继续研究。

---

# 15. Stage 1 — Formal F1 / F2 Premise Audit

所有 verdict 先执行 minimum-first rule。

## 15.1 F1 — Task-Relevant Communication Transport Exists

Dense track：

本项区分真实通信变化与reference未观察到的部分。先确定所评价的source/target物理时间范围与family目标pair集合；范围内的未知部分保留为未知，不能由reference缺失推断删除，也不能当作已经证实没有变化。以下定义同时适用于完整范围和明确声明的可观察子范围；子范围结论不外推至整个音频或family。

定义 reference transported occupancy：

\[
Y_p^{ref}=W_p^{ref}Y_x,
\]

strict identity occupancy：

\[
Y_p^{id}=W_{id,p}Y_x.
\]

本项单独定义 \(\mathcal J_{p,F1}^{ref}\) 与 \(\mathcal J_{p,F1}^{id}\)：它们分别由真实target物理网格中的cells构成，要求对应的独立 \(W_p^{ref}\) 或strict \(W_{id,p}\) 行非零且归一化有效、其取值依赖的source provenance已知；reference侧还须有该处独立可靠的时间对应证据。令 \(\mathcal S_p=\mathcal J_{p,F1}^{ref}\cap\mathcal J_{p,F1}^{id}\)。这些F1支持仅由物理网格、独立reference、strict identity与必需的独立provenance确定，禁止使用operational W/R或detector输出筛选；这里不复用02方法对照中包含operational reliability的同名identity支持。先同时裁切到 \(\mathcal S_p\)，再按其每个连续分量，以 `premise.occupancy_boundary_threshold` 二值化并提取内部manipulation boundaries。边界两侧的实际cells须都在该分量内；padding、未知缺口与裁切端点均不产生边界。禁止一侧在自己的完整支持上提取、另一侧仅在reference支持上提取。

记边界集合为 \(B_r,B_i\)。匹配仅在**同一共同支持连续分量、同polarity**内进行：先最大基数，再保持时间顺序并最小化总绝对时间差，仍并列时按边界时间索引字典序确定，得到 \(\mathcal M_p\)；不得跨未知缺口配对。

定义 boundary displacement：

\[
BTD_p^{task}
=
\operatorname{median}_{(b_r,b_i)\in\mathcal M_p}
\frac{|b_r-b_i|}{output\_grid\_ms}.
\]

无匹配时BTD为not applicable，不能填0。共同支持内的未匹配边界比例定义为：

\[
\boxed{U_{B,p}^{task}=\frac{|B_r|+|B_i|-2|\mathcal M_p|}{|B_r|+|B_i|}.}
\]

两组都为空时该量not applicable；只有一组非空时为1。该量描述共同可观察范围内的边界差异，不把范围外缺失的边界当作消失。若要声称真实边界消失，须有覆盖其相关位置的独立reference或独立删除记录；缺口、零行/零列本身均不是此类证据。\(\tau_B\)、\(\tau_U\)、\(q_{min}\)分别引用第7.7节的boundary displacement、task unmatched fraction、meaningful pair fraction。

删除分支使用独立的source物理时间证据。令 \(A_{x,p}\) 为评价source范围内、由独立source provenance确定的manipulated区间集合；\(D_p\)、\(K_p\) 分别为独立记录明确确认已删除、已保留的source区间，二者不重叠；其余未确认区间记为 \(H_p\)。时间范围及证据需支持这种区间划分；仅知某cell的占用比例并不确定区间在cell内的位置。记实际时长为 \(\mu\)，定义删除比例下、上界：

\[
\boxed{
U_{p,-}^{task}=\frac{\mu(A_{x,p}\cap D_p)}{\mu(A_{x,p})},\qquad
U_{p,+}^{task}=\frac{\mu(A_{x,p}\cap(D_p\cup H_p))}{\mu(A_{x,p})}.
}
\]

没有未知manipulated时长时，两界相等，记其为 \(U_p^{task}\)。\(\mu(A_{x,p})=0\) 时删除分支结构性不适用，不作除零计算；provenance本身缺失时为unknown。不得用 \(\sum_iW_{p,ij}^{ref}=0\) 确认source删除；也不得把fractional occupancy乘以某cell的删除比例来猜测两者的交集。只有cell级比例而无可定位区间时，须使用这些比例允许的保守交集界，或将该分支记unknown。

对所声明的target评价范围，先检查两个边界分支的证据完整性：默认要求 \(\mathcal S_p\) 覆盖该范围的全部真实cells及其实际时长，提取范围内部边界所需的两侧cells也均完整可观察。只要此条件不成立，**BTD与\(U_B\)两个分支均为unknown，不论已观察值高低**；这些值只能描述共同可观察子范围。原因是子集BTD的median可能高于完整匹配集的median，而裁切可能将完整范围内本可匹配的边界变成未匹配。可以另行明确评价一个满足完整性条件的可观察子范围，但其结论不能用于原范围。此完整性条件仅限制边界证据的解释；删除分支仍独立按上述下、上界判断。

原task-active条件仍为“足够boundary displacement、共同可观察的边界差异、足够删除质量”三者之一；实现时按证据采用三值判定：

- 已证active：满足上述完整性条件的边界证据确认 \(BTD_p^{task}\ge\tau_B\) 或 \(U_{B,p}^{task}>0\)，或独立删除下界 \(U_{p,-}^{task}\ge\tau_U\)。删除下界充分时，即使边界分支unknown，也可独立确认active。
- 已证inactive：各相关分支均能排除上述条件；删除分支需 \(U_{p,+}^{task}<\tau_U\)。边界分支没有匹配或没有边界只说明该统计量不适用；只有所声称范围内的相关位置已观察且确实没有该类事件时，才能作为结构性不适用而排除该分支。
- unknown：没有已证active，且至少一个相关分支仍不能排除，包括参考缺口、边界邻域缺失、删除比例两界跨过阈值等。不能仅因为另一个量可定义且低于阈值，就把该pair记为inactive。

family目标pair集合由评价范围和source任务对象决定，不按reference恢复成功或上述三个量是否可定义筛选。source本身确实没有manipulated内容的pair可作为结构性不适用单列；source标注未知的pair保留为unknown。记目标pair总数为 \(N\)，已证active、inactive、unknown数分别为 \(n_A,n_I,n_H\)，三者和为 \(N\)。则目标范围内task-active比例满足：

\[
\boxed{q_{active}^{-}=\frac{n_A}{N}\ \le q_{active}\le\ q_{active}^{+}=\frac{n_A+n_H}{N}.}
\]

unknown保留在两界的同一分母内，既不能算inactive，也不能删除后提高active比例。按第8.9节重采样完整source并重算两个界的CI；目标数与实际有证据的source/pair数、结构性不适用、unknown及coverage分别报告。仍按第7.11节 `premise_pairs_per_family` 检查实际可评价pairs的既有最低量，unknown不能冒充已评价证据凑数。最低量仅用于统计解释；证据不足为INCONCLUSIVE，不阻止其它方法开发。

F1 SUPPORTED：

\[
L_{95}(q_{active}^{-})\ge q_{min}.
\]

F1 PREMISE_REFUTED：

\[
U_{95}(q_{active}^{+})<q_{min}.
\]

其它为INCONCLUSIVE。本次将family判决统一到固定目标集合的比例上下界，避免由缺失选择出的matched子集单独决定整个family的结论。family median BTD及其CI仍在有匹配pairs上计算，并明确这是**共同可观察且有匹配的子集条件统计量**；不能以该子集median替代整个目标集合的 \(q_{active}^{-}\) 而绕过unknown。若另行评价该可观察子范围，其F1判决按同一规则独立计算，结论只覆盖该范围。所有分支都已完整观察时，\(q_{active}^{-}=q_{active}^{+}\)，退化为普通task-active比例判决。

数值核验例：identity通信中，若source唯一的manipulated区间恰落在缺失的5% reference区域，则共同支持上两组边界均为空；该区间属于 \(H_p\)，不是 \(D_p\)，故删除比例为 \([0,1]\)，pair为unknown。若所有目标pairs均如此，\(q_{active}\) 的范围为 \([0,1]\)，F1为INCONCLUSIVE。只有独立记录确认该manipulated区间真的被删除时，删除下界才升至1并产生active证据。

Sparse track使用independent landmarks建立禁止extrapolation的monotonic piecewise-linear map，仅使用已确认可可靠映射的连续时间段；不能跨未确认的插入、删除或landmark缺口补成可靠支持。边界同样在与identity的共同可观察支持内逐分量比较；未观察区间进入上述unknown规则，删除证据仍须来自独立source区间记录。Sparse按同一删除上下界、固定分母及三值判决计算F1；landmark覆盖以外不推断删除或零occupancy，也不声称前提已被否定。

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

完整的同scope机制主张需要以下前提支持；后续实现和探索不以此为准入：

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

每route的建议搜索规模见第7.13节，按实际收益与资源调整。

可先选取在dev上具有可用定位能力的实例，并继续比较其它路线；下列threshold用于完整结论解释，不强制first-qualified选择。

全部 route 在 dev 明确失败：

\[
\boxed{LOCALIZER_UNUSABLE.}
\]

## 16.2 Stage 2L — 当前localizer实例记录

可记下L路线、backbone/head、optimizer、基础增强、BCE/Dice权重、checkpoint选择、M4模块位置与tensor shape、实际seed及checkpoint路径。无需shape hash、锁文件或审查通过。

同次模型比较使用一致的起点及配置；换候选可以直接继续开发并说明差异。

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

评价失败或不确定后可切换L路线继续探索；该数据若参与选择，就不能再称为新候选的独立test。

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

每条路线可以迭代多个候选；记录有意义的变化和观察，无需candidate hash。

## 17.2 Stage 3Q-A — Primary Qualification

评价数据：

\[
D_{\mathrm{corr-qual-A}}.
\]

### 17.2.1 F3可计算统计对象、权重与重采样

Dense与sparse分别评价，不把两类reference混成一个误差池。先按02第10.0节把独立reference分成O+（已确认matched）、O−（已确认unmatched）与O?（未观察/未知）。下文P50/P90/Q95、恢复coverage和reliability只取O+：dense是02第10.1节真实cell，sparse是第10.2节实际独立landmarks。O−另算FalseMatch与FalseAccept；不能把零reference行或缺少reference等同于已确认unmatched。参考本身缺失/超出测量能力的位置不产生error，但应说明reference对原音频的覆盖与缺失pair数；没有某个必要family/stratum的有效reference时其结果为INCONCLUSIVE，不凭其它family补足。

对有reference可观察支持的parent source u、family f、realization r，令层级基础权重

\[
 b_{ufr}=\frac1{U F_u R_{uf}},\qquad
 a_{ufr\ell}=b_{ufr}\frac{v_{ufr\ell}}{\sum_{k\in\mathcal O_{ufr}}v_{ufrk}}.
\]

其中U为这些独立parent source数，F_u为本scope中该source有reference的family数，R_uf为其有reference的realization数；同一母音频的窗口/重复采集归入该source的realizations，不增加U。\(\mathcal O_{ufr}\)只由reference决定；dense取v=cell真实时长，sparse每个实际landmark取v=1。仅一family时F_u=1；不平衡family的整体统计之外，仍逐family报告，缺失的必要family不算通过。

令 \(c_{ufr\ell}=1\) 表示operational W在该reference位置非零且数值有效。\(c=0\)保留基础权重，**包括整对音频无恢复row的情况**。非有限W是实现失败，不能用删除该pair改善coverage。定义

\[
 Coverage=\sum a_{ufr\ell}c_{ufr\ell},\qquad
 \tilde a_{ufr\ell}=\frac{a_{ufr\ell}c_{ufr\ell}}{Coverage}.
\]

coverage是有reference支持上的恢复率，不代表reference对整段音频的覆盖。Coverage>0时，P50/P90及R-0的Q95均对逐row/landmark误差e使用条件权重 \(\tilde a\) 求加权inverse-CDF分位数：相同值合并，累计归一权重首次达到或超过q的值为Q(q)。禁止先求pair mean/median再取这些分位数，也不按预测R筛样或加权。Coverage=0时误差分位数和reliability未定义，报告该缺失及coverage=0；不能把未恢复当作零误差。是否足以给完整失败判决仍按minimum/precision及可计算的失败项解释。

数值例：每对音频均有100个等时长reference rows，89行误差0、11行170 ms且全部恢复。pair mean为18.7 ms，但F3 P90=170 ms，不能用18.7通过60/100 ms尾部阈值。另一例：两个等权source各一pair，一个完全恢复且误差0，另一个全部未恢复；Coverage=.5，条件P90=0，不能因已恢复部分准确就通过coverage检查。

可靠性使用同一e与 \(\tilde a\)。对任意值z定义加权中秩 \(r_w(z)=\sum_{z'<z}\tilde a_{z'}+\frac12\sum_{z'=z}\tilde a_{z'}\)；\(\rho_R\)是 \(r_w(R)\)、\(r_w(e)\) 的加权Pearson相关，等权时即普通tie-aware Spearman。最高四分之一按**权重质量**而不是点数选择：从R最大值向下累计至.25，边界R并列组按同一比例分配保留质量，使恰好.25，禁止用source编号任意选掉并列点。其误差median采用上述inverse-CDF Q(.5)，top权重单独归一；\(G_R=1-Q_{top,e}(.5)/Q_e(.5)\)。R/e常数、总误差median=0或无恢复支持时按未定义处理，不填零。

CI按第8.9节source membership分层的cluster bootstrap。每次整source有放回抽样，保留其全部families、realizations、rows/landmarks及候选间配对；用source multiplicity乘基础权重并重新归一，再从头计算Coverage、条件权重、误差分位数、加权中秩、top-quarter阈值及gain。不能bootstrap帧/landmark、复用全样本top-quarter列表或对pair均值取CI。必要authenticity stratum先在reference对象上筛选，重新建立该stratum的U/F/R及权重，最低量按含该stratum的独立parent sources计；没有该stratum不能判通过。插值点、rows或多个窗口均不增加独立样本量。

对O−按同样层级重建base权重，分别加权平均W非零指示与W非零且R>0指示，得到02第10.0节的FalseMatch与FalseAccept；整source重采样仍保留该source的O+/O−关联。O?单列未观察范围，不混入分母。没有O−观察时拒配证据缺失，不默认通过；实际误接受的位置不得进入可信支持。全零观测的bootstrap可能给[0,0]，不能将其当作总体零风险保证或有效误接受上界；本版不据此给完整partial-support资格。若以后需要推广拒配主张，按具体任务补独立样本与合适推断，现有matched评价及开发照常继续。

这些分位数用inverse-CDF；**bootstrap统计量的CI端点**仍用第8.9节type-7插值，两者不混用。任何重采样中必要统计量未定义按第8.9节保留原因并判相关项INCONCLUSIVE，不静默重抽。该统计合同服务于可解释结论，开发时可先计算少量样本点估计，不以CI尚未可计算阻止继续研究。

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

可按第8.10节规划样本/precision；实际precision不足时该候选结果为INCONCLUSIVE。后续探索或补数据按第7.14节解释，不因不确定而禁止换候选。

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

使用第17.2.1节相同reference对象、条件权重、weighted Spearman和最高四分之一权重的gain；CI整source重采样并重算所有非线性步骤。

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

R-0不经过Spearman/gain检验；其本节资格仅针对dense reference确认的matched支持，不等于完整partial-support或拒配能力。它仅在O+上评价同一W的independent row-error Q95：\(U_{95}(Q95)\le\texttt{r0.controlled\_q95\_ms}\)时ELIGIBLE并映射为该W的R=QUALIFIED；\(L_{95}(Q95)\)严格大于阈值时INELIGIBLE并映射为REJECTED；跨越阈值则INCONCLUSIVE。此严格Q95上限也适用于REAL dense，不随REAL的W阈值放宽。sparse-only永远INELIGIBLE，作为结构上不适用的候选跳过，不能冒充一次统计失败。R-0在O−上W非零就会实际误接受；Q95通过不能覆盖这些错误位置。O−缺失或O?存在时，不将matched资格外推为全支持可信。

若independent error恒定，或median(error)=0导致gain无定义，可直接检查同一W的R-0；必须dense reference、W整体及全部mandatory strata的minimum/precision/absolute fidelity均合格，且整体与每个mandatory stratum的 \(U_{95}(Q95)\le60\text{ ms}\)。通过时R-0在上述O+范围有支持，仍按O−/O?规则限制作用域；可记录reason `RANK_UNIDENTIFIABLE_HIGH_FIDELITY`，不将R-A/B/C无定义的值填成通过。仅R恒定而error非退化、数据/precision不足或普通CI跨阈值不能推断高保真；R-0未通过时保留它和原R各自的结果。后续可以改变R继续探索，但独立确认以实际未参与选择的数据为依据。

候选W/R的QUALIFIED解释同时需要W、R及主张scope内必要strata支持；只确认W不能代替R的证据。W的独立误差不以预测R遮蔽，所以换R不能抹去同一W的错误。失败或INCONCLUSIVE后均可继续尝试其它W/R，逐候选保留其结果，不设置sticky状态或固定顺序准入。

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

## 17.3 Stage 3Q-B — 第二组数据上的确认与诊断

Q-A之后可以在第二组source-identity独立的数据上评价同一W/R及同一指标，观察能否保持fidelity/reliability。Q-A尚未通过时也可用其它开发数据诊断，不以qualification手续限制探索。

Q-B支持则增加对当前候选的信心；明确失败记录REJECTED_EXTERNAL并分析分布差异；不确定记录缺少的信息。三种情况均可据此选择下一候选或调整方法，不设置sticky状态。若Q-B结果用于选路，独立确认另用未参与该选择的数据；缺少新数据时保留探索性质即可。

## 17.4 已试候选的结论

所有已评估候选均明确失败时，OPERATIONAL_SCOPE_REFUTED只覆盖这些候选及已测条件；有未解的不确定性则记录F3 INCONCLUSIVE。某候选支持不抹去其它失败。可以检索并尝试新候选，不要求先完成整个候选表或办理新版本。

W-E始终是reference/oracle，不能替代operational方法的实测支持。

## 17.5 Stage 3L — 当前对应实例记录

可在现有配置中记下W/R路线及参数、Grid Adapter、support规则、reference来源、scope和U-OP分析方式，链接已有评价。记录不作为运行门槛；实际估计器及信息/梯度边界按02实现。

## 17.6 Stage 3T — Final Corr-Test / F3

对当前具体W/R实例使用相同decision functions评价。

若 W 与 R 均 QUALIFIED，必要 authenticity strata 均满足 absolute fidelity floor，且precision参考条件满足，则在本次reference已确认matched的O+支持上：

\[
\boxed{F3[\mathrm{scope}]=SUPPORTED.}
\]

同时列明O−上的raw误配与实际误接受、O?未观察范围。现有判据未检验拒配总体风险，不能只把同一个family名称写上就扩展到完整partial-support。

Sparse的SUPPORTED明确限定landmark位置，采用分布误差而非重心误差；不能自动覆盖landmark之间、整个区间或全音频。全时间轴CEL/CS机制证据的解释遵循第3节scope规则。

若仅 precision / sample size 不足：

\[
\boxed{F3=INCONCLUSIVE.}
\]

若该具体实例在Corr-Test上明确REJECTED：

\[
\boxed{F3=OPERATIONAL\_REALIZATION\_FAILED.}
\]

并记录：

```text
external_validation_failure: true
next_action: diagnose_and_explore_candidates
```

该状态是合法终点。它**不**等价于 `OPERATIONAL_SCOPE_REFUTED`。

之后可直接尝试其它W/R路线，保留本次失败；后续评价按实际数据使用解释，不能择优拼接不同候选为一次成功。

---

# 18. 机制比较的输入与解释依赖

Stage4开发实际需要可计算的localizer输出、有效paired数据、W/R和M2/M3′/M4/M5损失，不要求F1/F2/F3或localizer先取得SUPPORTED。缺独立参考、localizer弱或对应误差大时仍能排查实现、观察训练行为，但结论应限制到这些实际条件。

F1/F2说明任务及occupancy传输前提，F3说明对应可靠性；完整同scope机制主张需结合这些证据。它们限制结论解释，不限制模块实现、CS探索、换路或轻量实验。

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

# 20. Stage 4P — Mechanism Power / Precision Planning

这是完整评价的样本量建议，输入为4D四个实际模型及mech-dev预测。模型或训练配置变化后，相应方差与样本规划需要重估才有适用意义。规划未完成或规模不足时可继续小实验，不能据此宣称充分功效或将未显著视为null。

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

则可按 `n_lock` 规划独立source数量；该变量名沿用公式，含义是计划样本量，不要求锁文件。可记下所用模型、dev数据、seed、方差、planning alternative和family分配。功效仅对应第8.6节的单项显著性检验；实际评价采用的模型若不同，不能沿用旧方差承诺其功效。

### POWER_INFEASIBLE

若：

\[
n_{lock}>n_{cap},
\]

则：

\[
\boxed{POWER\_INFEASIBLE.}
\]

可以用较少样本继续探索；低功效下未显著的结果不能直接解释为practical null。

---

# 21. Stage 4L — 当前机制比较记录

记录有助于解释的实际选择：M2/M3′/M4/M5实例、scope、lambda、M4位置与shape、seed、训练步数、指标、F4分解及U-OP方式。可复用训练配置和输出日志，不要求合同hash或lock。

相同比较按02保持必要差异，其余训练条件匹配。若变化引入额外解释，补相应对照或收窄结论；记录缺项不阻断研究。

---

# 22. Stage 4T — F4 / F5 / F6 Formal Mechanism Test

说明实际source数量和评价对象，与样本规划比较；规模不足限制判决，不禁止运行。

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

使用与当前W/R实例对应的independent operational error即可开展，说明reference与数据来源，不等待Stage3T或F3 SUPPORTED。

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

# 23. 机制比较的结论与下一步

## 23.1 F4/F5/F6均SUPPORTED

同scope的三项比较及必要前提支持时，可称为该已测scope内的Validated Mechanism Contribution；结合保护性指标说明适用边界。

## 23.2 任一PRACTICAL_NULL

保留该比较及效应上界，收窄相应创新主张。分析是标签传输已经足够、特征一致性已覆盖收益，还是方法假设不适用。可以直接检索、改变W/R、loss、tap或新增对照，检验新的可区分假设；新方法的成功不改写旧比较的null。

## 23.3 任一INCONCLUSIVE

说明样本、方差、实现或适用性的不确定来源。可继续探索、补充数据或改路线，按第7.14节说明后续选择对统计解释的影响。没有新信息时避免机械扩样；该判决不禁止Stage5/6开发或其它方法工作。

---

# 24. Stage 5T — Frozen Real-Chain Evaluation

形成Strong Real CEL解释所需的前提为：

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

Stage5可按第7.15、8.10节规划expected CI width，2000–3000是完整评价的参考规模。小规模先行或后续补数据均可，说明实际规模及第7.14节的统计限制；实际precision不足时保留INCONCLUSIVE。primary verdict按以下公式，最终Stage5 verdict再按第28.4节合并三类保护性检查；只有保护性检查通过时，primary PRACTICAL_NULL才按Outcome M解释，保留原REAL机制证据。

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

已有可计算的CEL实例、paired数据及合法negative bank即可开发CS，不等待F1–F6或Stage5全部通过。起步可使用构造例或oracle排查计算；其结果不能代替operational验证。

推荐先试N-A，再按观察考虑N-B/N-C或有依据的新候选。实际依赖为：

```text
1. 使用label/output-blind W/R；
2. 同样以label/output-blind路径构造合法negative bank；
3. gate读取Y_x，不能反向改变W/R或bank；
4. 从同一M5起点匹配追加训练CEL控制与CS分支。
```

不要求bank hash、封存或锁定文件。F3未验证时限制对gate及CS效果的实际语义解释，仍可计算和调试。

两分支使用同一seed的M5 checkpoint、\(D_{cs-train}\)、paired sampling次序、optimizer、学习率/weight decay、\(\lambda_{CEL}\)、追加optimizer步数、有效batch及checkpoint选择规则。CEL控制继续优化loc+CEL，CS增加selectivity；g=0的pair仍以相同规则参与两侧基础目标，不能只给CS筛选更容易的数据。detector可按合同继续更新，W/R及negative bank不更新。CS新增参数在cs-dev上探索并说明实际搜索投入，共享配置不为某一侧单独调优。

先按02第17.1节做G-A的teacher传输差异与selectivity梯度诊断。gate=1且hinge>0不保证梯度有效；相消时可继续source监督/CEL、修复localizer或探索其它实例。两侧共享改进后的同一起点，重新计算dev尺度，不用加大margin代替诊断。

第7.17节的margin及selectivity尺度用追加训练前的M5在cs-dev上的固定预测计算，先确定尺度再搜索CS参数，不使用test结果，也不以训练后CS输出定义门槛。开始匹配比较时给两侧相同的追加训练步数、共享optimizer配置和有效batch；可先用小步数调试，配置随运行记录，无需预登记手续。

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

可继续探索新的label/output-blind negative族，说明其与旧失败的差异及可判别问题。

这不否定已支持的 CEL。

---

# 26. Stage 6L — 当前CS实例与评价口径

第7.17节以追加训练前M5的cs-dev预测计算margin m及epsilon_sel_gain；该数据依赖服务于避免训练后输出反定义目标。CS尺度为零或不可识别时按该节记录真实数值问题，不凭空制造有效目标。

可随运行记下scope、negative族、bank构造规则、CEL/CS共同起点和数据、共享训练配置、delta_W、delta_Y_op、lambda_sel、seed及informative比例。保护性评价使用未按CS gate筛选的clean/BF/fullfake子集及共同M0参考。

上述内容可直接存在代码/config或日志里；没有manifest、hash或lock不影响继续研究。

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

分别给出第27.1节Discrimination、第27.2节Localization的primary判决，以及第28节三项guardrail的判决；合并状态不覆盖这些原始结果。

| 已观察条件（按此顺序合并） | F7合并状态 | 含义 |
|---|---|---|
| 任一guardrail明确FAIL | GUARDRAIL_FAILED | 当前CS实例出现保护性退化；不把primary效果写成零或低于epsilon |
| 无guardrail FAIL，至少一个primary component为PRACTICAL_NULL | PRACTICAL_NULL | 对应component有第27.1/27.2节规定的效应上界证据；另一component和不确定guardrail仍单列 |
| 两个primary components均SUPPORTED，且三个guardrails全部PASS | SUPPORTED | 当前scope和有限bank内CS扩展得到支持 |
| 其它 | INCONCLUSIVE | 明确尚缺的效果或保护性证据 |

每一项先按自己的minimum/precision判断是否可判；数据不足不会自动产生FAIL或NULL。`GUARDRAIL_FAILED`可与已支持的primary效果并存，表示可用性主张受限；既有CEL证据按原scope保留。任何状态都允许继续诊断、改进和新比较，不是停止研究的准入规则。

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

三项分别使用clean mixed-partial、bona-fide、fully-manipulated子集，若用于独立评价则与训练/dev身份隔离；探索评价说明实际数据用途，不按CS gate、negative-bank可用性或模型预测过滤。clean与informative可共享parent identity，其bootstrap multiplicity必须相同；纯真/纯假不需negative bank。三类各遵循第7.16、8.10节minimum/precision/cap，缺类或量不足为该guardrail INCONCLUSIVE，不默认PASS。CS的informative minimum不能抵扣这些子集。

M0是本次比较共同使用、对应seed的source监督localizer checkpoint，不为某个方法另行重训参考。Stage4/5检查M5对M0，Stage6检查CS对同一M0；匹配追加训练CEL仍是F7 primary comparator。Bona-fide与fullfake容忍量由相应stage dev上固定M0计算，在本次评价前确定，不用test计算门槛；配置随运行记录。第28.1节epsilon_clean引用第7.16节的clean容忍量。

组合guardrail：任一FAIL则FAIL；否则任一INCONCLUSIVE则INCONCLUSIVE；全部PASS才PASS。三项CI只代表各自marginal近似区间，不宣称联合95%覆盖。Stage4–6的主效果、guardrail状态、合并状态分别保存，不互相覆盖。

| 阶段 | 主效果之外的必需条件 | 未通过时的结论解释 |
|---|---|---|
| 4T | M5三类guardrail PASS | FAIL记Outcome N；INCONCLUSIVE记Outcome K；保留F4–F6效果判定，收窄可用CEL主张，可继续5/6探索或修复 |
| 5T | M5三类guardrail PASS | FAIL记Outcome N，Stage5合并verdict=INCONCLUSIVE并带GUARDRAIL_FAIL原因；INCONCLUSIVE记K；保留primary结果，不形成Strong Real CEL |
| 6T | CS三类guardrail PASS | FAIL使F7=GUARDRAIL_FAILED并记Outcome N；primary状态原样保留。无FAIL时按第27.3节处理NULL与不确定性；保留此前成立的CEL |

最低量/precision不足优先于对应项判定。Stage4若主效果已明确NULL仍记J；若主效果支持而guardrail失败记N，不把保护性失败当作机制效应小于epsilon。Stage5在guardrails PASS后才采用第24节primary/multi-family合并verdict；失败时不以primary上界解释guardrail。Stage6按第27.3节区分GUARDRAIL_FAILED与primary PRACTICAL_NULL。Outcome K/N可同时列原因，已成立的其它scope和旧版本证据保留各自身份。

---

# 29. Authenticity / Information-Boundary Audit

以下用于检查实际方法是否符合02及其适用范围。检查可在实现/调试中按需要完成，不要求独立审查角色、审计报告或检查清单全签。结构边界与经验稳定性是两个不同问题。

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

# 30. 实现与数值排查参考

优先检查会直接改变计算或混淆比较的问题：

- W/R是否读取了Y、伪造边界或detector输出；detector梯度是否误更新W/R，G-A是否确实阻断source teacher梯度。
- Grid Adapter的物理时间、有效支持、零行、归一化是否正确；W-C的phoneme/CTC位置是否有实际时间映射。
- 若raw row mass携带confidence，是否保留到R的证据；是否把未恢复对应当成零误差。
- M2是否严格identity；M3′是否与M5仅改变被传输对象；M4是否使用canonical pre-logit tensor及同W，而未增加独立projector或对齐器。
- CS bank是否按label/output-blind路径生成，gate是否只计算适用性而不反向改变bank；F7是否使用同起点匹配追加训练。
- 指标是否按真实cell时长、source单位和既定聚合计算；oracle、U-REF、U-OP与真实通信是否区分。

按本次变更选择有辨别力的小数值例、梯度检查或实际路径观察即可。发现具体错误则修复并重新计算受影响结果；没有执行整张清单、没有自动审计或缺少hash不会自动导致INVALID。科学解释看实际方法和数据，不看检查表完整度。

---

# 31. 实现组织建议

可以从少量函数、脚本或Notebook开始，按需要复用数据、网格、W/R、loss、localizer和metric代码。阶段编号用于说明问题，不要求一阶段一个唯一入口，也不禁止同一任务组合多个模块。

评价用途由真实数据流决定：训练或选路使用了某数据，就如实说明其不再是独立确认测试。入口数量、文件布局、封存机制或编排框架不是方法正确性的替代物。

---

# 32. 本地运行与环境记录

先使用现有可用环境实现并运行当前方法问题。需要时记录运行参数、checkpoint、输出、耗时和显存；依赖快照、Git版本、跨端同步、完整恢复状态与环境复现均为辅助，不作为启动或继续条件。脚本与Notebook可以共用函数，按实际复用价值组织，不强制平台或入口。

## 32.1 Backbone缓存建议

完全frozen backbone的特征可以缓存以节省计算，也可直接在线提取。复用前确认特征对应当前实际波形、变换、预处理、backbone和特征层/精度；不能只凭source ID混用不同realization。可用清晰路径、配置和shape作关联，无法确认时重算相关特征，无须专门hash校验系统。

## 32.2 中断后继续

有可用checkpoint及optimizer/scheduler状态时可恢复；只有部分状态也可另行继续或重启，说明实际差异及训练投入。不要把更换训练状态的两段声称为完全相同运行；无法完整重现不禁止进一步方法工作。

## 32.3 当前本地硬件与运行边界（2026-10-03 实测）

本节记录检查时的本地实施条件。环境资料与复现步骤供参考，不设研究准入；模型对照和实际计算按02实现，第7节提供可调整的起步配置及结论评价口径。

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
- 默认完整screen矩阵共28次runs，可按方法问题先运行其中少量实例，再决定是否扩大；多seed实验可串行安排。
- 长音频、端到端解冻骨干、复杂多编码器或learned correspondence的可行性需单批实测；本节不承诺全套formal研究均能在6 GiB显存完成。

本机优先小批提取特征、按需加载缓存。峰值显存、内存和耗时有用时记下，据此调整资源或实验规模；改变模型、batch或数据范围后说明差异并保持比较公平，不能把缩小后的实验称为原完整配置。

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

该报告中的耗时含首次调用开销，只用于软件安装验收；不代表预训练模型质量、真实数据吞吐、正式TCN实现或F1–F7证据，也不计入Stage P的28-run预算。实际使用预训练WavLM需要可加载权重及兼容的特征配置；revision等来源信息可随手记录。

## 32.5 本地显存、缓存与路径安排

采用第7.2节完整Stage P实例时，`effective_batch_size: 32`。更小的探索配置也可运行，说明实际batch、步数和对照条件。显存不足时可采用micro-batch与梯度累积，使每次optimizer更新对应32个有效训练样本；1500 / 1000训练步按optimizer更新计。BCE/Dice逐样本计算后按完整有效batch平均，辅助项按02第4.1.1节各自分母归约；禁止改成pooled Dice或独立micro-batch均值。训练采样跨epoch持续组成32个条目的完整batch，不执行不足32的末尾optimizer更新。优先在optimizer更新边界保存checkpoint。

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

2026-10-03本地环境验收时尚未建立Git仓库，故该报告记录脚本内容hash。随后已初始化本目录Git仓库，修订前基线为`710ba11`；后续可随手记下实际commit及有意义的未提交变化，未知信息说明未知。Git、hash、环境锁及完整复现仅供参考，不决定是否允许运行。

---

# 33. 简短运行记录示例

记录帮助解释尝试与避免重复；可直接使用已有终端日志、Markdown或表格，无需固定schema。下例字段任选，未知项可以留空，运行前不必填满：

```json
{
  "question": "本轮要区分的方法问题",
  "method_change": "相对已有尝试的关键变化",
  "data_and_model": "实际使用的数据范围与模型来源",
  "conditions": "必要对照、seed及主要训练条件",
  "observation": "指标、失败或尚不确定的事实",
  "artifacts": [],
  "next_step": "下一步及理由"
}
```

已有commit、revision、环境版本和耗时可顺手附上；不要求fingerprint、hash、seal、lock、完整manifest或防篡改存储。记录可更正、补充和合并；保留重要失败事实，不把未运行的计划写成结果。

---

# 34. 可选产物目录示例

下面仅供需要整理时参考，可使用更简单的目录；不要求预先创建全部阶段结构。

```text
artifacts/
├── versions/              # 按需要区分不同方法尝试
├── stageP_screen/
│   ├── P0/
│   ├── P1/
│   ├── P2/
│   └── P3/
├── stage0_reference/
├── stage0_notes/
├── stage1_premise/
├── stage2_localizer/
├── stage3_correspondence/
│   ├── dev/
│   ├── qual_A/
│   ├── qual_B/
│   └── corr_test/
├── stage4_mechanism/
│   ├── power_planning/
│   ├── dev/
│   └── formal/
├── stage5_real_chain/
├── stage6_cs/
└── final/
```

---

# 35. 工作与观察总表

| 工作 | 主要观察 | 不理想时的下一步 |
|---|---|---|
| P0–P3 | 数值正确性、可学习性、oracle机制信号 | 修复、分析或换有依据的候选 |
| 0A | reference可行性 | 继续CTRL探索，明确REAL证据缺口 |
| 0B | 当前配置与数据用途的简记 | 有用时补记，不阻断运行 |
| 1 | F1/F2前提 | 区分范围、数据问题与前提不成立 |
| 2 | localizer是否提供定位信息 | 改进模型或数据，继续独立模块 |
| 3 | W/R误差、coverage与reliability | 分析错误类型，尝试适用候选 |
| 4D/4P/4T | 必要对照效果及不确定性 | 调整机制、对照或评价规模；保留旧结果 |
| 5 | real-chain效果与退化 | 解释迁移边界，检索针对性改进 |
| 6 | CS selectivity及匹配定位收益 | 改进negative或放弃无效扩展 |
| 7 | 当前结果、失败和下一问题 | 交付现有观察，可继续实现 |

本表没有hash、审查或锁文件准入；阶段可按第4节实际依赖交叉进行。

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
| authenticity-label-agnostic estimator | 实际输入及梯度满足02的信息边界 |
| cross-authenticity fidelity stability | stratified Stage 3 evidence，不等价于 structural audit |

---

# 37. 结果状态与可支持的结论

本节给出完整评价下的结果解释。它们不是停工命令：方法开发、检索、诊断和换路线仍可继续；保留当前scope及比较的结论，不把后续探索改写成旧尝试成功。

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
F7 PRACTICAL_NULL / INCONCLUSIVE / GUARDRAIL_FAILED；
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

现有screen信号不足以支持扩大同一配置的投入，也不是F5 formal refutation。按第39节诊断并尝试能提供新信息的调整。

## Outcome F — Premise Refuted

```text
F1 PREMISE_REFUTED；
或 F2 PREMISE_REFUTED。
```

不继续主张该已测scope的对应前提成立；可分析条件、数据与方法变化并继续研究。

## Outcome G — Operational Scope Refuted

```text
已评估的W-A/B/C/D候选均明确REJECTED / REJECTED_EXTERNAL，结论限定这些候选与条件。
```

因此：

\[
F3=OPERATIONAL\_SCOPE\_REFUTED.
\]

## Outcome H — Operational Realization Failed

```text
当前具体W/R实例；
Stage 3T 独立 Corr-Test 明确 REJECTED。
```

因此：

\[
F3=OPERATIONAL\_REALIZATION\_FAILED.
\]

可以换路线继续研究；不把该结果扩大解释为整个operational family全部被证伪。

## Outcome I — Localizer Unusable

```text
Stage 2D 全 route dev failure；
或Stage2T当前localizer独立评价失败。
```

当前localizer不足以支撑有辨别力的机制比较，先定位原因并改善；其它独立模块可继续。

允许保留：

```text
F1/F2/F3 premise evidence；
detection-only contextual baseline；
failure analysis。
```

Stage4代码与小构造例仍可推进；弱localizer上的未显著结果不能直接否定CEL机制。

## Outcome J — Mechanism Partial Null

F4/F5/F6 任一：

```text
PRACTICAL_NULL。
```

收窄相应机制主张，保留效果上界。Stage5/6及新方法仍可用于探索其它可区分问题。

## Outcome K — Inconclusive

包括：

```text
现有样本不足以消除关键不确定性；
POWER_INFEASIBLE；
PRECISION_INFEASIBLE；
formal effect test 本身 INCONCLUSIVE；
N-route exhaustion 导致 F7 INCONCLUSIVE。
```

如实报告不确定性。是否继续取决于新增信息与实际资源，不要求先建立新版本；统计解释遵循第7.14节。

## Outcome L — 方法实现或证据使用错误

如W/R误读标签、oracle冒充operational、M3′或M4计算不符、网格/标签错位，则对应结果未检验所声称的方法，可记INVALID_IMPLEMENTATION并修复受影响计算。若训练或选择使用了被称为独立test的数据，结果仍可用于探索，但不能保留原独立确认解释；可记INVALID_FOR_FORMAL_EVIDENCE并说明具体影响。

缺少hash、provenance元数据、seal、lock、环境锁、完整可复现步骤或审查记录，本身不属于以上错误。评价后换路线也不自动无效；问题在于是否如实说明新方法与数据使用。

## Outcome M — REAL Scope Mechanism Supported, Real Strength Not Supported

同一REAL scope的F1–F6全部SUPPORTED且Stage4保护性检查通过，但Stage5 primary为PRACTICAL_NULL、Stage5保护性检查亦通过。允许报告该已测试REAL scope内的机制贡献及真实链效应上界；不主张Strong Real CEL，也不能在未独立验证CTRL时改称Controlled Mechanism CEL。

若按第25节另执行了F7，其结果作为该scope及登记negative族内的扩展证据单列，不把Stage 5未支持改写为Strong Real CS-CEL。若Stage 5为INCONCLUSIVE则使用Outcome K并同样保留已有机制证据。已有CTRL结论可按自己的独立证据同时保留，不能跨scope拼接。

---

## Outcome N — Guardrail Not Satisfied

当前版本Stage4、Stage5或Stage6的必要guardrail明确FAIL。保留已得到的主效应、scope及失败维度，收窄相应可用方法/Strong Real主张；不把该状态冒充PRACTICAL_NULL效应上界。Stage6同时记F7=GUARDRAIL_FAILED并保留先前合法CEL结论。三类guardrail有INCONCLUSIVE而无FAIL时使用K；实际primary NULL仍保留其单项证据。

# 38. 失败后工作的组织

同一执行者可以依次完成读结果、查文献、提出机制假设、实现和分析；有益时用子智能体分担独立阅读或检查。没有固定五角色、必须独立复核、会签或owner登记门槛。

| 观察 | 优先处理 |
|---|---|
| Screen或机制收益不足 | 比较必要对照，定位冗余或假设不适用 |
| W/R误差或reliability失效 | 分析错位、覆盖、时间映射、声学条件，再查针对性方法 |
| Localizer不学习 | 检查标签、监督、输出网格与优化，再评估模型实例 |
| 不确定性过大 | 看主要方差来源与实际可增加的信息，避免只追显著 |
| 真实链或保护性指标退化 | 查迁移、coverage及纯真/纯假行为，保留已有机制观察 |
| 数值、数据或实现错误 | 最小修复，重算受影响结果，然后继续方法工作 |

---

# 39. 失败后的自主研究与避免重复

## 39.1 区分观察与诊断

先看真实输出，区分实现错误、优化/资源问题、数据条件、统计不确定与机制不足。记录已观察事实及适用范围；原因不明写明未知并提出可区别的解释。科学失败不能仅因结果不理想就改称工程错误。

## 39.2 最小失败记录

可在现有研究笔记、表格或日志中简记：尝试了什么、关键条件、结果、失败/不确定点、产物位置和下一动作。普通文件即可，不要求events.jsonl、追加式账本、路线指纹、hash链、完整manifest或指定目录。记录整理不作为下一步前置；保留重要失败事实和相关结果，避免只留下最佳seed。

## 39.3 回顾相似尝试

尝试相似路线时快速查阅已有相关记录，判断旧失败是否适用于当前问题。这次若改了数据条件、机制、实现、参数或seed，说明它要回答的新问题。复测、seed稳健性与参数敏感性本身可以是有用问题，不要求预注册才能执行；只有改名或机械重复而没有新信息时，优先转向更有价值的实验。

## 39.4 主动文献检索

机制路线失败或原因不清时，自主检索原论文、作者代码/数据与官方技术资料，同时关注限制、反例和后续修正。简记已读来源链接、关键依据及适用前提；未读全文或只看到摘要时说明。文献事实与本项目推断分开，不能把已有论文的效果当作本项目已验证。

## 39.5 新候选与最小判别实验

根据诊断选择机制上有区别的候选，说明改变什么、为何可能改善、用什么必要对照区分解释；直接实现并运行最小有信息的实验，再决定是否扩大。候选数量、记录格式和阶段顺序按实际问题安排，不要求先登记完整实验计划、设定自行生成的审批cap或建立新research version。

在已授权的研究范围内自主推进实现、检索、普通工程修复、路线切换及本地CPU/GPU验证。遵守用户实际资源限制；根据运行时长、显存、信息增益调整投入。没有新候选、相同失败重复或资源确实不足时，说明具体原因并转向可独立推进的工作。真实超范围费用、受限权限或外部操作按04处理。

## 39.6 新旧结果与数据用途

直接更新当前方法与文档，保留旧结论及有用的关键变化记录即可。旧test一旦用于新路线诊断/选择，就是开发信息，可以继续用它探索；同source换codec/window/seed不能恢复独立性。若要作新的独立确认，则使用未参与选择的source及评价数据；没有独立数据时继续探索但收窄结论。

多轮方法结果分别说明，不挑有利片段拼成一次成功，也不声称普通单次p值控制了整个反复选路过程的错误率。无需通过版本隔离、快照hash或重新qualification手续来获得继续工作的许可。

---

# 40. Stage 7 — 当前结果交付

交付已完成的方法变化、实际执行、主要指标和失败、结论范围以及下一步，链接已有代码和产物。F1–F7/scope表、对照效果、F4分解和guardrail信息按实际运行内容展示；未运行部分写未运行，不虚构数值。

版本、环境、数据来源与检索信息已有则附上，不要求完整evidence package、hash或审计通过才能交付或继续研究。整理报告时若发现需要改进方法，可回到实现与实验。

---

# 41. 当前设计覆盖与尚待实际验证

设计已覆盖监督归约、物理时间网格、M3′/M4对照、F4分解、U-REF/U-OP、对应误差/reliability、CS bank/gate及公平追加训练、指标和统计解释。这表示能据此开始实现，不代表任何科学命题已被验证。

当前真实研究的待落实项是数据可用性、可加载模型及具体W/R实现效果。现有环境验收只说明部分工程路径可用。可以先完成不依赖真实资源的构造例、损失、网格和接口；随后接实际输入，不把治理记录缺项算作方法阻塞。

---

# 42. 当前推进重点

先做可运行的方法机制最小路径：数据/网格 → localizer与W/R → M2/M3′/M4/M5匹配比较 → CEL/CS匹配追加训练。按问题穿插检查前提与真实参考，观察结果后继续修复、检索和迭代。

F5仍以M5与M3′比较解释prediction transport的非冗余性，F6仍以canonical pre-logit M4作feature对照，F4结合coverage/common-support分解解释。方法结论依赖实际证据，记录完整度不决定项目能否继续。

本文保持可修订；治理、可复现、防篡改和协作安排仅供记录，不作为项目准则。

---
