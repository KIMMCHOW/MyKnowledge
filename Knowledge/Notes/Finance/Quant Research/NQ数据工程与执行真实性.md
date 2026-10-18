---
type: note
tags: [学习笔记, 量化研究]
created: 2026-10-19
---
# NQ数据工程与执行真实性

NQ tick size = 0.25 指数点，tick value = USD 5；MNQ 对应 USD 0.50/tick。持久保存 UTC、ET 和 CME trading day；夏令时采用时区数据库，不写死偏移量。原始字节→Parquet tick→分钟 OHLCV→逐日/日内 POC→连续合约映射，必须具备独立数据审计。

连续合约的调整价格主要用于研究信号；下单实际作用于特定到期合约。写明换月依据及前后合约映射，避免虚假跳空。

NautilusTrader 等框架只提供执行容器，不能证明策略逻辑复现正确。Bar 级同根触价的先后顺序未必确定，touch ≠ fill；检查订单状态、部分成交、撤单回报、滑点及断线恢复。Globex Day Session 可允许隔夜时钟时段但禁止跨 CME 交易日截止边界。Session 强平可视为合法退出设计，但必须与 target/stop/trailing 等退出分别归因。

