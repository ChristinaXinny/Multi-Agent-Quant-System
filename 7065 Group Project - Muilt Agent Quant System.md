
# 项目核心要点与技术路线总结（完整版）

## 一、项目定位

**一句话定义**：一个基于多智能体协作的股票量化分析原型系统，融合数据建模、AI Agent、大模型推理、最优化策略四大核心技术，输出结构化投资建议。

**项目性质**：课程作业（COMP7065 Mini-Project）+ 未来求职作品的基础MVP

**核心价值**：用AI模拟一个小型投研团队的工作流程，将技术分析、情绪分析、报告生成整合为自动化 pipeline。

---

## 二、核心功能点

### 用户视角功能
| 功能 | 描述 |
|------|------|
| 股票分析 | 用户输入股票代码（如 AAPL），系统自动分析 |
| 技术面信号 | 输出 LSTM 预测涨跌幅 + RSI/MACD 等指标 |
| 情绪面指数 | 输出基于新闻的 -1 到 1 情感得分 |
| 投资建议 | 输出结构化建议（操作/仓位/理由/风险） |
| 结果展示 | Streamlit 界面可视化呈现 |

### 系统内部功能
| 功能模块 | 核心任务 |
|---------|---------|
| 数据获取 | 下载历史日线数据 + 基本面数据 + 新闻数据 |
| 因子计算 | 生成 158 个技术因子（基于 Qlib） |
| 价格预测 | LSTM 模型预测未来 5 日涨跌幅 |
| 情感分析 | FinBERT 对新闻标题进行情感打分 |
| 任务调度 | 协调器 Agent 串/并联各模块 |
| 报告生成 | 大模型 API 生成结构化投资建议 |
| 回测验证 | 在历史数据上评估策略表现 |

---

## 三、四大核心技术点详解

### 1. 数据建模
**核心任务**：基于历史数据预测未来价格走势

**技术路线**：
- 数据源：yfinance（美股）/ akshare（A股）日线数据
- 因子库：直接复用 Qlib 内置的 158 个技术因子（动量、波动、价值、质量等）
- 预测模型：LSTM（2层 + Dropout），输入过去 20 日因子矩阵，输出未来 5 日涨跌幅
- 评估指标：MAE、RMSE、方向准确率

**可复用资源**：
- ✅ Qlib：微软开源，提供数据处理、因子计算、模型训练全套能力
- ✅ 无需自己实现复杂因子工程，直接调用现成因子

---

### 2. AI Agent
**核心任务**：负责任务拆解、模块调度、结果汇总

**技术路线**：
- 框架：LangChain 的 Agent 或 SequentialChain
- Agent 角色：
  - 协调器 Agent：接收用户输入，调度各子模块
  - 数据 Agent：封装数据获取接口
  - 技术 Agent：封装 LSTM 预测 + 指标计算
  - 情绪 Agent：封装 FinBERT 情感分析
  - 报告 Agent：封装大模型 API 调用
- 执行方式：技术 Agent 和情绪 Agent 可并行调用，提升响应速度

**可复用资源**：
- ✅ langchain-trading-agents：开源项目，提供现成的多智能体交易框架设计思路
- ✅ Alpha Agent（Devpost）：LangGraph 调度架构可借鉴

---

### 3. 大模型推理
**核心任务**：将数值信号转化为可读的投资建议

**技术路线**：
- 情感分析模型：FinBERT（港科大发布，在 49 亿金融语料上预训练）
  - 输入：新闻标题
  - 输出：-1 到 1 的连续情感得分
- 报告生成模型：DeepSeek API（性价比高，支持 JSON 输出）
  - 输入：技术信号 + 情绪指数 + 基本面数据
  - 输出：结构化 JSON（含操作、仓位、理由、风险）
- 提示词设计：三层模板（数据层 + 推理层 + 输出层），强制基于数据生成，减少幻觉

**可复用资源**：
- ✅ FinBERT：HuggingFace 直接加载预训练权重
- ✅ DeepSeek API：注册即用，成本极低
- ✅ nof1.ai Alpha Arena：AI 决策流程（request_decision → 提示词 → 输出验证）可参考
- ✅ langchain-trading-agents：内置新闻分析师 Agent 的提示词模板

---

### 4. 最优化策略
**核心任务**：将多维度信号转化为交易决策，并验证有效性

**技术路线**：
- 信号合成：加权打分（LSTM 预测 × 权重 + 情感得分 × 权重 + 基本面 × 权重）
- 决策规则：
  - 综合得分 > 阈值 → 买入信号
  - 综合得分 < 阈值 → 卖出信号
  - 否则 → 持有信号
- 回测框架：Backtrader 或 Qlib 回测引擎
- 评估指标：年化收益率、夏普比率、最大回撤、胜率

