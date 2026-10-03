# 算法原语设计：Communication-Equivariant Localization with Correspondence Selectivity（CEL / CS-CEL）

> 研究方向：真实通信场景下的局部语音 Deepfake 检测与时间定位  
> 文档职责：定义项目中不可反向修改的研究问题、核心数学对象、核心算法关系、原语级创新边界与证伪条件  
> 文档层级：**Algorithm Primitive / Invariant Specification**  
> 实现路线：不在本文固定  
> 项目流程：不在本文固定  
> 状态：**FINAL-FROZEN — ALGORITHM PRIMITIVE LOCKED**

---

# 0. 文档职责与冻结边界

本文只回答三个问题：

1. **研究问题是什么？**
2. **算法核心数学关系是什么？**
3. **什么变化仍属于该算法原语，什么变化已经偏离原语？**

本文不规定：

```text
backbone
temporal head
correspondence estimator 的具体实现
reliability estimator 的具体实现
DTW / CTC / ASR / SSL / learned alignment 等技术选择
negative correspondence 的具体生成算法
supervised loss 的具体形式
训练超参数
数据集构建
实验阶段
统计检验
GPU / Colab / 代码流程
A 路线失败后切换哪条 B / C 路线
```

这些分别属于：

```text
02_方法实现机制设计
03_项目推进路线
```

因此，后续技术路线可以改变，但不得改变本文冻结的算法关系。

---

# 1. 研究问题

局部语音 Deepfake 检测的目标不是只判断整段音频真假，而是恢复随时间变化的 manipulation field：

\[
u
\longmapsto
P_\theta(u),
\]

其中：

\[
P_\theta(u)_k\in[0,1]
\]

表示第 \(k\) 个时间单元属于 manipulated content 的模型置信度。

真实通信链路可能包含：

```text
codec / resampling
RTC processing
VAD
AGC
AEC
noise suppression
packet loss / jitter
neural codec
speaker-microphone re-recording
clock drift
```

这些过程不仅改变声学特征，也可能改变局部 manipulation region 在接收端时间轴上的：

```text
位置
长度
全局偏移
时间尺度
局部时间对应
删除 / unmatched support
```

因此，在存在 temporal correspondence change 时，直接要求：

