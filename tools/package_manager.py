# -*- coding: utf-8 -*-
"""心语包管理器

提供第三方库管理功能：
- 安装包
- 卸载包
- 列出已安装包
- 搜索包
- 更新包
"""

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class PackageManager:
    """包管理器"""

    def __init__(self, root_dir: str = None):
        """初始化包管理器

        Args:
            root_dir: 项目根目录
        """
        self.root_dir = Path(root_dir or os.getcwd())
        self.packages_dir = self.root_dir / "packages"
        self.registry_file = self.root_dir / "xinyu-packages.json"
        self.installed_file = self.packages_dir / "installed.json"

        # 确保目录存在
        self.packages_dir.mkdir(exist_ok=True)

        # 初始化已安装包记录
        if not self.installed_file.exists():
            self._save_installed({})

    def _load_installed(self) -> Dict:
        """加载已安装包记录"""
        if self.installed_file.exists():
            with open(self.installed_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_installed(self, installed: Dict):
        """保存已安装包记录"""
        with open(self.installed_file, "w", encoding="utf-8") as f:
            json.dump(installed, f, indent=2, ensure_ascii=False)

    def install(self, package_name: str, version: str = None) -> bool:
        """安装包

        Args:
            package_name: 包名
            version: 版本号（可选）

        Returns:
            bool: 是否成功
        """
        print(f"正在安装 {package_name}...")

        # 模拟从注册表获取包信息
        package_info = self._fetch_package_info(package_name, version)

        if not package_info:
            print(f"错误：找不到包 {package_name}")
            return False

        # 下载包（这里模拟）
        package_dir = self.packages_dir / package_name
        package_dir.mkdir(exist_ok=True)

        # 创建包文件
        package_file = package_dir / f"{package_name}.yan"
        with open(package_file, "w", encoding="utf-8") as f:
            f.write(package_info.get("code", f"# {package_name}\n"))

        # 更新已安装记录
        installed = self._load_installed()
        installed[package_name] = {
            "version": package_info.get("version", "1.0.0"),
            "path": str(package_dir),
            "installed_at": str(os.path.getctime(package_file)),
        }
        self._save_installed(installed)

        print(f"✅ 成功安装 {package_name}@{package_info.get('version', '1.0.0')}")
        return True

    def uninstall(self, package_name: str) -> bool:
        """卸载包

        Args:
            package_name: 包名

        Returns:
            bool: 是否成功
        """
        installed = self._load_installed()

        if package_name not in installed:
            print(f"错误：包 {package_name} 未安装")
            return False

        # 删除包目录
        package_dir = Path(installed[package_name]["path"])
        if package_dir.exists():
            shutil.rmtree(package_dir)

        # 更新已安装记录
        del installed[package_name]
        self._save_installed(installed)

        print(f"✅ 成功卸载 {package_name}")
        return True

    def list_installed(self) -> List[Dict]:
        """列出已安装包

        Returns:
            List[Dict]: 已安装包列表
        """
        installed = self._load_installed()
        packages = []

        for name, info in installed.items():
            packages.append({"name": name, "version": info["version"], "path": info["path"]})

        return packages

    def search(self, keyword: str) -> List[Dict]:
        """搜索包

        Args:
            keyword: 搜索关键词

        Returns:
            List[Dict]: 搜索结果
        """
        # 模拟搜索结果
        mock_packages = [
            {"name": "http", "version": "1.0.0", "description": "HTTP客户端库"},
            {"name": "json", "version": "1.0.0", "description": "JSON处理库"},
            {"name": "database", "version": "1.0.0", "description": "数据库操作库"},
            {"name": "crypto", "version": "1.0.0", "description": "加密解密库"},
            {"name": "datetime", "version": "1.0.0", "description": "日期时间库"},
        ]

        results = []
        for pkg in mock_packages:
            if (
                keyword.lower() in pkg["name"].lower()
                or keyword.lower() in pkg["description"].lower()
            ):
                results.append(pkg)

        return results

    def update(self, package_name: str = None) -> bool:
        """更新包

        Args:
            package_name: 包名（可选，不指定则更新所有）

        Returns:
            bool: 是否成功
        """
        if package_name:
            # 更新指定包
            return self.install(package_name)
        else:
            # 更新所有包
            installed = self._load_installed()
            success = True

            for name in installed:
                if not self.install(name):
                    success = False

            return success

    def _fetch_package_info(self, package_name: str, version: str = None) -> Optional[Dict]:
        """从注册表获取包信息（模拟）

        Args:
            package_name: 包名
            version: 版本号

        Returns:
            Optional[Dict]: 包信息
        """
        # 模拟包注册表
        mock_registry = {
            "http": {
                "version": "1.0.0",
                "description": "HTTP客户端库",
                "code": """# http.yan
函数 获取：
  参数 url。
  import requests。
  返回 requests.get(url)。

函数 提交：
  参数 url。
  参数 data。
  import requests。
  返回 requests.post(url, data=data)。
""",
            },
            "json": {
                "version": "1.0.0",
                "description": "JSON处理库",
                "code": """# json.yan
函数 解析：
  参数 s。
  import json。
  返回 json.loads(s)。

函数 序列化：
  参数 obj。
  import json。
  返回 json.dumps(obj, ensure_ascii=False)。
""",
            },
            "database": {
                "version": "1.0.0",
                "description": "数据库操作库",
                "code": """# database.yan
函数 连接：
  参数 connection_string。
  import sqlite3。
  返回 sqlite3.connect(connection_string)。

函数 查询：
  参数 conn。
  参数 sql。
  定义 cursor = conn.cursor()。
  cursor.execute(sql)。
  返回 cursor.fetchall()。
""",
            },
        }

        return mock_registry.get(package_name)


# 命令行接口
if __name__ == "__main__":
    import sys

    pm = PackageManager()

    if len(sys.argv) < 2:
        print("用法：")
        print("  xinyu-pm install <包名>    - 安装包")
        print("  xinyu-pm uninstall <包名>  - 卸载包")
        print("  xinyu-pm list              - 列出已安装包")
        print("  xinyu-pm search <关键词>   - 搜索包")
        print("  xinyu-pm update [包名]     - 更新包")
        sys.exit(1)

    command = sys.argv[1]

    if command == "install":
        if len(sys.argv) < 3:
            print("错误：请指定包名")
            sys.exit(1)
        pm.install(sys.argv[2])

    elif command == "uninstall":
        if len(sys.argv) < 3:
            print("错误：请指定包名")
            sys.exit(1)
        pm.uninstall(sys.argv[2])

    elif command == "list":
        packages = pm.list_installed()
        if packages:
            print("已安装的包：")
            for pkg in packages:
                print(f"  - {pkg['name']}@{pkg['version']}")
        else:
            print("没有已安装的包")

    elif command == "search":
        if len(sys.argv) < 3:
            print("错误：请指定搜索关键词")
            sys.exit(1)
        results = pm.search(sys.argv[2])
        if results:
            print("搜索结果：")
            for pkg in results:
                print(f"  - {pkg['name']}@{pkg['version']}: {pkg['description']}")
        else:
            print("没有找到匹配的包")

    elif command == "update":
        if len(sys.argv) >= 3:
            pm.update(sys.argv[2])
        else:
            pm.update()

    else:
        print(f"错误：未知命令 {command}")
        sys.exit(1)
