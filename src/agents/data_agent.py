"""数据Agent - 负责数据获取和处理"""
import pandas as pd
from typing import Dict, Any
from loguru import logger

from ..data.data_fetcher import DataFetcher
from ..data.data_processor import DataProcessor
from ..data.news_loader import NewsLoader
from .base_agent import BaseAgent


class DataAgent(BaseAgent):
    """数据Agent"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化数据Agent

        Args:
            config: 配置字典
        """
        super().__init__("DataAgent", config)

        self.fetcher = DataFetcher(config.get('raw_dir', 'data/raw'))
        self.processor = DataProcessor(config.get('processed_dir', 'data/processed'))
        self.news_loader = NewsLoader(config.get('news_dir', 'data/news'))

    def execute(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        load_news: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """
        执行数据获取任务

        Args:
            ticker: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            load_news: 是否加载新闻

        Returns:
            数据字典
        """
        self.log_start()

        try:
            # 获取股票数据
            stock_data = self.fetcher.fetch_stock_data(ticker, start_date, end_date)

            if stock_data.empty:
                raise ValueError(f"无法获取 {ticker} 的数据")

            # 处理数据
            processed_data = self.processor.process_and_save(ticker, stock_data)

            result = {
                'raw_data': stock_data,
                'processed_data': processed_data,
                'ticker': ticker
            }

            # 加载新闻(如果需要)
            if load_news:
                news_df = self.news_loader.load_news()
                ticker_news = self.news_loader.get_news_by_ticker(ticker, news_df)
                result['news'] = ticker_news

            self.log_complete(result)
            return result

        except Exception as e:
            self.log_error(e)
            raise
