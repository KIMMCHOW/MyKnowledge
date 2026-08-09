---
type: research-note
title: AS Model（Avellaneda–Stoikov）研究资料
aliases:
  - Avellaneda–Stoikov Model
  - AS 做市模型
tags:
  - 金融
  - 做市
  - 交易
  - 市场微观结构
  - 随机控制
domain: 经济
subdomain: 金融
topic: 做市
status: reference
source_type: primary-research
---

# AS Model（Avellaneda–Stoikov）研究资料

> [!info] 导航
> 概念入口：[[Avellaneda–Stoikov模型]] · [[做市]] · [[流动性]]；专题入口：[[Knowledge/Notes/Finance/Market Making/_索引_做市|做市研究索引]]。

> [!abstract] 这篇笔记是做什么的
> 这是一份可独立复制的“单资产、库存感知做市”理论与实施速查。它解释 Avellaneda–Stoikov（AS）模型如何在**赚取买卖价差**与**控制库存价格风险**之间求解最优 bid/ask，并明确区分原始论文中的有限期限近似、精确 HJB 问题，以及 Guéant–Lehalle–Fernandez-Tapia（GLFT）的有限期限严格解与长时稳态近似。

> [!warning] 使用边界
> AS 是教学基线与报价骨架，不是可直接上线的完整生产策略。原模型没有显式建模 tick、队列优先级、延迟、手续费、部分成交、盘口状态、订单流聚集、alpha、逆向选择、多资产相关性及对冲成本。

## 1. 一句话直觉

做市商以限价单同时提供 bid 和 ask：报价离中间价越近，越容易成交，但每次赚取的价差越少；报价离得越远，单次毛利更高，但成交率下降。库存又带来方向风险。因此，AS 模型把报价拆成两个部分：

1. 用**保留价格（reservation price / indifference price）**根据库存平移报价中心；
2. 用**最优点差（optimal spread）**权衡成交概率、风险厌恶和价格波动。

