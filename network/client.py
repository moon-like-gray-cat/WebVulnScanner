# 使用 httpx 做异步处理，比传统的requests快得多
import httpx
import random
import urllib3

# 禁用不安全的请求警告（针对自签名证书）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
]

class AsyncHttpClient:
    def __init__(self, timeout=10, proxy=None):
        # 限制连接池大小，防止并发过高被系统熔断
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        self.client = httpx.AsyncClient(
            timeout=timeout,
            proxy=proxy,
            verify=False,
            limits=limits,
            follow_redirects=True
        )

    async def get(self, url, **kwargs):
        headers = kwargs.get("headers", {})
        if "User-Agent" not in headers:
            headers["User-Agent"] = random.choice(UA_LIST)
        return await self.client.get(url, headers=headers, **kwargs)

    async def post(self, url, data=None, json=None, **kwargs):
        headers = kwargs.get("headers", {})
        if "User-Agent" not in headers:
            headers["User-Agent"] = random.choice(UA_LIST)
        return await self.client.post(url, data=data, json=json, headers=headers, **kwargs)

    async def close(self):
        await self.client.aclose()