#!/usr/bin/env python3
"""
BD2 MOD Manager - 主入口程序

BD2 Auto AB - Brown Dust 2 自动化MOD管理系统的统一入口点。

使用方法:
    python main.py                    # 启动控制台界面
    python main.py --workspace <name> # 直接打包指定工作区
    python main.py --create <name>    # 创建新的工作区
    python main.py --list             # 列出所有工作区
    python main.py --cleanup          # 清理空文件夹
    python main.py --check            # 检查依赖环境
    python main.py --help             # 显示帮助信息

作者: BD2 MOD实验室
版本: 2.0.0
日期: 2025-08-16
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="BD2 Auto AB - Brown Dust 2 自动化MOD打包系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py                    启动控制台界面
  python main.py --workspace replace 打包replace工作区
  python main.py --create "我的MOD"   创建新的工作区
  python main.py --list             列出所有工作区
  python main.py --cleanup          清理所有空文件夹
  python main.py --check            检查依赖环境

更多信息请访问: https://github.com/laoxinH/bd2_auto_ab
        """
    )
    
    parser.add_argument(
        '--workspace', '-w',
        type=str,
        help='指定要打包的工作区名称'
    )
    
    parser.add_argument(
        '--create', '-n',
        type=str,
        metavar='WORKSPACE_NAME',
        help='创建新的MOD工作区'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='列出所有工作区信息'
    )
    
    parser.add_argument(
        '--cleanup', '-c',
        action='store_true',
        help='清理所有工作区的空文件夹'
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='检查依赖环境'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='BD2 Auto AB v2.0.0'
    )
    
    return parser.parse_args()


def show_banner():
    """显示程序横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    BD2 MOD packer v2.0                   ║
║               Brown Dust 2 自动化MOD打包系统                  ║
║                                                             ║
║               🎮 让MOD制作变得简单而高效 🎮                  ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def list_workspaces():
    """列出所有工作区"""
    try:
        from bd2_mod_packer.core.manager import BD2ModManager
        
        manager = BD2ModManager()
        workspaces = manager.list_workspaces()
        
        if not workspaces:
            print("❌ 没有找到已配置的工作区")
            print("💡 请使用控制台界面创建工作区")
            return
        
        print("\n📋 已配置的MOD工作区:")
        print("-" * 60)
        
        for workspace in workspaces:
            status = "✅存在" if workspace['exists'] else "❌不存在"
            mod_count = workspace['mod_count']
            print(f"  • {workspace['name']}: {status}, {mod_count} 个MOD")
        
        print("-" * 60)
        print(f"总计: {len(workspaces)} 个工作区")
        
    except Exception as e:
        logger.error(f"列出工作区失败: {e}")
        print(f"❌ 列出工作区失败: {e}")


def package_workspace(workspace_name: str):
    """打包指定工作区"""
    try:
        from bd2_mod_packer.core.manager import BD2ModManager
        
        manager = BD2ModManager()
        
        print(f"\n🚀 开始打包工作区: {workspace_name}")
        print("-" * 60)
        
        success = manager.package_mod(workspace_name)
        
        print("-" * 60)
        if success:
            print(f"✅ 工作区 '{workspace_name}' 打包完成！")
        else:
            print(f"❌ 工作区 '{workspace_name}' 打包失败！")
            
    except Exception as e:
        logger.error(f"打包工作区失败: {e}")
        print(f"❌ 打包工作区失败: {e}")


def cleanup_empty_folders():
    """清理空文件夹"""
    try:
        from bd2_mod_packer.core.manager import BD2ModManager
        
        manager = BD2ModManager()
        
        print("\n🧹 开始清理空文件夹...")
        print("-" * 60)
        
        removed_count = manager.cleanup_empty_folders()
        
        print("-" * 60)
        print(f"🎉 清理完成！总共清理了 {removed_count} 个空文件夹")
        
    except Exception as e:
        logger.error(f"清理空文件夹失败: {e}")
        print(f"❌ 清理空文件夹失败: {e}")


def create_workspace(workspace_name: str):
    """创建新的工作区"""
    try:
        from bd2_mod_packer.core.manager import BD2ModManager
        
        manager = BD2ModManager()
        
        print(f"\n🏗️  创建工作区: {workspace_name}")
        print("-" * 60)
        
        # 检查工作区是否已存在
        if manager.config.workspace_exists(workspace_name):
            print(f"⚠️  工作区 '{workspace_name}' 已经存在")
            return False
        
        # 创建工作区
        success = manager.create_workspace(workspace_name)
        
        print("-" * 60)
        if success:
            print(f"✅ 工作区 '{workspace_name}' 创建成功！")
            
            # 显示工作区路径信息
            workspace_path = manager.config.get_mod_workspace_path(workspace_name)
            print(f"📁 工作区路径: {workspace_path}")
            print(f"💡 现在可以在该路径下放置您的MOD文件")
            print(f"📦 使用 'python main.py --workspace \"{workspace_name}\"' 打包MOD")
            return True
        else:
            print(f"❌ 工作区 '{workspace_name}' 创建失败！")
            return False
            
    except Exception as e:
        logger.error(f"创建工作区失败: {e}")
        print(f"❌ 创建工作区失败: {e}")
        return False


def check_dependencies():
    """检查依赖环境"""
    try:
        from bd2_mod_packer.utils import check_dependencies
        
        print("\n🔧 检查依赖环境...")
        print("-" * 60)
        
        success = check_dependencies()
        
        print("-" * 60)
        if success:
            print("✅ 所有依赖检查通过！")
        else:
            print("❌ 依赖检查发现问题，请根据提示安装缺失的依赖")
            
    except Exception as e:
        logger.error(f"依赖检查失败: {e}")
        print(f"❌ 依赖检查失败: {e}")


def start_console():
    """启动控制台界面"""
    try:
        from bd2_mod_packer.ui.console import BD2Console
        
        console = BD2Console()
        console.run()
        
    except Exception as e:
        logger.error(f"启动控制台失败: {e}")
        print(f"❌ 启动控制台失败: {e}")


def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_arguments()
        
        # 显示横幅（仅在控制台模式下）
        if not any([args.workspace, args.create, args.list, args.cleanup, args.check]):
            show_banner()
        
        # 根据参数执行相应功能
        if args.list:
            list_workspaces()
        elif args.workspace:
            package_workspace(args.workspace)
        elif args.create:
            create_workspace(args.create)
        elif args.cleanup:
            cleanup_empty_folders()
        elif args.check:
            check_dependencies()
        else:
            # 启动控制台界面
            start_console()
            
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断程序")
        logger.info("用户中断程序")
    except Exception as e:
        logger.error(f"程序异常: {e}")
        print(f"❌ 程序异常: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
