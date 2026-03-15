# 某些框架 会将 敏感信息刚在根目录下的 .env
from plugins.base import BasePoc

class Poc(BasePoc):
    def __init__(self):
        super().__init__()
        self.name = "Environment File Disclosure"
        self.app = "Common"  # 任何框架都可能存在
        self.severity = "High"

    async def verify(self, url, client):
        target_url = url.rstrip('/') + "/.env"
        try:
            resp = await client.get(target_url)
            # 匹配典型的环境变量格式：KEY=VALUE
            if resp.status_code == 200 and "DB_PASSWORD" in resp.text or "APP_KEY" in resp.text:
                return True, f"Critical config leaked: {target_url}"
        except Exception:
            pass
        return False, None