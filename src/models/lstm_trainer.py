"""LSTM模型训练模块"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, List
from loguru import logger

from .lstm_model import LSTMModel


class LSTMTrainer:
    """LSTM模型训练器"""

    def __init__(
        self,
        model: LSTMModel,
        learning_rate: float = 0.001,
        device: str = 'cpu'
    ):
        """
        初始化训练器

        Args:
            model: LSTM模型
            learning_rate: 学习率
            device: 运行设备
        """
        self.model = model
        self.device = device
        self.model.to(device)

        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        self.train_losses = []
        self.val_losses = []

    def prepare_sequences(
        self,
        data: pd.DataFrame,
        feature_cols: List[str],
        target_col: str,
        sequence_length: int = 20,
        prediction_horizon: int = 5
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        准备训练序列

        Args:
            data: 数据DataFrame
            feature_cols: 特征列名列表
            target_col: 目标列名
            sequence_length: 输入序列长度
            prediction_horizon: 预测未来几天

        Returns:
            (特征张量, 目标张量)
        """
        features = data[feature_cols].values
        target = data[target_col].values

        X, y = [], []

        for i in range(len(data) - sequence_length - prediction_horizon):
            X.append(features[i:i + sequence_length])
            y.append(target[i + sequence_length:i + sequence_length + prediction_horizon].mean())

        X = torch.FloatTensor(np.array(X))
        y = torch.FloatTensor(np.array(y)).unsqueeze(1)

        logger.info(f"准备序列: X shape={X.shape}, y shape={y.shape}")
        return X, y

    def train(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader = None,
        num_epochs: int = 100,
        verbose: bool = True
    ):
        """
        训练模型

        Args:
            train_loader: 训练数据加载器
            val_loader: 验证数据加载器
            num_epochs: 训练轮数
            verbose: 是否打印训练信息
        """
        for epoch in range(num_epochs):
            # 训练阶段
            self.model.train()
            train_loss = 0

            for batch_X, batch_y in train_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                self.optimizer.step()

                train_loss += loss.item()

            train_loss /= len(train_loader)
            self.train_losses.append(train_loss)

            # 验证阶段
            val_loss = 0
            if val_loader:
                val_loss = self.evaluate(val_loader)

            if verbose and (epoch + 1) % 10 == 0:
                logger.info(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}')

    def evaluate(self, data_loader: DataLoader) -> float:
        """
        评估模型

        Args:
            data_loader: 数据加载器

        Returns:
            平均损失
        """
        self.model.eval()
        total_loss = 0

        with torch.no_grad():
            for batch_X, batch_y in data_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                outputs = self.model(batch_X)
                loss = self.criterion(outputs, batch_y)
                total_loss += loss.item()

        return total_loss / len(data_loader)

    def save_model(self, path: str):
        """
        保存模型

        Args:
            path: 保存路径
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'train_losses': self.train_losses,
            'val_losses': self.val_losses
        }, path)
        logger.info(f"模型已保存: {path}")

    def load_model(self, path: str):
        """
        加载模型

        Args:
            path: 模型路径
        """
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.train_losses = checkpoint.get('train_losses', [])
        self.val_losses = checkpoint.get('val_losses', [])
        logger.info(f"模型已加载: {path}")
