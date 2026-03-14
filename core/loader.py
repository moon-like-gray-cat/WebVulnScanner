import importlib
import inspect
import pkgutil
from pathlib import Path
from loguru import logger
from plugins.base import BasePoc


class PluginLoader:
    def __init__(self, plugins_package="plugins"):
        """
        :param plugins_package: 插件所在的包名
        """
        self.plugins_package = plugins_package
        self.pocs = []

    def load_all(self):
        """
        自动扫描并加载指定包下的所有 PoC 类
        """
        self.pocs = []
        # 1. 找到 plugins 目录的绝对路径
        try:
            package = importlib.import_module(self.plugins_package)
        except ImportError as e:
            logger.error(f"无法导入插件目录 {self.plugins_package}: {e}")
            return []

        # 2. 遍历该包下的所有模块 (.py 文件)
        package_path = os.path.dirname(package.__file__)

        for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
            if is_pkg:
                continue  # 暂时跳过子目录

            # 构造完整的模块名，例如 plugins.spring_env_leak
            full_module_name = f"{self.plugins_package}.{module_name}"

            try:
                # 3. 动态导入模块
                module = importlib.import_module(full_module_name)

                # 4. 寻找模块里继承了 BasePoc 的类
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, BasePoc) and obj is not BasePoc:
                        # 实例化插件
                        instance = obj()
                        self.pocs.append(instance)
                        logger.debug(f"成功加载插件: [{instance.app}] {instance.name}")

            except Exception as e:
                logger.error(f"加载插件模块 {full_module_name} 出错: {e}")

        logger.info(f"共计加载成功 {len(self.pocs)} 个插件")
        return self.pocs


import os  # 别忘了导入 os