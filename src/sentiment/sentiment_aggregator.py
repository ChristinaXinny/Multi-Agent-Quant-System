"""情感聚合模块"""
import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta
from loguru import logger


class SentimentAggregator:
    """情感得分聚合器"""

    def __init__(self):
        """初始化聚合器"""
        pass

    def aggregate_by_date(
        self,
        news_df: pd.DataFrame,
        date_col: str = 'date',
        sentiment_col: str = 'sentiment_score'
    ) -> Dict[datetime, float]:
        """
        按日期聚合情感得分

        Args:
            news_df: 新闻数据DataFrame
            date_col: 日期列名
            sentiment_col: 情感列名

        Returns:
            日期到情感得分的映射
        """
        # 确保日期列是datetime类型
        news_df[date_col] = pd.to_datetime(news_df[date_col])

        # 按日期分组并计算平均情感得分
        daily_sentiment = news_df.groupby(date_col)[sentiment_col].mean().to_dict()

        logger.info(f"按日期聚合完成,共 {len(daily_sentiment)} 个日期")
        return daily_sentiment

    def aggregate_by_ticker(
        self,
        news_df: pd.DataFrame,
        ticker_col: str = 'ticker',
        sentiment_col: str = 'sentiment_score'
    ) -> Dict[str, float]:
        """
        按股票代码聚合情感得分

        Args:
            news_df: 新闻数据DataFrame
            ticker_col: 股票代码列名
            sentiment_col: 情感列名

        Returns:
            股票代码到情感得分的映射
        """
        ticker_sentiment = news_df.groupby(ticker_col)[sentiment_col].mean().to_dict()

        logger.info(f"按股票聚合完成,共 {len(ticker_sentiment)} 只股票")
        return ticker_sentiment

    def get_recent_sentiment(
        self,
        news_df: pd.DataFrame,
        target_date: datetime,
        window_days: int = 7,
        date_col: str = 'date',
        sentiment_col: str = 'sentiment_score'
    ) -> float:
        """
        获取最近一段时间内的情感得分

        Args:
            news_df: 新闻数据DataFrame
            target_date: 目标日期
            window_days: 时间窗口(天)
            date_col: 日期列名
            sentiment_col: 情感列名

        Returns:
            平均情感得分
        """
        news_df[date_col] = pd.to_datetime(news_df[date_col])

        start_date = target_date - timedelta(days=window_days)
        recent_news = news_df[
            (news_df[date_col] >= start_date) &
            (news_df[date_col] <= target_date)
        ]

        if recent_news.empty:
            logger.warning(f"没有找到 {target_date} 前{window_days}天的新闻")
            return 0.0

        avg_sentiment = recent_news[sentiment_col].mean()
        logger.info(f"最近{window_days}天平均情感得分: {avg_sentiment:.4f}")

        return avg_sentiment

    def smooth_sentiment(
        self,
        sentiment_series: pd.Series,
        window: int = 3
    ) -> pd.Series:
        """
        平滑情感序列(使用移动平均)

        Args:
            sentiment_series: 情感序列
            window: 窗口大小

        Returns:
            平滑后的情感序列
        """
        smoothed = sentiment_series.rolling(window=window, min_periods=1).mean()
        return smoothed
