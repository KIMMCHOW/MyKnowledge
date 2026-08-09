---
type: research-note
title: Avellaneda–Stoikov（AS）库存型做市模型
aliases:
  - AS model
  - Avellaneda–Stoikov Model
tags:
  - 金融
  - 做市
  - 交易
  - 随机控制
domain: 经济
subdomain: 金融
topic: 做市
status: reviewed
updated: 2026-08-09
---

# Avellaneda–Stoikov（AS）库存型做市模型

> [!info] 导航
> 概念入口：[[Avellaneda–Stoikov模型]] · [[做市]] · [[流动性]]；专题入口：[[_索引_做市|做市研究索引]]。

> **这篇笔记做什么**：说明经典 Avellaneda–Stoikov（AS）模型如何在“赚取买卖价差”和“控制库存风险”之间选择 Bid / Ask 报价，并给出可实现、可校准、可审计的公式与工程边界。
>
> **定位**：它是库存型做市的基准模型和控制框架，不是可原样上线的完整生产策略。

## 1. 一页结论

AS 模型把做市拆成两步：

1. 根据当前库存计算**保留价格**（reservation price），即做市商自己的库存调整后估值；
2. 根据成交强度随报价距离的衰减，计算应围绕保留价格设置多宽的买卖价差。

令剩余时间为

$$
\tau = T-t.
$$

经典有限期限近似下，保留价格为

$$
r_t = S_t-q_t\gamma\sigma^2\tau.
$$

最优总报价宽度为

$$
\psi_t
=P_t^{a,*}-P_t^{b,*}
=\gamma\sigma^2\tau
+\frac{2}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right).
$$

因此

$$
P_t^{a,*}=r_t+\frac{\psi_t}{2},
$$

$$
P_t^{b,*}=r_t-\frac{\psi_t}{2}.
$$

直觉：

- 当 $q_t>0$（多头库存）时，$r_t<S_t$，两侧报价整体下移：Ask 更容易成交，Bid 更不容易继续买入；
- 当 $q_t<0$（空头库存）时，$r_t>S_t$，两侧报价整体上移：Bid 更容易成交，Ask 更不容易继续卖出；
- 模型不是简单地“库存多就只扩大价差”，而是先**平移报价中心**，再决定报价宽度。

## 2. 符号与买卖方向

| 符号 | 含义 | 约定或单位 |
|---|---|---|
| $S_t$ | 中间价 / 参考价格（mid-price） | 经典论文中是价格水平，不是 $\log S_t$ |
| $P_t^b$ | 做市商的 Bid 报价 | 买入限价 |
| $P_t^a$ | 做市商的 Ask 报价 | 卖出限价 |
| $\delta_t^b=S_t-P_t^b$ | Bid 距离 | 通常要求 $\delta_t^b\ge 0$ |
| $\delta_t^a=P_t^a-S_t$ | Ask 距离 | 通常要求 $\delta_t^a\ge 0$ |
| $X_t$ | 现金余额 | Bid 成交时减少，Ask 成交时增加 |
| $Q_t=q_t$ | 库存 | 正数为多头，负数为空头 |
| $\sigma$ | 中间价波动率 | 价格单位 / $\sqrt{\text{时间}}$ |
| $\gamma$ | CARA 风险厌恶系数 | 若价格以货币计，量纲通常为 $1/\text{货币}$ |
| $A$ | 基础成交强度 | 成交次数 / 时间 |
| $k$ 或 $\kappa$ | 成交强度对报价距离的敏感度 | $1/\text{价格单位}$ |
| $T$ | 策略期限或终端时刻 | 必须与 $\sigma,A$ 的时间尺度一致 |
| $\tau=T-t$ | 剩余期限 | 时间 |

这里的上标 $a$ / $b$ 指**做市商挂单的一侧**：

- Ask 被市场买单击中：做市商卖出一单位，$Q_t$ 减少；
- Bid 被市场卖单击中：做市商买入一单位，$Q_t$ 增加。

## 3. 经典模型假设

