"""数据处理模块 - 数据清洗、对齐、预处理"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Optional
from loguru import logger


class DataProcessor:
    """数据处理器"""

    def __init__(self, processed_dir: str = "data/processed"):
        """
        初始化数据处理器

        Args:
            processed_dir: 处理后数据保存目录
        """
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        清洗数据

        Args:
            df: 原始数据

        Returns:
            清洗后的数据
        """
        # 删除缺失值
        df = df.dropna()

        # 删除重复数据
        df = df.drop_duplicates()

        # 确保数据按日期排序
        df = df.sort_index()

        return df

    def add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        添加基础特征

        Args:
            df: 原始数据

        Returns:
            添加特征后的数据
        """
        # 收益率
        df['returns'] = df['Close'].pct_change()

        # 涨跌幅
        df['pct_change'] = df['Close'].pct_change() * 100

        return df

    def align_data(
        self,
        data_dict: dict,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        对齐多只股票的数据

        Args:
            data_dict: 股票数据字典 {ticker: DataFrame}
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            对齐后的数据
        """
        # 确定共同的日期范围
        common_index = None

        for ticker, df in data_dict.items():
            if common_index is None:
                common_index = df.index
            else:
                common_index = common_index.intersection(df.index)

        # 应用日期范围
        if start_date:
            common_index = common_index[common_index >= pd.to_datetime(start_date)]
        if end_date:
            common_index = common_index[common_index <= pd.to_datetime(end_date)]

        # 对齐数据
        aligned_data = {}
        for ticker, df in data_dict.items():
            aligned_data[ticker] = df.loc[common_index]

        logger.info(f"数据对齐完成,日期范围: {common_index.min()} 到 {common_index.max()}")
        return aligned_data

    def process_and_save(
        self,
        ticker: str,
        df: pd.DataFrame,
        save: bool = True
    ) -> pd.DataFrame:
        """
        处理并保存数据

        Args:
            ticker: 股票代码
            df: 原始数据
            save: 是否保存

        Returns:
            处理后的数据
        """
        # 清洗数据
        df = self.clean_data(df)

        # 添加特征
        df = self.add_features(df)

        # 保存
        if save:
            file_path = self.processed_dir / f"{ticker}_processed.csv"
            df.to_csv(file_path)
            logger.info(f"处理后数据已保存: {file_path}")

        return df
