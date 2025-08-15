#!/usr/bin/env python3
"""
BD2资源管理控制台程序

BD2游戏资源管理的统一控制台界面，提供以下功能：
- 目录结构初始化
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
    - 0: 执行目录初始化
    - 1: 执行MOD打包和替换
    - 2: 依赖环境检查
    - 3: 显示帮助信息
    - 4: 退出程序
    """
    
    def __init__(self):
        """初始化控制台"""
        self.project_root = Path(__file__).parent.parent
        self.src_dir = self.project_root / "src"
        
        logger.info(f"BD2控制台初始化完成")
        logger.info(f"项目根目录: {self.project_root}")
        logger.info(f"源码目录: {self.src_dir}")
    
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
│  0️⃣  执行目录初始化 - 从谷歌表格创建角色目录结构           │
│  1️⃣  执行MOD打包   - 检测更新并打包替换资源               │
│  2️⃣  依赖环境检查 - 检查Python依赖库安装状态              │
│  3️⃣  显示帮助信息 - 查看详细使用说明                      │
│  4️⃣  退出程序     - 安全退出控制台                        │
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
│ 🏗️  目录初始化 (选项 0)                                     │
│   • 从大佬网站中获取最新角色数据                              │
│   • 自动创建 replace 目录结构                               │
│   • 格式: replace\\角色\\服装\\类型                         │
│   • 智能跳过已存在的目录                                    │
│   • 支持 CUTSCENE 和 IDLE 资源类型                         │
│                                                              │
│ 📦 MOD打包 (选项 1)                                         │
│   • 检测游戏版本更新                                        │
│   • 扫描替换文件变更                                        │
│   • 下载原始游戏资源                                        │
│   • 执行Unity资源替换                                       │
│   • 生成详细的README文件                                    │
│                                                              │
│ � 依赖环境检查 (选项 2)                                    │
│   • 检查Python版本兼容性                                   │
│   • 验证所有第三方库安装状态                               │
│   • 显示已安装库的版本信息                                 │
│   • 提供缺失依赖的安装建议                                 │
│   • 生成依赖环境报告                                       │
│                                                              │
│ �📁 目录结构说明                                              │
│   replace/                                                  │
│   ├── 角色名/                                               │
│   │   ├── 服装名/                                           │
│   │   │   ├── CUTSCENE/MOD文件夹（建议为MOD名称）  # 技能动画  │
│   │   │   └── IDLE/MOD文件夹（建议为MOD名称）  # 立绘动画       │
│                                                              │
│ ⚠️  使用注意事项                                             │
│   • 确保网络连接正常（需要访问谷歌表格和游戏CDN）           │
│   • 首次运行建议先执行目录初始化                            │
│   • MOD文件放置在对应的角色/服装/类型目录中                 │
│   • 程序会自动备份和版本管理                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
        """
        print(help_text)
    
    def execute_initialization(self):
        """执行目录初始化"""
        print("\n" + "="*60)
        print("🏗️  执行目录初始化")
        print("="*60)
        
        try:
            # 导入初始化模块
            from initialize_directories import DirectoryInitializer
            
            # 创建初始化器
            initializer = DirectoryInitializer(str(self.project_root))
            
            # 显示当前目录结构
            print("\n📋 当前目录结构:")
            initializer.list_existing_directories()
            
            # 询问用户确认
            response = input("\n是否继续执行初始化？(y/N): ").strip().lower()
            if response not in ['y', 'yes', '是']:
                print("⚠️  用户取消操作")
                return
            
            # 执行初始化
            initializer.initialize_all_directories()
            
            print("\n" + "="*60)
            print("✅ 目录初始化完成！")
            print("="*60)
            
        except ImportError as e:
            logger.error(f"无法导入初始化模块: {e}")
            print("❌ 初始化模块导入失败，请检查文件是否存在")
        except Exception as e:
            logger.error(f"初始化过程中发生错误: {e}")
            print(f"❌ 初始化失败: {e}")
    
    def execute_mod_packaging(self):
        """执行MOD打包"""
        print("\n" + "="*60)
        print("📦 执行MOD打包和替换")
        print("="*60)
        
        try:
            # 导入主程序模块
            from main_program import main as main_program
            
            # 询问用户确认
            response = input("\n是否开始MOD打包和替换过程？(y/N): ").strip().lower()
            if response not in ['y', 'yes', '是']:
                print("⚠️  用户取消操作")
                return
            
            print("\n🚀 启动MOD打包程序...")
            print("-" * 60)
            
            # 执行主程序
            result = main_program()
            
            print("-" * 60)
            if result == 0:
                print("✅ MOD打包和替换完成！")
            else:
                print("❌ MOD打包和替换失败！")
            print("="*60)
            
        except ImportError as e:
            logger.error(f"无法导入主程序模块: {e}")
            print("❌ 主程序模块导入失败，请检查文件是否存在")
        except Exception as e:
            logger.error(f"MOD打包过程中发生错误: {e}")
            print(f"❌ MOD打包失败: {e}")
    
    def execute_dependency_check(self):
        """执行依赖环境检查"""
        print("\n" + "="*60)
        print("🔧 执行依赖环境检查")
        print("="*60)
        
        try:
            # 导入依赖检查模块
            from check_dependencies import check_dependencies
            
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
            
            # 导入并运行依赖报告生成器
            import sys
            sys.path.append(str(self.project_root))
            from generate_dependency_report import generate_dependency_report
            
            generate_dependency_report()
            
        except ImportError as e:
            print(f"❌ 无法导入依赖报告模块: {e}")
            print("💡 请确保 generate_dependency_report.py 文件存在")
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
                choice = input("\n请选择操作 (0-4): ").strip()
                
                if choice in ['0', '1', '2', '3', '4']:
                    return int(choice)
                else:
                    print("⚠️  无效选择，请输入 0、1、2、3 或 4")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  用户中断程序")
                return 4
            except EOFError:
                print("\n\n⚠️  输入结束，退出程序")
                return 4
            except Exception as e:
                print(f"⚠️  输入错误: {e}")
    
    def run(self):
        """运行控制台程序"""
        try:
            # 显示横幅
            self.show_banner()
            
            while True:
                # 显示菜单
                self.show_menu()
                
                # 获取用户选择
                choice = self.get_user_choice()
                
                # 执行对应功能
                if choice == 0:
                    self.execute_initialization()
                    
                elif choice == 1:
                    self.execute_mod_packaging()
                    
                elif choice == 2:
                    self.execute_dependency_check()
                    
                elif choice == 3:
                    self.show_help()
                    
                elif choice == 4:
                    print("\n👋 感谢使用BD2 MOD资源打包控制台！")
                    print("再见！")
                    break
                
                # 等待用户按键继续
                if choice != 4:
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
