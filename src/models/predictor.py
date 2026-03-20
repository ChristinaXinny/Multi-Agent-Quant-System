"""统一预测接口"""
import torch
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any
from loguru import logger

from .lstm_model import LSTMModel, LSTMPredictor


class Predictor:
    """统一预测接口"""

    def __init__(self, model_path: str, config: Dict[str, Any] = None):
        """
        初始化预测器

        Args:
            model_path: 模型文件路径
            config: 模型配置
        """
        self.config = config or {}
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        # 加载模型
        self.model = self._load_model(model_path)
        self.predictor = LSTMPredictor(self.model, self.device)

        logger.info(f"预测器初始化完成,设备: {self.device}")

    def _load_model(self, model_path: str) -> LSTMModel:
        """
        加载LSTM模型

        Args:
            model_path: 模型路径

        Returns:
            LSTM模型实例
        """
        if not Path(model_path).exists():
            logger.error(f"模型文件不存在: {model_path}")
            raise FileNotFoundError(f"模型文件不存在: {model_path}")

        # 从配置获取模型参数
        input_dim = self.config.get('input_dim', 158)
        hidden_dim = self.config.get('hidden_dim', 64)
        num_layers = self.config.get('num_layers', 2)
        dropout = self.config.get('dropout', 0.2)

        model = LSTMModel(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            num_layers=num_layers,
            dropout=dropout
        )

        # 加载权重
        checkpoint = torch.load(model_path, map_location=self.device)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()

        logger.info(f"模型加载成功: {model_path}")
        return model

    def predict(
        self,
        data: pd.DataFrame,
        feature_cols: list,
        sequence_length: int = 20
    ) -> Dict[str, float]:
        """
        预测股票涨跌幅

        Args:
            data: 股票数据
            feature_cols: 特征列名
            sequence_length: 序列长度

        Returns:
            预测结果字典
        """
        # 准备输入数据
        features = data[feature_cols].values[-sequence_length:]
        x = torch.FloatTensor(features).unsqueeze(0)

        # 预测
        prediction = self.predictor.predict(x)

        result = {
            'prediction': prediction,
            'date': data.index[-1].strftime('%Y-%m-%d'),
            'model_type': 'LSTM'
        }

        logger.info(f"预测结果: {prediction:.4f}")
        return result

    def predict_batch(
        self,
        data_list: list,
        feature_cols: list,
        sequence_length: int = 20
    ) -> list:
        """
        批量预测

        Args:
            data_list: 股票数据列表
            feature_cols: 特征列名
            sequence_length: 序列长度

        Returns:
            预测结果列表
        """
        results = []

        for data in data_list:
            try:
                result = self.predict(data, feature_cols, sequence_length)
                results.append(result)
            except Exception as e:
                logger.error(f"预测出错: {e}")
                results.append(None)

        return results