### 3.1 中间价

原始模型使用无漂移算术布朗运动：

$$
dS_t=\sigma\,dW_t.
$$

它表达的是：短期内做市商没有方向观点，价格风险主要通过库存暴露进入目标函数。原论文选算术而非几何布朗运动，还与指数效用的有界性处理有关。

### 3.2 报价

$$
P_t^b=S_t-\delta_t^b,
$$

$$
P_t^a=S_t+\delta_t^a.
$$

### 3.3 成交到达过程

Bid 和 Ask 的成交分别由点过程 $N_t^b,N_t^a$ 描述。经典对称指数形式是

$$
\lambda^b(\delta)=\lambda^a(\delta)=A e^{-k\delta}.
$$

报价离中间价越远，成交强度越低。$A$ 控制整体流量水平，$k$ 控制流量对价格距离的敏感程度。

> 指数成交强度是便于求解的结构化假设，不等于真实订单簿中的排队成交概率。真实成交还受队列位置、盘口深度、撤单、延迟和订单流毒性影响。

### 3.4 现金与库存跳变

每次成交一单位时：

$$
dQ_t=dN_t^b-dN_t^a,
$$

$$
dX_t=P_t^a\,dN_t^a-P_t^b\,dN_t^b.
$$

等价地：

| 事件 | 现金变化 | 库存变化 |
|---|---:|---:|
| Bid 成交（做市商买入） | $X\mapsto X-(S-\delta^b)$ | $q\mapsto q+1$ |
| Ask 成交（做市商卖出） | $X\mapsto X+(S+\delta^a)$ | $q\mapsto q-1$ |

这张表是检查 HJB 符号最可靠的方法。

## 4. 优化目标与价值函数

做市商最大化终端按中间价盯市财富的 CARA 指数效用：

$$
u(s,x,q,t)
=\sup_{\delta^a,\delta^b}
\mathbb{E}_{t,s,x,q}
\left[-e^{-\gamma(X_T+Q_TS_T)}\right].
$$

终端条件为

$$
u(s,x,q,T)=-e^{-\gamma(x+qs)}.
$$

指数效用使现金财富与报价决策较容易分离。常用变换是

$$
u(s,x,q,t)=-e^{-\gamma\left(x+\theta(s,q,t)\right)},
$$

其中

$$
\theta(s,q,T)=qs.
$$

## 5. HJB 方程

先保留现金和库存跳变，HJB 写成

$$
\begin{aligned}
0={}&u_t+\frac{1}{2}\sigma^2u_{ss} \\
&+\max_{\delta^b}
\lambda^b(\delta^b)
\left[
u\!\left(s,x-s+\delta^b,q+1,t\right)-u(s,x,q,t)
\right] \\
&+\max_{\delta^a}
\lambda^a(\delta^a)
\left[
u\!\left(s,x+s+\delta^a,q-1,t\right)-u(s,x,q,t)
\right].
\end{aligned}
$$

定义保留 Bid 和保留 Ask：

$$
r^b(s,q,t)=\theta(s,q+1,t)-\theta(s,q,t),
$$

$$
r^a(s,q,t)=\theta(s,q,t)-\theta(s,q-1,t).
$$

代入指数效用变换后，$\theta$ 满足

$$
\begin{aligned}
0={}&\theta_t
+\frac{1}{2}\sigma^2\theta_{ss}
-\frac{1}{2}\gamma\sigma^2\theta_s^2 \\
&+\max_{\delta^b}
\frac{\lambda^b(\delta^b)}{\gamma}
\left[
1-e^{\gamma(s-\delta^b-r^b)}
\right] \\
&+\max_{\delta^a}
\frac{\lambda^a(\delta^a)}{\gamma}
\left[
1-e^{-\gamma(s+\delta^a-r^a)}
\right].
\end{aligned}
$$

这条方程把两类风险放在同一个控制问题中：

