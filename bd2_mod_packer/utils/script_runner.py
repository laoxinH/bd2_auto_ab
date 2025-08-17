#!/usr/bin/env python3
"""
脚本调用模块

在MOD打包完成后自动调用scripts目录中的脚本，并传递打包结果信息。

作者: BD2 MOD实验室
日期: 2025-08-16
"""

import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import tempfile
import os

logger = logging.getLogger(__name__)


class PackageResult:
    """打包结果信息类"""

    def __init__(self, workspace_name: str, mod_groups: Dict[str, List[str]] = None, mod_list: List[str] = None):
        self.package_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.workspace_name = workspace_name
        # 支持新的分组数据格式和旧的列表格式（向后兼容）
        self.mod_groups = mod_groups or {}
        self.mod_list = mod_list or []

        # 如果有分组数据，计算总数；否则使用列表数据
        if self.mod_groups:
            self.mod_count = sum(len(mods) for mods in self.mod_groups.values())
        else:
            self.mod_count = len(self.mod_list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {
            "package_time": self.package_time,
            "workspace_name": self.workspace_name,
            "mod_count": self.mod_count
        }

        # 如果有分组数据，使用分组格式；否则使用列表格式
        if self.mod_groups:
            result["mod_groups"] = self.mod_groups
        else:
            result["mod_list"] = self.mod_list

        return result

    def to_text_format(self) -> str:
        """转换为文本格式（与根目录打包结果信息.txt格式一致）"""
        text = f"打包时间：{self.package_time}\n"
        text += f"作者：{self.workspace_name}\n"
        text += f"MOD数量：{self.mod_count}\n"
        text += "---------------------------\n"

        if self.mod_groups:
            # 按分组格式化
            group_index = 1
            for target_dir, mod_names in self.mod_groups.items():
                # text += f"\n【{target_dir}】\n"
                text += f"MOD文件路径：{target_dir}\n"
                # for mod_name in mod_names:
                #     text += f"{group_index}.{mod_name}\n"
                #     group_index += 1
                text += f"包含MOD数量：{len(mod_names)}\n"
                text += "详细MOD信息查看MOD路径下的README.txt"
                text += "---------------------------\n"
        else:
            # 传统列表格式
            for i, mod_name in enumerate(self.mod_list, 1):
                text += f"{i}.{mod_name}\n"

        text += "---------------------------\n"
        return text


class ScriptRunner:
    """脚本调用器"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.scripts_dir = project_root / "scripts"

    def run_scripts(self, package_result: PackageResult) -> None:
        """
        运行scripts目录中的所有脚本
        
        Args:
            package_result: 打包结果信息
        """
        if not self.scripts_dir.exists():
            logger.info("scripts目录不存在，跳过脚本调用")
            return

        # 获取所有脚本文件
        script_files = self._get_script_files()
        if not script_files:
            logger.info("scripts目录中没有找到可执行脚本，跳过脚本调用")
            return

        logger.info(f"📜 发现 {len(script_files)} 个脚本，开始执行...")

        # 保存打包结果信息到根目录
        # self._save_package_result_to_root(package_result)
        #
        # 逐个执行脚本
        for script_file in script_files:
            self._run_single_script(script_file, package_result)

    def _get_script_files(self) -> List[Path]:
        """获取scripts目录中的所有脚本文件"""
        script_files = []

        try:
            for file_path in self.scripts_dir.iterdir():
                if file_path.is_file() and self._is_executable_script(file_path):
                    script_files.append(file_path)

            # 按文件名排序，确保执行顺序一致
            script_files.sort(key=lambda x: x.name)

        except Exception as e:
            logger.error(f"获取脚本文件列表失败: {e}")

        return script_files

    def _is_executable_script(self, file_path: Path) -> bool:
        """判断文件是否为可执行脚本"""
        # 支持的脚本扩展名
        executable_extensions = {'.py', '.bat', '.cmd', '.sh', '.ps1', '.exe'}

        # 检查扩展名
        if file_path.suffix.lower() in executable_extensions:
            return True

        # 检查是否为可执行文件（Unix系统）
        try:
            return os.access(file_path, os.X_OK)
        except Exception:
            return False

    def _run_single_script(self, script_file: Path, package_result: PackageResult) -> None:
        """
        执行单个脚本
        
        Args:
            script_file: 脚本文件路径
            package_result: 打包结果信息
        """
        logger.info(f"🔧 执行脚本: {script_file.name}")

        try:
            result_json_string = json.dumps(package_result.to_dict(), ensure_ascii=False, indent=2)

            try:
                # 根据脚本类型选择执行方式
                cmd = self._build_script_command(script_file,result_json_string, package_result)

                # 根据脚本类型选择编码
                script_encoding = 'gbk' if script_file.suffix.lower() in ['.bat', '.cmd'] else 'utf-8'

                # 执行脚本
                result = subprocess.run(
                    cmd,
                    cwd=self.scripts_dir,  # 在scripts目录中执行
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5分钟超时
                    encoding=script_encoding,  # Windows批处理使用gbk编码
                    # stderr=subprocess.STDOUT,
                    errors='ignore'  # 忽略编码错误
                )

                if result.returncode == 0:
                    logger.info(f"✅ 脚本 {script_file.name} 执行成功")

                else:
                    logger.warning(f"⚠️  脚本 {script_file.name} 执行失败 (返回码: {result.returncode})")

                logger.info(f"脚本标准日志输出: {result.stdout.strip()}")
                logger.info(f"脚本信息日志输出: {result.stderr.strip()}")
            finally:
                pass

        except subprocess.TimeoutExpired:
            logger.error(f"❌ 脚本 {script_file.name} 执行超时")
        except Exception as e:
            logger.error(f"❌ 脚本 {script_file.name} 执行异常: {e}")

    def _build_script_command(self, script_file: Path, result_json_string : str , package_result: PackageResult) -> List[str]:
        """
        构建脚本执行命令

        Args:
            script_file: 脚本文件路径
            result_json_string: 结果JSON字符串
            package_result: 打包结果信息

        Returns:
            命令列表
        """
        suffix = script_file.suffix.lower()

        if suffix == '.py':
            # Python脚本
            return [
                sys.executable,
                str(script_file),
                result_json_string,
                package_result.to_text_format(),
                package_result.workspace_name,
                str(package_result.mod_count)
            ]
        elif suffix in ['.bat', '.cmd']:
            # Windows批处理脚本
            return [
                str(script_file),
                result_json_string,

                package_result.to_text_format(),
                package_result.workspace_name,
                str(package_result.mod_count)
            ]
        elif suffix == '.sh':
            # Shell脚本
            return [
                'bash',
                str(script_file),
                result_json_string,

                package_result.to_text_format(),
                package_result.workspace_name,
                str(package_result.mod_count)
            ]
        elif suffix == '.ps1':
            # PowerShell脚本
            return [
                'powershell',
                '-ExecutionPolicy', 'Bypass',
                '-File', str(script_file),
                result_json_string,

                package_result.to_text_format(),
                package_result.workspace_name,
                str(package_result.mod_count)
            ]
        elif suffix == '.exe':
            # 可执行文件
            return [
                str(script_file),
                result_json_string,

                package_result.to_text_format(),
                package_result.workspace_name,
                str(package_result.mod_count)
            ]
        else:
            # 默认直接执行
            return [
                str(script_file),
                result_json_string,
                package_result.to_text_format(),
                package_result.workspace_name,
                str(package_result.mod_count)
            ]

    def _save_package_result_to_root(self, package_result: PackageResult) -> None:
        """
        保存打包结果信息到根目录（与现有格式一致）

        Args:
            package_result: 打包结果信息
        """
        try:
            result_file = self.project_root / "打包结果信息.txt"
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(package_result.to_text_format())
            logger.info(f"✅ 打包结果信息已保存到: {result_file}")
        except Exception as e:
            logger.error(f"❌ 保存打包结果信息失败: {e}")
