import asyncio
import sys
import argparse
from loguru import logger
from core.engine import ScanEngine
import config
from utils.reporter import MarkdownReporter

# 启动 Logo
BANNER = r"""
<red>
       ____
      /    \      <white>_______________________________</white>
     /      \    <white>/                               \</white>
    |  O  O  |   <white>|  Everything is Fine.         |</white>
    |   /\   |  <cyan><- </cyan><white>|  (Just scanning for vulns)   |</white>
    \        /    <white>\_______________________________/</white>
     \______/
        ||
      __||__
     /      \
    /________\
    |        |
    |  TEA   |   <yellow>~~~~</yellow>
    |________|
<red>
~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 
  (Fire) (Fire) (Fire) (Fire) (Fire)
<white>
-----------------------------------------------
   <yellow>WebPulse v1.1 - "Chaos Engineering" Edition</yellow>
-----------------------------------------------
</white>
"""

def setup_logger():
    """配置 Loguru 日志格式"""
    logger.remove()  # 移除默认配置
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        level="INFO"
    )

async def main():
    # 1. 打印 Logo
    print(BANNER)
    setup_logger()

    # 2. 参数解析
    parser = argparse.ArgumentParser(description="WebPulse: A high-performance web vulnerability scanner.")
    parser.add_argument("-u", "--url", help="Target URL (e.g., http://example.com)")
    parser.add_argument("-f", "--file", help="File containing target URLs")
    parser.add_argument("-c", "--concurrency", type=int, default=20, help="Max concurrency (default: 20)")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="Request timeout (default: 10)")

    args = parser.parse_args()

    # 3. 处理目标
    targets = []
    if args.url:
        targets.append(args.url)
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                targets = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"找不到文件: {args.file}")
            return
    else:
        parser.print_help()
        return

    # 4. 启动引擎
    # engine = ScanEngine(urls=targets, concurrency=args.concurrency, timeout=args.timeout)
    # 使用配置项
    engine = ScanEngine(
        urls=targets,
        concurrency=config.CONCURRENCY,
        timeout=config.TIMEOUT
    )
    results = await engine.run()

    # 5. 扫描结束总结
    reporter = MarkdownReporter()
    reporter.generate(results)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("\n用户强制退出扫描。")
        sys.exit(0)