import os
import logging
from openai import OpenAI

from exceptions import LLMAPIError
from retry import retry
from cost_logger import cost_logger
from logger import get_logger
from dotenv import load_dotenv

load_dotenv()


logger = get_logger("LLMClient")


class LLMClient:
    def __init__(self, api_key=None, model="deepseek-chat", base_url="https://api.deepseek.com"):
        # 1. 获取 API key
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("API key 未提供，请设置环境变量 DEEPSEEK_API_KEY 或传入 api_key 参数")

        # 2. 保存配置
        self.model = model
        self.base_url = base_url

        # 3. 初始化 OpenAI 客户端
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

        # 4. 记录日志
        logger.info(f"LLMClient 初始化完成，模型：{self.model}")


    @retry(max_retries=3, backoff=2)
    @cost_logger("llm_cost.csv")
    def chat(self, messages, temperature=0.7, top_p=1.0, max_tokens=1024, **kwargs):
        """同步调用大模型"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                **kwargs
            )
            return response
        except Exception as e:
            logger.error(f"API 调用失败: {e}")
            raise LLMAPIError(f"API调用失败: {e}")


    @retry(max_retries=3, backoff=2)
    @cost_logger("llm_cost.csv")
    async def achat(self, messages, temperature=0.7, top_p=1.0, max_tokens=1024, **kwargs):
        """异步调用大模型"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                **kwargs
            )
            return response
        except Exception as e:
            logger.error(f"异步 API 调用失败: {e}")
            raise LLMAPIError(f"API调用失败: {e}")