"""图表组件模块"""
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict


def create_candlestick_chart(data: pd.DataFrame, title: str = "价格走势") -> go.Figure:
    """
    创建K线图

    Args:
        data: 包含OHLCV数据的DataFrame
        title: 图表标题

    Returns:
        Plotly Figure对象
    """
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="K线"
    )])

    fig.update_layout(
        title=title,
        yaxis_title="价格",
        xaxis_rangeslider_visible=False,
        height=500
    )

    return fig


def create_line_chart(
    data: pd.Series,
    title: str = "走势图",
    color: str = "blue"
) -> go.Figure:
    """
    创建折线图

    Args:
        data: 数据序列
        title: 图表标题
        color: 线条颜色

    Returns:
        Plotly Figure对象
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data.values,
        mode='lines',
        name=title,
        line=dict(color=color)
    ))

    fig.update_layout(
        title=title,
        xaxis_title="日期",
        yaxis_title="数值",
        height=400
    )

    return fig


def create_pie_chart(labels: List[str], values: List[float], title: str = "分布图") -> go.Figure:
    """
    创建饼图

    Args:
        labels: 标签列表
        values: 数值列表
        title: 图表标题

    Returns:
        Plotly Figure对象
    """
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3
    )])

    fig.update_layout(
        title=title,
        height=400
    )

    return fig


def create_bar_chart(
    categories: List[str],
    values: List[float],
    title: str = "柱状图",
    color: str = "blue"
) -> go.Figure:
    """
    创建柱状图

    Args:
        categories: 类别列表
        values: 数值列表
        title: 图表标题
        color: 柱子颜色

    Returns:
        Plotly Figure对象
    """
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=color
    )])

    fig.update_layout(
        title=title,
        xaxis_title="类别",
        yaxis_title="数值",
        height=400
    )

    return fig