\[
P_\theta(x')
\approx
P_\theta(x)
\]

并不具有正确的时间坐标语义。

本文的核心研究问题固定为：

> **当真实通信过程改变局部 Deepfake manipulation field 的时间对应关系时，如何使接收端 manipulation output 遵循该 communication-induced temporal transport，并在 correspondence 可辨识的条件下对可信 correspondence 保持选择性？**

---

# 2. 基础对象

## 2.1 Manipulation provenance

对任意音频 \(u\)，定义 attack-level manipulation provenance：

\[
Z_u(t)\in\{0,1\}.
\]

其中：

\[
Z_u(t)=1
\]

表示该物理时间位置的内容属于目标 Deepfake manipulation。

Benign communication processing 本身不改变 attack-level provenance：

\[
\boxed{
\text{benign communication processing}
\not\Rightarrow
Z_u(t)=1
}
\]

因此，codec、AEC、NS、AGC、resampling、RTC enhancement 等可以改变信号，但不因其本身使真实内容成为 Deepfake manipulation。

---

## 2.2 Temporal manipulation occupancy

将连续 provenance 投影到离散时间网格，得到：

\[
Y_u\in[0,1]^{L_u}.
\]

\(Y_u\) 表示真实 temporal manipulation field 在离散网格上的 occupancy。

---

## 2.3 Temporal manipulation output

模型输出：

\[
P_\theta(u)\in[0,1]^{L_u},
\]

并固定数值方向：

\[
\boxed{
P_\theta(u)_k\uparrow
\Longleftrightarrow
\text{stronger evidence of manipulation}
}
\]

本文不要求 \(P_\theta\) 是精确 Bayes posterior。

---

## 2.4 Communication realization

定义：

\[
x'
=
T_{c,\xi}(x),
\]

其中：

- \(c\)：communication condition；
- \(\xi\)：该次 communication realization 的随机因素。

本文不把：

\[
T_{c,\xi}
\]

假设为固定 group action，也不要求存在固定 group representation。

---

# 3. Communication-Induced Partial Temporal Transport

对 paired sample：

\[
p=(x,x'),
\]

设 source / target manipulation-output grid 长度分别为：

\[
N_p,
\qquad
M_p.
\]

通信 realization 在 source / target 时间网格之间诱导一个真实但通常不可直接获得的 temporal correspondence：

\[
W_p^\star
\in
\mathbb R_{\ge0}^{M_p\times N_p}.
\]

其语义固定为：

> **target 时间单元中的 manipulation provenance 应由哪些 source 时间单元 transport 而来。**

该 transport 允许表示：

```text
identity
global offset
global time scale
clock drift
local non-affine warp
local deletion
target unmatched / orphan region
```

因此：

\[
W_p^\star
\]

不要求是方阵，也不要求是 permutation。

对存在可信 correspondence 的 target rows，其 transport row 应具有归一化的对应语义；无法建立对应关系的 row 视为：

\[
\boxed{
\text{unavailable correspondence}
}
\]

而不是 manipulation score 0。

---

# 4. Operational Correspondence

真实训练中通常不可直接使用：

\[
W_p^\star.
\]

定义 operational correspondence：

\[
(x,x')
\longmapsto
(\hat W_p,\hat R_p),
\]

其中：

\[
\hat W_p
\in
\mathbb R_{\ge0}^{M_p\times N_p},
\]

\[
\hat R_p
\in
[0,1]^{M_p}.
\]

\(\hat R_{p,i}\) 表示第 \(i\) 个 target row 的 correspondence reliability。

算法原语只冻结以下信息边界：

\[
\boxed{
(\hat W_p,\hat R_p)
\text{ must be authenticity-label-agnostic}
}
\]

即构造 correspondence 时不得读取：

```text
fake / real labels
manipulation boundaries
Y
P_theta
detector confidence
```

本文将：

\[
\hat W_p
\]

称为：

> **operational correspondence estimate**

而不在未经独立验证前将其称为 ground-truth / correct correspondence。

只有在后续独立 correspondence-validity 验证通过后，\(\hat W_p\) 才可在方法与实验文档中作为 **trusted operational correspondence** 使用；该验证方式不属于本文。

具体如何获得：

\[
(\hat W_p,\hat R_p)
\]

不属于算法原语。

---

# 5. 第一核心原语：Communication-Transport Equivariance

定义 correspondence-valid target set：

\[
\mathcal I_p^{+}
=
\left\{
i:
\hat R_{p,i}>0,
\;
\sum_j\hat W_{p,ij}>0
\right\}.
\]

对任意点级 discrepancy：

\[
d:
[0,1]\times[0,1]
\rightarrow
\mathbb R_{\ge0},
\]

只有当：

\[
\mathcal I_p^{+}\neq\varnothing
\]

时，定义 pair-level transport discrepancy：

\[
D_\theta^{+}(p)
=
\frac{
\sum_{i\in\mathcal I_p^{+}}
\hat R_{p,i}
\,d
\left(
P_\theta(x')_i,
[\hat W_pP_\theta(x)]_i
\right)
}{
\sum_{i\in\mathcal I_p^{+}}
\hat R_{p,i}
}.
\]

若：

\[
\mathcal I_p^{+}=\varnothing,
\]

则 CEL transport-equivariance 对该 pair **not applicable**；不得将其记为 zero discrepancy。

CEL 的核心要求为：

\[
\boxed{
D_\theta^{+}(p)\downarrow
}
\]

即：

\[
\boxed{
P_\theta(x')
\sim
\hat W_pP_\theta(x)
}
\]

只在 correspondence-valid regions 上成立。

该关系的含义不是：

\[
\text{representation invariance},
\]

而是：

\[
\boxed{
\text{task-output covariance under sample-conditioned communication transport}
}
\]

这构成 CEL 的**第一且必要的算法原语**。

---

# 6. Correspondence Selectivity：强扩展原语

仅要求：

\[
D_\theta^{+}(p)\downarrow
\]

仍可能出现一种退化情况：模型输出对大量不同 correspondence 都几乎不敏感。

因此，在 correspondence 本身对 task output **可辨识**时，可以进一步要求 operational correspondence estimate 在通过独立有效性验证后，应比形式合法但显著不同的 alternatives 更能解释 target manipulation output。

该扩展称为：

\[
\boxed{
\text{Correspondence Selectivity}
}
\]

它是 CEL 的**强扩展原语**，而不是 CEL 基础定义成立的必要前提。

---

## 6.1 Admissible separated alternatives

定义与：

\[
\hat W_p
\]

具有相同基本结构约束的 admissible correspondence class：

\[
\mathfrak W_p,
\qquad
\hat W_p\in\mathfrak W_p.
\]

候选 alternative：

\[
W_p^{-}\in\mathfrak W_p
\]

必须保持：

```text
same matrix shape
same valid target support
same row-normalization semantics
same reliability weighting
same monotonicity / locality / slope class（若这些约束属于具体实现）
```

但不能仅仅是任意微小扰动。

定义 correspondence discrepancy：

\[
d_W:
\mathfrak W_p\times\mathfrak W_p
\rightarrow
\mathbb R_{\ge0}.
\]

只把满足：

\[
\boxed{
d_W(W_p^{-},\hat W_p)
\ge
\delta_W
}
\]

的 alternatives 视为 selectivity negatives，其中：

\[
\delta_W>0.
\]

因此 negative set 定义为：

\[
\mathcal N_p(\delta_W)
=
\left\{
W_p^{-}\in\mathfrak W_p:
d_W(W_p^{-},\hat W_p)\ge\delta_W
\right\}.
\]

若：

\[
\boxed{
\mathcal N_p(\delta_W)=\varnothing
}
\]

则 correspondence selectivity 对该 pair **not applicable**；该 pair 仍可用于基础 CEL，但不得定义 \(D_\theta^{-}(p)\) 或施加 selectivity margin。

negative generation 同样不得读取 authenticity labels 或 detector outputs。

---

## 6.2 Correspondence-informative condition

并非所有 pair / region 都能从 manipulation output 中区分 correspondence。

例如，当某一长区间的 manipulation field 为常数时，不同 transports 可能产生完全相同的 transported output。

因此 correspondence selectivity 只在 **correspondence-informative pair / region** 上定义。

为定义“correspondence 是否在任务语义上可辨识”，引入一个仅用于**原语语义定义**的 occupancy-field discrepancy：

\[
d_Y:
[0,1]^{M_p}\times[0,1]^{M_p}
\rightarrow
\mathbb R_{\ge0}.
\]

当且仅当：

\[
\mathcal N_p(\delta_W)\neq\varnothing
\]

时，定义真实 task-semantic separation：

\[
\boxed{
\operatorname{Sep}_p^\star
=
\inf_{
W_p^{-}\in\mathcal N_p(\delta_W)
}
d_Y
\left(
W_p^\star Y_x,
W_p^{-}Y_x
\right)
}
\]

其中 \(d_Y\) 只比较真实 transport 与该 alternative **共同具有 correspondence 的 target support**；unavailable / unmatched rows 不作为 occupancy 0 参与比较。

其含义是：

> 在与 operational correspondence 结构约束一致、且与其至少相隔 \(\delta_W\) 的 admissible alternatives 中，真实 communication transport 与 alternatives 对 source manipulation occupancy 所产生 target occupancy 的最小可辨识差异。

只当：

\[
\boxed{
\operatorname{Sep}_p^\star
\ge
\delta_Y
}
\]

时，pair \(p\) 才称为 **correspondence-informative**，其中：

\[
\delta_Y>0.
\]

该定义只规定 correspondence selectivity 的**任务语义适用域**。训练时如何近似判断 correspondence-informative pair / region，由 `02_方法实现机制设计` 决定；不得因此允许 correspondence estimator 读取 \(Y\)、fake boundary 或 detector output。

---

## 6.3 Selectivity discrepancy

对任意：

\[
W_p^{-}
\in
\mathcal N_p(\delta_W),
\]

定义：

\[
D_\theta
(
p;W_p^{-}
)
=
\frac{
\sum_{i\in\mathcal I_p^{+}}
\hat R_{p,i}
\,d
\left(
P_\theta(x')_i,
[W_p^{-}P_\theta(x)]_i
\right)
}{
\sum_{i\in\mathcal I_p^{+}}
\hat R_{p,i}
}.
\]

仅当：

\[
\mathcal N_p(\delta_W)\neq\varnothing
\]

时定义 hardest admissible alternative：

\[
D_\theta^{-}(p)
=
\min_{
W_p^{-}\in\mathcal N_p(\delta_W)
}
D_\theta
(
p;W_p^{-}
).
\]

在 correspondence-informative 且 negative set 非空的 pair 上，selectivity 要求：

\[
\boxed{
D_\theta^{-}(p)
-
D_\theta^{+}(p)
\ge
m
}
\]

其中：

\[
m>0.
\]

对应的抽象 margin term：

\[
\boxed{
\mathcal L_{\mathrm{sel}}(p)
=
\left[
m
+
D_\theta^{+}(p)
-
D_\theta^{-}(p)
\right]_+
}
\]

只在 correspondence-informative pair 上启用。

---

# 7. CEL 与 CS-CEL 的层级关系

本文明确区分：

## 7.1 基础原语：CEL

\[
\boxed{
P_\theta(x')
\sim
\hat W_pP_\theta(x)
}
\]

即：

> temporal manipulation output 对 sample-conditioned communication transport 保持 covariance / conditional equivariance。

---

## 7.2 强扩展：CS-CEL

在 CEL 基础上增加：

\[
\boxed{
D_\theta^{-}(p)
-
D_\theta^{+}(p)
\ge
m
}
\]

即：

> 在 correspondence-informative 条件下，independently validated operational correspondence estimate 比 admissible separated alternatives 更能解释 target manipulation field。

因此：

\[
\boxed{
\text{CS-CEL}
=
\text{CEL}
+
\text{Correspondence Selectivity}
}
\]

若后续研究证明 selectivity 没有独立价值，但 CEL 本身成立，则：

\[
\boxed{
\text{CEL remains a valid primitive}
}
\]

而不能为了保留 CS-CEL claim 反向修改算法原语。

---

# 8. Correspondence Selectivity 能解决什么

若：

\[
P_\theta(x)
=
c\mathbf 1,
\]

且 positive / alternative transports 在同一 valid support 上具有 row-normalized semantics，则：

\[
\hat W_pP_\theta(x)
=
W_p^{-}P_\theta(x)
=
c\mathbf 1.
\]

于是：

\[
D_\theta^{+}(p)
=
D_\theta^{-}(p).
\]

当：

\[
m>0
\]

时，selectivity margin 无法满足。

因此 correspondence selectivity 至少排除了：

\[
\boxed{
\text{constant-field equivariance collapse}
}
\]

本文**不声称**该机制排除所有可能的 shortcut / degenerate solutions。

---

# 9. 算法原语的允许实现自由度

以下内容可以在后续方法设计中改变，而不改变 CEL / CS-CEL：

```text
backbone
temporal localization head
correspondence estimator
reliability estimator
waveform / SSL / phoneme / ASR representation
hard / soft / probabilistic transport
point discrepancy d
correspondence discrepancy d_W
alternative-correspondence generator
supervised localization objective
optimization strategy
```

不同实现路线只要保持：

\[
\boxed{
(x,x')
\rightarrow
(\hat W_p,\hat R_p)
\rightarrow
P_\theta\text{-space transport equivariance}
}
\]

就仍然属于 CEL。

若进一步保持 correspondence selectivity：

\[
\boxed{
D_\theta^{-}(p)
-
D_\theta^{+}(p)
\ge
m
}
\]

则属于 CS-CEL。

---

# 10. 什么情况下已经偏离原语

## 10.1 删除 sample-conditioned correspondence

若核心关系变成：

\[
P_\theta(x')
\approx
P_\theta(x),
\]

而不再使用 sample-conditioned temporal correspondence，则不是 CEL。

---

## 10.2 只做 communication augmentation

若方法只对通信后的样本做监督训练，而不存在：

\[
P_\theta(x')
\sim
\hat W_pP_\theta(x),
\]

则不是 CEL。

---

## 10.3 只做 feature invariance / alignment

若核心机制只剩：

\[
h_\theta(x')
\approx
\operatorname{Align}(h_\theta(x)),
\]

而不再对 temporal manipulation output 施加 transport relation，则不是 CEL。

---

## 10.4 correspondence 使用 authenticity information

若：

\[
\hat W_p
\]

或：

\[
\hat R_p
\]

由 fake labels、fake boundaries、\(Y\)、\(P_\theta\) 或 detector confidence 辅助构造，则违反 CEL 的信息边界。

---

## 10.5 取消 selectivity

取消 correspondence selectivity 后：

- 仍可能是 CEL；
- 但不再属于 CS-CEL。

---

# 11. 原语级强对照

为判断算法原语是否具有独立必要性，至少需要概念上区分以下机制。

## 11.1 Identity / No-Transport Control

使用 strict identity correspondence：

\[
W_{\mathrm{id}}
\]

代替 sample-conditioned：

\[
\hat W_p.
\]

用于判断：

\[
\boxed{
\text{sample-conditioned transport 是否必要}
}
\]

---

## 11.2 Same-Physical-Transport Feature Control

在相同 correspondence information 下，仅在 feature space 施加 transport / alignment，而不在 manipulation output space 施加 CEL relation。

用于判断：

\[
\boxed{
\text{output-space transport 是否具有独立价值}
}
\]

---

## 11.3 Aligned-Supervision Control

利用同一 correspondence 对 source supervision 进行 target-grid transport：

\[
Y_x
\longmapsto
\hat W_pY_x,
\]

但不要求：

\[
P_\theta(x')
\sim
\hat W_pP_\theta(x).
\]

用于回答：

\[
\boxed{
\text{paired prediction transport 是否超出“对齐标签后监督训练”的价值}
}
\]

这是一项原语级必要性对照。

---

## 11.4 Separated-Alternative Correspondence Control

比较 independently validated operational correspondence estimate 与 admissible separated alternatives。

用于判断：

\[
\boxed{
\text{correspondence correctness / selectivity 是否具有机制价值}
}
\]

---

# 12. Primitive-Level Falsifiability

本文只冻结原语级证伪条件，不固定具体统计协议。

## F1：Task-Relevant Communication Transport Exists

真实 communication condition 必须在 task-relevant 时间区域产生不可忽略的 temporal correspondence variation。

若实际 communication 基本满足：

\[
W_p^\star
\approx
W_{\mathrm{id}},
\]

则 sample-conditioned transport 缺少足够必要性。

---

## F2：Manipulation Occupancy Is Transportable

在独立 reference correspondence 下，应在 correspondence-valid / transportable regions 上存在：

\[
Y_{x'}
\sim
W_p^\star Y_x
\]

的关系。

unavailable / unmatched regions 不被解释为 occupancy 0。若 manipulation occupancy 在 correspondence-valid regions 上仍不能被 communication correspondence 合理 transport，则 CEL 的基础语义 premise 被否定。

---

## F3：Operational Correspondence Is Recoverable

必须存在至少一种 authenticity-label-agnostic 技术路线，使：

\[
\hat W_p
\]

具有足够 correspondence fidelity。

若所有合理技术路线都无法得到可信 correspondence，则 CEL 缺少 operational feasibility。

---

## F4：Transport Is Necessary

使用 sample-conditioned：

\[
\hat W_p
\]

的 CEL 应提供超出 strict identity / no-transport 的价值。

否则 sample-conditioned transport 没有证明必要性。

---

## F5：Paired Output Transport Is Necessary

CEL 应提供超出 aligned-supervision control 的价值。

若：

\[
\hat W_pY_x
\]

直接监督已经可以完全替代 paired prediction transport，则：

\[
P_\theta(x')
\sim
\hat W_pP_\theta(x)
\]

缺少独立必要性。

---

## F6：Output-Space Transport Has Independent Value

在相同 physical correspondence information 下，CEL 应提供超出纯 feature-space transport / alignment 的价值。

否则不能强主张：

\[
\boxed{
\text{temporal manipulation output is the necessary action space}
}
\]

---

## F7：Correspondence Selectivity Has Independent Value

只有当 correspondence-informative pairs 存在时，CS-CEL 才要求 independently validated operational correspondence estimate 优于 admissible separated alternatives。

若 selectivity：

```text
不能稳定区分 trusted 与 separated alternatives
或
对 localization 没有独立收益
```

则 correspondence-selective extension 被否定。

此时允许保留 CEL，不允许继续强主张 CS-CEL。

---

# 13. 创新边界

已有研究已经覆盖：

```text
partial Deepfake localization
frame / segment localization
temporal self-consistency
temporal difference modeling
segment-aware localization
RTC robustness
paired clean / communication views
phoneme-guided consistency
soft temporal alignment
feature-level consistency
```

因此，上述内容均不能单独作为本文创新。

---

## 13.1 CEL 的核心创新候选

CEL 的创新限定为：

> **将真实通信后的局部 Deepfake 定位建模为 temporal manipulation output 对 sample-conditioned communication-induced temporal transport 的 covariance / conditional equivariance。**

核心关系：

\[
\boxed{
P_\theta(x')
\sim
\hat W_pP_\theta(x)
}
\]

创新重点在：

```text
task-output space
sample-conditioned transport
partial temporal correspondence
real communication setting
```

的组合，而不是 soft alignment 本身。

---

## 13.2 CS-CEL 的附加强创新

CS-CEL 进一步要求：

> **在 correspondence-informative 条件下，independently validated operational correspondence estimate 比同信息预算、显著分离的 admissible alternatives 更能解释 target manipulation field。**

核心关系：

\[
\boxed{
D_\theta^{-}(p)
-
D_\theta^{+}(p)
\ge
m
}
\]

这使 correspondence correctness 从事后消融变成可学习、可证伪的机制约束。

---

## 13.3 安全主张

本文不声称首次提出：

```text
equivariance
contrastive / ranking loss
negative correspondence
soft alignment
temporal consistency
partial localization
RTC robustness
```

安全表述为：

> **CEL applies sample-conditioned communication-induced temporal transport directly to the temporal manipulation output of partial speech deepfake localization. CS-CEL further introduces correspondence selectivity on correspondence-informative cases so that the trusted operational correspondence must explain the target manipulation field better than admissible separated alternatives.**

---

# 14. 与后续文档的接口

## 14.1 `02_方法实现机制设计`

负责在不改变本文原语的前提下确定：

```text
如何估计 W_hat / R_hat
如何定义 d / d_W
如何判断 correspondence-informative region
如何构造 separated alternatives
首选实现路线
A 失败后允许哪些 B / C 技术路线
backbone / temporal head
监督项与 CEL / CS-CEL 如何组合
```

02 可以改变技术路线，但不得修改本文冻结的数学语义。

---

## 14.2 `03_项目推进路线`

负责确定：

```text
代码构建顺序
数据 / reference construction
最小验证
阶段 PASS / FAIL
实验矩阵
统计协议
GPU / Colab 流程
结果文件
图表
论文结果包
```

03 负责执行，不重新定义算法。

---

# 15. 最终冻结核心

若最终采用基础 CEL，冻结核心为：

\[
\boxed{
T_{c,\xi}
\rightarrow
(\hat W_p,\hat R_p)
}
\]

以及：

\[
\boxed{
P_\theta(x')
\sim
\hat W_pP_\theta(x)
}
\]

即：

\[
\boxed{
\text{Communication-Transport Equivariance}
}
\]

若最终采用强扩展 CS-CEL，则额外冻结：

\[
\boxed{
D_\theta^{-}(p)
-
D_\theta^{+}(p)
\ge
m
}
\]

且该关系只对：

\[
\boxed{
\text{correspondence-informative pairs / regions}
}
\]

要求成立。

因此：

\[
\boxed{
\text{CEL}
=
\text{primary primitive}
}
\]

\[
\boxed{
\text{CS-CEL}
=
\text{CEL}
+
\text{Correspondence Selectivity}
}
\]

后续可以改变实现路线，但不得改变上述核心算法关系。

---

# 16. 冻结声明

本文件自此冻结为项目的算法原语文档。

后续允许改变：

```text
具体 correspondence estimator
reliability estimator
backbone / temporal head
hard / soft / probabilistic transport
d / d_W / d_Y 的具体实现
correspondence-informative 的 operational 判定方式
alternative-correspondence generator
supervised objective
A / B / C 技术路线
```

但这些变化必须在 `02_方法实现机制设计` 中完成，且不得改变本文冻结的核心语义。

后续实验流程、阶段门、统计协议、代码任务、GPU 执行与论文结果包只允许在 `03_项目推进路线` 中定义。

若后续实验否定 F1–F7 中任一原语级条件，应按证伪结果降级或放弃相应 claim，而不是反向修改本文来适配结果。

\[
\boxed{
\textbf{01 Algorithm Primitive: FINAL-FROZEN}
}
\]
