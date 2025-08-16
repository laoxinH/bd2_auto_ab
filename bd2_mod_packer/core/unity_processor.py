#!/usr/bin/env python3
"""
Unity资源处理工具

Unity Bundle文件处理工具，用于替换Spine动画资源。
支持替换.skel、.atlas文件和贴图资源。

功能特性：
- 🎯 智能文件匹配和替换
- 🛡️ 完善的错误处理机制
- 📝 详细的中文日志记录
- 🔄 批量处理支持
- 💾 自动备份功能

作者: OLDNEW
日期: 2025-08-14
"""

import logging
import os
import shutil
import time
from typing import Optional, Dict, List, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

import UnityPy
from PIL import Image
from UnityPy.enums import TextureFormat

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        # 可选：添加文件日志
        # logging.FileHandler('unity_tools.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class ProcessingError(Exception):
    """Unity资源处理自定义异常类"""
    pass


class FileType(Enum):
    """支持的文件类型枚举"""
    SKEL = "skel"
    ATLAS = "atlas"
    PNG = "png"
    UNKNOWN = "unknown"


@dataclass
class ProcessingStats:
    """处理统计信息"""
    total_bundles: int = 0
    processed_bundles: int = 0
    skipped_bundles: int = 0
    failed_bundles: int = 0
    replaced_files: int = 0
    skipped_files: int = 0
    start_time: float = 0.0
    end_time: float = 0.0
    
    @property
    def duration(self) -> float:
        """处理总耗时（秒）"""
        return self.end_time - self.start_time if self.end_time > 0 else time.time() - self.start_time
    
    def __str__(self) -> str:
        return (
            f"处理统计:\n"
            f"  总Bundle数: {self.total_bundles}\n"
            f"  已处理: {self.processed_bundles}\n"
            f"  已跳过: {self.skipped_bundles}\n"
            f"  失败: {self.failed_bundles}\n"
            f"  替换文件数: {self.replaced_files}\n"
            f"  跳过文件数: {self.skipped_files}\n"
            f"  处理耗时: {self.duration:.2f}秒"
        )


