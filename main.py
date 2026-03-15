import asyncio
import sys
import argparse
from loguru import logger
from core.engine import ScanEngine
import config
from utils.reporter import MarkdownReporter
from utils.logger import setup_logger

# 1. 全局初始化日志（只需一次，放在最上方）
setup_logger()

# 极简 Banner
BANNER = r"""
[ WebVulnScanner ]----------------------------------------------------
| Status: Active   | Engine: Async     | Dev: Moon-Like-Gray-Cat      |
-----------------------------------------------------------------------
"""

async def main():
    # 2. 打印 Logo
    print(BANNER)

    # 3. 参数解析
    parser = argparse.ArgumentParser(description="WebVulnScanner: High-performance vulnerability scanner.")
    parser.add_argument("-u", "--url", help="Target URL (e.g., http://example.com)")
    parser.add_argument("-f", "--file", help="File containing target URLs")
    # 增加默认值关联 config.py，这样用户不输入时才用配置文件的值
    parser.add_argument("-c", "--concurrency", type=int, default=config.CONCURRENCY, help="Max concurrency")
    parser.add_argument("-t", "--timeout", type=int, default=config.TIMEOUT, help="Request timeout")

    args = parser.parse_args()

    # 4. 处理目标
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

    logger.info(f"任务启动 | 目标总数: {len(targets)} | 并发数: {args.concurrency}")

    # 5. 启动引擎 (使用解析后的 args，灵活性更高)
    engine = ScanEngine(
        urls=targets,
        concurrency=args.concurrency,
        timeout=args.timeout
    )
    results = await engine.run()

    # 6. 扫描结束总结
    if results:
        reporter = MarkdownReporter()
        report_path = reporter.generate(results)
        logger.success(f"扫描完成！发现 {len(results)} 个漏洞。报告已生成: {report_path}")
    else:
        logger.info("扫描完成，未发现安全漏洞。")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # 这里用 print 更干净，因为此时可能已经不需要日志格式了
        print("\n[!] 用户强制退出扫描。")
        sys.exit(0)