- 扩散项表示持有库存时的价格风险；
- 跳跃项表示报价更激进可提高成交概率，但会牺牲单次成交边际；
- $q+1$ 必须对应 Bid 成交，$q-1$ 必须对应 Ask 成交。

## 6. 从 HJB 到常用闭式近似

### 6.1 冻结库存时的价值

若从 $t$ 到 $T$ 不再交易，只持有 $q$ 单位库存，则

$$
v(x,s,q,t)
=-e^{-\gamma(x+qs)}
e^{\frac{1}{2}\gamma^2q^2\sigma^2(T-t)}.
$$

由无差异定价可得冻结库存下的保留价格中心：

$$
r(s,q,t)=s-q\gamma\sigma^2(T-t).
$$

### 6.2 冻结库存与二次库存近似

冻结库存问题严格给出下面的 $\theta$；原论文再对主动做市问题中的 $\theta$ 关于库存 $q$ 做渐近展开，并对成交到达项做一阶近似，从而得到相同的报价中心。便于审计的二次库存形式是

$$
\theta(s,q,t)
\approx qs
-\frac{1}{2}\gamma q^2\sigma^2(T-t).
$$

注意这里是 $(T-t)$，不是 $(T-t)^2$。

这不是主动做市完整 HJB 的普遍精确闭式解；它是冻结库存解，也是经典有限期限报价近似背后的二次库存结构。

### 6.3 保留价格与最优宽度

令

$$
r_t=S_t-q_t\gamma\sigma^2\tau.
$$

在对称指数成交强度下，经典近似给出

$$
\psi_t
=\gamma\sigma^2\tau
+\frac{2}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right).
$$

将该宽度围绕 $r_t$ 对称放置：

$$
P_t^{a,*}
=S_t-q_t\gamma\sigma^2\tau
+\frac{1}{2}\gamma\sigma^2\tau
+\frac{1}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right),
$$

$$
P_t^{b,*}
=S_t-q_t\gamma\sigma^2\tau
-\frac{1}{2}\gamma\sigma^2\tau
-\frac{1}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right).
$$

相对中间价的两侧距离分别是

$$
\delta_t^{a,*}
=-q_t\gamma\sigma^2\tau
+\frac{\psi_t}{2},
$$

$$
\delta_t^{b,*}
=q_t\gamma\sigma^2\tau
+\frac{\psi_t}{2}.
$$

若极端库存导致某一侧 $\delta<0$，不能机械地在中间价内侧交叉报价；生产实现通常采用库存边界、单侧停报、最小报价距离或主动减仓规则。

## 7. 参数如何影响报价

| 参数变化 | 报价中心 | 报价宽度 | 主要含义 |
|---|---|---|---|
| $q$ 增加 | 向下移动 | 经典对称近似中总宽度不直接随 $q$ 变化 | 加快卖出、抑制继续买入 |
| $\sigma$ 增加 | 库存偏移增大 | 风险项增大 | 库存盯市风险更高 |
| $\tau$ 增加 | 库存偏移增大 | 风险项增大 | 库存暴露持续更久 |
| $\gamma$ 增加 | 对库存更敏感 | 风险项增大；流动性项也发生非线性变化 | 策略更厌恶库存风险 |
| $k$ 增加 | 不变 | 流动性加价项通常减小 | 成交强度随距离衰减更快 |
| $A$ 增加 | 不变 | 在该特殊闭式距离中消去 | 成交更频繁，但不代表 $A$ 对 P&L 和库存路径不重要 |

最后一行很重要：$A$ 在对称指数模型的闭式最优距离中会消去，但它仍直接影响成交频率、库存分布和 P&L 分布。

## 8. 参数校准

### 8.1 波动率 $\sigma$

在与策略一致的时间尺度上估计中间价变化：

$$
\widehat{\sigma}^2
=\frac{1}{\Delta t}
\operatorname{Var}(S_{t+\Delta t}-S_t).
$$

若 $t$ 以秒为单位，$\sigma$ 就必须使用“每平方根秒”的尺度；不能把年化波动率直接代入秒级模型。

### 8.2 成交强度 $A,k$