class UnityResourceProcessor:
    """
    Unity资源处理器
    
    专业的Unity Bundle资源替换工具，支持Spine动画相关资源的批量替换。
    """
    
    def __init__(self, 
                 unity_version: str = '2022.3.22f1',
                 create_backup: bool = True,
                 backup_suffix: str = '.backup'):
        """
        初始化Unity资源处理器
        
        参数:
            unity_version: Unity版本号
            create_backup: 是否创建备份文件
            backup_suffix: 备份文件后缀
        """
        self.unity_version = unity_version
        self.create_backup = create_backup
        self.backup_suffix = backup_suffix
        self.stats = ProcessingStats()
        
        # 设置UnityPy配置
        UnityPy.config.FALLBACK_UNITY_VERSION = unity_version
        
        logger.info(f"Unity资源处理器初始化完成 (Unity版本: {unity_version})")
    
    def _validate_paths(self, *paths: str) -> None:
        """
        验证路径是否存在
        
        参数:
            *paths: 要验证的路径列表
            
        异常:
            ProcessingError: 如果路径不存在
        """
        for path in paths:
            if not os.path.exists(path):
                raise ProcessingError(f"路径不存在: {path}")
    
    def _create_backup(self, file_path: str) -> Optional[str]:
        """
        创建文件备份
        
        参数:
            file_path: 要备份的文件路径
            
        返回:
            Optional[str]: 备份文件路径，如果创建失败返回None
        """
        if not self.create_backup:
            return None
            
        try:
            backup_path = f"{file_path}{self.backup_suffix}"
            if not os.path.exists(backup_path):
                shutil.copy2(file_path, backup_path)
                logger.debug(f"创建备份: {backup_path}")
                return backup_path
        except Exception as e:
            logger.warning(f"创建备份失败 {file_path}: {e}")
        return None
    
    def _get_file_type(self, filename: str) -> FileType:
        """
        根据文件名确定文件类型
        
        参数:
            filename: 文件名
            
        返回:
            FileType: 文件类型枚举
        """
        filename_lower = filename.lower()
        if filename_lower.endswith('.skel'):
            return FileType.SKEL
        elif filename_lower.endswith('.atlas'):
            return FileType.ATLAS
        elif filename_lower.endswith('.png'):
            return FileType.PNG
        else:
            return FileType.UNKNOWN
    
    def _should_skip_file(self, data_name: str, replace_root: str) -> bool:
        """
        判断是否应该跳过文件（基于.json文件和.skel文件的存在性）
        
        参数:
            data_name: 数据文件名
            replace_root: 替换文件根目录
            
        返回:
            bool: 是否应该跳过
        """
        # 检查是否存在对应的.json文件但没有.skel文件
        json_path = os.path.join(replace_root, data_name.replace('.atlas', '.json').replace('.png', '.json'))
        skel_path = os.path.join(replace_root, data_name.replace('.atlas', '.skel').replace('.png', '.skel'))
        
        if os.path.exists(json_path) and not os.path.exists(skel_path):
            logger.info(f"发现.json文件但无.skel文件，跳过 {data_name}")
            return True
        return False
    
    def _find_replacement_file(self, target_name: str, replace_dir: str) -> Optional[str]:
        """
        在替换目录中查找匹配的文件
        
        参数:
            target_name: 目标文件名
            replace_dir: 替换文件目录
            
        返回:
            Optional[str]: 找到的文件路径，未找到返回None
        """
        for root, _, files in os.walk(replace_dir):
            if target_name in files:
                return os.path.join(root, target_name)
        return None
    
    def _replace_text_asset(self, data, replacement_path: str) -> bool:
        """
        替换文本资源（.skel, .atlas文件）
        
        参数:
            data: Unity文本资源对象
            replacement_path: 替换文件路径
            
        返回:
            bool: 是否成功替换
        """
        try:
            with open(replacement_path, 'rb') as f:
                content = f.read().decode("utf-8", "surrogateescape")
                data.m_Script = content
                data.save()
                logger.info(f"成功替换文本资源: {data.m_Name}")
                return True
        except Exception as e:
            logger.error(f"替换文本资源失败 {data.m_Name}: {e}")
            return False
    
    def _replace_texture(self, data, replacement_path: str) -> bool:
        """
        替换贴图资源
        
        参数:
            data: Unity贴图对象
            replacement_path: 替换文件路径
            
        返回:
            bool: 是否成功替换
        """
        try:
            pil_img = Image.open(replacement_path)
            data.set_image(img=pil_img, target_format=TextureFormat.RGBA32)
            data.save()
            logger.info(f"成功替换贴图资源: {data.m_Name}")
            return True
        except Exception as e:
            logger.error(f"替换贴图资源失败 {data.m_Name}: {e}")
            return False
    
    def process_single_bundle(self, bundle_path: str, replace_dir: str, target_path: str) -> bool:
        """
        处理单个Bundle文件
        
        参数:
            bundle_path: Bundle文件路径
            replace_dir: 替换文件目录
            target_path: 输出文件路径
            
        返回:
            bool: 是否成功处理
        """
        try:
            logger.info(f"开始处理Bundle: {bundle_path}")
            
            # 创建备份
            self._create_backup(bundle_path)
            
            # 加载Bundle
            env = UnityPy.load(bundle_path)
            replaced_count = 0
            
            # 遍历Bundle中的所有对象
            for obj in env.objects:
                try:
                    if obj.type.name == 'TextAsset':
                        data = obj.read()
                        file_type = self._get_file_type(data.m_Name)
                        
                        if file_type in [FileType.SKEL, FileType.ATLAS]:
                            # 检查是否应该跳过
                            if self._should_skip_file(data.m_Name, replace_dir):
                                self.stats.skipped_files += 1
                                continue
                            
                            # 查找替换文件
                            replacement_path = self._find_replacement_file(data.m_Name, replace_dir)
                            if replacement_path:
                                if self._replace_text_asset(data, replacement_path):
                                    replaced_count += 1
                                    self.stats.replaced_files += 1
                    
                    elif obj.type.name == 'Texture2D':
                        data = obj.read()
                        png_name = f"{data.m_Name}.png"
                        
                        # 检查是否应该跳过
                        if self._should_skip_file(png_name, replace_dir):
                            self.stats.skipped_files += 1
                            continue
                        
                        # 查找替换文件
                        replacement_path = self._find_replacement_file(png_name, replace_dir)
                        if replacement_path:
                            if self._replace_texture(data, replacement_path):
                                replaced_count += 1
                                self.stats.replaced_files += 1
                
                except Exception as e:
                    logger.error(f"处理对象失败: {e}")
                    continue
            
            # 保存Bundle
            if replaced_count > 0:
                # 确保目标目录存在
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                with open(target_path, "wb") as f:
                    envdata = env.file.save(packer="lz4")
                    f.write(envdata)
                    logger.info(f"Bundle保存完成: {target_path} (替换了{replaced_count}个文件)")
            else:
                logger.info(f"Bundle无变更，跳过保存: {bundle_path}")
            
            self.stats.processed_bundles += 1
            return True
            
        except Exception as e:
            logger.error(f"处理Bundle失败 {bundle_path}: {e}")
            self.stats.failed_bundles += 1
            return False
    
    def process_multiple_replace_dirs(self, bundle_path: str, replace_dirs: List[str], target_path: str) -> bool:
        """
        使用多个替换目录处理单个Bundle文件
        
        参数:
            bundle_path: 源Bundle文件路径
            replace_dirs: 替换文件目录列表
            target_path: 输出文件路径
            
        返回:
            bool: 是否成功处理
        """
        try:
            logger.info(f"开始处理Bundle (多目录替换): {bundle_path}")
            logger.info(f"替换目录数量: {len(replace_dirs)}")
            logger.info(f"目标路径: {target_path}")
            
            # 验证路径
            self._validate_paths(bundle_path)
            for replace_dir in replace_dirs:
                self._validate_paths(replace_dir)
            
            # 创建备份
            self._create_backup(bundle_path)
            
            # 创建目标目录
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # 加载Bundle
            env = UnityPy.load(bundle_path)
            replaced_count = 0
            total_files = 0
            
            # 遍历Bundle中的所有对象
            for obj in env.objects:
                try:
                    if obj.type.name == 'TextAsset':
                        data = obj.read()
                        
                        # 安全获取对象名称
                        try:
                            object_name = data.m_Name
                        except AttributeError:
                            logger.debug(f"TextAsset对象没有name属性，跳过")
                            continue
                        
                        file_type = self._get_file_type(object_name)
                        
                        if file_type in [FileType.SKEL, FileType.ATLAS]:
                            total_files += 1
                            
                            # 在所有替换目录中查找替换文件
                            replacement_found = False
                            for replace_dir in replace_dirs:
                                # 检查是否应该跳过
                                if self._should_skip_file(object_name, replace_dir):
                                    continue
                                
                                # 查找替换文件
                                replacement_path = self._find_replacement_file(object_name, replace_dir)
                                if replacement_path:
                                    if self._replace_text_asset(data, replacement_path):
                                        replaced_count += 1
                                        replacement_found = True
                                        logger.info(f"从目录 {replace_dir} 替换了 {object_name}")
                                        break  # 找到替换文件后跳出循环
                            
                            if not replacement_found:
                                logger.debug(f"未找到替换文件: {object_name}")
                    
                    elif obj.type.name == 'Texture2D':
                        data = obj.read()
                        
                        # 安全获取对象名称
                        try:
                            object_name = data.m_Name
                        except AttributeError:
                            logger.debug(f"Texture2D对象没有name属性，跳过")
                            continue
                        
                        png_name = f"{object_name}.png"
                        total_files += 1
                        
                        # 在所有替换目录中查找替换文件
                        replacement_found = False
                        for replace_dir in replace_dirs:
                            # 检查是否应该跳过
                            if self._should_skip_file(png_name, replace_dir):
                                continue
                            
                            # 查找替换文件
                            replacement_path = self._find_replacement_file(png_name, replace_dir)
                            if replacement_path:
                                if self._replace_texture(data, replacement_path):
                                    replaced_count += 1
                                    replacement_found = True
                                    logger.info(f"从目录 {replace_dir} 替换了 {png_name}")
                                    break  # 找到替换文件后跳出循环
                        
                        if not replacement_found:
                            logger.debug(f"未找到替换文件: {png_name}")
                
                except Exception as e:
                    logger.warning(f"处理对象失败: {e}")
                    continue
            
            # 保存到目标路径
            with open(target_path, 'wb') as f:
                f.write(env.file.save(packer="lz4"))
            
            logger.info(f"Bundle处理完成: 总文件={total_files}, 替换文件={replaced_count}")
            logger.info(f"输出文件: {target_path}")
            
            self.stats.processed_bundles += 1
            self.stats.replaced_files += replaced_count
            
            return True
            
        except Exception as e:
            logger.error(f"多目录处理Bundle失败 {bundle_path}: {e}")
            self.stats.failed_bundles += 1
            return False
    
    def replace_spine_files(self, data_dir: str, replace_dir: str, target_dir: str) -> ProcessingStats:
        """
        批量替换Spine文件
        
        参数:
            data_dir: 源数据目录
            replace_dir: 替换文件目录  
            target_dir: 目标输出目录
            
        返回:
            ProcessingStats: 处理统计信息
            
        异常:
            ProcessingError: 处理过程中的错误
        """
        try:
            # 验证路径
            self._validate_paths(data_dir, replace_dir)
            
            # 初始化统计
            self.stats = ProcessingStats()
            self.stats.start_time = time.time()
            
            logger.info(f"开始批量处理Spine文件")
            logger.info(f"源目录: {data_dir}")
            logger.info(f"替换目录: {replace_dir}")
            logger.info(f"目标目录: {target_dir}")
            
            # 创建目标目录
            os.makedirs(target_dir, exist_ok=True)
            
            # 统计总文件数
            bundle_files = []
            for root, dirs, files in os.walk(data_dir):
                for file in files:
                    if file == "__data":
                        bundle_path = os.path.join(root, file)
                        bundle_files.append(bundle_path)
            
            self.stats.total_bundles = len(bundle_files)
            logger.info(f"发现 {self.stats.total_bundles} 个Bundle文件")
            
            # 处理每个Bundle文件
            for i, bundle_path in enumerate(bundle_files, 1):
                logger.info(f"进度: [{i}/{self.stats.total_bundles}] 处理 {bundle_path}")
                
                # 构建目标文件路径
                rel_path = os.path.relpath(bundle_path, data_dir)
                target_path = os.path.join(target_dir, rel_path)
                
                # 处理Bundle
                if not self.process_single_bundle(bundle_path, replace_dir, target_path):
                    self.stats.skipped_bundles += 1
            
            self.stats.end_time = time.time()
            
            logger.info("批量处理完成")
            logger.info(str(self.stats))
            
            return self.stats
            
        except Exception as e:
            self.stats.end_time = time.time()
            logger.error(f"批量处理失败: {e}")
            raise ProcessingError(f"批量处理失败: {e}")
    
    def get_bundle_info(self, bundle_path: str) -> Dict:
        """
        获取Bundle文件信息
        
        参数:
            bundle_path: Bundle文件路径
            
        返回:
            Dict: Bundle信息字典
        """
        try:
            self._validate_paths(bundle_path)
            
            env = UnityPy.load(bundle_path)
            info = {
                "path": bundle_path,
                "size": os.path.getsize(bundle_path),
                "objects": [],
                "text_assets": [],
                "textures": []
            }
            
            for obj in env.objects:
                obj_info = {
                    "type": obj.type.name,
                    "path_id": obj.path_id
                }
                info["objects"].append(obj_info)
                
                if obj.type.name == 'TextAsset':
                    data = obj.read()
                    info["text_assets"].append({
                        "name": data.m_Name,
                        "size": len(data.m_Script) if hasattr(data, 'm_Script') else 0
                    })
                elif obj.type.name == 'Texture2D':
                    data = obj.read()
                    info["textures"].append({
                        "name": data.m_Name,
                        "width": data.m_Width if hasattr(data, 'm_Width') else 0,
                        "height": data.m_Height if hasattr(data, 'm_Height') else 0,
                        "format": str(data.m_TextureFormat) if hasattr(data, 'm_TextureFormat') else "unknown"
                    })
            
            return info
            
        except Exception as e:
            logger.error(f"获取Bundle信息失败 {bundle_path}: {e}")
            raise ProcessingError(f"获取Bundle信息失败: {e}")


