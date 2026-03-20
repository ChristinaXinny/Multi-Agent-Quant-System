"""LSTM模型定义"""
import torch
import torch.nn as nn
from loguru import logger


class LSTMModel(nn.Module):
    """LSTM价格预测模型"""

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int = 64,
        num_layers: int = 2,
        dropout: float = 0.2,
        output_dim: int = 1
    ):
        """
        初始化LSTM模型

        Args:
            input_dim: 输入特征维度
            hidden_dim: 隐藏层维度
            num_layers: LSTM层数
            dropout: Dropout比率
            output_dim: 输出维度(预测目标数量)
        """
        super(LSTMModel, self).__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.output_dim = output_dim

        # LSTM层
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )

        # Dropout层
        self.dropout = nn.Dropout(dropout)

        # 全连接层
        self.fc = nn.Linear(hidden_dim, output_dim)

        logger.info(f"LSTM模型初始化: input_dim={input_dim}, hidden_dim={hidden_dim}, num_layers={num_layers}")

    def forward(self, x):
        """
        前向传播

        Args:
            x: 输入张量, shape=(batch_size, sequence_length, input_dim)

        Returns:
            预测结果, shape=(batch_size, output_dim)
        """
        # LSTM层
        lstm_out, (h_n, c_n) = self.lstm(x)

        # 取最后一个时间步的输出
        last_output = lstm_out[:, -1, :]

        # Dropout
        last_output = self.dropout(last_output)

        # 全连接层
        predictions = self.fc(last_output)

        return predictions

    def get_model_size(self):
        """获取模型参数量"""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


class LSTMPredictor:
    """LSTM预测器"""

    def __init__(self, model: LSTMModel, device: str = 'cpu'):
        """
        初始化预测器

        Args:
            model: 训练好的LSTM模型
            device: 运行设备
        """
        self.model = model
        self.device = device
        self.model.to(device)
        self.model.eval()

    def predict(self, x: torch.Tensor) -> float:
        """
        预测

        Args:
            x: 输入张量, shape=(1, sequence_length, input_dim)

        Returns:
            预测值
        """
        with torch.no_grad():
            x = x.to(self.device)
            prediction = self.model(x)
            return prediction.item()

    def predict_batch(self, x: torch.Tensor) -> list:
        """
        批量预测

        Args:
            x: 输入张量, shape=(batch_size, sequence_length, input_dim)

        Returns:
            预测值列表
        """
        with torch.no_grad():
            x = x.to(self.device)
            predictions = self.model(x)
            return predictions.cpu().numpy().tolist()
