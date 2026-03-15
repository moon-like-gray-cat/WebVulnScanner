import os

# ==========================================
# 全局配置文件
# ==========================================

# --- 扫描控制 ---
CONCURRENCY = 20          # 默认并发数（信号量控制）
TIMEOUT = 10              # HTTP 请求超时时间（秒）
RETRIES = 2               # 请求失败重试次数

# --- 网络设置 ---
# 如果需要挂代理（如 Burp Suite 或 科学上网），在这里设置
# 格式示例: "http://127.0.0.1:8080"
PROXY = None

# 常用 Header 设置
HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
}

# --- 输出与日志 ---
LOG_LEVEL = "INFO"        # 日志等级: DEBUG, INFO, SUCCESS, WARNING, ERROR
REPORT_DIR = "reports"     # 报告保存目录

# --- 指纹与插件 ---
FINGERPRINT_FILE = "fingerprints.yaml"
PLUGINS_DIR = "plugins"

# 确保报告目录存在
if not os.path.exists(REPORT_DIR):
    os.makedirs(REPORT_DIR)