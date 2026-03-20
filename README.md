# 多智能体股票量化分析系统

一个基于多智能体协作的股票量化分析原型系统,融合数据建模、AI Agent、大模型推理、最优化策略四大核心技术。

## 项目简介

本项目是一个课程作业(COMP7065 Mini-Project),通过模拟一个小型投研团队的工作流程,将技术分析、情绪分析、报告生成整合为自动化pipeline。

### 核心功能

- **📊 数据获取**: 使用yfinance下载股票历史数据
- **🔬 技术分析**: LSTM模型预测 + Qlib 158个技术因子
- **💭 情绪分析**: FinBERT新闻情感分析
- **🤖 AI Agent**: LangChain多智能体协作调度
- **📝 报告生成**: DeepSeek API生成投资建议
- **📈 回测验证**: Backtrader策略回测

## 技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| 数据处理 | pandas, yfinance, Qlib | 数据获取、因子计算 |
| 深度学习 | PyTorch, LSTM | 价格预测 |
| NLP | transformers, FinBERT | 情感分析 |
| Agent框架 | LangChain | 多智能体调度 |
| 大模型API | DeepSeek API | 报告生成 |
| 回测 | Backtrader | 策略验证 |
| 前端 | Streamlit | 可视化展示 |

## 项目结构

```
multi-agent-quant-system/
├── config/              # 配置文件
├── data/                # 数据目录
│   ├── raw/            # 原始数据
│   ├── processed/      # 处理后的数据
│   ├── news/           # 新闻数据
│   └── models/         # 模型文件
├── src/                # 核心源代码
│   ├── data/          # 数据模块
│   ├── features/      # 特征工程
│   ├── models/        # 模型模块
│   ├── sentiment/     # 情绪分析
│   ├── agents/        # Agent模块
│   ├── llm/           # 大模型模块
│   ├── backtest/      # 回测模块
│   ├── optimization/  # 优化模块
│   └── utils/         # 工具函数
├── app/                # Streamlit应用
├── scripts/            # 运行脚本
├── tests/              # 测试代码
└── docs/               # 文档
```

## 快速开始

### 1. 环境配置

```bash
# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并配置API密钥:

```bash
cp .env.example .env
```

编辑 `.env` 文件,添加你的DeepSeek API密钥:

```
DEEPSEEK_API_KEY=your_api_key_here
```

### 3. 下载数据

```bash
python scripts/download_data.py
```



## 使用说明

1. 在左侧选择股票代码和日期范围
2. 选择需要分析的类型(技术分析、情绪分析)
3. 点击"开始分析"按钮
4. 查看AI生成的投资建议报告

## 系统架构

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
【报告生成】调用大模型API,生成结构化投资建议
    ↓
【前端展示】Streamlit界面显示结果
```

## 开源参考

本项目参考并借鉴了以下开源项目:

- [Qlib](https://github.com/microsoft/qlib) - 微软开源量化投资平台
- [FinBERT](https://huggingface.co/ProsusAI/finbert) - 金融情感分析模型
- [LangChain](https://github.com/langchain-ai/langchain) - LLM应用开发框架
- [Backtrader](https://github.com/mementum/backtrader) - 回测框架

## 免责声明

⚠️ **本系统仅供学习和研究使用,不构成任何投资建议。**

股票投资有风险,入市需谨慎。使用本系统进行投资决策所造成的任何损失,本系统不承担责任。

## 许可证

MIT License

## 联系方式

- 项目: COMP7065课程项目
- 版本: v1.0.0
- 日期: 2025-03-20
