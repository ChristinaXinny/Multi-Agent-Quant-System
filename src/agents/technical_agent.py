"""技术分析Agent - 负责LSTM预测和技术指标"""
import pandas as pd
from typing import Dict, Any
from loguru import logger

from ..models.predictor import Predictor
from ..features.qlib_factors import QlibFactorCalculator
from ..features.technical_indicators import TechnicalIndicators
from .base_agent import BaseAgent


class TechnicalAgent(BaseAgent):
    """技术分析Agent"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化技术分析Agent

        Args:
            config: 配置字典
        """
        super().__init__("TechnicalAgent", config)

        # 初始化因子计算器
        self.factor_calculator = QlibFactorCalculator()

        # 初始化技术指标计算器
        self.indicator_calculator = TechnicalIndicators()

        # 初始化预测器(如果有模型)
        model_path = config.get('model_path') if config else None
        if model_path:
            self.predictor = Predictor(model_path, config)
        else:
            self.predictor = None
            logger.warning("未指定LSTM模型路径,预测功能不可用")

    def execute(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        执行技术分析任务

        Args:
            data: 股票数据

        Returns:
            技术分析结果
        """
        self.log_start()

        try:
            # 计算因子
            factor_data = self.factor_calculator.calculate_factors(data)

            # 计算技术指标
            rsi = self.indicator_calculator.rsi(data['Close'])
            macd_line, signal_line, histogram = self.indicator_calculator.macd(data['Close'])

            # LSTM预测(如果有模型)
            lstm_prediction = None
            if self.predictor:
                # 这里需要根据实际特征列调整
                feature_cols = self.config.get('feature_cols', [])
                if feature_cols:
                    prediction_result = self.predictor.predict(factor_data, feature_cols)
                    lstm_prediction = prediction_result['prediction']

            result = {
                'factor_data': factor_data,
                'rsi': rsi.iloc[-1] if not rsi.empty else None,
                'macd': {
                    'macd_line': macd_line.iloc[-1] if not macd_line.empty else None,
                    'signal_line': signal_line.iloc[-1] if not signal_line.empty else None,
                    'histogram': histogram.iloc[-1] if not histogram.empty else None
                },
                'lstm_prediction': lstm_prediction,
                'current_price': data['Close'].iloc[-1]
            }

            self.log_complete(result)
            return result

        except Exception as e:
            self.log_error(e)
            raise
