"""Streamlit主应用"""
import streamlit as st
import yaml
import pandas as pd
from pathlib import Path

# 设置页面配置
st.set_page_config(
    page_title="多智能体股票量化分析系统",
    layout="wide",
    page_icon="📈"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def load_config():
    """加载配置文件"""
    config_path = Path("config/config.yaml")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def main():
    """主函数"""
    # 加载配置
    config = load_config()

    # 页面标题
    st.markdown('<h1 class="main-header">📈 多智能体股票量化分析系统</h1>', unsafe_allow_html=True)

    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 分析参数")

        # 股票选择
        tickers = config.get('stocks', {}).get('tickers', ['AAPL', 'MSFT', 'TSLA'])
        ticker = st.selectbox("选择股票代码", tickers)

        # 日期范围
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("开始日期", value=pd.to_datetime("2020-01-01"))
        with col2:
            end_date = st.date_input("结束日期", value=pd.to_datetime("today"))

        # 分析选项
        st.subheader("分析选项")
        enable_technical = st.checkbox("技术分析", value=True)
        enable_sentiment = st.checkbox("情绪分析", value=True)
        enable_backtest = st.checkbox("回测验证", value=False)

        # 分析按钮
        analyze_btn = st.button("🚀 开始分析", type="primary", use_container_width=True)

    # 主界面
    if analyze_btn:
        # 显示加载状态
        with st.spinner("AI智能体团队正在分析中..."):
            try:
                # 这里调用协调器Agent
                from src.agents.coordinator import CoordinatorAgent

                coordinator = CoordinatorAgent(config)
                result = coordinator.run(ticker)

                # 显示分析结果
                st.success("✅ 分析完成!")

                # 基本信息
                st.header("📊 基本信息")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("股票代码", result['ticker'])
                with col2:
                    st.metric("当前价格", f"${result['current_price']:.2f}")
                with col3:
                    st.metric("分析日期", pd.Timestamp.now().strftime("%Y-%m-%d"))

                # 技术分析
                if enable_technical and 'technical_analysis' in result:
                    st.header("🔬 技术分析")
                    tech = result['technical_analysis']

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        lstm_pred = tech.get('lstm_prediction', 0)
                        delta_color = "normal" if lstm_pred > 0 else "inverse"
                        st.metric("LSTM预测", f"{lstm_pred:.2f}%", delta=f"{lstm_pred:.2f}%", delta_color=delta_color)

                    with col2:
                        rsi = tech.get('rsi', 50)
                        st.metric("RSI指标", f"{rsi:.2f}")

                    with col3:
                        macd = tech.get('macd', {}).get('macd_line', 0)
                        st.metric("MACD", f"{macd:.4f}")

                # 情绪分析
                if enable_sentiment and 'sentiment_analysis' in result:
                    st.header("💭 情绪分析")
                    sent = result['sentiment_analysis']

                    score = sent.get('recent_sentiment', 0)
                    sentiment_label = "正面" if score > 0.3 else "负面" if score < -0.3 else "中性"

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("情感指数", f"{score:.4f}")
                    with col2:
                        st.metric("情感倾向", sentiment_label)

                # 投资建议
                st.header("💡 AI投资建议")
                rec = result['recommendation']

                    # 显示操作建议
                action = rec.get('action', 'HOLD')
                action_emoji = {
                    'BUY': '🟢',
                    'SELL': '🔴',
                    'HOLD': '🟡'
                }.get(action, '⚪')

                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric(
                        "操作建议",
                        f"{action_emoji} {action}",
                        delta=None
                    )

                with col2:
                    confidence = rec.get('confidence', 0)
                    st.metric("信心指数", f"{confidence:.0f}%")

                # 显示理由和风险
                st.subheader("分析理由")
                st.info(rec.get('reason', '暂无理由'))

                st.subheader("风险提示")
                st.warning(rec.get('risk', '暂无风险提示'))

                # 详细信息(可折叠)
                with st.expander("📋 查看详细分析数据"):
                    st.json(result)

            except Exception as e:
                st.error(f"❌ 分析过程中出现错误: {str(e)}")
                st.exception(e)

    else:
        # 欢迎页面
        st.markdown("""
        ## 👋 欢迎使用多智能体股票量化分析系统!

        本系统由多个AI智能体协同工作,为您提供专业的股票分析:

        ### 🔬 技术分析
        - 基于**LSTM深度学习模型**预测价格走势
        - 计算**158个Qlib技术因子**
        - 分析RSI、MACD等经典指标

        ### 💭 情绪分析
        - 使用**FinBERT模型**分析新闻情感
        - 聚合多源情绪数据
        - 提供市场情绪指数

        ### 🤖 智能决策
        - **多智能体协作**模拟投研团队
        - **加权融合**多维度信号
        - 生成**结构化投资建议**

        ### 📊 回测验证
        - **Backtrader**策略回测
        - 计算夏普比率、最大回撤等指标
        - 验证策略有效性

        ---

        ### 🚀 使用步骤
        1. 在左侧选择股票代码
        2. 设置日期范围和分析选项
        3. 点击"开始分析"按钮
        4. 查看AI生成的投资建议

        ---
        """)

        # 系统特性
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🤖</h3>
                <p>多智能体协作</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🔬</h3>
                <p>AI深度分析</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📈</h3>
                <p>量化策略</p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
