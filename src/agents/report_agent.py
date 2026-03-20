"""报告生成Agent - 负责生成投资建议报告"""
import json
from typing import Dict, Any
from loguru import logger

from ..llm.deepseek_client import DeepSeekClient
from ..llm.prompt_builder import PromptBuilder
from .base_agent import BaseAgent


class ReportAgent(BaseAgent):
    """报告生成Agent"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化报告生成Agent

        Args:
            config: 配置字典
        """
        super().__init__("ReportAgent", config)

        # 初始化DeepSeek客户端
        self.client = DeepSeekClient()

        # 初始化提示词构建器
        prompts_file = config.get('prompts_file') if config else None
        self.prompt_builder = PromptBuilder(prompts_file)

    def execute(
        self,
        ticker: str,
        technical_result: Dict[str, Any],
        sentiment_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        执行报告生成任务

        Args:
            ticker: 股票代码
            technical_result: 技术分析结果
            sentiment_result: 情绪分析结果

        Returns:
            生成的报告
        """
        self.log_start()

        try:
            # 构建提示词
            prompt = self.prompt_builder.build_report_prompt(
                ticker=ticker,
                current_price=technical_result.get('current_price', 0),
                lstm_prediction=technical_result.get('lstm_prediction', 0),
                rsi=technical_result.get('rsi', 50),
                macd_signal=technical_result.get('macd', {}).get('signal', 'neutral'),
                sentiment_score=sentiment_result.get('recent_sentiment', 0),
                pe_ratio=None,  # 可以从基本面数据获取
                pb_ratio=None
            )

            # 调用API生成报告
            report = self.client.generate_report(prompt, json_output=True)

            # 添加额外信息
            report['ticker'] = ticker
            report['technical_signal'] = self._get_technical_signal(technical_result)
            report['sentiment_signal'] = self._get_sentiment_signal(sentiment_result)

            self.log_complete(report)
            return report

        except Exception as e:
            self.log_error(e)
            # 返回错误报告
            return {
                'action': 'HOLD',
                'confidence': 0,
                'reason': f'生成报告时出错: {str(e)}',
                'risk': '无法提供风险提示',
                'error': str(e)
            }

    def _get_technical_signal(self, technical_result: Dict[str, Any]) -> str:
        """根据技术分析结果生成信号"""
        lstm_pred = technical_result.get('lstm_prediction', 0)
        rsi = technical_result.get('rsi', 50)

        if lstm_pred > 2 and rsi < 70:
            return 'BULLISH'
        elif lstm_pred < -2 or rsi > 70:
            return 'BEARISH'
        else:
            return 'NEUTRAL'

    def _get_sentiment_signal(self, sentiment_result: Dict[str, Any]) -> str:
        """根据情绪分析结果生成信号"""
        score = sentiment_result.get('recent_sentiment', 0)

        if score > 0.3:
            return 'POSITIVE'
        elif score < -0.3:
            return 'NEGATIVE'
        else:
            return 'NEUTRAL'
