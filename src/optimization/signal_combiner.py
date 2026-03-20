"""信号合成模块"""
from typing import Dict, Any
import numpy as np
from loguru import logger


class SignalCombiner:
    """信号合成器"""

    def __init__(
        self,
        technical_weight: float = 0.5,
        sentiment_weight: float = 0.3,
        fundamental_weight: float = 0.2
    ):
        """
        初始化信号合成器

        Args:
            technical_weight: 技术面权重
            sentiment_weight: 情绪面权重
            fundamental_weight: 基本面权重
        """
        self.technical_weight = technical_weight
        self.sentiment_weight = sentiment_weight
        self.fundamental_weight = fundamental_weight

        # 归一化权重
        total = technical_weight + sentiment_weight + fundamental_weight
        self.technical_weight /= total
        self.sentiment_weight /= total
        self.fundamental_weight /= total

        logger.info(f"权重配置 - 技术: {self.technical_weight:.2f}, "
                   f"情绪: {self.sentiment_weight:.2f}, "
                   f"基本面: {self.fundamental_weight:.2f}")

    def combine_signals(
        self,
        technical_signal: Dict[str, Any],
        sentiment_signal: Dict[str, Any],
        fundamental_signal: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        合成多个信号

        Args:
            technical_signal: 技术面信号
            sentiment_signal: 情绪面信号
            fundamental_signal: 基本面信号(可选)

        Returns:
            合成后的信号
        """
        # 提取得分
        tech_score = self._normalize_technical(technical_signal)
        sent_score = self._normalize_sentiment(sentiment_signal)
        fund_score = self._normalize_fundamental(fundamental_signal) if fundamental_signal else 0

        # 加权合成
        composite_score = (
            tech_score * self.technical_weight +
            sent_score * self.sentiment_weight +
            fund_score * self.fundamental_weight
        )

        result = {
            'composite_score': composite_score,
            'technical_score': tech_score,
            'sentiment_score': sent_score,
            'fundamental_score': fund_score,
            'weights': {
                'technical': self.technical_weight,
                'sentiment': self.sentiment_weight,
                'fundamental': self.fundamental_weight
            }
        }

        logger.info(f"信号合成完成,综合得分: {composite_score:.4f}")
        return result

    def _normalize_technical(self, signal: Dict[str, Any]) -> float:
        """归一化技术信号到[-1, 1]"""
        lstm_pred = signal.get('lstm_prediction', 0)

        # 将LSTM预测(涨跌幅百分比)转换为[-1, 1]
        # 假设涨跌幅范围在[-10%, 10%]
        tech_score = np.clip(lstm_pred / 10, -1, 1)

        return tech_score

    def _normalize_sentiment(self, signal: Dict[str, Any]) -> float:
        """归一化情绪信号到[-1, 1]"""
        sentiment_score = signal.get('recent_sentiment', 0)

        # FinBERT输出已经在[-1, 1]范围内
        return np.clip(sentiment_score, -1, 1)

    def _normalize_fundamental(self, signal: Dict[str, Any]) -> float:
        """归一化基本面信号到[-1, 1]"""
        # 这里简化处理,实际可以使用PE、PB等指标
        # 示例: PE越低越好,假设合理范围[5, 50]
        pe = signal.get('pe', 25)

        # 转换为[-1, 1]
        if pe <= 5:
            return 1
        elif pe >= 50:
            return -1
        else:
            # 线性映射
            return 1 - (pe - 5) / 45 * 2
