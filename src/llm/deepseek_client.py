"""DeepSeek API客户端模块"""
import os
from typing import Dict, Any, List
from openai import OpenAI
from loguru import logger

from ..utils.helpers import get_env


class DeepSeekClient:
    """DeepSeek API客户端"""

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        初始化DeepSeek客户端

        Args:
            api_key: API密钥
            base_url: API基础URL
        """
        self.api_key = api_key or get_env('DEEPSEEK_API_KEY')
        self.base_url = base_url or get_env('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')

        if not self.api_key:
            logger.warning("未设置DEEPSEEK_API_KEY环境变量")
            raise ValueError("请设置DEEPSEEK_API_KEY环境变量")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        logger.info("DeepSeek客户端初始化成功")

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek-chat",
        temperature: float = 0.3,
        max_tokens: int = 1000,
        response_format: Dict[str, str] = None
    ) -> str:
        """
        调用DeepSeek聊天API

        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            response_format: 响应格式(如 {"type": "json_object"})

        Returns:
            API响应文本
        """
        try:
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            if response_format:
                kwargs["response_format"] = response_format

            response = self.client.chat.completions.create(**kwargs)

            content = response.choices[0].message.content
            logger.info(f"API调用成功,返回 {len(content)} 字符")

            return content

        except Exception as e:
            logger.error(f"DeepSeek API调用失败: {e}")
            raise

    def generate_report(
        self,
        prompt: str,
        json_output: bool = True
    ) -> Dict[str, Any]:
        """
        生成投资建议报告

        Args:
            prompt: 提示词
            json_output: 是否输出JSON格式

        Returns:
            报告内容
        """
        messages = [
            {"role": "system", "content": "你是一个专业的股票投资分析师。"},
            {"role": "user", "content": prompt}
        ]

        response_format = {"type": "json_object"} if json_output else None

        response = self.chat(messages, response_format=response_format)

        if json_output:
            import json
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                logger.warning("JSON解析失败,返回原始文本")
                return {"raw_response": response}

        return response
