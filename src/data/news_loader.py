"""新闻数据加载模块"""
import pandas as pd
from pathlib import Path
from typing import List, Dict
from loguru import logger


class NewsLoader:
    """新闻数据加载器"""

    def __init__(self, news_dir: str = "data/news"):
        """
        初始化新闻加载器

        Args:
            news_dir: 新闻数据目录
        """
        self.news_dir = Path(news_dir)

    def load_news(self, file_name: str = "financial_news.csv") -> pd.DataFrame:
        """
        加载新闻数据

        Args:
            file_name: 新闻文件名

        Returns:
            新闻数据DataFrame,应包含: date, title, ticker等列
        """
        file_path = self.news_dir / file_name

        if not file_path.exists():
            logger.warning(f"新闻文件不存在: {file_path}")
            return pd.DataFrame(columns=['date', 'title', 'ticker', 'sentiment'])

        try:
            news_df = pd.read_csv(file_path, parse_dates=['date'])
            logger.info(f"加载新闻数据: {len(news_df)} 条记录")
            return news_df

        except Exception as e:
            logger.error(f"加载新闻数据出错: {e}")
            return pd.DataFrame()

    def get_news_by_ticker(
        self,
        ticker: str,
        news_df: pd.DataFrame,
        start_date: str = None,
        end_date: str = None
    ) -> pd.DataFrame:
        """
        获取特定股票的新闻

        Args:
            ticker: 股票代码
            news_df: 新闻数据DataFrame
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            筛选后的新闻数据
        """
        # 筛选股票
        filtered = news_df[news_df['ticker'] == ticker].copy()

        # 筛选日期范围
        if start_date:
            filtered = filtered[filtered['date'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered = filtered[filtered['date'] <= pd.to_datetime(end_date)]

        logger.info(f"{ticker} 的新闻数量: {len(filtered)}")
        return filtered

    def create_sample_news(self, file_name: str = "financial_news.csv"):
        """
        创建示例新闻数据

        Args:
            file_name: 文件名
        """
        self.news_dir.mkdir(parents=True, exist_ok=True)

        sample_data = {
            'date': pd.date_range('2024-01-01', periods=100),
            'title': [
                'AAPL reports strong quarterly earnings',
                'TSLA faces production challenges',
                'MSFT announces new AI partnership',
                'Tech stocks rally on positive outlook',
                'Market volatility concerns weigh on investors'
            ] * 20,
            'ticker': ['AAPL', 'TSLA', 'MSFT', 'AAPL', 'TSLA'] * 20,
            'sentiment': [0.8, -0.5, 0.6, 0.7, -0.3] * 20
        }

        news_df = pd.DataFrame(sample_data)
        file_path = self.news_dir / file_name
        news_df.to_csv(file_path, index=False)

        logger.info(f"示例新闻数据已创建: {file_path}")
