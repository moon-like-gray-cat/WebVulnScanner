# WebVulnScanner

**WebVulnScanner** 是一款基于 Python 异步协程开发的高性能 Web 漏洞扫描框架。它采用“指纹探测 + 精确 PoC 验证”的两级架构，旨在实现大规模目标下的快速、准确评估。

---

## 核心特性

* **极速并发**：基于 `httpx` + `asyncio` 的全异步引擎，支持数百个任务并发调度。
* **智能指纹**：预设轻量级指纹库，根据目标 Web 框架自动匹配相关插件，拒绝盲目扫描。
* **插件化设计**：采用统一基类 `BasePoc`，开发者只需关注漏洞检测逻辑即可快速扩展。
* **现代工具链**：完全适配 `uv` 依赖管理方案，实现一键环境配置与运行。
* **专业报告**：扫描结束自动生成 Markdown 格式的漏洞详情报告。

---

## 快速启动

### 1. 环境准备
确保你已安装 [uv](https://github.com/astral-sh/uv)。

```bash
# 克隆项目
git clone https://github.com/moon-like-gray-cat/WebVulnScanner.git

cd WebVulnScanner

# 安装依赖
uv sync
```
### 2. 运行扫描

```bash
# 扫描单个 URL
uv run main.py -u [http://example.com](http://example.com)

# 批量扫描文件中的目标
uv run main.py -f targets.txt
```
### 3.项目结构
```angular2html
WebVulnScanner/
├── core/               # 核心引擎 (Loader, Engine)
├── network/            # 网络模块 (Async Client)
├── plugins/            # 漏洞插件 (ThinkPHP, GitLeak, etc.)
├── utils/              # 工具类 (Reporter, Logger)
├── fingerprints.yaml   # 指纹特征库
├── config.py           # 全局配置 (并发数, 超时时间)
└── main.py             # 入口程序
```
### 4.插件开发
只需在 plugins/ 目录下创建 Python 文件并继承 BasePoc
```python
from plugins.base import BasePoc

class Poc(BasePoc):
    def __init__(self):
        super().__init__()
        self.name = "漏洞名称"
        self.app = "关联指纹"  # 匹配 fingerprints.yaml 中的 name

    async def verify(self, url, client):
        # 编写检测逻辑
        return True/False, "证据信息"
```

### 5.免责声明
本工具仅用于合法合规的安全检测与学习研究。用户因使用本工具导致的任何法律纠纷，由使用者自行承担，开发者不承担任何责任。
