"""股票分析页面"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def stock_analysis_page():
    """股票分析页面"""
    st.title("📈 股票技术分析")

    # 获取session state中的数据
    if 'analysis_result' not in st.session_state:
        st.warning("请先在首页进行股票分析")
        return

    result = st.session_state['analysis_result']

    # 价格走势图
    st.header("价格走势")
    # 这里应该显示实际的K线图
    st.info("K线图功能开发中...")

    # 技术指标图表
    st.header("技术指标")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("RSI指标")
        rsi_value = result['technical_analysis'].get('rsi', 50)
        st.metric("当前RSI", f"{rsi_value:.2f}")

        # RSI gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=rsi_value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "RSI"},
            gauge={
                'axis': {'range': [0, 100]},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "gray"},
                    {'range': [70, 100], 'color': "lightgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("MACD指标")
        st.info("MACD图表功能开发中...")


if __name__ == "__main__":
    stock_analysis_page()
