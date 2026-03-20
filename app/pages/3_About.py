"""关于页面"""
import streamlit as st


def about_page():
    """关于页面"""
    st.title("ℹ️ 关于系统")

    st.markdown("""
    # 多智能体股票量化分析系统

    ## 系统简介

    本系统是一个基于多智能体协作的股票量化分析原型系统,融合了数据建模、AI Agent、大模型推理、最优化策略四大核心技术。

    ## 核心技术

    ### 1. 数据建模
    - 使用yfinance获取股票数据
    - 集成Qlib的158个技术因子
    - LSTM深度学习模型预测价格走势

    ### 2. AI Agent
    - 基于LangChain的多智能体框架
    - 协调器Agent统一调度
    - 数据、技术、情绪、报告各司其职

    ### 3. 大模型推理
    - FinBERT进行新闻情感分析
    - DeepSeek API生成投资建议报告
    - 结构化输出JSON格式结果

    ### 4. 最优化策略
    - 加权融合多维度信号
    - 动态阈值决策
    - Backtrader回测验证

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
        ↓
    【回测验证】(可选)在历史数据上评估策略表现
    ```

    ## 使用说明

    1. 在首页选择股票代码和日期范围
    2. 选择需要分析的类型(技术分析、情绪分析、回测)
    3. 点击"开始分析"按钮
    4. 查看AI生成的投资建议报告

    ## 技术栈

    - **数据处理**: pandas, yfinance, Qlib
    - **深度学习**: PyTorch, LSTM
    - **NLP**: transformers, FinBERT
    - **Agent框架**: LangChain
    - **大模型**: DeepSeek API
    - **回测**: Backtrader
    - **前端**: Streamlit

    ## 开源项目

    本项目参考并借鉴了以下开源项目:

    - [Qlib](https://github.com/microsoft/qlib) - 微软开源量化投资平台
    - [FinBERT](https://huggingface.co/ProsusAI/finbert) - 金融情感分析模型
    - [LangChain](https://github.com/langchain-ai/langchain) - LLM应用开发框架
    - [Backtrader](https://github.com/mementum/backtrader) - 回测框架

    ## 免责声明

    ⚠️ **本系统仅供学习和研究使用,不构成任何投资建议。**

    股票投资有风险,入市需谨慎。使用本系统进行投资决策所造成的任何损失,本系统不承担责任。

    ---

    **开发团队**: COMP7065课程项目组
    **版本**: v1.0.0
    **更新日期**: 2025-03-20
    """)


if __name__ == "__main__":
    about_page()