**可复用资源**：
- ✅ Backtrader：轻量级回测框架，文档齐全
- ✅ Qlib 回测引擎：更专业，支持更复杂的回测场景
- ✅ nof1.ai Alpha Arena：Smart-RR 计算、回撤防护、波动监控等风控机制可参考

---

## 四、数据来源

| 数据类型 | 来源 | 说明 |
|---------|------|------|
| 日线量价 | yfinance / akshare | 2020-2025 年，10 只代表性股票 |
| 基本面 | yfinance | PE、PB、ROE 等 |
| 新闻 | 预置数据集 | 500 条财经新闻，含日期、标题、相关股票 |

**简化策略**：预置 10 只股票的数据，避免每次运行时重复下载

---

## 五、技术栈全景

| 类别 | 技术 | 用途 |
|------|------|------|
| 数据处理 | Qlib, pandas | 因子计算、数据清洗 |
| 深度学习 | PyTorch | LSTM 模型训练 |
| NLP | FinBERT (HuggingFace) | 情感分析 |
| 大模型 API | DeepSeek API | 报告生成 |
| Agent 框架 | LangChain | 多智能体调度 |
| 回测 | Backtrader / Qlib | 策略验证 |
| 前端 | Streamlit | 可视化展示 |

---

## 六、可复用的开源项目资源

| 项目 | 可复用部分 | 用途 |
|------|-----------|------|
| **Qlib (微软)** | 158 个技术因子 + 数据处理 + 回测引擎 | 因子工程、回测 |
| **FinBERT (港科大)** | 预训练情感分析模型 | 情绪分析 |
| **langchain-trading-agents** | 多智能体框架设计 + 提示词模板 | Agent 调度、报告生成 |
| **Alpha Agent (Devpost)** | LangGraph 调度架构 | 复杂 Agent 协作参考 |
| **nof1.ai Alpha Arena** | AI 决策流程 + 风控机制 + 指标集成架构 | 报告生成、风险控制 |
| **DeepSeek API** | 大模型调用 | 报告生成 |

---

## 七、系统工作流程

```
用户输入股票代码
    ↓
【数据获取】→ 下载/读取预置数据
    ↓
【并行处理】
    ├─→ 【技术分析】LSTM预测 + 技术指标
    └─→ 【情绪分析】FinBERT新闻情感打分
    ↓
【信号合成】加权计算综合得分
    ↓
【报告生成】调用大模型API，生成结构化投资建议
    ↓
【前端展示】Streamlit界面显示结果
    ↓
【回测验证】（可选）在历史数据上评估策略表现
```

---

## 八、项目亮点

1. **多智能体协作**：模拟真实投研团队分工，各 Agent 各司其职
2. **技术融合**：LSTM（时序建模）+ FinBERT（金融NLP）+ 大模型（推理生成）三种 AI 技术协同
3. **可解释性**：每个决策步骤都有迹可循，符合金融场景要求
4. **模块化设计**：各模块解耦，未来可独立升级（如替换更先进的模型）
5. **快速验证**：回测模块可评估策略有效性，避免盲目决策

---

## 九、一句话总结

本项目是一个**基于多智能体协作的股票量化分析原型系统**，通过 LSTM 做价格预测、FinBERT 做情绪分析、大模型做报告生成、LangChain 做任务调度，最终输出结构化投资建议。系统设计借鉴了 Qlib、FinBERT、langchain-trading-agents、Alpha Agent、nof1.ai 等多个开源项目的优秀实践，在 1 个月内完成可演示的 MVP 版本，为后续扩展为完整量化平台奠定基础。


# 项目具体实现总结（简洁版）

## 一、系统核心流程

**输入**：用户输入股票代码（如 AAPL）
**输出**：结构化投资建议报告（含技术信号、情绪指数、操作建议）

**执行流程**：
1. 数据获取 → 2. 技术分析 + 情绪分析（并行）→ 3. 信号合成 → 4. 报告生成 → 5. 前端展示

---

## 二、五大模块具体实现

### 模块1：数据获取
- **实现**：用 yfinance 下载 10 只股票 2020-2025 年日线数据
- **预置**：500 条财经新闻（含日期、标题、相关股票）
- **存储**：CSV/Parquet 格式，避免重复下载

### 模块2：技术分析
- **因子**：直接复用 Qlib 的 158 个技术因子
- **模型**：LSTM（2层，hidden_size=64），输入过去20日数据，预测未来5日涨跌幅
- **指标**：同时计算 RSI、MACD、布林带作为辅助信号

### 模块3：情绪分析
- **模型**：FinBERT（HuggingFace 预训练）
- **处理**：对每条新闻输出 -1 到 1 情感得分，按天聚合为情绪指数
- **输入**：新闻标题（无需额外训练）

