"""提示词构建模块"""
import yaml
from pathlib import Path
from typing import Dict, Any
from loguru import logger


class PromptBuilder:
    """提示词构建器"""

    def __init__(self, prompts_file: str = "config/prompts.yaml"):
        """
        初始化提示词构建器

        Args:
            prompts_file: 提示词配置文件路径
        """
        self.prompts_file = Path(prompts_file)
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, str]:
        """加载提示词配置"""
        if not self.prompts_file.exists():
            logger.warning(f"提示词配置文件不存在: {self.prompts_file}")
            return {}

        with open(self.prompts_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def build_report_prompt(
        self,
        ticker: str,
        current_price: float,
        lstm_prediction: float,
        rsi: float,
        macd_signal: str,
        sentiment_score: float,
        pe_ratio: float = None,
        pb_ratio: float = None
    ) -> str:
        """
        构建报告生成提示词

        Args:
            ticker: 股票代码
            current_price: 当前价格
            lstm_prediction: LSTM预测值
            rsi: RSI指标
            macd_signal: MACD信号
            sentiment_score: 情感得分
            pe_ratio: 市盈率
            pb_ratio: 市净率

        Returns:
            完整提示词
        """
        template = self.prompts.get('report_generation', self._get_default_template())

        prompt = template.format(
            ticker=ticker,
            current_price=f"{current_price:.2f}",
            date=pd.Timestamp.now().strftime('%Y-%m-%d'),
            lstm_prediction=f"{lstm_prediction:.2f}",
            rsis=f"{rsi:.2f}",
            macd_signal=macd_signal,
            sentiment_score=f"{sentiment_score:.2f}",
            pe_ratio=f"{pe_ratio:.2f}" if pe_ratio else "N/A",
            pb_ratio=f"{pb_ratio:.2f}" if pb_ratio else "N/A"
        )

        return prompt

    def _get_default_template(self) -> str:
        """获取默认提示词模板"""
        return """
你是一个专业的股票投资分析师。请根据以下数据生成投资建议报告。

## 股票基本信息
股票代码: {ticker}
当前价格: {current_price}
分析日期: {date}

## 技术面分析
LSTM预测涨跌幅: {lstm_prediction}%
RSI指标: {rsi}
MACD信号: {macd_signal}

## 情绪面分析
情感指数: {sentiment_score} (-1到1之间,负值表示悲观,正值表示乐观)

## 基本面数据
市盈率(PE): {pe_ratio}
市净率(PB): {pb_ratio}

## 要求
1. 综合以上数据,给出操作建议(BUY/SELL/HOLD)
2. 给出信心指数(0-100)
3. 简要说明理由(不超过100字)
4. 指出主要风险(不超过50字)

请以JSON格式返回:
{{
  "action": "BUY/SELL/HOLD",
  "confidence": 0-100,
  "reason": "理由说明",
  "risk": "风险提示"
}}
"""
