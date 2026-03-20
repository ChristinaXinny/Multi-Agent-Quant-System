"""指标展示组件模块"""
import streamlit as st
from typing import Dict, Any


def display_metric_card(title: str, value: str, delta: str = None, help_text: str = None):
    """
    显示指标卡片

    Args:
        title: 指标标题
        value: 指标值
        delta: 变化量
        help_text: 帮助文本
    """
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; text-align: center;">
        <h3 style="margin: 0; color: #666;">{title}</h3>
        <p style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">{value}</p>
        {f'<p style="color: {"green" if delta and float(delta) > 0 else "red"}; margin: 0;">{delta}</p>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

    if help_text:
        st.caption(help_text)


def display_signal_gauge(score: float, title: str = "信号强度"):
    """
    显示信号强度仪表盘

    Args:
        score: 信号得分(-1到1)
        title: 标题
    """
    # 将score转换到0-100范围
    normalized_score = (score + 1) / 2 * 100

    # 确定颜色
    if score > 0.3:
        color = "🟢"
        status = "看涨"
    elif score < -0.3:
        color = "🔴"
        status = "看跌"
    else:
        color = "🟡"
        status = "中性"

    st.markdown(f"""
    <div style="text-align: center;">
        <h3>{title}</h3>
        <div style="font-size: 3rem; margin: 1rem 0;">{color}</div>
        <p style="font-size: 1.5rem;">{status}</p>
        <p>得分: {score:.4f}</p>
    </div>
    """, unsafe_allow_html=True)


def display_recommendation_card(recommendation: Dict[str, Any]):
    """
    显示投资建议卡片

    Args:
        recommendation: 建议字典,包含action, confidence, reason, risk
    """
    action = recommendation.get('action', 'HOLD')
    confidence = recommendation.get('confidence', 0)
    reason = recommendation.get('reason', '')
    risk = recommendation.get('risk', '')

    action_emojis = {
        'BUY': '🟢 买入',
        'SELL': '🔴 卖出',
        'HOLD': '🟡 持有'
    }

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 0.5rem; color: white;">
        <h2 style="margin: 0; font-size: 2rem;">{action_emojis.get(action, action)}</h2>
        <p style="font-size: 1.2rem; margin: 0.5rem 0;">信心指数: {confidence:.0f}%</p>
    </div>
    """, unsafe_allow_html=True)

    if reason:
        st.info(f"💡 {reason}")

    if risk:
        st.warning(f"⚠️ {risk}")


def display_key_metrics(metrics: Dict[str, float]):
    """
    显示关键指标

    Args:
        metrics: 指标字典
    """
    col1, col2, col3, col4 = st.columns(4)

    metric_names = list(metrics.keys())
    metric_values = list(metrics.values())

    with col1:
        if len(metric_names) > 0:
            st.metric(metric_names[0], f"{metric_values[0]:.4f}")

    with col2:
        if len(metric_names) > 1:
            st.metric(metric_names[1], f"{metric_values[1]:.4f}")

    with col3:
        if len(metric_names) > 2:
            st.metric(metric_names[2], f"{metric_values[2]:.4f}")

    with col4:
        if len(metric_names) > 3:
            st.metric(metric_names[3], f"{metric_values[3]:.4f}")
