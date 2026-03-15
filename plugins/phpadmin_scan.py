# 是否存在 数据库管理后台
from plugins.base import BasePoc

class Poc(BasePoc):
    def __init__(self):
        super().__init__()
        self.name = "phpMyAdmin Dashboard Found"
        self.app = "PHP"
        self.severity = "Medium"

    async def verify(self, url, client):
        paths = ["/phpmyadmin/", "/pma/", "/pmd/"]
        for path in paths:
            target_url = url.rstrip('/') + path
            try:
                resp = await client.get(target_url)
                if resp.status_code == 200 and "phpMyAdmin" in resp.text:
                    return True, f"phpMyAdmin console found at: {target_url}"
            except Exception:
                continue
        return False, None