### 模块4：Agent调度
- **框架**：LangChain SequentialChain
- **流程**：
  - 协调器接收输入
  - 并行调用技术Agent和情绪Agent
  - 汇总结果传给报告Agent

### 模块5：报告生成
- **模型**：DeepSeek API
- **提示词**：三层模板（数据层+推理层+输出层），强制JSON格式
- **输出示例**：
```json
{
  "action": "BUY",
  "confidence": 75,
  "reason": "技术面看涨+情绪面偏正面",
  "risk": "大盘调整风险"
}
```

### 模块6：回测与展示
- **回测**：Backtrader 验证策略历史表现（夏普比率、最大回撤）
- **前端**：Streamlit 搭建交互界面，输入股票代码，实时显示结果

---

## 三、技术栈速览

| 模块 | 技术 | 用途 |
|------|------|------|
| 数据处理 | Qlib, pandas | 因子计算、数据清洗 |
| 价格预测 | PyTorch LSTM | 涨跌幅预测 |
| 情感分析 | FinBERT | 新闻情感打分 |
| 报告生成 | DeepSeek API | 投资建议生成 |
| Agent调度 | LangChain | 多模块串联 |
| 回测 | Backtrader | 策略验证 |
| 前端 | Streamlit | 可视化展示 |

---

## 四、可复用资源清单

| 资源 | 用途 | 来源 |
|------|------|------|
| 158个技术因子 | 特征工程 | Qlib（微软开源） |
| FinBERT模型 | 情感分析 | 港科大 HuggingFace |
| 多Agent架构 | 调度设计 | langchain-trading-agents |
| AI决策流程 | 报告生成参考 | nof1.ai Alpha Arena |
| 大模型API | 文本生成 | DeepSeek |

---

## 五、一句话总结

**用 yfinance 拿数据 → Qlib 算因子 → LSTM 预测涨跌 → FinBERT 读新闻 → LangChain 串起来 → DeepSeek 写报告 → Streamlit 展示，1 个月做出一个能演示的 AI 股票分析助手。**



# 项目工程框架搭建指南

## 一、项目目录结构

```
multi-agent-quant-system/
│
├── README.md                 # 项目说明文档
├── requirements.txt          # 依赖包列表
├── .gitignore                # Git忽略文件
│
├── data/                      # 数据目录
│   ├── raw/                   # 原始数据（yfinance下载）
│   ├── processed/             # 处理后的数据（清洗对齐）
│   ├── news/                   # 新闻数据集
│   └── cache/                  # 缓存文件
│
├── notebooks/                  # Jupyter Notebooks
│   ├── 01_data_exploration.ipynb      # 数据探索
│   ├── 02_lstm_training.ipynb          # LSTM模型训练
│   ├── 03_finbert_sentiment.ipynb      # FinBERT情感分析测试
│   └── 04_backtesting.ipynb             # 回测分析
│
├── src/                         # 核心源代码
│   ├── __init__.py
│   │
│   ├── data/                     # 数据模块
│   │   ├── __init__.py
│   │   ├── data_fetcher.py        # 数据下载（yfinance）
│   │   ├── data_processor.py      # 数据清洗对齐
│   │   └── news_loader.py         # 新闻数据加载
│   │
│   ├── factors/                   # 因子模块
│   │   ├── __init__.py
│   │   ├── qlib_factors.py        # Qlib因子调用
│   │   └── technical_indicators.py # 技术指标计算
│   │
│   ├── models/                    # 模型模块
│   │   ├── __init__.py
│   │   ├── lstm_model.py           # LSTM模型定义
│   │   ├── train_lstm.py           # 训练脚本
│   │   └── predict.py              # 预测函数
│   │
│   ├── sentiment/                  # 情绪分析模块（NLP同学）
│   │   ├── __init__.py
│   │   ├── finbert_sentiment.py    # FinBERT情感分析
│   │   └── sentiment_aggregator.py # 情感聚合
│   │
│   ├── agents/                     # Agent模块
│   │   ├── __init__.py
│   │   ├── base_agent.py            # Agent基类
│   │   ├── data_agent.py            # 数据Agent
│   │   ├── technical_agent.py       # 技术分析Agent
│   │   ├── sentiment_agent.py       # 情绪分析Agent
│   │   ├── report_agent.py          # 报告生成Agent（NLP同学）
│   │   └── coordinator.py           # 协调器Agent
│   │
│   ├── llm/                        # 大模型模块（NLP同学）
│   │   ├── __init__.py
│   │   ├── deepseek_api.py          # DeepSeek API调用
│   │   └── prompts.py               # 提示词模板
│   │
│   ├── backtest/                    # 回测模块
│   │   ├── __init__.py
│   │   ├── strategy.py               # 策略定义
│   │   └── backtest_engine.py        # 回测引擎（Backtrader/Qlib）
│   │
│   └── utils/                       # 工具函数
│       ├── __init__.py
│       ├── config.py                  # 配置文件
│       └── logger.py                  # 日志
│
├── app.py                         # Streamlit主应用
├── config.yaml                    # 项目配置文件
│
├── tests/                         # 测试代码
│   ├── test_data.py
│   ├── test_models.py
│   └── test_agents.py
│
├── scripts/                       # 辅助脚本
│   ├── download_data.py            # 数据下载脚本
│   ├── train_models.py             # 模型训练脚本
│   └── run_backtest.py             # 运行回测脚本
│
└── docs/                          # 文档
    ├── proposal.pdf                # 项目提案
    └── images/                     # 文档用图
```

