"""LSTM模型训练脚本"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset

from src.models.lstm_model import LSTMModel
from src.models.lstm_trainer import LSTMTrainer
from src.utils.logger import logger
from src.utils.config_loader import ConfigLoader


def prepare_dummy_data(sequence_length: int = 20):
    """
    准备示例训练数据

    注意:这是示例数据,实际使用时应该从真实数据加载
    """
    # 生成示例数据
    n_samples = 1000
    n_features = 158

    X = torch.randn(n_samples, sequence_length, n_features)
    y = torch.randn(n_samples, 1)

    # 创建数据加载器
    dataset = TensorDataset(X, y)
    train_size = int(0.8 * n_samples)
    val_size = n_samples - train_size

    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32)

    return train_loader, val_loader


def main():
    """主函数"""
    logger.info("开始训练LSTM模型...")

    # 加载配置
    config = ConfigLoader()
    model_config = config.get('model.lstm', {})

    input_dim = model_config.get('input_dim', 158)
    hidden_dim = model_config.get('hidden_dim', 64)
    num_layers = model_config.get('num_layers', 2)
    dropout = model_config.get('dropout', 0.2)
    sequence_length = model_config.get('sequence_length', 20)

    # 创建模型
    model = LSTMModel(
        input_dim=input_dim,
        hidden_dim=hidden_dim,
        num_layers=num_layers,
        dropout=dropout
    )

    logger.info(f"模型参数量: {model.get_model_size()}")

    # 准备数据
    logger.info("准备训练数据...")
    train_loader, val_loader = prepare_dummy_data(sequence_length)

    # 创建训练器
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f"使用设备: {device}")

    trainer = LSTMTrainer(model, device=device)

    # 训练模型
    logger.info("开始训练...")
    trainer.train(
        train_loader=train_loader,
        val_loader=val_loader,
        num_epochs=50,
        verbose=True
    )

    # 保存模型
    model_dir = Path(config.get('paths.model_dir', 'data/models'))
    model_path = model_dir / 'lstm_model.pth'

    trainer.save_model(str(model_path))

    logger.info("模型训练完成!")


if __name__ == "__main__":
    main()
