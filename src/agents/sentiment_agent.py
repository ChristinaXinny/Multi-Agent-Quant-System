"""情绪分析Agent - 负责情感分析"""
import pandas as pd
from typing import Dict, Any
from loguru import logger

from ..sentiment.finbert_analyzer import FinBertAnalyzer
from ..sentiment.sentiment_aggregator import SentimentAggregator
from .base_agent import BaseAgent


class SentimentAgent(BaseAgent):
    """情绪分析Agent"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化情绪分析Agent

        Args:
            config: 配置字典
        """
        super().__init__("SentimentAgent", config)

        # 初始化FinBERT分析器
        model_name = config.get('model_name', 'ProsusAI/finbert') if config else 'ProsusAI/finbert'
        self.analyzer = FinBertAnalyzer(model_name)

        # 初始化聚合器
        self.aggregator = SentimentAggregator()

    def execute(
        self,
        news_df: pd.DataFrame,
        target_date: str = None
    ) -> Dict[str, Any]:
        """
        执行情绪分析任务

        Args:
            news_df: 新闻数据
            target_date: 目标日期(可选)

        Returns:
            情绪分析结果
        """
        self.log_start()

        try:
            # 分析新闻情感
            analyzed_news = self.analyzer.analyze_news(news_df)

            # 聚合情感得分
            daily_sentiment = self.aggregator.aggregate_by_date(analyzed_news)

            # 获取最近的情感得分
            if target_date:
                from datetime import datetime
                target_dt = pd.to_datetime(target_date)
                recent_sentiment = self.aggregator.get_recent_sentiment(
                    analyzed_news,
                    target_dt,
                    window_days=7
                )
            else:
                recent_sentiment = analyzed_news['sentiment_score'].mean()

            result = {
                'daily_sentiment': daily_sentiment,
                'recent_sentiment': recent_sentiment,
                'average_sentiment': analyzed_news['sentiment_score'].mean(),
                'news_count': len(analyzed_news)
            }

            self.log_complete(result)
            return result

        except Exception as e:
            self.log_error(e)
            raise