# 兼容性函数（保持原有接口）
def replace_spine_files(data_dir: str, replace_dir: str, target_dir: str) -> None:
    """
    批量替换Spine文件（兼容性函数）
    
    保持与原有函数相同的接口，内部使用新的UnityResourceProcessor实现。
    
    参数:
        data_dir: 源数据目录
        replace_dir: 替换文件目录
        target_dir: 目标输出目录
    """
    processor = UnityResourceProcessor()
    try:
        stats = processor.replace_spine_files(data_dir, replace_dir, target_dir)
        logger.info(f"兼容性函数调用完成: {stats.replaced_files}个文件被替换")
    except ProcessingError as e:
        logger.error(f"兼容性函数调用失败: {e}")
        raise


# 主函数和测试代码
if __name__ == "__main__":
    print("🎮 Unity资源处理工具 - 测试模式")
    print("=" * 50)
    
    # 创建处理器实例
    processor = UnityResourceProcessor(create_backup=True)
    
    # 示例用法
    try:
        # 这里可以添加测试代码
        print("✅ Unity资源处理器初始化成功")
        print("💡 使用示例:")
        print("   processor = UnityResourceProcessor()")
        print("   stats = processor.replace_spine_files(data_dir, replace_dir, target_dir)")
        print("   print(stats)")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")


# 导出的公共API
__all__ = [
    "UnityResourceProcessor", 
    "ProcessingStats", 
    "ProcessingError",
    "FileType",
    "replace_spine_files"  # 兼容性函数
]
