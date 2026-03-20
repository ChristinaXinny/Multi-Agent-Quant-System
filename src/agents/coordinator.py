"""协调器Agent - 负责协调各Agent工作"""
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

from .data_agent import DataAgent
from .technical_agent import TechnicalAgent
from .sentiment_agent import SentimentAgent
from .report_agent import ReportAgent
from .base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):
    """协调器Agent - 总调度"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化协调器Agent

        Args:
            config: 配置字典
        """
        super().__init__("CoordinatorAgent", config)

        # 初始化各子Agent
        self.data_agent = DataAgent(config)
        self.technical_agent = TechnicalAgent(config)
        self.sentiment_agent = SentimentAgent(config)
        self.report_agent = ReportAgent(config)

        # 是否并行执行
        self.parallel = config.get('parallel', True) if config else True

    def run(self, ticker: str) -> Dict[str, Any]:
        """
        运行完整的分析流程

        Args:
            ticker: 股票代码

        Returns:
            完整的分析结果
        """
        self.log_start()

        try:
            # 1. 数据获取
            logger.info("步骤1: 获取数据")
            data_result = self.data_agent.execute(
                ticker=ticker,
                start_date=self.config.get('start_date', '2020-01-01'),
                end_date=self.config.get('end_date', '2025-12-31'),
                load_news=True
            )

            stock_data = data_result['processed_data']
            news_data = data_result.get('news', None)

            # 2. 技术分析和情绪分析(并行或串行)
            if self.parallel and news_data is not None:
                logger.info("步骤2: 并行执行技术分析和情绪分析")
                with ThreadPoolExecutor(max_workers=2) as executor:
                    technical_future = executor.submit(self.technical_agent.execute, stock_data)
                    sentiment_future = executor.submit(
                        self.sentiment_agent.execute,
                        news_data,
                        stock_data.index[-1]
                    )

                    technical_result = technical_future.result()
                    sentiment_result = sentiment_future.result()
            else:
                # 串行执行
                logger.info("步骤2: 串行执行技术分析和情绪分析")
                technical_result = self.technical_agent.execute(stock_data)

                sentiment_result = None
                if news_data is not None:
                    sentiment_result = self.sentiment_agent.execute(
                        news_data,
                        stock_data.index[-1]
                    )

            # 3. 生成报告
            logger.info("步骤3: 生成投资建议报告")
            if sentiment_result is None:
                sentiment_result = {'recent_sentiment': 0}

            report = self.report_agent.execute(
                ticker=ticker,
                technical_result=technical_result,
                sentiment_result=sentiment_result
            )

            # 4. 汇总结果
            final_result = {
                'ticker': ticker,
                'current_price': technical_result.get('current_price'),
                'technical_analysis': technical_result,
                'sentiment_analysis': sentiment_result,
                'recommendation': report
            }

            self.log_complete(final_result)
            return final_result

        except Exception as e:
            self.log_error(e)
            raise
