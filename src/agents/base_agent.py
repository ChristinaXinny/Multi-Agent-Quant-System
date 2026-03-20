"""Agent基类模块"""
from abc import ABC, abstractmethod
from typing import Any, Dict
from loguru import logger


class BaseAgent(ABC):
    """Agent基类"""

    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        初始化Agent

        Args:
            name: Agent名称
            config: 配置字典
        """
        self.name = name
        self.config = config or {}
        logger.info(f"初始化Agent: {self.name}")

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        执行Agent任务

        子类必须实现此方法
        """
        pass

    def log_start(self):
        """记录任务开始"""
        logger.info(f"[{self.name}] 任务开始")

    def log_complete(self, result: Any = None):
        """记录任务完成"""
        logger.info(f"[{self.name}] 任务完成")
        if result:
            logger.debug(f"[{self.name}] 结果: {result}")

    def log_error(self, error: Exception):
        """记录错误"""
        logger.error(f"[{self.name}] 出错: {str(error)}")
