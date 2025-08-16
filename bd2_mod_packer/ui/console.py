#!/usr/bin/env python3
"""
BD2资源管理控制台程序

BD2游戏资源管理的统一控制台界面，提供以下功能：
- MOD工作目录创建和管理
- MOD资源打包和替换
- 交互式菜单操作

使用方法:
    python console.py

作者: oldnew
日期: 2025-08-15
"""

import os
import sys
import logging
from pathlib import Path

import bd2_mod_packer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class BD2Console:
    """
    BD2资源管理控制台
    
    功能菜单：
    - 0: 创建MOD工作目录
    - 1: 执行MOD打包和替换
    - 2: 依赖环境检查
    - 3: 显示帮助信息
    - 4: 退出程序
    """
    
    def __init__(self):
        """初始化控制台"""
        # 导入配置管理器
        from ..config.settings import get_config
        self.config = get_config()
        
        # 从配置获取项目根目录和工作区路径
        self.project_root = self.config.project_root
        self.workspace_root = self.config.get_workspace_root()
        self.mod_projects_dir = self.config.get_mod_projects_dir()
        
        logger.info(f"BD2控制台初始化完成")
        logger.info(f"项目根目录: {self.project_root}")
        logger.info(f"工作区根目录: {self.workspace_root}")
        logger.info(f"MOD项目目录: {self.mod_projects_dir}")
    
    def show_banner(self):
        """显示程序横幅"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    BD2 MOD资源打包控制台                      ║
║               Brown Dust 2 MOD Resource Manager               ║
║                                                             ║
║               🎮 自动化MOD资源替换和管理工具 🎮               ║ 
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def show_menu(self):
        """显示主菜单"""
        menu = """
