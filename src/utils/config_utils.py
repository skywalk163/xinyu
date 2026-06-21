"""
配置工具模块

提供统一的配置管理功能，减少重复的配置读取代码。
"""

import copy
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径（可选）
        """
        self.config_path = Path(config_path) if config_path else None
        self.config: Dict[str, Any] = {}
        self.loaded = False

    def file_exists(self) -> bool:
        """
        检查配置文件是否存在

        Returns:
            配置文件是否存在
        """
        return self.config_path is not None and self.config_path.exists()

    def load(self, config_path: Optional[Union[str, Path]] = None) -> bool:
        """
        加载配置文件

        Args:
            config_path: 配置文件路径（可选）

        Returns:
            是否加载成功
        """
        if config_path:
            self.config_path = Path(config_path)

        if not self.config_path or not self.config_path.exists():
            return False

        try:
            if self.config_path.suffix.lower() in [".yaml", ".yml"]:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = yaml.safe_load(f) or {}
            elif self.config_path.suffix.lower() == ".json":
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            else:
                # 尝试自动检测格式
                with open(self.config_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    try:
                        self.config = json.loads(content)
                    except json.JSONDecodeError:
                        try:
                            self.config = yaml.safe_load(content)
                        except yaml.YAMLError:
                            raise ValueError(f"无法解析配置文件: {self.config_path}")

            self.loaded = True
            return True

        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return False

    def save(
        self,
        config_data: Optional[Dict[str, Any]] = None,
        config_path: Optional[Union[str, Path]] = None,
    ) -> bool:
        """
        保存配置文件

        Args:
            config_data: 配置数据（可选，默认为当前配置）
            config_path: 配置文件路径（可选）

        Returns:
            是否保存成功
        """
        if config_path:
            self.config_path = Path(config_path)

        if not self.config_path:
            return False

        # 使用传入的配置数据或当前配置
        data_to_save = config_data if config_data is not None else self.config

        try:
            # 确保目录存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            if self.config_path.suffix.lower() in [".yaml", ".yml"]:
                with open(self.config_path, "w", encoding="utf-8") as f:
                    yaml.dump(data_to_save, f, default_flow_style=False)
            elif self.config_path.suffix.lower() == ".json":
                with open(self.config_path, "w", encoding="utf-8") as f:
                    json.dump(data_to_save, f, indent=2)
            else:
                # 默认使用JSON格式
                with open(self.config_path.with_suffix(".json"), "w", encoding="utf-8") as f:
                    json.dump(data_to_save, f, indent=2)

            return True

        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键（支持点号分隔，如 'database.host'）
            default: 默认值

        Returns:
            配置值或默认值
        """
        if not self.loaded and self.config_path:
            self.load()

        # 支持点号分隔的键
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        设置配置值

        Args:
            key: 配置键（支持点号分隔，如 'database.host'）
            value: 配置值
        """
        if not self.loaded and self.config_path:
            self.load()

        # 支持点号分隔的键
        keys = key.split(".")
        config = self.config

        # 遍历到最后一个键的父级
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]

        # 设置值
        config[keys[-1]] = value

    def update(self, updates: Dict[str, Any]) -> None:
        """
        批量更新配置

        Args:
            updates: 更新字典
        """
        for key, value in updates.items():
            self.set(key, value)

    def delete(self, key: str) -> bool:
        """
        删除配置项

        Args:
            key: 配置键（支持点号分隔）

        Returns:
            是否删除成功
        """
        if not self.loaded and self.config_path:
            self.load()

        # 支持点号分隔的键
        keys = key.split(".")
        config = self.config

        # 遍历到最后一个键的父级
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                return False
            config = config[k]

        # 删除值
        if keys[-1] in config:
            del config[keys[-1]]
            return True

        return False

    def merge(self, other_config: Dict[str, Any], overwrite: bool = True) -> None:
        """
        合并其他配置

        Args:
            other_config: 其他配置字典
            overwrite: 是否覆盖现有值
        """
        self._merge_dicts(self.config, other_config, overwrite)

    def _merge_dicts(self, target: Dict, source: Dict, overwrite: bool = True) -> None:
        """递归合并字典"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_dicts(target[key], value, overwrite)
            elif overwrite or key not in target:
                target[key] = copy.deepcopy(value)

    def to_dict(self) -> Dict[str, Any]:
        """
        获取配置字典的副本

        Returns:
            配置字典
        """
        return copy.deepcopy(self.config)

    def clear(self) -> None:
        """清空配置"""
        self.config = {}

    def get_config(self) -> Dict[str, Any]:
        """
        获取配置字典

        Returns:
            配置字典
        """
        if not self.loaded and self.config_path:
            self.load()
        return self.config.copy()

    def reload(self) -> bool:
        """
        重新加载配置文件

        Returns:
            是否重新加载成功
        """
        if self.config_path:
            return self.load(self.config_path)
        return False


