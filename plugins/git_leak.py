from plugins.base import BasePoc
from loguru import logger


class Poc(BasePoc):
    def __init__(self):
        super().__init__()
        self.name = "Git Repository Disclosure"  # 插件名称
        self.app = "Common"  # 无需特定指纹，全平台扫描
        self.severity = "High"  # 危害等级
        self.desc = "检测目标是否存在 .git 目录泄露，可能导致源代码和敏感配置泄露。"

    async def verify(self, url, client):
        """
        核心检测逻辑
        """
        # 1. 拼接探测路径
        # 访问 .git/config 是判断 Git 泄露最稳妥的方式
        target_url = url.rstrip('/') + "/.git/config"

        try:
            # 2. 发起异步请求
            # 使用我们在 network/client.py 中封装的异步客户端
            response = await client.get(target_url)

            # 3. 结果判断
            # 如果返回 200，且包含 Git 配置文件的特有关键字，则确认存在漏洞
            if response.status_code == 200:
                content = response.text
                if "repositoryformatversion" in content or "[core]" in content:
                    # 返回 True 表示存在漏洞，并附带证据
                    return True, f"Found .git/config leak! URL: {target_url}"

            # 4. 进阶检测：如果是 403，可能存在目录但禁止访问，可以在这里扩展其他探测逻辑

        except Exception as e:
            # 记录日志，但不让插件崩溃影响整体扫描
            logger.debug(f"[Poc: {self.name}] 执行异常: {e}")

        return False, None