"""Qlib因子计算模块"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict
from loguru import logger

# from qlib.contrib.data.handler import Alpha360
# from qlib.data.dataset import DatasetH
# from qlib.data.dataset.loader import DataLoader

# Qlib相关导入
try:
    from qlib.contrib.data.handler import Alpha360
    from qlib.data.dataset import DatasetH
    from qlib.data.dataset.loader import DataLoader
    logger.info("Qlib导入成功")
except ImportError:
    logger.warning("Qlib未安装,将使用简化版本")


class QlibFactorCalculator:
    """Qlib因子计算器"""

    def __init__(self):
        """初始化因子计算器"""
        self.factors_list = self._get_default_factors()

    def _get_default_factors(self) -> List[str]:
        """
        获取默认的158个因子列表

        Returns:
            因子名称列表
        """
        # 这里列出常用的Qlib因子(简化版本)
        # 实际使用时可以从Qlib配置文件加载完整的158个因子
        common_factors = [
            # 动量因子
            'MA5', 'MA10', 'MA20', 'MA60',
            'EMA5', 'EMA10', 'EMA20',

            # 波动因子
            'STD5', 'STD10', 'STD20',
            'VOL5', 'VOL10', 'VOL20',

            # 价值因子
            'PE', 'PB', 'PS', 'PCF',

            # 质量因子
            'ROE', 'ROA', 'GrossMargin',

            # 技术指标
            'RSI', 'MACD', 'BBANDS',
        ]

        logger.info(f"加载了 {len(common_factors)} 个因子")
        return common_factors

    def calculate_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算技术因子

        Args:
            df: 原始OHLCV数据

        Returns:
            包含因子的DataFrame
        """
        factor_df = df.copy()

        # 移动平均
        for period in [5, 10, 20, 60]:
            factor_df[f'MA{period}'] = df['Close'].rolling(window=period).mean()
            factor_df[f'EMA{period}'] = df['Close'].ewm(span=period).mean()

        # 波动率
        for period in [5, 10, 20]:
            factor_df[f'STD{period}'] = df['Close'].rolling(window=period).std()
            factor_df[f'VOL{period}'] = df['Volume'].rolling(window=period).mean()

        # RSI
        factor_df['RSI'] = self._calculate_rsi(df['Close'])

        # MACD
        macd, signal = self._calculate_macd(df['Close'])
        factor_df['MACD'] = macd
        factor_df['MACD_Signal'] = signal

        # 布林带
        upper, middle, lower = self._calculate_bollinger_bands(df['Close'])
        factor_df['BB_Upper'] = upper
        factor_df['BB_Middle'] = middle
        factor_df['BB_Lower'] = lower

        logger.info(f"计算了 {len(self.factors_list)} 个因子")
        return factor_df

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """计算RSI指标"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _calculate_macd(
        self,
        prices: pd.Series,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> tuple:
        """计算MACD指标"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        return macd, macd_signal

    def _calculate_bollinger_bands(
        self,
        prices: pd.Series,
        period: int = 20,
        std_dev: int = 2
    ) -> tuple:
        """计算布林带"""
        middle = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        return upper, middle, lower
