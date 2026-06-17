"""
文件工具模块

提供统一的文件操作函数，减少重复的文件读写代码。
"""

import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, List, Optional, Union

import yaml


def read_json_file(filepath: Union[str, Path], default: Any = None, encoding: str = "utf-8") -> Any:
    """
    读取JSON文件

    Args:
        filepath: 文件路径
        default: 如果文件不存在或读取失败时的默认值
        encoding: 文件编码

    Returns:
        JSON数据或默认值
    """
    try:
        with open(filepath, "r", encoding=encoding) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        if default is not None:
            return default
        raise e


def write_json_file(
    filepath: Union[str, Path], data: Any, indent: int = 2, default=str, encoding: str = "utf-8"
) -> None:
    """
    写入JSON文件

    Args:
        filepath: 文件路径
        data: 要写入的数据
        indent: 缩进空格数
        default: 序列化函数
        encoding: 文件编码
    """
    # 确保目录存在
    dirname = os.path.dirname(filepath)
    if dirname:  # 只有在有目录时才创建
        os.makedirs(dirname, exist_ok=True)

    with open(filepath, "w", encoding=encoding) as f:
        json.dump(data, f, indent=indent, default=default)


def read_yaml_file(filepath: Union[str, Path], default: Any = None, encoding: str = "utf-8") -> Any:
    """
    读取YAML文件

    Args:
        filepath: 文件路径
        default: 如果文件不存在或读取失败时的默认值
        encoding: 文件编码

    Returns:
        YAML数据或默认值
    """
    try:
        with open(filepath, "r", encoding=encoding) as f:
            return yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError) as e:
        if default is not None:
            return default
        raise e


def write_yaml_file(
    filepath: Union[str, Path], data: Any, default_flow_style: bool = False, encoding: str = "utf-8"
) -> None:
    """
    写入YAML文件

    Args:
        filepath: 文件路径
        data: 要写入的数据
        default_flow_style: YAML流式风格
        encoding: 文件编码
    """
    # 确保目录存在
    dirname = os.path.dirname(filepath)
    if dirname:  # 只有在有目录时才创建
        os.makedirs(dirname, exist_ok=True)

    with open(filepath, "w", encoding=encoding) as f:
        yaml.dump(data, f, default_flow_style=default_flow_style)


def ensure_directory(directory: Union[str, Path]) -> str:
    """
    确保目录存在，如果不存在则创建

    Args:
        directory: 目录路径

    Returns:
        目录路径
    """
    os.makedirs(directory, exist_ok=True)
    return str(directory)


def get_file_hash(
    filepath: Union[str, Path], algorithm: str = "md5", chunk_size: int = 8192
) -> str:
    """
    计算文件哈希值

    Args:
        filepath: 文件路径
        algorithm: 哈希算法（md5, sha1, sha256）
        chunk_size: 读取块大小

    Returns:
        文件哈希值
    """
    hash_func = getattr(hashlib, algorithm)()

    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def copy_file_with_backup(
    src: Union[str, Path], dst: Union[str, Path], backup_suffix: str = ".bak"
) -> bool:
    """
    复制文件并创建备份

    Args:
        src: 源文件路径
        dst: 目标文件路径
        backup_suffix: 备份文件后缀

    Returns:
        是否成功
    """
    try:
        src_path = Path(src)
        dst_path = Path(dst)

        # 如果目标文件存在，创建备份
        if dst_path.exists():
            backup_path = dst_path.with_suffix(dst_path.suffix + backup_suffix)
            shutil.copy2(dst_path, backup_path)

        # 复制文件
        shutil.copy2(src_path, dst_path)
        return True
    except Exception:
        return False


def find_files_by_pattern(
    directory: Union[str, Path], pattern: str = "*.py", recursive: bool = True
) -> List[Path]:
    """
    查找匹配模式的文件

    Args:
        directory: 目录路径
        pattern: 文件模式（如 '*.py', '*.json'）
        recursive: 是否递归查找

    Returns:
        文件路径列表
    """
    directory = Path(directory)
    if recursive:
        return list(directory.rglob(pattern))
    else:
        return list(directory.glob(pattern))


def read_file_lines(filepath: Union[str, Path], encoding: str = "utf-8") -> List[str]:
    """
    读取文件的所有行

    Args:
        filepath: 文件路径
        encoding: 文件编码

    Returns:
        文件行列表
    """
    with open(filepath, "r", encoding=encoding) as f:
        return f.readlines()


def write_file_lines(filepath: Union[str, Path], lines: List[str], encoding: str = "utf-8") -> None:
    """
    写入文件行

    Args:
        filepath: 文件路径
        lines: 要写入的行列表
        encoding: 文件编码
    """
    # 确保目录存在
    dirname = os.path.dirname(filepath)
    if dirname:  # 只有在有目录时才创建
        os.makedirs(dirname, exist_ok=True)

    with open(filepath, "w", encoding=encoding) as f:
        f.writelines(lines)


def create_temp_file(
    content: str = "",
    suffix: str = ".tmp",
    prefix: str = "temp_",
    directory: Optional[Union[str, Path]] = None,
) -> str:
    """
    创建临时文件

    Args:
        content: 文件内容
        suffix: 文件后缀
        prefix: 文件前缀
        directory: 临时文件目录

    Returns:
        临时文件路径
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=suffix, prefix=prefix, dir=directory, delete=False, encoding="utf-8"
    ) as f:
        f.write(content)
        return f.name


def get_file_size(filepath: Union[str, Path]) -> int:
    """
    获取文件大小（字节）

    Args:
        filepath: 文件路径

    Returns:
        文件大小（字节）
    """
    return os.path.getsize(filepath)


def get_file_extension(filepath: Union[str, Path]) -> str:
    """
    获取文件扩展名

    Args:
        filepath: 文件路径

    Returns:
        文件扩展名（小写，不带点）
    """
    return Path(filepath).suffix.lower().lstrip(".")


def is_binary_file(filepath: Union[str, Path]) -> bool:
    """
    判断文件是否为二进制文件

    Args:
        filepath: 文件路径

    Returns:
        是否为二进制文件
    """
    try:
        with open(filepath, "tr") as f:
            f.read()
        return False
    except UnicodeDecodeError:
        return True


def ensure_dir(directory: Union[str, Path]) -> None:
    """
    确保目录存在

    Args:
        directory: 目录路径
    """
    os.makedirs(directory, exist_ok=True)
