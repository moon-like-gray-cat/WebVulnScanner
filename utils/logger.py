import sys
from loguru import logger
from pathlib import Path

def setup_logger(log_dir="logs"):
    """
    统一配置 WebVulnScanner 的日志系统
    - 屏幕输出：简洁、带颜色
    - 文件输出：详细、自动滚动、持久化
    """
    # 1. 创建日志目录
    Path(log_dir).mkdir(exist_ok=True)

    # 2. 移除 Loguru 默认配置
    logger.remove()

    # 3. 配置终端输出 (面向用户)
    # 仅显示小时:分:秒，保持界面整洁
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        level="INFO"
    )

    # 4. 配置日志文件 (面向开发者/后期审计)
    # 记录详细的日期时间，并保存 DEBUG 级别的详细信息
    log_file = Path(log_dir) / "scanner.log"
    logger.add(
        str(log_file),
        rotation="5 MB",      # 文件满 5MB 自动切分
        retention="7 days",   # 自动清理一周前的日志
        compression="zip",    # 旧日志自动压缩
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {file}:{line} | {message}",
        level="DEBUG"
    )

    return logger