# shiro 中 rememberme 的 反序列化漏洞
from plugins.base import BasePoc

class Poc(BasePoc):
    def __init__(self):
        super().__init__()
        self.name = "Apache Shiro Default RememberMe Key"
        self.app = "Shiro"  # 联动 fingerprints.yaml 中的 Shiro 指纹
        self.severity = "Critical"

    async def verify(self, url, client):
        # 探测 Shiro 的最简单方式是查看响应头是否有 rememberMe=deleteMe
        headers = {"Cookie": "rememberMe=1"}
        try:
            resp = await client.get(url, headers=headers)
            set_cookie = str(resp.headers.get("Set-Cookie", ""))
            if "rememberMe=deleteMe" in set_cookie:
                return True, f"Target uses Apache Shiro. Key might be default (need tool check)."
        except Exception:
            pass
        return False, None