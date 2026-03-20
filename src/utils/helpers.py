"""通用辅助函数"""
import os
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv


def load_env():
    """加载环境变量"""
    load_dotenv()


def get_env(key: str, default: Any = None) -> Any:
    """
    获取环境变量

    Args:
        key: 环境变量键
        default: 默认值

    Returns:
        环境变量值
    """
    return os.getenv(key, default)


def ensure_dir(path: str) -> Path:
    """
    确保目录存在,不存在则创建

    Args:
        path: 目录路径

    Returns:
        Path对象
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """
    展平嵌套字典

    Args:
        d: 嵌套字典
        parent_key: 父键
        sep: 分隔符

    Returns:
        展平后的字典
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
