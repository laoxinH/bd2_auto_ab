import argparse
import logging
import os
from pathlib import Path
from typing import List

from ..core.resource_manager import ReplaceTask


class BD2MainProgram:
    """BD2 Resource Replacement Main Program"""

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.actually_packaged = False  # 标识是否实际执行了打包
        self.replace_tasks = []  # 用于存储替换任务信息

    def parse_arguments(self, replace_dir='replace'):
        """Parse command-line arguments"""
        parser = argparse.ArgumentParser(
            description='BD2 Resource Replacement Main Program',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Usage examples:
  python main_program.py                    # Use the default 'replace' directory
  python main_program.py "laoxin's mod"     # Use the 'laoxin's mod' directory
  python main_program.py "author_name"      # Use the 'author_name' directory

Notes:
  - The specified directory is relative to the project root
  - If the directory does not exist, the program will prompt the user
  - Directory names with Chinese characters and spaces are supported
            """
        )

        parser.add_argument(
            'replace_dir',
            nargs='?',
            default=replace_dir,
            help='Replacement directory name (relative to the project root, default: replace)'
        )

        return parser.parse_args()

    def validate_replace_directory(self, replace_dir):
        """Validate if the replacement directory exists"""
        project_root = self.config.get_mod_projects_dir()
        replace_path = os.path.join(project_root, replace_dir)

        if not os.path.exists(replace_path):
            self.logger.error(f"❌ MOD工作目录不存在: {replace_path}")
            self.logger.info(f"💡 确保已建立工作目录 '{replace_dir}'")
            return False, None

        if not os.path.isdir(replace_path):
            self.logger.error(f"❌ 所选路径不是文件夹: {replace_path}")
            return False, None

        self.logger.info(f"✅ MOD工作路径 {replace_path}")
        return True, replace_path

    def get_replace_tasks(self) -> List[ReplaceTask]:
        """Get the list of replacement tasks"""
        return self.replace_tasks

    def run(self, replace_dir='replace'):
        """Main method to execute the program"""
        try:
            replace_tasks = []
            self.logger.info("🎮 BD2 MOD 打包系统主程序运行")
            self.logger.info("=" * 60)
            self.logger.info(f"📁 所选工作目录路径: {replace_dir}")

            # Validate replacement directory
            is_valid, replace_path = self.validate_replace_directory(replace_dir)
            if not is_valid:
                return 1

            # Create resource manager instance
            from .resource_manager import BD2ResourceManager
            manager = BD2ResourceManager(
                proxies=self.config.get_proxies(),
                replace_dir=replace_dir
            )

            # Step 1: Check version and updates
            self.logger.info("📋 Step 1: 检查版本更新和MOD文件更新...")
            needs_update, summary = manager.check_version_and_updates()

            # Output detection results
            self.logger.info("📊 检查结果:")
            self.logger.info(f"  版本是否更新: {summary.version_changed}")
            if summary.old_version is not None and summary.new_version is not None:
                self.logger.info(f"  版本变化: {summary.old_version} -> {summary.new_version}")
            self.logger.info(f"  所有MOD目录数: {summary.total_replace_dirs}")
            self.logger.info(f"  有更新的MOD目录数: {len(summary.replace_dirs_to_update)}")

            # Determine if replacement process is needed
            if not needs_update:
                self.logger.info("✅ 无需更新, MOD打包结束")
                self.actually_packaged = False
                return 0

            # Execute full replacement process if version changed
            if summary.version_changed:
                self.logger.info("🔄 发现游戏版本更新, 执行全MOD打包...")
                success, replace_tasks = manager.process_updates(summary)
                if success:
                    self.logger.info("✅ 全MOD打包完成")
                    self.actually_packaged = True
                else:
                    self.logger.error("❌ 全MOD打包失败")
                    self.actually_packaged = False
                    return 1

            # Execute incremental replacement if only files are updated
            elif summary.replace_dirs_to_update:
                self.logger.info("🔄 发现MOD文件更新, 执行增量MOD打包...")
                success, replace_tasks = manager.process_updates(summary)
                if success:
                    self.logger.info("✅ 增量MOD打包完成")
                    self.actually_packaged = True
                else:
                    self.logger.error("❌ 增量MOD打包失败")
                    self.actually_packaged = False
                    return 1
            self.replace_tasks = replace_tasks
            self.logger.info("🎉 BD2 MOD打包执行完成")
            return 0

        except KeyboardInterrupt:
            self.logger.info("⚠️ 程序被用户中断")
            return 1
        except Exception as e:
            self.logger.error(f"💥 程序异常退出: {e}")
            return 1