将报价距离分桶。对第 $j$ 个距离桶，以暴露时间估计成交强度：

$$
\widehat{\lambda}(\delta_j)
=\frac{\text{该距离桶内的成交次数}}
{\text{该距离桶内的有效挂单时间}}.
$$

再拟合

$$
\ln \widehat{\lambda}(\delta_j)
=\ln A-k\delta_j.
$$

实务上至少要分 Bid / Ask、时段、波动状态和流动性状态；还要明确“成交”是否考虑自己的队列位置。2025 年的遍历型扩展把 $k$ 记作 $\kappa$，并研究了如何依据成交 / 未成交 Bernoulli 信号在线更新该参数。

### 8.3 风险厌恶系数 $\gamma$

$\gamma$ 不是纯粹从市场中观测到的参数，而是策略的风险政策参数。应通过以下约束反推和回测：

- 库存均值、标准差和尾部分位数；
- 最大持仓与库存停留时间；
- P&L 波动、回撤和尾部损失；
- 单侧成交后回到中性库存的速度；
- 在不同波动和订单流状态下的稳定性。

## 9. 可实现的报价循环

```text
每个报价周期：
1. 读取有效的参考价 S、库存 q、时间 t 和市场状态。
2. 用同一时间单位更新 sigma、A、k，并设置 tau = T - t。
3. 计算保留价格 r = S - q * gamma * sigma^2 * tau。
4. 计算理论宽度 psi。
5. 得到连续价格 ask_raw = r + psi/2，bid_raw = r - psi/2。
6. 加入手续费、返佣、最小边际、波动缓冲和 adverse-selection 缓冲。
7. Ask 向上取整到 tick，Bid 向下取整到 tick；检查 bid < ask。
8. 若 q >= q_max，停止或显著削弱 Bid；若 q <= q_min，停止或削弱 Ask。
9. 依据队列位置、最短挂单时间和撤单限频决定是否 cancel/replace。
10. 记录成交、未成交暴露、markout、库存和 P&L，供下一轮校准。
```

报价价格与报价数量是两个不同控制维度。2018 年的实现资料在 AS 定价外叠加了动态订单数量控制；这个思路适合工程扩展，但不是原始闭式公式的一部分。

## 10. 上线前必须补齐的风险控制

- **库存硬边界**：$q_{\min}\le q_t\le q_{\max}$，触边时停报增加风险的一侧；
- **参考价失效保护**：行情陈旧、盘口异常或价差交叉时立即撤单；
- **最大损失与 kill switch**：日内亏损、异常成交率、延迟或连接状态触发停机；
- **价格粒度与队列**：tick rounding、price-time priority、订单规模与部分成交；
- **成本**：maker rebate、taker fee、清算和对冲成本；
- **逆向选择**：成交后短周期 markout、订单流不平衡和毒性流量；
- **多场所与自成交保护**：跨场所库存汇总、重复报价和 self-trade prevention；
- **收盘与隔夜风险**：终端库存不能假设总能无成本按 $S_T$ 清算。

## 11. 模型局限与扩展层次

### 11.1 经典 AS 没有建模的内容

- 漂移、短期 alpha、跳跃和随机波动率；
- tick size、盘口档位、队列优先级和部分成交；
- 延迟、撤单失败和 stale quotes；
- 成交之间的相关性、订单流自激和不对称强度；
- 交易费用、返佣、市场冲击和主动对冲；
- 多资产相关风险与跨品种库存净额；
- 信息不对称与成交后的价格漂移。

因此，AS 更适合作为以下对象之一：

1. 库存 skew 的理论基线；
2. 仿真器中的基准策略；
3. 生产策略的一个报价中心 / 风险模块；
4. 检验更复杂模型是否真正带来增量的对照组。

### 11.2 三份资料对应的层次