---

## 二、核心文件说明

### 配置文件 `config.yaml`

```yaml
# 项目配置
project:
  name: "Multi-Agent Quant System"
  version: "1.0.0"

# 股票配置
stocks:
  tickers:
    - "AAPL"
    - "MSFT"
    - "TSLA"
    - "0700.HK"
    - "9988.HK"
  start_date: "2020-01-01"
  end_date: "2025-12-31"

# 数据路径
data:
  raw_dir: "data/raw"
  processed_dir: "data/processed"
  news_file: "data/news/financial_news.csv"

# 模型配置
model:
  lstm:
    input_dim: 158  # Qlib因子维度
    hidden_dim: 64
    num_layers: 2
    dropout: 0.2
    sequence_length: 20
    prediction_horizon: 5

# Agent配置
agent:
  parallel: true  # 是否并行调用技术Agent和情绪Agent

# 大模型配置
llm:
  provider: "deepseek"
  model: "deepseek-chat"
  temperature: 0.3
  max_tokens: 1000

# 回测配置
backtest:
  framework: "backtrader"  # 或 "qlib"
  initial_capital: 100000
  commission: 0.001
  slippage: 0.001
```

### 依赖文件 `requirements.txt`

```
# 核心库
numpy>=1.24.0
pandas>=2.0.0
pyyaml>=6.0

# 数据获取
yfinance>=0.2.0
akshare>=1.0.0

# 深度学习
torch>=2.0.0
torchvision>=0.15.0

# Qlib
pyqlib>=0.9.0

# 金融NLP
transformers>=4.30.0
torch>=2.0.0

# Agent框架
langchain>=0.1.0
langchain-community>=0.1.0

# 大模型API
openai>=1.0.0  # DeepSeek兼容OpenAI SDK

# 回测
backtrader>=1.9.0

# 可视化
streamlit>=1.28.0
plotly>=5.17.0
matplotlib>=3.7.0

# 工具
python-dotenv>=1.0.0
loguru>=0.7.0
tqdm>=4.65.0
```

### 主应用 `app.py`

```python
import streamlit as st
import yaml
from src.agents.coordinator import CoordinatorAgent

# 加载配置
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

st.set_page_config(page_title="AI量化分析系统", layout="wide")
st.title("📈 多智能体股票量化分析系统")

# 侧边栏输入
with st.sidebar:
    st.header("分析参数")
    ticker = st.selectbox("选择股票", config['stocks']['tickers'])
    analyze_btn = st.button("开始分析", type="primary")

# 主界面
if analyze_btn:
    with st.spinner("AI智能体团队正在分析..."):
        # 初始化协调器
        coordinator = CoordinatorAgent(config)
        
        # 执行分析
        result = coordinator.run(ticker)
        
        # 显示结果
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("当前价格", f"${result['price']:.2f}")
        with col2:
            st.metric("技术信号", result['technical_signal'])
        with col3:
            st.metric("情绪指数", f"{result['sentiment_score']:.2f}")
        
        # 投资建议
        st.subheader("💡 AI投资建议")
        st.info(result['recommendation'])
        
        # 详细数据
        with st.expander("查看详细分析"):
            st.json(result)
```

---

## 三、开发顺序建议

### 第一阶段：数据准备（第1周）
1. 创建项目目录结构
2. 编写 `data_fetcher.py` 下载股票数据
3. 准备新闻数据集
4. 测试Qlib因子计算

### 第二阶段：模型开发（第2周）
1. 编写LSTM模型并训练
2. 测试FinBERT情感分析
3. 保存模型文件

### 第三阶段：Agent集成（第3周）
1. 实现各Agent的基类和具体功能
2. 编写协调器串联流程
3. 测试端到端调用

### 第四阶段：前端与回测（第4周）
1. 搭建Streamlit界面
2. 集成回测模块
3. 整体联调测试

---

## 四、快速开始命令

```bash
# 1. 克隆仓库
git clone https://github.com/yourname/multi-agent-quant-system.git
cd multi-agent-quant-system

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 下载数据
python scripts/download_data.py

# 5. 训练模型
python scripts/train_models.py

# 6. 运行应用
streamlit run app.py
```

---
