#!/usr/bin/env python3
"""
BD2 MOD Manager - 主程序管理器

统一的MOD管理器，集成所有功能模块，提供统一的接口。

主要功能：
- 工作区管理
- 资源下载和处理
- MOD打包
- 配置管理

作者: BD2 MOD实验室
日期: 2025-08-15
"""

import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

from .resource_manager import ReplaceTask

logger = logging.getLogger(__name__)


class BD2ModManager:
    """BD2 MOD管理器主类"""

    def __init__(self):
        """
        初始化MOD管理器
        
        使用配置系统管理所有路径，不再需要手动指定项目根目录
        """
        self.config = None
        self._initialize()

    def _initialize(self):
        """初始化管理器组件"""
        try:
            # 延迟导入避免循环依赖
            from ..config.settings import get_config
            self.config = get_config()
            # 从配置获取项目根目录
            self.project_root = self.config.project_root
            logger.info(f"BD2 MOD管理器初始化完成，项目根目录: {self.project_root}")
        except Exception as e:
            logger.error(f"BD2 MOD管理器初始化失败: {e}")
            raise

    def create_workspace(self, workspace_name: str) -> bool:
        """
        创建新的MOD工作区
        
        Args:
            workspace_name: 工作区名称
            
        Returns:
            是否创建成功
        """
        try:
            # 添加到配置
            success = self.config.add_mod_workspace(workspace_name)
            if not success:
                logger.error(f"添加工作区到配置失败: {workspace_name}")
                return False


            # 确保基础目录存在
            workspace_path = self.config.get_mod_workspace_path(workspace_name)
            workspace_path.mkdir(parents=True, exist_ok=True)
            # 创建IDLE和CUTSCENE目录
            for animation_type in ["IDLE", "CUTSCENE"]:
                (workspace_path / animation_type).mkdir(parents=True, exist_ok=True)

            logger.info(f"成功创建MOD工作区目录: {workspace_path}")
            return True

        except Exception as e:
            logger.error(f"创建MOD工作区失败: {e}")
            return False

    def delete_workspace(self, workspace_name: str, delete_files: bool = False) -> bool:
        """
        删除MOD工作区
        
        Args:
            workspace_name: 工作区名称
            delete_files: 是否删除物理文件
            
        Returns:
            是否删除成功
        """
        try:
            # 从配置中移除
            success = self.config.remove_mod_workspace(workspace_name)
            if not success:
                logger.error(f"从配置中移除工作区失败: {workspace_name}")
                return False

            # 删除物理文件（如果指定）
            if delete_files:
                workspace_path = self.config.get_mod_workspace_path(workspace_name)
                # print(f"正在删除工作区物理文件: {workspace_path}")
                if workspace_path.exists():
                    import shutil
                    shutil.rmtree(workspace_path)
                    logger.info(f"已删除工作区物理文件: {workspace_path}")

            logger.info(f"成功删除MOD工作区: {workspace_name}")
            return True

        except Exception as e:
            logger.error(f"删除MOD工作区失败: {e}")
            return False

    def list_workspaces(self) -> List[Dict[str, Any]]:
        """
        列出所有工作区及其信息
        
        Returns:
            工作区信息列表
        """
        workspaces = []
        try:
            workspace_names = self.config.get_mod_workspaces()

            for name in workspace_names:
                workspace_path = self.config.get_mod_workspace_path(name)
                workspace_info = {
                    'name': name,
                    'path': str(workspace_path),
                    'exists': workspace_path.exists(),
                    'mod_count': 0
                }

                if workspace_path.exists():
                    # 统计MOD数量（包含文件的文件夹）
                    workspace_info['mod_count'] = self._count_mod_folders(workspace_path)

                workspaces.append(workspace_info)

        except Exception as e:
            logger.error(f"列出工作区失败: {e}")

        return workspaces

    def _count_mod_folders(self, workspace_path: Path) -> int:
        """
        统计工作区中的MOD数量（包含文件的文件夹）
        
        Args:
            workspace_path: 工作区路径
            
        Returns:
            MOD数量
        """
        count = 0
        try:
            for item in workspace_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # 检查文件夹是否包含文件
                    if self._folder_contains_files(item):
                        count += 1
        except Exception:
            pass

        return count

    def _folder_contains_files(self, folder_path: Path) -> bool:
        """
        检查文件夹是否包含文件
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            是否包含文件
        """
        try:
            for item in folder_path.rglob('*'):
                if item.is_file() and not item.name.startswith('.'):
                    return True
        except Exception:
            pass

        return False

    def cleanup_empty_folders(self, workspace_name: Optional[str] = None) -> int:
        """
        清理空文件夹
        
        Args:
            workspace_name: 工作区名称，None表示清理所有工作区
            
        Returns:
            清理的文件夹数量
        """
        total_removed = 0
        try:
            if workspace_name:
                workspace_paths = [self.config.get_mod_workspace_path(workspace_name)]
            else:
                workspace_names = self.config.get_mod_workspaces()
                workspace_paths = [self.config.get_mod_workspace_path(name) for name in workspace_names]

            for workspace_path in workspace_paths:
                if workspace_path.exists():
                    removed = self._remove_empty_folders(workspace_path)
                    total_removed += removed
                    logger.info(f"清理工作区 {workspace_path.name}: {removed} 个空文件夹")

        except Exception as e:
            logger.error(f"清理空文件夹失败: {e}")

        return total_removed

    def _remove_empty_folders(self, path: Path) -> int:
        """
        递归移除空文件夹
        
        Args:
            path: 要清理的路径
            
        Returns:
            移除的空文件夹数量
        """
        removed_count = 0

        try:
            if not path.exists() or not path.is_dir():
                return 0

            # 获取所有子目录，按深度倒序排列
            subdirs = []
            for item in path.rglob('*'):
                if item.is_dir() and not item.name.startswith('.'):
                    subdirs.append(item)

            # 按路径深度排序，深度大的先处理
            subdirs.sort(key=lambda x: len(x.parts), reverse=True)

            for subdir in subdirs:
                try:
                    if self._is_folder_empty(subdir):
                        subdir.rmdir()
                        removed_count += 1
                        logger.debug(f"删除空文件夹: {subdir.relative_to(path)}")
                except Exception:
                    pass

        except Exception as e:
            logger.error(f"清理过程中发生错误: {e}")

        return removed_count

    def _is_folder_empty(self, folder_path: Path) -> bool:
        """
        检查文件夹是否为空
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            是否为空文件夹
        """
        try:
            if not folder_path.exists() or not folder_path.is_dir():
                return False

            for _ in folder_path.iterdir():
                return False

            return True

        except Exception:
            return False

    def package_mod(self, workspace_name: str) -> bool:
        """
        打包指定工作区的MOD
        
        Args:
            workspace_name: 工作区名称
            
        Returns:
            是否打包成功
        """
        try:
            # 这里将调用原有的main_program逻辑
            # 暂时保持兼容性

            # 动态导入main_program以避免循环依赖
            from .main_program import BD2MainProgram

            main_program = BD2MainProgram(self.config)

            result = main_program.run(workspace_name)
            success = result == 0

            if success:
                logger.info(f"MOD打包成功: {workspace_name}")
                
                # 检查是否实际执行了打包任务
                if getattr(main_program, 'actually_packaged', False):
                    replace_tasks = main_program.get_replace_tasks()

                    # 实际执行了打包后调用脚本
                    self._run_post_package_scripts(workspace_name,replace_tasks)
                else:
                    logger.info("未执行任何打包任务，跳过脚本调用")
            else:
                logger.error(f"MOD打包失败: {workspace_name}")

            return success

        except Exception as e:
            logger.error(f"MOD打包过程中发生错误: {e}")
            return False
    
    def _run_post_package_scripts(self, workspace_name: str, tasks : list[ReplaceTask]) -> None:
        """
        打包完成后运行脚本
        
        Args:
            workspace_name: 工作区名称
            tasks: 替换任务列表
        """
        try:
            
            # 按目标目录分组任务
            # 是否执行脚本
            executed_count = 0
            grouped_tasks = {}
            for task in tasks:
                if task.should_execute:
                    executed_count += 1
                task.target_dir = task.target_dir.replace('\\', '/')  # 确保路径格式统一
                task.target_dir = task.target_dir.replace(self.config.get_targetdata_dir().as_posix(), '')  # 去掉项目根目录部分
                if task.should_execute:  # 只处理已执行的任务
                    target_dir = task.target_dir
                    if target_dir not in grouped_tasks:
                        grouped_tasks[target_dir] = []
                    # 使用 mod_name 如果有的话，否则使用 char
                    mod_name = task.mod_name if task.mod_name else task.char
                    if mod_name not in grouped_tasks[target_dir]:
                        grouped_tasks[target_dir].append(mod_name)
            if executed_count == 0:
                logger.info("✅ 没有需要执行的替换任务,跳过脚本执行")
                return 
            # 对每组内的MOD名称排序
            for target_dir in grouped_tasks:
                grouped_tasks[target_dir].sort()

            # 创建打包结果信息
            from ..utils.script_runner import PackageResult, ScriptRunner
            
            package_result = PackageResult(workspace_name, mod_groups=grouped_tasks)
            
            # 运行scripts目录中的脚本
            script_runner = ScriptRunner(self.project_root)
            script_runner.run_scripts(package_result)
            
        except Exception as e:
            logger.error(f"运行打包后脚本失败: {e}")

    def _get_mod_list(self, workspace_name: str) -> List[str]:
        """
        获取工作区中的MOD列表
        
        Args:
            workspace_name: 工作区名称
            
        Returns:
            MOD名称列表
        """
        mod_list = []
        
        try:
            workspace_path = self.config.get_mod_workspace_path(workspace_name)
            
            if not workspace_path.exists():
                return mod_list
                
            # 遍历工作区中的所有目录
            for item in workspace_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # 检查文件夹是否包含文件（真正的MOD）
                    if self._folder_contains_files(item):
                        mod_list.append(item.name)
                        
            # 按名称排序
            mod_list.sort()
            
        except Exception as e:
            logger.error(f"获取MOD列表失败: {e}")
            
        return mod_list
