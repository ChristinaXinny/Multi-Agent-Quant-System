"""配置加载模块"""
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """配置文件加载器"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        初始化配置加载器

        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载YAML配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项

        Args:
            key: 配置键,支持点号分隔的嵌套键(如 'model.lstm.hidden_dim')
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value if value is not None else default

    def get_stocks(self) -> list:
        """获取股票列表"""
        return self.get('stocks.tickers', [])

    def get_paths(self) -> Dict[str, str]:
        """获取所有路径配置"""
        return self.get('paths', {})

    def get_model_config(self) -> Dict[str, Any]:
        """获取模型配置"""
        return self.get('model', {})

    def get_llm_config(self) -> Dict[str, Any]:
        """获取大模型配置"""
        return self.get('llm', {})
