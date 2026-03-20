"""数据获取模块 - 使用yfinance下载股票数据"""
import yfinance as yf
import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from loguru import logger


class DataFetcher:
    """股票数据获取器"""

    def __init__(self, save_dir: str = "data/raw"):
        """
        初始化数据获取器

        Args:
            save_dir: 数据保存目录
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def fetch_stock_data(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        save: bool = True
    ) -> pd.DataFrame:
        """
        下载单只股票的历史数据

        Args:
            ticker: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            save: 是否保存到文件

        Returns:
            股票数据DataFrame
        """
        logger.info(f"正在下载 {ticker} 的数据...")

        try:
            # 下载数据
            data = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                progress=False
            )

            if data.empty:
                logger.warning(f"{ticker} 没有获取到数据")
                return pd.DataFrame()

            # 保存到文件
            if save:
                file_path = self.save_dir / f"{ticker}_{start_date}_{end_date}.csv"
                data.to_csv(file_path)
                logger.info(f"数据已保存到: {file_path}")

            return data

        except Exception as e:
            logger.error(f"下载 {ticker} 数据时出错: {e}")
            return pd.DataFrame()

    def fetch_multiple_stocks(
        self,
        tickers: List[str],
        start_date: str,
        end_date: str
    ) -> Dict[str, pd.DataFrame]:
        """
        批量下载多只股票的数据

        Args:
            tickers: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            字典,键为股票代码,值为对应的DataFrame
        """
        results = {}

        for ticker in tickers:
            data = self.fetch_stock_data(ticker, start_date, end_date)
            if not data.empty:
                results[ticker] = data

        logger.info(f"成功下载 {len(results)}/{len(tickers)} 只股票的数据")
        return results

    def load_from_file(self, ticker: str, file_path: str) -> pd.DataFrame:
        """
        从文件加载股票数据

        Args:
            ticker: 股票代码
            file_path: 文件路径

        Returns:
            股票数据DataFrame
        """
        try:
            data = pd.read_csv(file_path, index_col=0, parse_dates=True)
            logger.info(f"从文件加载 {ticker} 数据: {file_path}")
            return data
        except Exception as e:
            logger.error(f"加载文件出错: {e}")
            return pd.DataFrame()