| 资料 | 层次 | 本笔记如何使用 |
|---|---|---|
| Avellaneda & Stoikov (2008) | 经典有限期限模型 | 作为定义、HJB、保留价格和价差近似的公式基准 |
| Fushimi, González Rojas & Herman (2018) | 实现与仿真案例 | 补充动态订单数量、仿真和库存管理思路；正文自身存在若干符号不一致，不作为原始公式的权威来源 |
| Cao, Šiška, Szpruch & Treetanthiploet (2025/2026) | 遍历控制与在线学习扩展 | 补充库存边界、运行期库存惩罚、在线学习 $\kappa$ 与 regret 分析；其目标函数和风险参数不能与经典 AS 直接混用 |

遍历型（ergodic）扩展与经典有限期限模型不是同一个目标：

- 经典模型关注固定 $T$ 的终端效用；
- 遍历模型关注长期平均收益，并持续惩罚库存；
- 后者允许策略在运行中用正则化极大似然估计更新未知 $\kappa$，论文给出的期望 regret 上界为 $O((\ln T)^2)$。

## 12. 常见错误与审计清单

### 12.1 公式错误

- [ ] 经典原论文中的 $S_t$ 写成价格水平，而不是误写成 $\log S_t$；
- [ ] Bid 成交使用 $q+1$、现金 $x-s+\delta^b$；
- [ ] Ask 成交使用 $q-1$、现金 $x+s+\delta^a$；
- [ ] 指数成交强度写作 $Ae^{-k\delta}$，负号没有丢失；
- [ ] 保留价格写作 $S-q\gamma\sigma^2(T-t)$；
- [ ] 库存风险项使用 $(T-t)$，没有误写成 $(T-t)^2$；
- [ ] $\delta^a,\delta^b$ 是相对中间价的距离，不是最终报价；
- [ ] 闭式报价标明是渐近 / 一阶近似，不冒充完整 HJB 的普遍精确解。

### 12.2 工程错误

- [ ] $\sigma,A,k,T-t$ 的时间单位一致；
- [ ] $\delta$ 与 $k$ 的价格单位一致（货币、tick 或 bps 不可混用）；
- [ ] 取整后仍满足 $P^b<P^a$；
- [ ] 成交概率使用 $1-e^{-\lambda\Delta t}$，而不是在较大步长下直接把 $\lambda\Delta t$ 当成任意范围的概率；
- [ ] 回测包含队列、部分成交、费用、延迟和撤单；
- [ ] 对不同市场状态做样本外验证，防止 $A,k,\sigma$ 过期。

## 13. 公式排版约定

为保证 Obsidian、GitHub 和常见 Markdown 渲染器中的可读性：

- 每条独立公式使用独立的 `$$ ... $$`；
- 多行推导使用 `aligned` 并以 `\\` 显式换行；
- 不依靠数学块中的空行换行，因为 LaTeX 会忽略这些空行；
- 较长公式按等号或加号拆行，避免横向溢出。

## 14. 参考资料

1. Marco Avellaneda & Sasha Stoikov, *High-frequency trading in a limit order book*, Quantitative Finance 8(3), 217–224, 2008. [DOI](https://doi.org/10.1080/14697680701381228) · [作者公开稿](https://math.nyu.edu/inmemoriam/avellaneda/HighFrequencyTrading.pdf)
2. Takahiro Fushimi, Christian González Rojas & Molly Herman, *Optimal High-Frequency Market Making*, Stanford course project, 2018. [PDF](https://web.stanford.edu/class/msande448/2018/Final/Reports/gr5.pdf)
3. Jialun Cao, David Šiška, Lukasz Szpruch & Tanut Treetanthiploet, *Logarithmic regret in the ergodic Avellaneda–Stoikov market making model*, arXiv:2409.02025，2024，2025 修订；后被 SIAM Journal on Financial Mathematics 接收。 [arXiv](https://arxiv.org/abs/2409.02025)

---

**可移植性说明**：本笔记只使用标准 Markdown、Markdown 表格、代码块、外部链接和 LaTeX 数学块；不依赖 Obsidian wikilink、Dataview 或本仓库附件路径，可以单独复制到其他仓库。
