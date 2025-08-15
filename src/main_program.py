#!/usr/bin/env python3
"""
BD2资源替换主程序

BD2游戏资源替换自动化程序，包括：
- 版本检测和更新
- 替换文件变更追踪
- 资源下载和替换

使用方法:
    python main_program.py

作者: oldnew
日期: 2025-08-14
"""

import logging
import sys

# 导入BD2ResourceManager和配置
from BD2ResourceManager import BD2ResourceManager
from config import get_config

# 获取配置
config = get_config()
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    try:
        logger.info("🎮 BD2资源替换主程序启动")
        logger.info("=" * 60)
        
        # 创建资源管理器实例
        manager = BD2ResourceManager(proxies=config.get_proxies())
        
        # 第一步：检查版本和更新
        logger.info("📋 第一步：检查版本和文件更新...")
        needs_update, summary = manager.check_version_and_updates()
        
        # 输出检测结果
        logger.info("📊 检测结果摘要:")
        logger.info(f"  版本变化: {summary.version_changed}")
        if summary.old_version is not None and summary.new_version is not None:
            logger.info(f"  版本: {summary.old_version} -> {summary.new_version}")
        logger.info(f"  总替换目录数: {summary.total_replace_dirs}")
        logger.info(f"  需要更新的目录数: {len(summary.replace_dirs_to_update)}")
        
        # 判断是否需要执行替换流程
        if not needs_update:
            logger.info("✅ 无需更新，程序退出")
            return 0
        
        # 如果版本有变化，执行完整替换流程
        if summary.version_changed:
            logger.info("🔄 检测到版本更新，开始执行完整替换流程...")
            
            # 处理更新
            success = manager.process_updates(summary)
            
            if success:
                logger.info("✅ 完整替换流程执行完成")
            else:
                logger.error("❌ 完整替换流程执行失败")
                return 1
        
        # 如果只是文件更新，执行增量替换
        elif summary.replace_dirs_to_update:
            logger.info("🔄 检测到文件更新，开始执行增量替换...")
            
            # 处理更新
            success = manager.process_updates(summary)
            
            if success:
                logger.info("✅ 增量替换执行完成")
            else:
                logger.error("❌ 增量替换执行失败")
                return 1
        
        logger.info("🎉 BD2资源替换程序执行完成")
        return 0
        
    except KeyboardInterrupt:
        logger.info("⚠️ 用户中断程序")
        return 1
    except Exception as e:
        logger.error(f"💥 程序异常退出: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
