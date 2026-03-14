import asyncio
from loguru import logger
from network.client import AsyncHttpClient
from core.loader import PluginLoader


class ScanEngine:
    def __init__(self, urls, concurrency=20, timeout=10):
        """
        :param urls: 目标 URL 列表
        :param concurrency: 最大并发数
        :param timeout: HTTP 超时时间
        """
        self.urls = urls
        self.concurrency = concurrency
        self.timeout = timeout
        self.loader = PluginLoader()
        self.results = []
        # 使用信号量控制并发数
        self.semaphore = asyncio.Semaphore(concurrency)

    async def scan_task(self, url, poc, client):
        """
        单个 PoC 对单个 URL 的扫描任务
        """
        # 自动管理并发：只有拿到“许可证”的任务才能继续执行
        async with self.semaphore:
            try:
                logger.debug(f"正在检测: {url} -> {poc.name}")
                is_vuln, info = await poc.verify(url, client)

                if is_vuln:
                    result = {
                        "url": url,
                        "poc_name": poc.name,
                        "severity": poc.severity,
                        "info": info
                    }
                    self.results.append(result)
                    logger.success(f"发现漏洞! [{poc.severity}] {url} : {poc.name}")
            except Exception as e:
                logger.error(f"插件执行异常 ({poc.name}) on {url}: {e}")

    async def run(self):
        """
        启动扫描引擎
        """
        # 1. 加载所有插件
        pocs = self.loader.load_all()
        if not pocs:
            logger.warning("未加载到任何插件，扫描终止。")
            return

        # 2. 初始化全局 HTTP 客户端
        client = AsyncHttpClient(timeout=self.timeout)

        # 3. 构造任务池
        tasks = []
        for url in self.urls:
            for poc in pocs:
                # 注意：这里可以加入指纹识别过滤逻辑
                # if poc.app == "Common" or poc.app == detected_app:
                tasks.append(self.scan_task(url, poc, client))

        logger.info(f"扫描开始：共 {len(self.urls)} 个目标，{len(pocs)} 个插件，总计 {len(tasks)} 个任务")

        # 4. 并发执行所有任务
        if tasks:
            await asyncio.gather(*tasks)

        # 5. 清理资源
        await client.close()
        logger.info(f"扫描任务完成，共发现 {len(self.results)} 个漏洞。")
        return self.results