┌─────────────────────────────────────────────────────────────┐
│                          主菜单                             │
├─────────────────────────────────────────────────────────────┤
│  0️⃣  创建MOD工作目录 - 设置和初始化新的MOD工作环境          │
│  1️⃣  执行MOD打包     - 选择工作目录并打包替换资源          │
│  2️⃣  删除MOD工作目录 - 删除指定的MOD工作目录               │
│  3️⃣  清理空文件夹   - 清理工作目录中的空文件夹             │
│  4️⃣  依赖环境检查   - 检查Python依赖库安装状态             │
│  5️⃣  显示帮助信息   - 查看详细使用说明                     │
│  6️⃣  退出程序       - 安全退出控制台                       │
└─────────────────────────────────────────────────────────────┘
        """
        print(menu)
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
┌─────────────────────────────────────────────────────────────┐
│                        功能说明                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 🏗️  创建MOD工作目录 (选项 0)                                │
│   • 输入自定义的MOD工作目录名称                              │
│   • 保存工作目录配置到config.json                           │
│   • 从谷歌表格获取最新角色数据                              │
│   • 自动创建完整的角色目录结构                              │
│   • 格式: 工作目录\\角色\\服装\\类型                         │
│   • 支持多个独立的MOD工作环境                               │
│                                                              │
│ 📦 MOD打包 (选项 1)                                         │
│   • 列出所有已配置的工作目录                                │
│   • 选择要打包的特定工作目录                                │
│   • 检测游戏版本更新                                        │
│   • 扫描工作目录中的替换文件                                │
│   • 下载原始游戏资源                                        │
│   • 执行Unity资源替换                                       │
│   • 生成详细的README文件                                    │
│                                                              │
│ �️  删除MOD工作目录 (选项 2)                                │
│   • 列出所有已配置的工作目录                                │
│   • 选择要删除的特定工作目录                                │
│   • 从配置文件中移除工作目录记录                            │
│   • 可选择同时删除物理目录文件                              │
│   • 需要输入确认文本防止误删                                │
│                                                              │
│ 🧹 清理空文件夹 (选项 3)                                    │
│   • 扫描工作目录中的空文件夹                                │
│   • 可以选择清理单个或所有工作目录                          │
│   • 递归清理所有层级的空文件夹                              │
│   • 保留包含文件的文件夹结构                                │
│   • 显示清理统计信息                                        │
│                                                              │
│ �🔧 依赖环境检查 (选项 4)                                    │
│   • 检查Python版本兼容性                                   │
│   • 验证所有第三方库安装状态                               │
│   • 显示已安装库的版本信息                                 │
│   • 提供缺失依赖的安装建议                                 │
│   • 生成依赖环境报告                                       │
│                                                              │
│ 📁 工作目录结构说明                                          │
│   工作目录名/                                               │
│   ├── 角色名/                                               │
│   │   ├── 服装名/                                           │
│   │   │   ├── CUTSCENE/MOD文件夹  # 技能动画                │
│   │   │   └── IDLE/MOD文件夹      # 立绘动画                │
│                                                              │
│ ⚠️  使用注意事项                                             │
│   • 确保网络连接正常（需要访问谷歌表格和游戏CDN）           │
│   • 建议为不同作者或MOD类型创建独立工作目录                 │
│   • 工作目录名支持中文、英文和特殊字符                      │
│   • 可以同时维护多个MOD项目                                 │
│   • 程序会自动保存工作目录配置                              │
│   • 删除工作目录前请确保重要文件已备份                      │
│   • 清理空文件夹功能不会删除包含文件的目录                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
        """
        print(help_text)
    
    def create_mod_workspace(self):
        """创建MOD工作目录"""
        print("\n" + "="*60)
        print("🏗️  创建MOD工作目录")
        print("="*60)
        
        try:
            # 显示现有工作目录
            existing_workspaces = self.config.get_mod_workspaces()
            print(f"\n📋 当前已配置的工作目录: {', '.join(existing_workspaces)}")
            
            # 输入新的工作目录名称
            print("\n💡 请输入新的MOD工作目录名称:")
            print("   - 支持中文、英文和特殊字符")
            print("   - 建议使用有意义的名称，如'laoxin的mod'、'bikini_mods'等")
            print("   - 输入 'cancel' 取消操作")
            
            while True:
                workspace_name = input("\n工作目录名称: ").strip()
                
                if workspace_name.lower() == 'cancel':
                    print("⚠️  用户取消操作")
                    return
                
                if not workspace_name:
                    print("❌ 工作目录名称不能为空，请重新输入")
                    continue
                
                # 检查名称是否合法
                if not self._validate_workspace_name(workspace_name):
                    print("❌ 工作目录名称包含非法字符，请使用中文、英文、数字、下划线或中划线")
                    continue
                
                # 检查是否已存在
                if self.config.workspace_exists(workspace_name):
                    print(f"❌ 工作目录 '{workspace_name}' 已存在，请使用其他名称")
                    continue
                
                # 检查物理目录是否已存在
                workspace_path = self.config.get_mod_workspace_path(workspace_name)
                if workspace_path.exists():
                    response = input(f"⚠️  目录 '{workspace_name}' 已存在于磁盘上，是否继续使用？(y/N): ").strip().lower()
                    if response not in ['y', 'yes', '是']:
                        continue
                else:
                    # 如果目录不存在，创建
                    print(f"📂 物理目录 '{workspace_name}' 不存在，将自动创建")
                    workspace_path.mkdir(parents=True, exist_ok=True)
                
                break
            
            # 确认创建
            print(f"\n📂 将要创建工作目录: {workspace_name}")
            print(f"📍 物理路径: {self.config.get_mod_workspace_path(workspace_name)}")
            
            response = input("\n是否确认创建？(y/N): ").strip().lower()
            if response not in ['y', 'yes', '是']:
                print("⚠️  用户取消操作")
                return
            
            # 添加到配置
            if not  self.config.add_mod_workspace(workspace_name):
                print(f"❌ 工作目录 '{workspace_name}' 添加到配置失败，请检查配置文件")
                return
            print(f"✅ 工作目录 '{workspace_name}' 已添加到配置")
            # 创建物理目录

            print("="*60)
            response = input("\n是否创建角色MOD路径（默认创建全部角色路径）？(y/N): ").strip().lower()
            if response not in ['y', 'yes', '是']:
                print(f"✅ MOD工作区 '{workspace_name}' 创建完成，但未创建角色路径，后续请手动创建！")
                return
            print(f"\n📂 将要创建 {workspace_name} 的角色MOD目录")

            from bd2_mod_packer.utils import DirectoryInitializer
            # 创建初始化器，指定工作目录
            initializer = DirectoryInitializer(str(self.config.get_mod_projects_dir()), workspace_name)
            # 执行初始化
            initializer.initialize_all_directories()
            print(f"✅ MOD工作区 '{workspace_name}' 创建完成，并完创建了所有角色路径！")
        except Exception as e:
            logger.error(f"创建工作目录过程中发生错误: {e}")
            print(f"❌ 创建工作目录失败: {e}")
    
    def _validate_workspace_name(self, name: str) -> bool:
        """
        验证工作目录名称是否合法
        
        Args:
            name: 目录名称
            
        Returns:
            是否合法
        """
        import re
        # 允许中文、英文、数字、下划线、中划线、空格、单引号和一些常见符号
        pattern = r'^[\w\u4e00-\u9fff\s\-_.()（）【】\[\]\'\"]+$'
        return bool(re.match(pattern, name)) and len(name) <= 50
    
    def execute_mod_packaging(self):
        """执行MOD打包"""
        print("\n" + "="*60)
        print("📦 执行MOD打包和替换")
        print("="*60)
        
        try:
            # 获取所有工作目录
            workspaces = self.config.get_mod_workspaces()
            
            if not workspaces:
                print("❌ 没有配置任何工作目录")
                print("💡 请先使用选项 0 创建MOD工作目录")
                return
            
            # 检查工作目录的物理存在性
            valid_workspaces = []
            for workspace in workspaces:
                workspace_path = self.config.get_mod_workspace_path(workspace)
                if workspace_path.exists():
                    valid_workspaces.append(workspace)
                else:
                    print(f"⚠️  工作目录 '{workspace}' 在配置中存在但物理路径不存在")
            
            if not valid_workspaces:
                print("❌ 没有找到有效的工作目录")
                print("💡 请先使用选项 0 创建MOD工作目录")
                return
            
            # 显示可用的工作目录
            print(f"\n📋 可用的MOD工作目录:")
            for i, workspace in enumerate(valid_workspaces, 1):
                workspace_path = self.config.get_mod_workspace_path(workspace)
                # 统计目录中的MOD数量（包含文件的文件夹）
                mod_count = self._count_mod_folders(workspace_path)
                print(f"  {i}. {workspace} (发现 {mod_count} 个MOD)")
            
            # 让用户选择工作目录
            while True:
                try:
                    choice = input(f"\n请选择要打包的工作目录 (1-{len(valid_workspaces)}) 或输入 'cancel' 取消: ").strip()
                    
                    if choice.lower() == 'cancel':
                        print("⚠️  用户取消操作")
                        return
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(valid_workspaces):
                        selected_workspace = valid_workspaces[choice_idx]
                        break
                    else:
                        print(f"❌ 无效选择，请输入 1-{len(valid_workspaces)} 之间的数字")
                        
                except ValueError:
                    print("❌ 请输入有效的数字")
            
            print(f"\n✅ 已选择工作目录: {selected_workspace}")
            
            # 询问用户确认
            response = input(f"\n是否开始对 '{selected_workspace}' 进行MOD打包和替换？(y/N): ").strip().lower()
            if response not in ['y', 'yes', '是']:
                print("⚠️  用户取消操作")
                return
            
            print(f"\n🚀 启动MOD打包程序 (工作目录: {selected_workspace})...")
            print("-" * 60)
            
            # 使用新的MOD管理器进行打包
            from ..core.manager import BD2ModManager
            
            try:
                manager = BD2ModManager()
                success = manager.package_mod(selected_workspace)
                
                print("-" * 60)
                if success:
                    print(f"✅ '{selected_workspace}' MOD打包和替换完成！")
                else:
                    print(f"❌ '{selected_workspace}' MOD打包和替换失败！")
                    
            except Exception as e:
                logger.error(f"MOD打包过程中发生错误: {e}")
                print(f"❌ MOD打包失败: {e}")
            
            print("="*60)
            
        except Exception as e:
            logger.error(f"MOD打包过程中发生错误: {e}")
            print(f"❌ MOD打包失败: {e}")
    
    def _count_mod_folders(self, workspace_path: Path) -> int:
        """
        统计工作目录中的MOD数量（包含文件的文件夹）
        
        Args:
            workspace_path: 工作目录路径
            
        Returns:
            包含文件的文件夹数量
        """
        if not workspace_path.exists():
            return 0
        
        count = 0
        try:
            # 遍历工作目录下的所有子目录
            for item in workspace_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # 检查文件夹是否包含文件（递归检查）
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
            # 递归查找文件夹中是否有文件
            for item in folder_path.rglob('*'):
                if item.is_file() and not item.name.startswith('.'):
                    return True
        except Exception:
            pass
        
        return False
    
    def delete_mod_workspace(self):
        """删除MOD工作目录"""
        print("\n" + "="*60)
        print("🗑️  删除MOD工作目录")
        print("="*60)
        
        try:
            # 获取所有配置的工作目录
            workspaces = self.config.get_mod_workspaces()
            
            if not workspaces:
                print("❌ 没有找到已配置的工作目录")
                print("💡 请先使用选项 0 创建MOD工作目录")
                return
            
            # 显示可用的工作目录
            print(f"\n📋 已配置的MOD工作目录:")
            for i, workspace in enumerate(workspaces, 1):
                workspace_path = self.config.get_mod_workspace_path(workspace)
                if workspace_path.exists():
                    mod_count = self._count_mod_folders(workspace_path)
                    print(f"  {i}. {workspace} (✅存在, {mod_count} 个MOD)")
                else:
                    print(f"  {i}. {workspace} (❌不存在)")
            
            # 让用户选择要删除的工作目录
            while True:
                try:
                    choice = input(f"\n请选择要删除的工作目录 (1-{len(workspaces)}) 或输入 'cancel' 取消: ").strip()
                    
                    if choice.lower() == 'cancel':
                        print("⚠️  用户取消操作")
                        return
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(workspaces):
                        selected_workspace = workspaces[choice_idx]
                        break
                    else:
                        print(f"❌ 无效选择，请输入 1-{len(workspaces)} 之间的数字")
                        
                except ValueError:
                    print("❌ 请输入有效的数字")
            
            # 警告用户删除的后果
            print(f"\n⚠️  警告: 将要删除工作目录 '{selected_workspace}'")
            workspace_path = self.config.get_mod_workspace_path(selected_workspace)
            
            if workspace_path.exists():
                print(f"📂 物理路径: {workspace_path}")
                print("⚠️  这将永久删除该目录及其所有内容！")
            else:
                print("📋 该工作目录仅在配置中存在，物理路径不存在")
            
            # 要求用户确认
            confirm = input(f"\n请输入 'DELETE' 确认删除 '{selected_workspace}': ").strip()
            if confirm != 'DELETE':
                print("⚠️  确认文本不匹配，取消删除操作")
                return
            
            # 使用MOD管理器删除工作区
            from ..core.manager import BD2ModManager
            manager = BD2ModManager()
            success = manager.delete_workspace(selected_workspace)
            
            if success:
                print(f"✅ 工作目录 '{selected_workspace}' 删除完成！")
            else:
                print(f"❌ 工作目录 '{selected_workspace}' 删除失败！")
            
        except Exception as e:
            logger.error(f"删除工作目录过程中发生错误: {e}")
            print(f"❌ 删除工作目录失败: {e}")
    
    def cleanup_empty_folders(self):
        """清理空文件夹"""
        print("\n" + "="*60)
        print("🧹 清理工作目录中的空文件夹")
        print("="*60)
        
        try:
            # 获取所有配置的工作目录
            workspaces = self.config.get_mod_workspaces()
            
            if not workspaces:
                print("❌ 没有找到已配置的工作目录")
                print("💡 请先使用选项 0 创建MOD工作目录")
                return
            
            # 检查工作目录的物理存在性
            valid_workspaces = []
            for workspace in workspaces:
                workspace_path = self.config.get_mod_workspace_path(workspace)
                if workspace_path.exists():
                    valid_workspaces.append(workspace)
                else:
                    print(f"⚠️  工作目录 '{workspace}' 在配置中存在但物理路径不存在")
            
            if not valid_workspaces:
                print("❌ 没有找到有效的工作目录")
                return
            
            # 显示可用的工作目录
            print(f"\n📋 可用的MOD工作目录:")
            for i, workspace in enumerate(valid_workspaces, 1):
                workspace_path = self.config.get_mod_workspace_path(workspace)
                mod_count = self._count_mod_folders(workspace_path)
                print(f"  {i}. {workspace} (发现 {mod_count} 个MOD)")
            
            print(f"  {len(valid_workspaces) + 1}. 清理所有工作目录")
            
            # 让用户选择要清理的工作目录
            while True:
                try:
                    choice = input(f"\n请选择要清理的工作目录 (1-{len(valid_workspaces) + 1}) 或输入 'cancel' 取消: ").strip()
                    
                    if choice.lower() == 'cancel':
                        print("⚠️  用户取消操作")
                        return
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(valid_workspaces):
                        selected_workspaces = [valid_workspaces[choice_idx]]
                        break
                    elif choice_idx == len(valid_workspaces):
                        selected_workspaces = valid_workspaces
                        break
                    else:
                        print(f"❌ 无效选择，请输入 1-{len(valid_workspaces) + 1} 之间的数字")
                        
                except ValueError:
                    print("❌ 请输入有效的数字")
            
            # 使用MOD管理器执行清理
            from ..core.manager import BD2ModManager
            manager = BD2ModManager()
            
            if len(selected_workspaces) == 1:
                removed_count = manager.cleanup_empty_folders(selected_workspaces[0])
                print(f"\n🎉 清理完成！总共清理了 {removed_count} 个空文件夹")
            else:
                removed_count = manager.cleanup_empty_folders()
                print(f"\n🎉 清理完成！总共清理了 {removed_count} 个空文件夹")
            
        except Exception as e:
            logger.error(f"清理空文件夹过程中发生错误: {e}")
            print(f"❌ 清理空文件夹失败: {e}")
    
    def execute_dependency_check(self):
        """执行依赖环境检查"""
        print("\n" + "="*60)
        print("🔧 执行依赖环境检查")
        print("="*60)
        
        try:
            # 导入依赖检查模块
            from ..utils.dependency_checker import check_dependencies
            
            print("\n📋 正在检查Python环境和依赖库...")
            print("-" * 60)
            
            # 执行依赖检查
            success = check_dependencies()
            
            print("-" * 60)
            
            if success:
                print("✅ 所有依赖检查通过！环境配置正确。")
                
                # 询问是否查看详细报告
                response = input("\n是否查看详细的依赖分析报告？(y/N): ").strip().lower()
                if response in ['y', 'yes', '是']:
                    self.show_dependency_report()
            else:
                print("❌ 发现依赖问题，请根据上述提示安装缺失的库。")
                
                # 提供快速修复选项
                response = input("\n是否显示快速修复命令？(y/N): ").strip().lower()
                if response in ['y', 'yes', '是']:
                    self.show_quick_fix_commands()
            
            print("="*60)
            
        except ImportError as e:
            logger.error(f"无法导入依赖检查模块: {e}")
            print("❌ 依赖检查模块导入失败，请检查 check_dependencies.py 文件是否存在")
            print("\n💡 提示: 您可以手动运行以下命令检查依赖:")
            print("    python src/check_dependencies.py")
        except Exception as e:
            logger.error(f"依赖检查过程中发生错误: {e}")
            print(f"❌ 依赖检查失败: {e}")
    
    def show_dependency_report(self):
        """显示详细的依赖分析报告"""
        try:
            print("\n" + "="*60)
            print("📊 详细依赖分析报告")
            print("="*60)
            
            import pkg_resources
            import sys
            
            print(f"Python版本: {sys.version}")
            print(f"Python路径: {sys.executable}")
            print("\n已安装的包:")
            
            # 获取所有已安装的包
            installed_packages = [d for d in pkg_resources.working_set]
            installed_packages.sort(key=lambda x: x.project_name.lower())
            
            for package in installed_packages:
                print(f"  {package.project_name} == {package.version}")
            
            print(f"\n总共安装了 {len(installed_packages)} 个包")
            
        except ImportError as e:
            print(f"❌ 无法生成依赖报告: {e}")
            print("💡 请检查 pkg_resources 模块是否可用")
        except Exception as e:
            print(f"❌ 生成依赖报告时出错: {e}")
    
    def show_quick_fix_commands(self):
        """显示快速修复命令"""
        print("\n" + "="*60)
        print("🔧 快速修复命令")
        print("="*60)
        
        print("以下是一些常见的依赖安装命令:")
        print()
        
        commands = [
            ("更新pip", "python -m pip install --upgrade pip"),
            ("安装所有依赖", "pip install -r requirements.txt"),
            ("安装requests", "pip install requests>=2.31.0"),
            ("安装beautifulsoup4", "pip install beautifulsoup4>=4.12.0"),
            ("安装lxml", "pip install lxml>=4.9.0"),
            ("安装tqdm", "pip install tqdm>=4.65.0"),
            ("安装UnityPy", "pip install UnityPy>=1.20.0"),
            ("安装Pillow", "pip install Pillow>=10.0.0"),
            ("安装blackboxprotobuf", "pip install blackboxprotobuf>=1.0.0"),
        ]
        
        for i, (desc, cmd) in enumerate(commands, 1):
            print(f"{i:2}. {desc}")
            print(f"    {cmd}")
            print()
        
        print("💡 建议: 优先使用 'pip install -r requirements.txt' 安装所有依赖")
        print("📁 requirements.txt 文件位置: 项目根目录")
        print()
        
        # 显示国内镜像源选项
        print("🌏 如果下载速度慢，可以使用国内镜像源:")
        mirrors = [
            ("清华大学", "pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/"),
            ("阿里云", "pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/"),
            ("豆瓣", "pip install -r requirements.txt -i https://pypi.douban.com/simple/"),
        ]
        
        for name, cmd in mirrors:
            print(f"  {name}: {cmd}")
        print()
    
    def get_user_choice(self):
        """获取用户选择"""
        while True:
            try:
                choice = input("\n请选择操作 (0-6): ").strip()
                
                if choice in ['0', '1', '2', '3', '4', '5', '6']:
                    return int(choice)
                else:
                    print("⚠️  无效选择，请输入 0、1、2、3、4、5 或 6")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  用户中断程序")
                return 6
            except EOFError:
                print("\n\n⚠️  输入结束，退出程序")
                return 4
            except Exception as e:
                print(f"⚠️  输入错误: {e}")
    
    def run(self):
        """运行控制台程序"""
        try:
            # 显示横幅
            # self.show_banner()
            
            while True:
                # 显示菜单
                self.show_menu()
                
                # 获取用户选择
                choice = self.get_user_choice()
                
                # 执行对应功能
                if choice == 0:
                    self.create_mod_workspace()
                    
                elif choice == 1:
                    self.execute_mod_packaging()
                    
                elif choice == 2:
                    self.delete_mod_workspace()
                    
                elif choice == 3:
                    self.cleanup_empty_folders()
                    
                elif choice == 4:
                    self.execute_dependency_check()
                    
                elif choice == 5:
                    self.show_help()
                    
                elif choice == 6:
                    print("\n👋 感谢使用BD2 MOD资源打包控制台！")
                    print("再见！")
                    break
                
                # 等待用户按键继续
                if choice != 6:
                    input("\n按 Enter 键继续...")
                    # 清屏（跨平台）
                    os.system('cls' if os.name == 'nt' else 'clear')
        
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断程序")
        except Exception as e:
            logger.error(f"控制台运行异常: {e}")
            print(f"❌ 程序异常: {e}")
        finally:
            print("\n程序结束")


def main():
    """主函数"""
    try:
        # 创建控制台实例
        console = BD2Console()
        
        # 运行控制台
        console.run()
        
        return 0
        
    except Exception as e:
        logger.error(f"程序启动失败: {e}")
        print(f"❌ 程序启动失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
