"""策略评估模块"""
import pandas as pd
import numpy as np
from typing import Dict, Any
from loguru import logger


class StrategyEvaluator:
    """策略评估器"""

    def __init__(self):
        """初始化评估器"""
        pass

    def evaluate(
        self,
        returns: pd.Series,
        benchmark_returns: pd.Series = None
    ) -> Dict[str, float]:
        """
        评估策略表现

        Args:
            returns: 策略收益率序列
            benchmark_returns: 基准收益率序列

        Returns:
            评估指标字典
        """
        metrics = {}

        # 总收益率
        total_return = (1 + returns).prod() - 1
        metrics['total_return'] = total_return

        # 年化收益率
        annual_return = (1 + total_return) ** (252 / len(returns)) - 1
        metrics['annual_return'] = annual_return

        # 波动率
        volatility = returns.std() * np.sqrt(252)
        metrics['volatility'] = volatility

        # 夏普比率
        risk_free_rate = 0.03  # 假设无风险利率为3%
        sharpe_ratio = (annual_return - risk_free_rate) / volatility
        metrics['sharpe_ratio'] = sharpe_ratio

        # 最大回撤
        cumulative_returns = (1 + returns).cumprod()
        running_max = cumulative_returns.cummax()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        metrics['max_drawdown'] = max_drawdown

        # 胜率
        win_rate = (returns > 0).mean()
        metrics['win_rate'] = win_rate

        # 如果有基准,计算超额收益和相对指标
        if benchmark_returns is not None:
            excess_returns = returns - benchmark_returns
            metrics['excess_return'] = excess_returns.mean()
            metrics['information_ratio'] = excess_returns.mean() / excess_returns.std()

        logger.info(f"策略评估完成,夏普比率: {sharpe_ratio:.4f}, 最大回撤: {max_drawdown:.4f}")
        return metrics

    def generate_report(self, metrics: Dict[str, float]) -> str:
        """
        生成评估报告

        Args:
            metrics: 评估指标

        Returns:
            格式化的报告字符串
        """
        report = f"""
策略评估报告
================
总收益率: {metrics['total_return']:.2%}
年化收益率: {metrics['annual_return']:.2%}
波动率: {metrics['volatility']:.2%}
夏普比率: {metrics['sharpe_ratio']:.4f}
最大回撤: {metrics['max_drawdown']:.2%}
胜率: {metrics['win_rate']:.2%}
"""
        if 'excess_return' in metrics:
            report += f"超额收益: {metrics['excess_return']:.2%}\n"
        if 'information_ratio' in metrics:
            report += f"信息比率: {metrics['information_ratio']:.4f}\n"

        return report
