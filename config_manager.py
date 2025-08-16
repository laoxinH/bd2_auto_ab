#!/usr/bin/env python3
"""
BD2项目配置管理工具

用于管理BD2项目的配置设置，包括：
- 代理设置
- 网络超时配置
- 日志级别设置
- API端点配置

使用方法:
    python config_manager.py

作者: oldnew
日期: 2025-08-15
"""

import os
import sys
from pathlib import Path
from typing import Optional
# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
# 导入配置模块
from bd2_mod_packer.config import get_config, reload_config


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        """初始化配置管理器"""
        self.config = get_config()
        print("BD2项目配置管理器已启动")
        print(f"配置文件路径: {self.config.config_file}")
    
    def show_banner(self):
        """显示横幅"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                   BD2项目配置管理工具                        ║
║                  BD2 Project Config Manager                  ║
║                                                             ║
║               ⚙️  统一管理项目配置设置 ⚙️                  ║ 
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def show_menu(self):
        """显示主菜单"""
        menu = """
┌─────────────────────────────────────────────────────────────┐
│                        配置管理菜单                          │
├─────────────────────────────────────────────────────────────┤
│  1️⃣  查看当前配置 - 显示所有配置项                        │
│  2️⃣  管理代理设置 - 修改网络代理配置                      │
│  3️⃣  管理网络设置 - 修改超时和重试配置                    │
│  4️⃣  管理日志设置 - 修改日志级别和格式                    │
│  5️⃣  重置为默认配置 - 恢复所有设置为默认值                │
│  6️⃣  重新加载配置 - 从文件重新加载配置                    │
│  0️⃣  退出程序     - 保存并退出配置管理器                  │
└─────────────────────────────────────────────────────────────┘
        """
        print(menu)
    
    def show_current_config(self):
        """显示当前配置"""
        print("\n" + "="*60)
        print("📋 当前配置信息")
        print("="*60)
        
        # 网络配置
        print("\n🌐 网络配置:")
        print(f"  代理启用: {'✅ 是' if self.config.network.proxy_enabled else '❌ 否'}")
        if self.config.network.proxy_enabled:
            print(f"  HTTP代理: {self.config.network.proxy_http}")
            print(f"  HTTPS代理: {self.config.network.proxy_https}")
        print(f"  请求超时: {self.config.network.request_timeout}秒")
        print(f"  下载超时: {self.config.network.download_timeout}秒")
        print(f"  最大重试: {self.config.network.max_retries}次")
        print(f"  重试延迟: {self.config.network.retry_delay}秒")
        
        # 日志配置
        print("\n📝 日志配置:")
        print(f"  日志级别: {self.config.log.level}")
        print(f"  文件日志: {'✅ 启用' if self.config.log.file_enabled else '❌ 禁用'}")
        if self.config.log.file_enabled:
            print(f"  日志文件: {self.config.log.file_path}")
        
        # API配置
        print("\n🔗 API配置:")
        print(f"  谷歌表格URL: {self.config.api.google_sheets_url[:50]}...")
        print(f"  BD2 CDN地址: {self.config.api.bd2_base_url}")
        
        # 项目配置
        print("\n🎮 项目配置:")
        print(f"  项目名称: {self.config.project.project_name}")
        print(f"  项目版本: {self.config.project.version}")
        print(f"  Unity版本: {self.config.project.unity_version}")
        print(f"  最大并发: {self.config.project.max_workers}")
        
        print("="*60)
    
    def manage_proxy_settings(self):
        """管理代理设置"""
        print("\n" + "="*60)
        print("🌐 代理设置管理")
        print("="*60)
        
        # 显示当前代理设置
        print(f"\n当前代理状态: {'✅ 启用' if self.config.network.proxy_enabled else '❌ 禁用'}")
        if self.config.network.proxy_enabled:
            print(f"HTTP代理: {self.config.network.proxy_http}")
            print(f"HTTPS代理: {self.config.network.proxy_https}")
        
        print("\n代理设置选项:")
        print("1. 启用/禁用代理")
        print("2. 修改代理地址")
        print("3. 返回主菜单")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            self._toggle_proxy()
        elif choice == "2":
            self._modify_proxy_address()
        elif choice == "3":
            return
        else:
            print("❌ 无效选择")
    
    def _toggle_proxy(self):
        """切换代理启用状态"""
        current_status = self.config.network.proxy_enabled
        new_status = not current_status
        
        confirm = input(f"\n是否{'禁用' if current_status else '启用'}代理？(y/N): ").strip().lower()
        if confirm in ['y', 'yes', '是']:
            self.config.network.proxy_enabled = new_status
            self.config.save_config()
            status_text = "启用" if new_status else "禁用"
            print(f"✅ 代理已{status_text}")
        else:
            print("⚠️  操作已取消")
    
    def _modify_proxy_address(self):
        """修改代理地址"""
        print(f"\n当前HTTP代理: {self.config.network.proxy_http}")
        print(f"当前HTTPS代理: {self.config.network.proxy_https}")
        
        new_http = input("\n请输入新的HTTP代理地址 (回车保持不变): ").strip()
        new_https = input("请输入新的HTTPS代理地址 (回车保持不变): ").strip()
        
        changed = False
        if new_http and new_http != self.config.network.proxy_http:
            self.config.network.proxy_http = new_http
            changed = True
        
        if new_https and new_https != self.config.network.proxy_https:
            self.config.network.proxy_https = new_https
            changed = True
        
        if changed:
            self.config.save_config()
            print("✅ 代理地址已更新")
        else:
            print("⚠️  未进行任何修改")
    
    def manage_network_settings(self):
        """管理网络设置"""
        print("\n" + "="*60)
        print("⏱️  网络设置管理")
        print("="*60)
        
        print(f"\n当前网络设置:")
        print(f"请求超时: {self.config.network.request_timeout}秒")
        print(f"下载超时: {self.config.network.download_timeout}秒")
        print(f"最大重试: {self.config.network.max_retries}次")
        print(f"重试延迟: {self.config.network.retry_delay}秒")
        
        print("\n是否要修改网络设置？")
        confirm = input("输入 'y' 继续修改，其他键返回主菜单: ").strip().lower()
        
        if confirm in ['y', 'yes', '是']:
            self._modify_network_settings()
        else:
            return
    
    def _modify_network_settings(self):
        """修改网络设置"""
        try:
            new_request_timeout = input(f"\n请求超时 (当前: {self.config.network.request_timeout}秒, 回车保持不变): ").strip()
            if new_request_timeout:
                self.config.network.request_timeout = float(new_request_timeout)
            
            new_download_timeout = input(f"下载超时 (当前: {self.config.network.download_timeout}秒, 回车保持不变): ").strip()
            if new_download_timeout:
                self.config.network.download_timeout = float(new_download_timeout)
            
            new_max_retries = input(f"最大重试 (当前: {self.config.network.max_retries}次, 回车保持不变): ").strip()
            if new_max_retries:
                self.config.network.max_retries = int(new_max_retries)
            
            new_retry_delay = input(f"重试延迟 (当前: {self.config.network.retry_delay}秒, 回车保持不变): ").strip()
            if new_retry_delay:
                self.config.network.retry_delay = float(new_retry_delay)
            
            self.config.save_config()
            print("✅ 网络设置已更新")
            
        except ValueError as e:
            print(f"❌ 输入格式错误: {e}")
    
    def manage_log_settings(self):
        """管理日志设置"""
        print("\n" + "="*60)
        print("📝 日志设置管理")
        print("="*60)
        
        print(f"\n当前日志设置:")
        print(f"日志级别: {self.config.log.level}")
        print(f"文件日志: {'✅ 启用' if self.config.log.file_enabled else '❌ 禁用'}")
        if self.config.log.file_enabled:
            print(f"日志文件: {self.config.log.file_path}")
        
        print("\n日志级别选项:")
        print("1. DEBUG - 详细调试信息")
        print("2. INFO - 一般信息 (推荐)")
        print("3. WARNING - 警告信息")
        print("4. ERROR - 错误信息")
        print("5. 切换文件日志状态")
        print("6. 返回主菜单")
        
        choice = input("\n请选择 (1-6): ").strip()
        
        if choice == "1":
            self.config.log.level = "DEBUG"
            self.config.save_config()
            print("✅ 日志级别已设置为 DEBUG")
        elif choice == "2":
            self.config.log.level = "INFO"
            self.config.save_config()
            print("✅ 日志级别已设置为 INFO")
        elif choice == "3":
            self.config.log.level = "WARNING"
            self.config.save_config()
            print("✅ 日志级别已设置为 WARNING")
        elif choice == "4":
            self.config.log.level = "ERROR"
            self.config.save_config()
            print("✅ 日志级别已设置为 ERROR")
        elif choice == "5":
            self.config.log.file_enabled = not self.config.log.file_enabled
            self.config.save_config()
            status = "启用" if self.config.log.file_enabled else "禁用"
            print(f"✅ 文件日志已{status}")
        elif choice == "6":
            return
        else:
            print("❌ 无效选择")
    
    def reset_to_default(self):
        """重置为默认配置"""
        print("\n" + "="*60)
        print("🔄 重置配置")
        print("="*60)
        
        print("⚠️  警告：此操作将重置所有配置为默认值！")
        confirm = input("是否确定要重置配置？请输入 'RESET' 确认: ").strip()
        
        if confirm == "RESET":
            # 删除配置文件，重新加载会创建默认配置
            if self.config.config_file.exists():
                self.config.config_file.unlink()
            
            # 重新加载配置
            self.config = reload_config()
            print("✅ 配置已重置为默认值")
        else:
            print("⚠️  重置操作已取消")
    
    def reload_configuration(self):
        """重新加载配置"""
        print("\n" + "="*60)
        print("🔄 重新加载配置")
        print("="*60)
        
        try:
            self.config = reload_config()
            print("✅ 配置已重新加载")
        except Exception as e:
            print(f"❌ 重新加载配置失败: {e}")
    
    def get_user_choice(self) -> Optional[str]:
        """获取用户选择"""
        try:
            choice = input("\n请选择操作 (0-6): ").strip()
            return choice
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断程序")
            return "0"
        except EOFError:
            print("\n\n⚠️  输入结束，退出程序")
            return "0"
        except Exception as e:
            print(f"⚠️  输入错误: {e}")
            return None
    
    def run(self):
        """运行配置管理器"""
        try:
            # 显示横幅
            self.show_banner()
            
            while True:
                # 显示菜单
                self.show_menu()
                
                # 获取用户选择
                choice = self.get_user_choice()
                
                if choice is None:
                    continue
                
                # 执行对应功能
                if choice == "1":
                    self.show_current_config()
                elif choice == "2":
                    self.manage_proxy_settings()
                elif choice == "3":
                    self.manage_network_settings()
                elif choice == "4":
                    self.manage_log_settings()
                elif choice == "5":
                    self.reset_to_default()
                elif choice == "6":
                    self.reload_configuration()
                elif choice == "0":
                    print("\n💾 保存配置并退出...")
                    self.config.save_config()
                    print("👋 感谢使用BD2配置管理工具！")
                    break
                else:
                    print("❌ 无效选择，请输入 0-6")
                
                # 等待用户按键继续
                if choice != "0":
                    input("\n按 Enter 键继续...")
                    # 清屏（跨平台）
                    os.system('cls' if os.name == 'nt' else 'clear')
        
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断程序")
        except Exception as e:
            print(f"❌ 程序异常: {e}")
        finally:
            print("\n程序结束")


def main():
    """主函数"""
    try:
        # 创建配置管理器实例
        manager = ConfigManager()
        
        # 运行配置管理器
        manager.run()
        
        return 0
        
    except Exception as e:
        print(f"❌ 程序启动失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
