import re
import yaml
from pathlib import Path
from loguru import logger


class Fingerprinter:
    def __init__(self, config_path="fingerprints.yaml"):
        self.config_path = config_path
        self.rules = self._load_rules()

    def _load_rules(self):
        """从 YAML 加载规则"""
        try:
            if not Path(self.config_path).exists():
                logger.warning(f"指纹库文件 {self.config_path} 不存在，将使用空规则。")
                return []

            with open(self.config_path, "r", encoding="utf-8") as f:
                rules = yaml.safe_load(f)
                logger.info(f"成功加载 {len(rules)} 条指纹识别规则。")
                return rules
        except Exception as e:
            logger.error(f"加载指纹库失败: {e}")
            return []

    def identify(self, header_str, body_text):
        """
        根据响应头和内容识别框架
        :return: 标签列表 (list)
        """
        tags = ["Common"]  # 默认包含通用标签

        for rule in self.rules:
            app_name = rule.get("name")
            matched = False

            # 1. 匹配 Header (不区分大小写)
            headers_rule = rule.get("headers", {})
            for h_key, h_pattern in headers_rule.items():
                # 检查 Header 键是否存在，并正则匹配其值
                if h_key in header_str and re.search(h_pattern, header_str, re.I):
                    matched = True
                    break

            # 2. 如果 Header 没匹配上，匹配 Body
            if not matched:
                body_rules = rule.get("body", [])
                for keyword in body_rules:
                    if keyword in body_text:
                        matched = True
                        break

            if matched:
                tags.append(app_name)
                logger.debug(f"[Chaos-Radar] 发现指纹特征: {app_name}")

        return list(set(tags))