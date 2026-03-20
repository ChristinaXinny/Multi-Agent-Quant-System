"""交易策略定义模块"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd
from loguru import logger


class BaseStrategy(ABC):
    """策略基类"""

    def __init__(self, name: str):
        """
        初始化策略

        Args:
            name: 策略名称
        """
        self.name = name

    @abstractmethod
    def generate_signal(self, data: pd.DataFrame) -> str:
        """
        生成交易信号

        Args:
            data: 市场数据

        Returns:
            信号: 'BUY', 'SELL', 'HOLD'
        """
        pass


class MultiFactorStrategy(BaseStrategy):
    """多因子策略"""

    def __init__(
        self,
        technical_weight: float = 0.5,
        sentiment_weight: float = 0.3,
        fundamental_weight: float = 0.2,
        buy_threshold: float = 0.6,
        sell_threshold: float = -0.6
    ):
        """
        初始化多因子策略

        Args:
            technical_weight: 技术面权重
            sentiment_weight: 情绪面权重
            fundamental_weight: 基本面权重
            buy_threshold: 买入阈值
            sell_threshold: 卖出阈值
        """
        super().__init__("MultiFactorStrategy")
        self.technical_weight = technical_weight
        self.sentiment_weight = sentiment_weight
        self.fundamental_weight = fundamental_weight
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def generate_signal(
        self,
        technical_score: float,
        sentiment_score: float,
        fundamental_score: float = 0
    ) -> str:
        """
        生成交易信号

        Args:
            technical_score: 技术面得分
            sentiment_score: 情绪面得分
            fundamental_score: 基本面得分

        Returns:
            交易信号
        """
        # 加权计算综合得分
        composite_score = (
            technical_score * self.technical_weight +
            sentiment_score * self.sentiment_weight +
            fundamental_score * self.fundamental_weight
        )

        logger.info(f"综合得分: {composite_score:.4f}")

        # 根据阈值生成信号
        if composite_score >= self.buy_threshold:
            return 'BUY'
        elif composite_score <= self.sell_threshold:
            return 'SELL'
        else:
            return 'HOLD'
