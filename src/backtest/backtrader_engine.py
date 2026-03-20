"""Backtrader回测引擎模块"""
import backtrader as bt
import pandas as pd
from pathlib import Path
from typing import Dict, Any
from loguru import logger

from .strategy import MultiFactorStrategy


class BacktraderEngine:
    """Backtrader回测引擎"""

    def __init__(self, initial_capital: float = 100000, commission: float = 0.001):
        """
        初始化回测引擎

        Args:
            initial_capital: 初始资金
            commission: 手续费率
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.cerebro = None

    def run_backtest(
        self,
        data: pd.DataFrame,
        strategy: MultiFactorStrategy
    ) -> Dict[str, Any]:
        """
        运行回测

        Args:
            data: 价格数据
            strategy: 交易策略

        Returns:
            回测结果
        """
        # 创建Cerebro引擎
        self.cerebro = bt.Cerebro()

        # 添加策略
        self.cerebro.addstrategy(
            BacktestStrategy,
            strategy_obj=strategy
        )

        # 准备数据
        data_feed = bt.feeds.PandasData(
            dataname=data,
            datetime=None,
            open='Open',
            high='High',
            low='Low',
            close='Close',
            volume='Volume',
            openinterest=-1
        )
        self.cerebro.adddata(data_feed)

        # 设置初始资金
        self.cerebro.broker.setcash(self.initial_capital)

        # 设置手续费
        self.cerebro.broker.setcommission(commission=self.commission)

        # 运行回测
        logger.info("开始回测...")
        results = self.cerebro.run()
        final_value = self.cerebro.broker.getvalue()

        # 计算收益率
        total_return = (final_value - self.initial_capital) / self.initial_capital * 100

        result = {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'strategy': strategy.name
        }

        logger.info(f"回测完成,总收益率: {total_return:.2f}%")
        return result


class BacktestStrategy(bt.Strategy):
    """Backtrader策略适配器"""

    def __init__(self, strategy_obj: MultiFactorStrategy):
        """
        初始化策略

        Args:
            strategy_obj: 多因子策略对象
        """
        self.strategy_obj = strategy_obj
        self.data_close = self.datas[0].close

    def next(self):
        """
        每个bar调用
        """
        # 这里简化处理,实际应根据策略生成信号
        # 实际使用时需要传入技术面、情绪面等数据

        # 示例: 基于简单的价格动量
        if len(self.data) >= 2:
            if self.data_close[0] > self.data_close[-1]:
                signal = 'BUY'
            else:
                signal = 'SELL'

            # 执行交易
            if signal == 'BUY' and not self.position:
                self.buy()
            elif signal == 'SELL' and self.position:
                self.sell()