# 全局配置管理器实例
_global_config = None


def get_global_config() -> ConfigManager:
    """
    获取全局配置管理器

    Returns:
        全局配置管理器实例
    """
    global _global_config
    if _global_config is None:
        _global_config = ConfigManager()
    return _global_config


def load_config(
    config_path: Union[str, Path], default_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径
        default_config: 默认配置（可选）

    Returns:
        配置字典
    """
    config_path = Path(config_path)

    if not config_path.exists():
        if default_config:
            # 创建默认配置
            config_path.parent.mkdir(parents=True, exist_ok=True)
            save_config(config_path, default_config)
            return default_config.copy()
        else:
            return {}

    try:
        if config_path.suffix.lower() in [".yaml", ".yml"]:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        elif config_path.suffix.lower() == ".json":
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # 尝试自动检测
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    try:
                        return yaml.safe_load(content) or {}
                    except yaml.YAMLError:
                        raise ValueError(f"无法解析配置文件: {config_path}")
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        return default_config.copy() if default_config else {}


def save_config(config_path: Union[str, Path], config: Dict[str, Any]) -> bool:
    """
    保存配置文件

    Args:
        config_path: 配置文件路径
        config: 配置字典

    Returns:
        是否保存成功
    """
    config_path = Path(config_path)

    try:
        # 确保目录存在
        config_path.parent.mkdir(parents=True, exist_ok=True)

        if config_path.suffix.lower() in [".yaml", ".yml"]:
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False)
        else:
            # 默认使用JSON格式
            with open(config_path.with_suffix(".json"), "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)

        return True

    except Exception as e:
        print(f"保存配置文件失败: {e}")
        return False


def get_config_value(config: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    从配置字典中获取值（支持点号分隔键）

    Args:
        config: 配置字典
        key: 配置键（支持点号分隔，如 'database.host'）
        default: 默认值

    Returns:
        配置值或默认值
    """
    # 支持点号分隔的键
    keys = key.split(".")
    value = config

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default

    return value


def set_config_value(config: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
    """
    在配置字典中设置值（支持点号分隔键）

    Args:
        config: 配置字典
        key: 配置键（支持点号分隔，如 'database.host'）
        value: 配置值

    Returns:
        更新后的配置字典
    """
    # 创建副本
    result = copy.deepcopy(config)

    # 支持点号分隔的键
    keys = key.split(".")
    current = result

    # 遍历到最后一个键的父级
    for k in keys[:-1]:
        if k not in current or not isinstance(current[k], dict):
            current[k] = {}
        current = current[k]

    # 设置值
    current[keys[-1]] = value

    return result


def merge_configs(
    base_config: Dict[str, Any], override_config: Dict[str, Any], overwrite: bool = True
) -> Dict[str, Any]:
    """
    合并两个配置字典

    Args:
        base_config: 基础配置
        override_config: 覆盖配置
        overwrite: 是否覆盖现有值

    Returns:
        合并后的配置字典
    """
    result = copy.deepcopy(base_config)

    def _merge(target: Dict, source: Dict):
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                _merge(target[key], value)
            elif overwrite or key not in target:
                target[key] = copy.deepcopy(value)

    _merge(result, override_config)
    return result


# 环境变量配置支持
def load_from_env(prefix: str = "APP_") -> Dict[str, Any]:
    """
    从环境变量加载配置

    Args:
        prefix: 环境变量前缀

    Returns:
        配置字典
    """
    config = {}

    for key, value in os.environ.items():
        if key.startswith(prefix):
            # 移除前缀并转换为小写
            config_key = key[len(prefix) :].lower()

            # 支持嵌套配置（使用双下划线分隔）
            keys = config_key.split("__")
            current = config

            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]

            # 尝试解析值
            try:
                # 尝试解析为JSON
                parsed_value = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                # 如果不是JSON，保持原样
                parsed_value = value

            current[keys[-1]] = parsed_value

    return config


def config_to_env(config: Dict[str, Any], prefix: str = "APP_") -> Dict[str, str]:
    """
    将配置字典转换为环境变量格式

    Args:
        config: 配置字典
        prefix: 环境变量前缀

    Returns:
        环境变量字典
    """
    env_vars = {}

    def _flatten_dict(prefix_path: str, data: Dict):
        for key, value in data.items():
            full_key = f"{prefix_path}__{key}" if prefix_path else key

            if isinstance(value, dict):
                _flatten_dict(full_key, value)
            else:
                # 将值转换为字符串
                if isinstance(value, (list, dict)):
                    str_value = json.dumps(value)
                else:
                    str_value = str(value)

                env_key = f"{prefix}{full_key.upper().replace('.', '__')}"
                env_vars[env_key] = str_value

    _flatten_dict("", config)
    return env_vars
