"""决策引擎模块"""
from typing import Dict, Any
from loguru import logger


class DecisionEngine:
    """决策引擎"""

    def __init__(
        self,
        buy_threshold: float = 0.6,
        sell_threshold: float = -0.6
    ):
        """
        初始化决策引擎

        Args:
            buy_threshold: 买入阈值
            sell_threshold: 卖出阈值
        """
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

        logger.info(f"决策阈值 - 买入: {buy_threshold}, 卖出: {sell_threshold}")

    def make_decision(self, composite_signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        做出交易决策

        Args:
            composite_signal: 合成信号

        Returns:
            决策结果
        """
        score = composite_signal['composite_score']

        # 根据阈值做出决策
        if score >= self.buy_threshold:
            action = 'BUY'
            confidence = min((score - self.buy_threshold) / (1 - self.buy_threshold) * 100, 100)
        elif score <= self.sell_threshold:
            action = 'SELL'
            confidence = min((self.sell_threshold - score) / (1 + self.sell_threshold) * 100, 100)
        else:
            action = 'HOLD'
            # 计算中性行情的置信度(越接近0越不明确)
            distance = min(abs(score - self.buy_threshold), abs(score - self.sell_threshold))
            confidence = max(0, 100 - distance * 100)

        result = {
            'action': action,
            'confidence': confidence,
            'score': score,
            'reason': self._generate_reason(action, score, composite_signal)
        }

        logger.info(f"决策: {action}, 置信度: {confidence:.2f}%, 得分: {score:.4f}")
        return result

    def _generate_reason(
        self,
        action: str,
        score: float,
        signal: Dict[str, Any]
    ) -> str:
        """生成决策理由"""
        tech = signal['technical_score']
        sent = signal['sentiment_score']
        fund = signal.get('fundamental_score', 0)

        if action == 'BUY':
            reasons = []
            if tech > 0.3:
                reasons.append("技术面看涨")
            if sent > 0.3:
                reasons.append("情绪面正面")
            if fund > 0.3:
                reasons.append("基本面良好")

            if reasons:
                return "、".join(reasons)
            else:
                return "综合指标偏积极"

        elif action == 'SELL':
            reasons = []
            if tech < -0.3:
                reasons.append("技术面看跌")
            if sent < -0.3:
                reasons.append("情绪面负面")
            if fund < -0.3:
                reasons.append("基本面疲弱")

            if reasons:
                return "、".join(reasons)
            else:
                return "综合指标偏消极"

        else:
            return "多空信号不明确,建议观望"
