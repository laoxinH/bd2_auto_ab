#!/usr/bin/env python3
"""
BD2 目录初始化脚本

从谷歌表格获取角色数据，自动创建replace目录结构。
目录格式: replace\\{Character}\\{Costume}\\{Type}

支持的类型:
- CUTSCENE: 技能动画资源
- IDLE: 待机动画资源

使用示例:
    python initialize_directories.py
    
功能特性:
- 🌐 从谷歌表格获取最新角色数据
- 📁 自动创建目录结构
- 🔍 智能跳过已存在的目录
- 📊 显示创建统计信息
- 🛡️ 完善的错误处理
"""

import os
import sys
from pathlib import Path
from typing import Set, Tuple
import logging
from CharacterScraper import CharacterScraper, CharacterData

# 导入配置
try:
    from config import get_config
    _config_available = True
except ImportError:
    _config_available = False

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DirectoryInitializer:
    """
    BD2 目录初始化器
    
    功能：
    - 从谷歌表格获取角色数据
    - 创建replace目录结构
    - 支持IDLE和CUTSCENE类型
    - 智能跳过已存在目录
    """
    
    def __init__(self, project_root: str = None):
        """
        初始化目录创建器
        
        Args:
            project_root: 项目根目录路径，如果不提供则自动检测
        """
        if project_root is None:
            # 自动检测项目根目录
            current_dir = Path(__file__).parent
            project_root = current_dir.parent
            
        self.project_root = Path(project_root)
        self.replace_root = self.project_root / "replace"
        
        # 创建CharacterScraper实例，会自动使用配置文件中的代理设置
        if _config_available:
            config = get_config()
            self.scraper = CharacterScraper(proxies=config.get_proxies())
        else:
            self.scraper = CharacterScraper()
        
        logger.info(f"项目根目录: {self.project_root}")
        logger.info(f"替换目录根路径: {self.replace_root}")
    
    def ensure_replace_root(self) -> None:
        """确保replace根目录存在"""
        if not self.replace_root.exists():
            self.replace_root.mkdir(parents=True, exist_ok=True)
            logger.info(f"创建replace根目录: {self.replace_root}")
        else:
            logger.info(f"replace根目录已存在: {self.replace_root}")
    
    def sanitize_name(self, name: str) -> str:
        """
        清理文件名，移除Windows不支持的字符
        
        Args:
            name: 原始名称
            
        Returns:
            清理后的名称
        """
        # Windows不支持的字符
        invalid_chars = '<>:"|?*'
        for char in invalid_chars:
            name = name.replace(char, '')
        
        # 移除前后空格和点号
        name = name.strip(' .')
        
        return name
    
    def get_directory_types(self, character_data: CharacterData) -> Set[str]:
        """
        根据角色数据确定需要创建的目录类型
        
        Args:
            character_data: 角色数据
            
        Returns:
            目录类型集合 (IDLE, CUTSCENE)
        """
        types = set()
        
        # 检查IDLE值
        if character_data.idle and str(character_data.idle).strip():
            idle_str = str(character_data.idle).strip()
            if idle_str and idle_str != "0" and idle_str.lower() != "none":
                types.add("IDLE")
        
        # 检查CUTSCENE值
        if character_data.cutscene and str(character_data.cutscene).strip():
            cutscene_str = str(character_data.cutscene).strip()
            if cutscene_str and cutscene_str != "0" and cutscene_str.lower() != "none":
                types.add("CUTSCENE")
        
        return types
    
    def create_character_directories(self, character_data: CharacterData) -> Tuple[int, int]:
        """
        为单个角色创建目录结构
        
        Args:
            character_data: 角色数据
            
        Returns:
            (创建的目录数, 跳过的目录数)
        """
        created = 0
        skipped = 0
        
        # 清理角色和服装名称
        character_name = self.sanitize_name(character_data.character)
        costume_name = self.sanitize_name(character_data.costume)
        
        if not character_name or not costume_name:
            logger.warning(f"跳过无效的角色数据: character='{character_data.character}', costume='{character_data.costume}'")
            return 0, 0
        
        # 获取需要创建的目录类型
        types = self.get_directory_types(character_data)
        
        if not types:
            logger.debug(f"跳过无资源的角色: {character_name}/{costume_name}")
            return 0, 0
        
        # 为每种类型创建目录
        for dir_type in types:
            dir_path = self.replace_root / character_name / costume_name / dir_type
            
            if dir_path.exists():
                logger.debug(f"目录已存在，跳过: {dir_path.relative_to(self.project_root)}")
                skipped += 1
            else:
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"✅ 创建目录: {dir_path.relative_to(self.project_root)}")
                created += 1
        
        return created, skipped
    
    def initialize_all_directories(self) -> None:
        """
        初始化所有角色目录
        """
        logger.info("🚀 开始初始化BD2角色目录结构...")
        
        # 确保replace根目录存在
        self.ensure_replace_root()
        
        try:
            # 从谷歌表格获取所有角色数据
            logger.info("📊 从谷歌表格获取角色数据...")
            all_data = self.scraper.get_all_data()
            logger.info(f"获取到 {len(all_data)} 条角色数据")
            
            if not all_data:
                logger.warning("未获取到任何角色数据，请检查网络连接或数据源")
                return
            
            # 统计信息
            total_created = 0
            total_skipped = 0
            processed_characters = set()
            
            # 为每个角色创建目录
            logger.info("📁 开始创建目录结构...")
            for i, character_data in enumerate(all_data, 1):
                try:
                    created, skipped = self.create_character_directories(character_data)
                    total_created += created
                    total_skipped += skipped
                    
                    # 记录处理的角色
                    char_key = f"{character_data.character}/{character_data.costume}"
                    processed_characters.add(char_key)
                    
                    # 显示进度
                    if i % 10 == 0 or i == len(all_data):
                        logger.info(f"进度: {i}/{len(all_data)} ({i/len(all_data)*100:.1f}%)")
                        
                except Exception as e:
                    logger.error(f"处理角色数据时出错: {character_data} - {e}")
                    continue
            
            # 显示最终统计
            logger.info("🎉 目录初始化完成!")
            logger.info(f"📊 统计信息:")
            logger.info(f"  - 处理角色数据: {len(all_data)} 条")
            logger.info(f"  - 处理角色/服装组合: {len(processed_characters)} 个")
            logger.info(f"  - 创建新目录: {total_created} 个")
            logger.info(f"  - 跳过已存在目录: {total_skipped} 个")
            logger.info(f"  - 目录根路径: {self.replace_root}")
            
        except Exception as e:
            logger.error(f"初始化过程中发生错误: {e}")
            raise
    
    def list_existing_directories(self) -> None:
        """
        列出已存在的目录结构
        """
        if not self.replace_root.exists():
            logger.info("replace目录不存在")
            return
        
        logger.info("📋 当前目录结构:")
        
        count = 0
        for character_dir in sorted(self.replace_root.iterdir()):
            if not character_dir.is_dir():
                continue
                
            for costume_dir in sorted(character_dir.iterdir()):
                if not costume_dir.is_dir():
                    continue
                    
                types = []
                for type_dir in sorted(costume_dir.iterdir()):
                    if type_dir.is_dir():
                        types.append(type_dir.name)
                
                if types:
                    relative_path = costume_dir.relative_to(self.project_root)
                    logger.info(f"  {relative_path} -> {', '.join(types)}")
                    count += 1
        
        logger.info(f"总计: {count} 个角色/服装组合")


def main():
    """主函数"""
    try:
        # 创建初始化器
        initializer = DirectoryInitializer()
        
        # 显示当前目录结构
        initializer.list_existing_directories()
        
        # 执行初始化
        initializer.initialize_all_directories()
        
        # 再次显示目录结构
        print("\n" + "="*60)
        initializer.list_existing_directories()
        
    except KeyboardInterrupt:
        logger.info("用户中断操作")
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