如果库存为正（long inventory），模型下调报价中心：ask 更容易成交、bid 更不容易成交，从而推动库存回到零；库存为负时则相反。[原始论文，第 2.2、3.2 节](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

## 2. 原始资料与版本边界

| 资料 | 本笔记中的用途 |
|---|---|
| Marco Avellaneda & Sasha Stoikov, *High-frequency trading in a limit order book*, 2008；[作者托管全文](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)，[DOI/出版页](https://doi.org/10.1080/14697680701381228) | 原始 AS 状态、目标、HJB、到达强度与有限期限近似 |
| Olivier Guéant, Charles-Albert Lehalle & Joaquin Fernandez-Tapia, *Dealing with the Inventory Risk*, 2011/2013；[arXiv 摘要](https://arxiv.org/abs/1105.3115)，[全文 PDF](https://arxiv.org/pdf/1105.3115) | 加入硬库存上限，严格求解有限期限问题，并给出真正的长时极限及谱近似 |
| Olivier Guéant, *Optimal market making*, 2016；[arXiv 摘要与全文](https://arxiv.org/abs/1605.01862) | 一般强度、多资产扩展以及模型适用边界 |

> [!important] 不要混写三个不同对象
> - 原始 AS 第 2.3 节的 “infinite horizon” 是**冻结库存、不主动做市**时的折现效用保留价。
> - 原始 AS 第 3.2 节常见的含 $T-t$ 公式，是对库存与订单到达项做近似后得到的**有限期限近似**。
> - GLFT 在硬库存边界下证明的 $T\to\infty$ 极限，才是主动做市问题的**长时/稳态（ergodic-like）报价**。

### 2.1 当前目录内三份 PDF 的定位

| 本地文件 | 性质 | 应该怎样使用 |
|---|---|---|
| [[References/High-frequency trading in a limit order book.pdf|High-frequency trading in a limit order book]] | Avellaneda–Stoikov 的 2006 年作者预印本，共 14 页；内容后来发表于 2008 年 *Quantitative Finance* | **基础公式的首要依据**。本地版的式号主要是 (2.1)–(3.18)，与 2008 出版版内容基本一致，但分页和式号不同 |
| [[References/Optimal High-Frequency Market Making .pdf|Optimal High-Frequency Market Making]] | Takahiro Fushimi、Christian González Rojas、Molly Herman 的 2018 年 Stanford 项目报告 | **二手实施案例**：可参考模拟器、动态订单量和实证实验，不可作为 AS 公式权威；其正文存在库存符号、现金跳变和 ask 成交库存方向不一致的问题 |
| [[References/LOGARITHMIC REGRET IN THE ERGODIC  AVELLANEDA–STOIKOV MARKET MAKING MODEL.pdf|Logarithmic Regret in the Ergodic AS Model]] | Cao、Šiška、Szpruch、Treetanthiploet 的 2025 年研究预印本，[arXiv:2409.02025](https://arxiv.org/abs/2409.02025) | **在线学习扩展**：研究 ergodic 平均收益目标下在线估计价格敏感度 $\kappa$ 的 regret；它改用了长期平均盯市收益减二次库存惩罚，不是原始 AS 的 CARA 有限期限模型 |

第三篇 ergodic 论文适合回答“未知成交敏感度怎样边交易边学习”，但不能拿它的 $\kappa$、风险惩罚 $\phi$ 或长期平均目标直接替换原始 AS 的 $k$、$\gamma$ 和终端效用，然后仍声称是同一个模型。

## 3. 符号与单位

| 符号 | 含义 | 典型单位 |
|---|---|---|
| $S_t$，$s$ | 时刻 $t$ 的中间价或参考价 | price |
| $p_t^b$，$p_t^a$ | 做市商 bid / ask 报价 | price |
| $\delta_t^b=S_t-p_t^b$ | bid 到中间价的距离 | price |
| $\delta_t^a=p_t^a-S_t$ | ask 到中间价的距离 | price |
| $X_t$ | 现金账户 | currency |
| $q_t$ | 有符号库存；正数为多头、负数为空头 | model lots |
| $N_t^b$ | 做市商的 bid 被打到、买入的累计次数 | count |
| $N_t^a$ | 做市商的 ask 被吃掉、卖出的累计次数 | count |
| $\sigma$ | 参考价波动率 | price$/\sqrt{\text{time}}$ |
| $\gamma>0$ | CARA 绝对风险厌恶系数 | $1/$currency |
| $A>0$ | 当 $\delta=0$ 时外推的基准成交强度 | $1/$time |
| $k>0$ | 成交强度对报价距离的指数衰减斜率 | $1/$price |
| $T$ | 风险或清算期限 | time |
| $\tau=T-t$ | 剩余期限 | time |
| $Q$ | GLFT 模型中的库存硬上限 | model lots |

> [!note] $s$ 不是 $\log S_t$
> 原始 AS 主模型使用算术布朗运动，状态中的 $s$ 就是原始中间价 $S_t$。论文附录才讨论几何布朗运动的替代版本。[原始论文，第 2.1 节与附录](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

## 4. 模型假设

### 4.1 参考价过程

原始模型假设做市商对 drift 和自相关没有观点：

$$
dS_t=\sigma\,dW_t.
$$

这是零漂移算术布朗运动。$S_t$ 用于衡量库存的盯市价值，但模型并不假定做市商能无成本地在该价格成交。[原始论文，第 2.1 节，式 (1)](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

### 4.2 报价与成交

做市商持续提交：

$$
p_t^b=S_t-\delta_t^b,
\qquad
p_t^a=S_t+\delta_t^a.
$$

ask 被市场买单吃掉时，做市商卖出；bid 被市场卖单打到时，做市商买入。在单位成交量设定下：

$$
dq_t=dN_t^b-dN_t^a,
$$

$$
dX_t=(S_t+\delta_t^a)dN_t^a-(S_t-\delta_t^b)dN_t^b.
$$

原始论文将 $N^a$、$N^b$ 建模为 Poisson 点过程，并假设它们与价格布朗运动独立。[原始论文，第 2.4 节](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

### 4.3 成交到达强度

一般情形下，成交强度是报价距离的递减函数：

$$
\lambda^a=\lambda^a(\delta^a),
\qquad
\lambda^b=\lambda^b(\delta^b),
\qquad
\frac{d\lambda}{d\delta}<0.
$$

原始论文使用的对称指数特例是：

$$
\lambda^a(\delta)=\lambda^b(\delta)=A e^{-k\delta}.
$$

$A=\lambda(0)$ 是将报价放在参考价处时的**外推基准强度**，不能解释成“价内成交率”；$k$ 表示报价每远离参考价一个价格单位，强度下降的速度。原论文从市场单频率、单量分布和暂时价格冲击出发说明了指数或幂律形状的经验动机。[原始论文，第 2.5 节，式 (9)–(12)](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

## 5. 优化目标与边界条件

做市商选择可预测的报价距离过程 $\delta^a,\delta^b$，最大化终端现金与库存盯市价值的 CARA 效用：

$$
u(s,x,q,t)
=sup_{\delta^a,\delta^b}
\mathbb{E}_t\!\left[
-\exp\!\left(-\gamma(X_T+q_T S_T)\right)
\right].
$$

终端条件是：

$$
u(s,x,q,T)=-\exp\!\left[-\gamma(x+qs)\right].
$$

因此，目标不是只优化 $X_T$；它明确包含 $q_T S_T$。这也隐含了终端库存能够按中间价无摩擦盯市或清算。[原始论文，第 2.4、3.1 节，式 (13) 与 HJB 终端条件](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

若实际系统存在清仓费用或残余库存惩罚 $\ell(q)$，应改为：

$$
u(s,x,q,T)=-\exp\!\left[-\gamma\bigl(x+qs-\ell(q)\bigr)\right].
$$

这属于对原模型的工程扩展，不能仍称为原始边界条件。

## 6. HJB 方程

### 6.1 原始价值函数形式

对 $u=u(s,x,q,t)$，动态规划给出：

$$
\begin{aligned}
0={}&u_t+\frac{1}{2}\sigma^2u_{ss} \\
&+\sup_{\delta^b}\lambda^b(\delta^b)
\left[
u(s,x-s+\delta^b,q+1,t)-u(s,x,q,t)
\right] \\
&+\sup_{\delta^a}\lambda^a(\delta^a)
\left[
u(s,x+s+\delta^a,q-1,t)-u(s,x,q,t)
\right].
\end{aligned}
$$

每个跳跃项必须同时反映现金和库存变化：bid 成交使现金减少 $s-\delta^b$、库存增加 1；ask 成交使现金增加 $s+\delta^a$、库存减少 1。[原始论文，第 3.1 节](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

### 6.2 降维后的 $\theta$ 形式

令：

$$
u(s,x,q,t)
=-\exp(-\gamma x)\exp\!\left[-\gamma\theta(s,q,t)\right].
$$

定义库存变化一单位时的保留 bid / ask：

$$
r^b(s,q,t)=\theta(s,q+1,t)-\theta(s,q,t),
$$

$$
r^a(s,q,t)=\theta(s,q,t)-\theta(s,q-1,t).
$$

则：

$$
\begin{aligned}
0={}&\theta_t+\frac{1}{2}\sigma^2\theta_{ss}
-\frac{1}{2}\gamma\sigma^2\theta_s^2 \\
&+\sup_{\delta^b}
\frac{\lambda^b(\delta^b)}{\gamma}
\left[1-e^{\gamma(s-\delta^b-r^b)}\right] \\
&+\sup_{\delta^a}
\frac{\lambda^a(\delta^a)}{\gamma}
\left[1-e^{-\gamma(s+\delta^a-r^a)}\right],
\end{aligned}
$$

$$
\theta(s,q,T)=qs.
$$

注意指数中的符号、$r^a/r^b$、$q\pm1$ 和 $\delta^a/\delta^b$ 不能互换，也不能把 $\theta(q-1)$ 与 $\theta(q)$ 误写成相加。[原始论文，第 3.1 节，式 (14)–(17)](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

## 7. 一般强度下的最优性条件

对可微且递减的成交强度，最优报价距离满足隐式条件：

$$
s-r^b
=\delta^b
-\frac{1}{\gamma}
\ln\!\left(
1-\gamma\frac{\lambda^b(\delta^b)}{(\lambda^b)'(\delta^b)}
\right),
$$

$$
r^a-s
=\delta^a
-\frac{1}{\gamma}
\ln\!\left(
1-\gamma\frac{\lambda^a(\delta^a)}{(\lambda^a)'(\delta^a)}
\right).
$$

因此模型的求解流程是：先解 HJB 得到 $r^a,r^b$，再把主观保留价与市场成交强度曲线结合，求得可执行的最优报价。[原始论文，第 3.1 节，式 (18)–(19)](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

对于指数强度，定义单侧流动性项：

$$
c_0=\frac{1}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right).
$$

这时：

$$
\delta^{b*}=s-r^b+c_0,
\qquad
\delta^{a*}=r^a-s+c_0.
$$

## 8. 冻结库存保留价

如果做市商从时刻 $t$ 到 $T$ 不再交易，只持有库存 $q$，则保留 bid / ask 为：

$$
r^a(s,q,t)
=s+\frac{1-2q}{2}\gamma\sigma^2(T-t),
$$

$$
r^b(s,q,t)
=s-\frac{1+2q}{2}\gamma\sigma^2(T-t).
$$

两者的平均值是中央保留价格：

$$
r(s,q,t)
=\frac{r^a+r^b}{2}
=s-q\gamma\sigma^2(T-t).
$$

若 $q>0$，$r<s$；若 $q<0$，$r>s$。这是库存 skew 的核心方向。[原始论文，第 2.2 节，式 (3)–(8)](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

> [!warning] 不要使用错误的 $\theta$ 闭式
> 冻结库存情形对应
> $$
> \theta_{\mathrm{frozen}}(s,q,t)
> =qs-\frac{\gamma}{2}q^2\sigma^2(T-t).
> $$
> 只有一次 $(T-t)$，外面没有额外的 $-\gamma$。主动做市的 $\theta$ 一般没有这种简单精确闭式。

## 9. 原始 AS 的有限期限常用近似

原始论文在指数强度下，对 $\theta$ 作库存展开，并对订单到达项作一阶近似，得到：[原始论文，第 3.2 节，式 (20)–(30)](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

### 9.1 报价中心

令 $\tau=T-t$：

$$
r_t=S_t-q_t\gamma\sigma^2\tau.
$$

### 9.2 总报价点差

$$
\psi_t
=\delta_t^{a*}+\delta_t^{b*}
=\gamma\sigma^2\tau
+\frac{2}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right).
$$

### 9.3 最优 bid / ask

$$
p_t^{b*}=r_t-\frac{\psi_t}{2},
$$

$$
p_t^{a*}=r_t+\frac{\psi_t}{2}.
$$

等价地，相对中间价的距离为：

$$
\delta_t^{b*}
=c_0+\frac{1+2q_t}{2}\gamma\sigma^2\tau,
$$

$$
\delta_t^{a*}
=c_0+\frac{1-2q_t}{2}\gamma\sigma^2\tau.
$$

方向检查：当 $q_t>0$ 时，bid 距离变大、ask 距离变小，报价整体下移；当 $q_t<0$ 时相反。

> [!danger] 这不是一般有限期限精确解
> GLFT 指出，上述 AS 近似可理解为最优报价在 $t$ 接近 $T$ 时的 Taylor 展开；远离终点时，真实最优报价很快接近与时间几乎无关的长时形状。因此，不应把含 $T-t$ 的公式标为“精确解”或“ergodic 解”。[GLFT，第 4 节前的脚注 8 与图 1–3](https://arxiv.org/pdf/1105.3115)

## 10. GLFT：有库存上限的有限期限严格解

GLFT 加入库存边界：

$$
q\in\{-Q,-Q+1,\ldots,Q\}.
$$

当 $q=Q$ 时停止挂 bid；当 $q=-Q$ 时停止挂 ask。这既符合风险限额，也使 verification argument 成立。[GLFT，第 2–3 节](https://arxiv.org/pdf/1105.3115)

定义：

$$
\alpha=\frac{k\gamma\sigma^2}{2},
$$

$$
\eta
=A\left(1+\frac{\gamma}{k}\right)^{-\left(1+\frac{k}{\gamma}\right)}.
$$

对 $|q|<Q$，正函数 $v_q(t)$ 满足三对角线性 ODE：

$$
\dot v_q(t)
=\alpha q^2 v_q(t)
-\eta\bigl(v_{q-1}(t)+v_{q+1}(t)\bigr),
$$

$$
v_q(T)=1.
$$

在边界 $q=\pm Q$ 时只保留指向库存区间内部的相邻项。若 $M$ 的对角元为 $\alpha q^2$、相邻非对角元为 $-\eta$，则：

$$
\boldsymbol v(t)
=e^{-M(T-t)}\boldsymbol 1.
$$

有限期限最优距离为：

$$
\delta_t^{b*}(q)
=c_0+\frac{1}{k}\ln\!\frac{v_q(t)}{v_{q+1}(t)},
\qquad q<Q,
$$

$$
\delta_t^{a*}(q)
=c_0+\frac{1}{k}\ln\!\frac{v_q(t)}{v_{q-1}(t)},
\qquad q>-Q.
$$

这提供了一个可数值实现、带硬库存限额的有限期限解；它会依赖 $A$，而原始 AS 的简单有限期限近似中 $A$ 消失。[GLFT，Proposition 1–2 与 Theorem 1](https://arxiv.org/pdf/1105.3115)

## 11. GLFT：真正的长时/稳态近似

当起点远离终点、等价地考察 $T\to\infty$ 的极限时，$M$ 的最小特征值对应正特征向量 $f^0$，精确长时距离为：

$$
\delta_\infty^{b*}(q)
=c_0+\frac{1}{k}\ln\!\frac{f_q^0}{f_{q+1}^0},
$$

$$
\delta_\infty^{a*}(q)
=c_0+\frac{1}{k}\ln\!\frac{f_q^0}{f_{q-1}^0}.
$$

这是带硬库存上限下由 GLFT 证明的长时极限，而不是原始 AS 的 $T-t$ 公式。[GLFT，Theorem 2](https://arxiv.org/pdf/1105.3115)

进一步用连续 Gaussian 谱近似，定义：

$$
C
=\sqrt{
\frac{\sigma^2\gamma}{2kA}
\left(1+\frac{\gamma}{k}\right)^{1+\frac{k}{\gamma}}
}.
$$

则：

$$
\delta_\infty^{b*}(q)
\approx c_0+\frac{2q+1}{2}C,
$$

$$
\delta_\infty^{a*}(q)
\approx c_0-\frac{2q-1}{2}C.
$$

因此稳态报价中心与总点差近似为：

$$
r_\infty(q)\approx s-qC,
$$

$$
\psi_\infty(q)
\approx 2c_0+C.
$$

这些是 **GLFT 谱近似**，不是 2008 年原论文的公式。[GLFT，第 4 节，Proposition 3 后的近似](https://arxiv.org/pdf/1105.3115)

## 12. 参数含义与比较静态

### $q$：库存

- $q>0$：报价中心下移，鼓励卖出、抑制继续买入；
- $q<0$：报价中心上移，鼓励买入、抑制继续卖出；
- 实施时通常使用相对目标库存 $q-q^\star$，但这是工程扩展。

### $\gamma$：风险厌恶

- $\gamma$ 越大，库存 skew 和有限期限风险点差通常越强；
- 它不是直接从价格序列统计得到的市场参数，而是风险预算旋钮；
- 可按允许的库存分布、PnL 方差、回撤或库存 VaR 反向调参。

### $\sigma$：价格风险

- $\sigma$ 越大，持有库存的风险越高；
- 必须保证 $\sigma$ 的采样尺度与 $T,t,A$ 的时间单位完全一致；
- 在存在 intraday seasonality 时，不宜只用全天单一常数。

### $A,k$：流动性与成交衰减

- $A$ 控制基准成交频率；
- $k$ 越大，成交强度随报价距离衰减越快；
- 指数强度下可拟合

$$
\log\lambda(\delta)=\log A-k\delta.
$$

### $T$：风险期限

- $T$ 不必机械等同于交易日收盘；它可以是风险重置或计划清仓的期限；
- 当 $\tau\to0$ 时，原始 AS 近似中的库存风险项消失，但流动性项 $2c_0$ 不消失；
- 若市场没有自然终点，应优先考虑 GLFT 稳态框架或滚动期限，并显式说明选择。

## 13. 数据校准方案

### 13.1 波动率 $\sigma$

1. 选择与报价刷新一致的时间单位；
2. 对中间价增量估计局部实现方差；
3. 过滤明显的坏价、停牌和数据断层；
4. 对日内时段、波动率状态分别估计，避免常数 $\sigma$ 掩盖 regime change。

### 13.2 强度 $A,k$

对报价距离分桶。设第 $j$ 桶的可成交暴露时间为 $E_j$，被动成交次数为 $n_j$，则：

$$
\widehat\lambda_j=\frac{n_j}{E_j}.
$$

再对：

$$
\log\widehat\lambda_j
=\log A-k\delta_j
$$

做 Poisson 回归或带权线性拟合。实际应至少按 bid/ask、时段、当前市场 spread、波动状态和订单量分层。GLFT 的实证讨论也指出，$\sigma,A,k$ 可从逐笔 LOB 数据校准，而 $\gamma$ 需要由策略设计者选择；$A,k$ 至少会随实际 bid-ask spread 变化。[GLFT，第 7 节](https://arxiv.org/pdf/1105.3115)

> [!warning] 成交强度不是简单的“挂单后成交次数”
> 必须使用暴露时间，并处理撤单、改价、盘口穿越和队列位置；否则 $A,k$ 会混入策略自身的挂单选择偏差。

## 14. 单步报价算法

以下是原始有限期限近似的最小实现流程：

1. 统一 $\sigma,A,T,t$ 的时间单位，并把库存转换为模型 lot；
2. 计算 $\tau=T-t$；
3. 计算保留价格

$$
r_t=S_t-q_t\gamma\sigma^2\tau;
$$

4. 计算总点差

$$
\psi_t
=\gamma\sigma^2\tau
+\frac{2}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right);
$$

5. 生成连续报价

$$
p_t^{b*}=r_t-\frac{\psi_t}{2},
\qquad
p_t^{a*}=r_t+\frac{\psi_t}{2};
$$

6. 加上 tick rounding、手续费/返佣保护、最小和最大点差、价格带、库存硬限额；
7. 只有当新报价变化足以抵消丢失队列优先级的成本时才撤改单；
8. 记录每次报价的状态、预测强度、成交与 markout，持续重估 $A,k,\sigma$。

### 三个最小方向测试

| 场景 | 必须出现的行为 |
|---|---|
| $q=0$ | 报价关于 $S_t$ 对称 |
| $q>0$ | bid 与 ask 整体下移；ask 更积极，bid 更保守 |
| $q<0$ | bid 与 ask 整体上移；bid 更积极，ask 更保守 |

## 15. 工程边界条件

### 15.1 库存硬限额

$$
q=Q\Rightarrow\text{不再挂 bid},
$$

$$
q=-Q\Rightarrow\text{不再挂 ask}.
$$

这不是简单扩大 skew 能完全替代的约束。

### 15.2 Tick 与队列

连续最优价必须离散到 tick。若简单四舍五入，可能造成 bid/ask 不对称、交叉报价或频繁抖动。应制定 side-aware rounding、最小点差与不交叉约束。GLFT 明确提醒，频繁改价会丢失队列优先级；Guéant 进一步指出，离散价格以及 LOB 的队列、优先级和挂单量是将 AS 类模型用于股票市场时的重要缺口。[GLFT，第 7 节](https://arxiv.org/pdf/1105.3115)；[Guéant 2016，第 1 节](https://arxiv.org/abs/1605.01862)

### 15.3 费用和最小经济点差

若单边费率、返佣和预期逆向选择损失合计为 $c$，报价点差必须至少覆盖它们。原始 AS 目标没有这些成本，因此生产实现需显式加入，而不是只在最后随意扩大点差。

### 15.4 终端库存

原始模型在 $T$ 按 $S_T$ 盯市，不会自动产生真实的清仓冲击。如果策略必须在收盘前归零，应使用终端库存惩罚、强制减仓或包含市价清仓成本的边界条件。

## 16. 模型局限

### 原始假设中没有的内容

- drift、短期 alpha 与中间价可预测性；
- 逆向选择与 informed flow；
- 做市商自身订单的市场冲击；
- 非 Poisson、聚集或自激订单流；
- 当前 spread、深度、imbalance、queue position；
- tick、延迟、撤改单成本、手续费和返佣；
- 部分成交、随机成交量和多档挂单；
- 多资产相关、期货/现货对冲和 basis risk；
- 参数随时间变化和 regime switch。

原始论文明确把研究重点放在 **inventory effect**，虽然引言讨论了 asymmetric information risk，但模型并没有把信息不对称写入状态或成交强度。[原始论文，第 1 节](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf)

### 数学严谨性边界

GLFT 指出，原始无库存上限的 AS 模型缺少 verification theorem，原论文声称的报价在该无界设置下是否 admissible 仍存在问题；GLFT 通过库存硬上限和线性 ODE 系统给出严格解。[GLFT，第 1、3 节](https://arxiv.org/pdf/1105.3115)

### 闭式近似的边界

- 原始 AS 的简单 $T-t$ 公式是近似，不是完整 HJB 的一般精确解；
- GLFT 的 Gaussian 谱公式也是对长时特征向量的近似；
- GLFT 后续研究显示，闭式近似在库存绝对值较小时更可靠，库存较大时真实最优报价并不保持库存的仿射函数。[Guéant 2016，第 4、6 节](https://arxiv.org/abs/1605.01862)

## 17. 可迁移性：适合与不适合

### 适合

- 作为库存 skew 的可解释基线；
- 比较“关于中间价对称报价”和“库存感知报价”；
- 仿真环境中的 benchmark；
- RL / MPC 策略的初始 policy、action prior 或安全层；
- 小 tick、成交概率随距离相对平滑的市场；
- 作为更复杂做市模型的模块接口：fair value、inventory penalty、fill model。

### 不宜直接照搬

- 大 tick、队列价值主导的股票或期货；
- 盘口稀疏、成交量离散且部分成交显著的市场；
- 有强 alpha、趋势、毒性订单流或延迟套利的环境；
- 多资产库存风险和对冲成本占主导的做市台；
- 永续合约、期权等存在 funding、Greeks、波动率曲面或 basis risk 的产品。

迁移到其他资产时，应保留 AS 的“价值中心 + 库存惩罚 + 成交曲线”结构，而重新建模参考价值、风险度量、fill probability 与执行约束。

## 18. 现有公式草稿的关键纠错清单

| 常见错误 | 正确处理 |
|---|---|
| 把 $s$ 写成 $\log S_t$ | 原始主模型中 $s=S_t$ |
| 目标只写 $E[U(X_T)]$ | 应包含 $X_T+q_TS_T$ 与 CARA 形式 |
| 卖出保留价仍写 $r^b$ | 应为 $v(x+r^a,s,q-1,t)=v(x,s,q,t)$ |
| HJB 指数中把 $\theta(q\pm1)$ 与 $\theta(q)$ 相加 | 应通过 $r^a,r^b$ 的离散差分进入，符号见第 6 节 |
| bid 控制项使用 $\delta^a$ | bid 必须使用 $\delta^b$ |
| 写成 $(T-t)^2$ | 冻结库存与常用有限期限近似都是一次 $T-t$ |
| 把 $\theta_{\mathrm{frozen}}$ 当主动做市精确解 | 主动做市一般需解 HJB；简单公式只是近似 |
| 把含 $T-t$ 的公式称为 ergodic | 真正长时极限见 GLFT 特征向量/谱近似 |
| 把 $A$ 称为“价内成交率” | $A=\lambda(0)$，是 $\delta=0$ 的外推基准强度 |
| 声称原 HJB 包含信息不对称 | 原模型只显式处理库存风险和成交风险 |
| 混淆“报价”与“价差” | $p^a,p^b$ 是价格；$\delta^a,\delta^b$ 是到中间价距离；$\psi$ 是总点差 |

## 19. 快速公式卡

### 原始 AS 有限期限近似

$$
r_t=S_t-q_t\gamma\sigma^2(T-t),
$$

$$
\psi_t
=\gamma\sigma^2(T-t)
+\frac{2}{\gamma}\ln\!\left(1+\frac{\gamma}{k}\right),
$$

$$
p_t^{b*}=r_t-\frac{\psi_t}{2},
\qquad
p_t^{a*}=r_t+\frac{\psi_t}{2}.
$$

### GLFT 有限期限严格解

$$
\boldsymbol v(t)=e^{-M(T-t)}\boldsymbol 1,
$$

$$
\delta_t^{b*}(q)
=c_0+\frac{1}{k}\ln\frac{v_q(t)}{v_{q+1}(t)},
$$

$$
\delta_t^{a*}(q)
=c_0+\frac{1}{k}\ln\frac{v_q(t)}{v_{q-1}(t)}.
$$

### GLFT 长时 Gaussian 谱近似

$$
C
=\sqrt{
\frac{\sigma^2\gamma}{2kA}
\left(1+\frac{\gamma}{k}\right)^{1+\frac{k}{\gamma}}
},
$$

$$
r_\infty(q)\approx s-qC,
$$

$$
\psi_\infty(q)\approx 2c_0+C.
$$

## 20. 参考文献

1. Avellaneda, M. & Stoikov, S. (2008). *High-frequency trading in a limit order book*. Quantitative Finance, 8(3), 217–224. [作者托管全文](https://people.orie.cornell.edu/sfs33/LimitOrderBook.pdf) · [DOI](https://doi.org/10.1080/14697680701381228)
2. Guéant, O., Lehalle, C.-A. & Fernandez-Tapia, J. (2013). *Dealing with the inventory risk: a solution to the market making problem*. Mathematics and Financial Economics, 7, 477–507. [arXiv](https://arxiv.org/abs/1105.3115) · [PDF](https://arxiv.org/pdf/1105.3115)
3. Guéant, O. (2016). *Optimal market making*. [arXiv](https://arxiv.org/abs/1605.01862)
