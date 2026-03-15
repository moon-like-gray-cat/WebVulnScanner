# 基类
from abc import ABC, abstractmethod
from loguru import logger

class BasePoc(ABC):
    def __init__(self):
        # 基础属性，子类可以通过 super().__init__() 或直接赋值来覆盖
        self.name = "Base PoC"      # 插件名称（如：ThinkPHP 5.x RCE）
        self.app = "Common"         # 归属应用（如：SpringBoot, ThinkPHP, IIS）
        self.severity = "Low"       # 危害等级：Critical, High, Medium, Low, Info
        self.desc = "No description" # 插件描述

    @abstractmethod
    async def verify(self, url: str, client):
        """
        抽象方法：每个插件必须实现这个方法。
        :param url: 目标基础 URL (例如: http://example.com)
        :param client: 传入的 network/client.py 中的 AsyncHttpClient 实例
        :return: (is_vuln: bool, result_info: str/None)
        """
        pass

    def log_attempt(self, url):
        """内置一个简单的辅助方法，方便插件记录日志"""
        logger.debug(f"[{self.name}] 正在尝试检测目标: {url}")