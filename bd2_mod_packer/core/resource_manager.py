#!/usr/bin/env python3
"""
BD2资源替换主控制器

BD2游戏资源替换自动化流程控制器，包括：
- 版本检测和更新
- 替换文件变更追踪
- 资源下载和替换

作者: OLDNEW
日期: 2025-08-14
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

# 导入项目模块
from ..config.settings import BD2Config
from ..api import BD2CDNAPI
from .data_downloader import BD2DataDownloader
from .unity_processor import UnityResourceProcessor
from ..api import CharacterScraper

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ReplaceTask:
    """替换任务信息"""
    type: str  # IDLE或CUTSCENE
    replace_dir: str
    data_name: str
    downloaded_dir: str
    target_dir: str
    mod_name: str = ""
    idle_or_cutscene_value: str = ""
    hash_id: str = ""
    char_id: str = ""  # 角色ID，从mod文件名获取
    should_execute: bool = True  # 是否需要执行该任务
    


@dataclass
class ReplaceEntry:
    """替换目录条目"""
    path: str
    mtime: float
    subfile: List[Dict[str, Any]]


@dataclass
class UpdateSummary:
    """更新摘要"""
    version_changed: bool = False
    old_version: Optional[int] = None
    new_version: Optional[int] = None
    replace_dirs_to_update: List[str] = None
    total_replace_dirs: int = 0
    
    def __post_init__(self):
        if self.replace_dirs_to_update is None:
            self.replace_dirs_to_update = []


class BD2ResourceManager:
    """BD2资源管理器主控制器"""
    
    def __init__(self, project_root: str = None, proxies : Optional[Dict[str, str]] = None, replace_dir: str = "replace"):
        """
        初始化BD2资源管理器
        
        参数:
            project_root: 项目根目录，默认为当前脚本的上级目录
            proxies: 代理设置
            replace_dir: 替换目录名称，相对于项目根目录，默认为"replace"
        """
        # 初始化配置系统
        self.config = BD2Config()
        
        if project_root is None:
            # 获取项目根目录（main_v2.py的上级目录）
            current_file = Path(__file__).resolve()
            self.project_root = current_file.parent.parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.data_json_path = self.project_root / "data.json"
        # 使用workspace路径
        self.replace_dir = self.config.get_mod_workspace_path(replace_dir)
        self.replace_dir_name = replace_dir  # 保存目录名称用于data.json键值
        self.downloaded_dir = self.config.get_sourcedata_dir()
        self.target_dir = self.config.get_targetdata_dir() / replace_dir  # 为每个作者创建独立的target子目录
        
        # 初始化组件
        self.cdn_api = BD2CDNAPI(proxies=proxies)
        self.character_scraper = CharacterScraper(url=self.config.get_google_sheets_url(), proxies=proxies)
        self.unity_processor = UnityResourceProcessor()
        self.data_downloader = BD2DataDownloader(output_dir=str(self.downloaded_dir), proxies=proxies)

        logger.info(f"BD2资源管理器初始化完成，项目根目录: {self.project_root}")
        logger.info(f"使用替换目录: {self.replace_dir} (键值: {self.replace_dir_name})")
    
    def _load_data_json(self) -> Dict[str, Any]:
        """
        加载data.json文件
        
        返回:
            Dict[str, Any]: data.json内容，如果文件不存在返回默认结构
        """
        if not self.data_json_path.exists():
            logger.info("data.json不存在，将创建默认配置")
            return {
                "authors": {}  # 改为按作者分组的结构，移除全局版本信息
            }
        
        try:
            with open(self.data_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 兼容旧格式：如果发现旧的replaceDir字段，进行迁移
                if "replaceDir" in data and "authors" not in data:
                    logger.info("检测到旧格式data.json，正在迁移到新格式...")
                    old_replace_dirs = data.pop("replaceDir", [])
                    old_version = data.pop("version", 0)
                    old_update_time = data.pop("updateTime", 0)
                    data["authors"] = {
                        "replace": {
                            "version": old_version,
                            "updateTime": old_update_time,
                            "dirs": old_replace_dirs
                        }
                    }
                    # 保存迁移后的数据
                    self._save_data_json(data)
                    logger.info("data.json格式迁移完成")
                elif "authors" not in data:
                    data["authors"] = {}
                
                # 迁移旧的authors格式（数组格式）到新格式（对象格式）
                authors_data = data.get("authors", {})
                migration_needed = False
                for author_name, author_data in list(authors_data.items()):
                    if isinstance(author_data, list):  # 旧格式：直接是目录数组
                        logger.info(f"迁移作者'{author_name}'数据到新格式...")
                        old_version = data.get("version", 0)
                        old_update_time = data.get("updateTime", 0)
                        authors_data[author_name] = {
                            "version": old_version,
                            "updateTime": old_update_time,
                            "dirs": author_data
                        }
                        migration_needed = True
                
                if migration_needed:
                    # 清理全局版本信息
                    data.pop("version", None)
                    data.pop("updateTime", None)
                    data["authors"] = authors_data
                    self._save_data_json(data)
                    logger.info("作者数据格式迁移完成")
                
                # 获取当前作者的版本信息
                current_author = authors_data.get(self.replace_dir_name, {})
                current_version = current_author.get("version", 0)
                logger.info(f"成功加载data.json，作者'{self.replace_dir_name}'当前版本: {current_version}")
                return data
        except Exception as e:
            logger.error(f"加载data.json失败: {e}")
            logger.info("使用默认配置")
            return {
                "authors": {}
            }
    
    def _save_data_json(self, data: Dict[str, Any]) -> None:
        """
        保存data.json文件
        
        参数:
            data: 要保存的数据
        """
        try:
            with open(self.data_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            # 获取当前作者的版本信息用于日志
            current_author = data.get("authors", {}).get(self.replace_dir_name, {})
            current_version = current_author.get("version", 0)
            logger.info(f"成功保存data.json，作者'{self.replace_dir_name}'版本: {current_version}")
        except Exception as e:
            logger.error(f"保存data.json失败: {e}")
            raise
    
    def _get_directory_mtime(self, dir_path: Path) -> float:
        """
        获取目录的最后修改时间（取目录内所有文件的最新修改时间）
        
        参数:
            dir_path: 目录路径
            
        返回:
            float: 最后修改时间戳
        """
        if not dir_path.exists():
            return 0.0
        
        max_mtime = dir_path.stat().st_mtime
        
        try:
            for item in dir_path.rglob('*'):
                if item.is_file():
                    max_mtime = max(max_mtime, item.stat().st_mtime)
        except Exception as e:
            logger.warning(f"获取目录修改时间失败 {dir_path}: {e}")
        
        return max_mtime
    
    def _get_subfiles_info(self, dir_path: Path) -> List[Dict[str, Any]]:
        """
        获取目录下所有子文件的信息
        
        参数:
            dir_path: 目录路径
            
        返回:
            List[Dict]: 子文件信息列表
        """
        subfiles = []
        if not dir_path.exists():
            return subfiles
        
        try:
            for item in dir_path.iterdir():
                if item.is_file():
                    subfiles.append({
                        "path": str(item),
                        "mtime": item.stat().st_mtime
                    })
                elif item.is_dir():
                    # 递归处理子目录
                    subfiles.append({
                        "path": str(item),
                        "mtime": self._get_directory_mtime(item)
                    })
        except Exception as e:
            logger.warning(f"获取子文件信息失败 {dir_path}: {e}")
        
        return subfiles
    
    def _scan_replace_directories(self) -> List[str]:
        """
        扫描replace目录下的所有MOD目录
        
        新目录结构: workspace/mod_projects/作者名/IDLE或CUTSCENE/MOD名称/
        
        返回:
            List[str]: MOD目录路径列表
        """
        replace_dirs = []
        
        if not self.replace_dir.exists():
            logger.warning(f"replace目录不存在: {self.replace_dir}")
            return replace_dirs
        
        try:
            # 遍历作者目录
            
                
                # 在作者目录下查找IDLE和CUTSCENE目录
            for animation_type_dir in self.replace_dir.iterdir():
                if (animation_type_dir.is_dir() and 
                    animation_type_dir.name in ["IDLE", "CUTSCENE"]):
                    # 遍历MOD目录
                    for mod_dir in animation_type_dir.iterdir():
                        if mod_dir.is_dir():
                            relative_path = mod_dir.relative_to(self.project_root)
                            replace_dirs.append(str(relative_path))
            
            logger.info(f"扫描到 {len(replace_dirs)} 个替换目录")
            return replace_dirs
            
        except Exception as e:
            logger.error(f"扫描replace目录失败: {e}")
            return replace_dirs
    
    def _is_directory_empty(self, dir_path: Path) -> bool:
        """
        检查目录是否为空（没有任何文件，只有空文件夹）
        
        参数:
            dir_path: 目录路径
            
        返回:
            bool: 如果目录为空返回True
        """
        if not dir_path.exists():
            return True
        
        try:
            # 检查是否有任何文件
            for item in dir_path.rglob('*'):
                if item.is_file():
                    # logger.info(f"目录不为空: {dir_path}")
                    return False
            # logger.info(f"目录为空: {dir_path}")
            return True
        except Exception as e:
            logger.warning(f"检查目录是否为空失败 {dir_path}: {e}")
            return True
    
    def check_version_and_updates(self) -> Tuple[bool, UpdateSummary]:
        """
        检测游戏版本和替换文件更新
        
        返回:
            Tuple[bool, UpdateSummary]: (是否需要更新, 更新摘要)
        """
        logger.info("开始检测版本和文件更新...")
        
        # 加载当前配置
        data = self._load_data_json()
        
        # 获取当前作者的数据
        authors_data = data.get("authors", {})
        current_author_data = authors_data.get(self.replace_dir_name, {})
        current_version = current_author_data.get("version", 0)
        current_update_time = current_author_data.get("updateTime", 0)
        
        # 创建更新摘要
        summary = UpdateSummary()
        summary.old_version = current_version
        
        needs_update = False
        
        try:
            # 第一步：检测游戏版本
            logger.info("检测游戏版本...")
            server_info = self.cdn_api.get_version_info()
            server_version = int(server_info.version)  # BD2VersionInfo.version
            server_update_time = int(server_info.version)  # 使用版本号作为更新时间
            
            summary.new_version = server_version
            
            if server_version != current_version or server_update_time != current_update_time:
                logger.info(f"作者'{self.replace_dir_name}'游戏版本有更新: {current_version} -> {server_version}")
                summary.version_changed = True
                needs_update = True
                
                # 更新当前作者的版本信息
                if self.replace_dir_name not in authors_data:
                    authors_data[self.replace_dir_name] = {}
                authors_data[self.replace_dir_name]["version"] = server_version
                authors_data[self.replace_dir_name]["updateTime"] = server_update_time
                
                # 保持现有的dirs数据
                if "dirs" not in authors_data[self.replace_dir_name]:
                    authors_data[self.replace_dir_name]["dirs"] = []
                
                data["authors"] = authors_data
                self._save_data_json(data)
            else:
                logger.info(f"作者'{self.replace_dir_name}'游戏版本无变化")
            
            # 第二步：建立replace_update清单
            logger.info("检测替换文件更新...")
            current_replace_dirs = self._scan_replace_directories()
            summary.total_replace_dirs = len(current_replace_dirs)
            
            # 获取当前作者的目录数据
            current_author_dirs = current_author_data.get("dirs", [])
            
            # 构建现有replaceDir映射
            existing_replace_map = {}
            for entry in current_author_dirs:
                # 将绝对路径转换为相对路径进行比较
                rel_path = Path(entry["path"]).relative_to(self.project_root)
                existing_replace_map[str(rel_path)] = entry
            
            updated_replace_dirs = []
            dirs_to_update = []
            
            # 检查每个替换目录
            for replace_dir_rel in current_replace_dirs:
                replace_dir_path = self.project_root / replace_dir_rel
                current_mtime = self._get_directory_mtime(replace_dir_path)
                current_subfiles = self._get_subfiles_info(replace_dir_path)
                
                # 检查是否已存在
                if replace_dir_rel in existing_replace_map:
                    existing_entry = existing_replace_map[replace_dir_rel]
                    existing_mtime = existing_entry.get("mtime", 0)
                    existing_subfiles = existing_entry.get("subfile", [])
                    
                    # 比较目录修改时间
                    if abs(current_mtime - existing_mtime) > 1:  # 允许1秒误差
                        logger.info(f"目录已更新: {replace_dir_rel}")
                        dirs_to_update.append(replace_dir_rel)
                        needs_update = True
                    else:
                        # 比较子文件
                        subfiles_changed = False
                        existing_subfile_map = {sf["path"]: sf["mtime"] for sf in existing_subfiles}
                        
                        for subfile in current_subfiles:
                            subfile_path = subfile["path"]
                            subfile_mtime = subfile["mtime"]
                            
                            if (subfile_path not in existing_subfile_map or 
                                abs(subfile_mtime - existing_subfile_map[subfile_path]) > 1):
                                subfiles_changed = True
                                break
                        
                        # 检查是否有子文件被删除
                        current_subfile_paths = {sf["path"] for sf in current_subfiles}
                        for existing_subfile_path in existing_subfile_map:
                            if existing_subfile_path not in current_subfile_paths:
                                subfiles_changed = True
                                break
                        
                        if subfiles_changed:
                            logger.info(f"子文件已更新: {replace_dir_rel}")
                            dirs_to_update.append(replace_dir_rel)
                            needs_update = True
                
                else:
                    # 新增的目录
                    logger.info(f"发现新目录: {replace_dir_rel}")
                    dirs_to_update.append(replace_dir_rel)
                    needs_update = True
                
                # 更新条目
                updated_replace_dirs.append({
                    "path": str(replace_dir_path),
                    "mtime": current_mtime,
                    "subfile": current_subfiles
                })
            
            # 检查已删除的目录（只检查当前作者的目录）
            for existing_rel_path in existing_replace_map:
                if existing_rel_path not in current_replace_dirs:
                    logger.info(f"目录已删除: {existing_rel_path}")
                    needs_update = True
            
            # 更新data.json中的当前作者数据
            if needs_update:
                # 确保当前作者的数据结构正确
                if self.replace_dir_name not in authors_data:
                    authors_data[self.replace_dir_name] = {
                        "version": current_version,
                        "updateTime": current_update_time,
                        "dirs": []
                    }
                
                # 更新目录信息，保持版本信息
                authors_data[self.replace_dir_name]["dirs"] = updated_replace_dirs
                data["authors"] = authors_data
                self._save_data_json(data)
            
            summary.replace_dirs_to_update = dirs_to_update
            
            logger.info(f"检测完成: 需要更新={needs_update}, 版本变化={summary.version_changed}, 目录更新数={len(dirs_to_update)}")
            
            return needs_update, summary
            
        except Exception as e:
            logger.error(f"检测版本和更新失败: {e}")
            return True, summary  # 出错时返回需要更新
    
    def _build_replace_mapping(self, specific_dirs: List[str] = None) -> List[ReplaceTask]:
        """
        建立替换映射清单
        
        新目录结构: workspace/mod_projects/作者名/IDLE或CUTSCENE/MOD名称/
        
        参数:
            specific_dirs: 指定要处理的目录列表（增量更新时使用），为None时处理所有目录
            
        返回:
            List[ReplaceTask]: 替换任务列表
        """
        if specific_dirs:
            logger.info(f"开始建立增量替换映射清单，处理 {len(specific_dirs)} 个目录...")
        else:
            logger.info("开始建立完整替换映射清单...")
        
        replace_tasks = []
        
        if not self.replace_dir.exists():
            logger.warning(f"replace目录不存在: {self.replace_dir}")
            return replace_tasks
        
        try:
            # 转换specific_dirs为相对路径的集合以便快速查找
            specific_dirs_set = set()
            if specific_dirs:
                for dir_path in specific_dirs:
                    specific_dirs_set.add(dir_path.replace("\\", "/"))
            
            # 新目录结构：遍历 作者目录 -> IDLE/CUTSCENE目录 -> MOD目录
            
                
            logger.info(f"处理作者目录: {self.replace_dir.name}")
            
            # 在作者目录下查找IDLE和CUTSCENE目录
            for animation_type_dir in self.replace_dir.iterdir():
                if not animation_type_dir.is_dir():
                    continue
                
                # 只处理IDLE和CUTSCENE目录
                if animation_type_dir.name not in ["IDLE", "CUTSCENE"]:
                    continue
                
                type_name = animation_type_dir.name
                logger.info(f"  处理动画类型: {type_name}")
                
                # 遍历MOD目录
                for mod_dir in animation_type_dir.iterdir():
                    if not mod_dir.is_dir():
                        continue
                    
                    mod_name = mod_dir.name
                    logger.info(f"    处理MOD: {mod_name}")
                    
                    # 检查目录是否为空
                    if self._is_directory_empty(mod_dir):
                        logger.info(f"    跳过空目录: {type_name}/{mod_name}")
                        continue
                    # logger.info(f"    开始创建替换任务======================================")
                    # 确定任务是否应该执行
                    should_execute = True
                    if specific_dirs:
                        # 构建当前目录的相对路径
                        current_dir_rel = mod_dir.relative_to(self.project_root)
                        current_dir_rel_str = str(current_dir_rel).replace("\\", "/")
                        should_execute = current_dir_rel_str in specific_dirs_set
                        if should_execute:
                            logger.info(f"    ✓ 目录在更新列表中: {type_name}/{mod_name}")
                        else:
                            logger.info(f"    - 目录不在更新列表中: {type_name}/{mod_name}")
                    
                    task = self._create_replace_task(type_name, mod_dir, should_execute)
                    # logger.info(f"    创建替换任务: {task}")
                    if task:
                        replace_tasks.append(task)
            
            # 如果是增量更新，需要额外处理相同目标路径的任务
            if specific_dirs:
                # 收集所有可执行任务的目标路径
                executable_target_dirs = set()
                for task in replace_tasks:
                    if task.should_execute:
                        executable_target_dirs.add(task.target_dir)
                
                # 标记具有相同目标路径的其他任务为可执行
                additional_count = 0
                for task in replace_tasks:
                    if not task.should_execute and task.target_dir in executable_target_dirs:
                        task.should_execute = True
                        additional_count += 1
                        logger.info(f"    ✓ 相同目标路径，标记为可执行: {task.type}/{task.mod_name}")
                
                if additional_count > 0:
                    logger.info(f"因相同目标路径额外标记 {additional_count} 个任务为可执行")
            
            # 统计任务数量
            execute_count = sum(1 for task in replace_tasks if task.should_execute)
            total_count = len(replace_tasks)
            logger.info(f"替换映射清单建立完成，共 {total_count} 个任务，其中 {execute_count} 个需要执行")

            return replace_tasks
            
        except Exception as e:
            logger.error(f"建立替换映射清单失败: {e}")
            return replace_tasks
    
    def _create_replace_task(self, type_name: str, mod_dir: Path, should_execute: bool = True) -> Optional[ReplaceTask]:
        # logger.info(f"    创建替换任务: {type_name}/{mod_dir.name}/ {should_execute}")
        """
        为单个MOD目录创建替换任务
        
        新逻辑:
        1. 从MOD目录路径判断IDLE/CUTSCENE类型
        2. 从mod文件名提取角色ID
        3. 使用ID查找方法获取idle/cutscene值
        
        参数:
            type_name: 类型名(IDLE/CUTSCENE)，从目录路径获取
            mod_dir: MOD目录路径
            should_execute: 是否需要执行该任务
            
        返回:
            Optional[ReplaceTask]: 创建的任务，失败时返回None
        """
        try:
            mod_name = mod_dir.name
            
            # 步骤1：从mod文件中获取角色ID
            char_id = self._extract_char_id_from_mod_files(mod_dir)
            if not char_id:
                logger.warning(f"    无法从MOD文件中提取角色ID，跳过: {type_name}/{mod_name}")
                return None
            
            logger.info(f"    提取到角色ID: {char_id}")
            
            # 步骤2：使用ID查找方法获取idle或cutscene值
            try:
                if type_name.upper() == "IDLE":
                    idle_or_cutscene_value = self.character_scraper.get_idle_by_id(char_id)
                elif type_name.upper() == "CUTSCENE":
                    idle_or_cutscene_value = self.character_scraper.get_cutscene_by_id(char_id)
                else:
                    logger.warning(f"    未知类型: {type_name}，跳过")
                    return None
            except Exception as e:
                logger.warning(f"    无法获取 {char_id} 的{type_name}值: {e}")
                return None
            
            if not idle_or_cutscene_value:
                logger.warning(f"    角色ID {char_id} 的{type_name}值为空，跳过")
                return None
            
            logger.info(f"    获取到{type_name}值: {idle_or_cutscene_value}")
            
            # 步骤3：通过BD2CDNAPI获取资源名称和hash
            result = self.cdn_api.get_resource_bundle_name_and_hash(idle_or_cutscene_value)
            if not result:
                logger.warning(f"    无法获取 {idle_or_cutscene_value} 的资源信息，跳过")
                return None
            
            resource_name, hash_id = result
            logger.info(f"    资源名称: {resource_name}, Hash: {hash_id}")
            
            # 步骤4：构建路径
            replace_dir_path = str(mod_dir)
            downloaded_dir = f"{self.downloaded_dir}{os.sep}{resource_name}"
            target_dir = f"{self.target_dir}/{idle_or_cutscene_value}/{hash_id}/__data"
            
            # 步骤5：创建替换任务
            task = ReplaceTask(
                type=type_name,
                replace_dir=replace_dir_path,
                data_name=resource_name,
                downloaded_dir=downloaded_dir,
                target_dir=target_dir,
                mod_name=mod_name,
                idle_or_cutscene_value=idle_or_cutscene_value,
                hash_id=hash_id,
                char_id=char_id,
                should_execute=should_execute
            )
            
            status_text = "✅ 添加替换任务" if should_execute else "📋 添加任务(不执行)"
            logger.info(f"    {status_text}: {type_name}/{mod_name} (ID: {char_id})")
            return task
            
        except Exception as e:
            logger.error(f"创建替换任务失败 {type_name}/{mod_dir.name}: {e}")
            return None
    
    def _extract_char_id_from_mod_files(self, mod_dir: Path) -> Optional[str]:
        """
        从MOD目录中的文件名提取角色ID
        
        查找规则：
        1. 查找后缀为 .atlas, .modfile, .skel, .json 的文件
        2. 提取文件名（不含后缀）作为角色ID
        3. 移除可能存在的 cutscene_ 或 idle_ 前缀
        4. 如果找到多个文件，使用第一个匹配的ID
        
        参数:
            mod_dir: MOD目录路径
            
        返回:
            Optional[str]: 提取到的角色ID（已移除前缀），失败时返回None
        """
        try:
            # 支持的文件后缀
            supported_extensions = ['.atlas', '.modfile', '.skel', '.json']
            
            # 查找匹配的文件
            found_files = []
            for file_path in mod_dir.iterdir():
                if file_path.is_file():
                    file_ext = file_path.suffix.lower()
                    if file_ext in supported_extensions:
                        found_files.append(file_path)
            
            if not found_files:
                logger.warning(f"    目录中未找到有效的mod文件 (.atlas, .modfile, .skel, .json): {mod_dir}")
                return None
            
            # 提取所有文件的ID（不含后缀的文件名）
            char_ids = []
            for file_path in found_files:
                char_id = file_path.stem  # 获取不含后缀的文件名
                
                # 移除可能的前缀
                if char_id:
                    original_id = char_id
                    # 移除常见的文件前缀
                    if char_id.startswith('cutscene_'):
                        char_id = char_id[9:]  # 移除 'cutscene_' 前缀（9个字符）
                        logger.info(f"    移除cutscene_前缀，角色ID: {char_id}")
                    elif char_id.startswith('idle_'):
                        char_id = char_id[5:]  # 移除 'idle_' 前缀（5个字符）
                        logger.info(f"    移除idle_前缀，角色ID: {char_id}")
                    
                    # 检查是否为有效的角色ID（使用配置的前缀）
                    if not self.config.is_valid_character_id_prefix(char_id):
                        logger.warning(f"    提取的ID '{char_id}' 不匹配任何已知前缀，原始文件名: {original_id}")
                
                if char_id and char_id not in char_ids:
                    char_ids.append(char_id)
            
            if not char_ids:
                logger.warning(f"    无法从文件名提取角色ID: {mod_dir}")
                return None
            
            # 如果有多个ID，输出警告并使用第一个
            if len(char_ids) > 1:
                logger.warning(f"    发现多个角色ID: {char_ids}，使用第一个: {char_ids[0]}")
            
            return char_ids[0]
            
        except Exception as e:
            logger.error(f"提取角色ID失败 {mod_dir}: {e}")
            return None
    
    def _save_replace_mapping(self, tasks: List[ReplaceTask], filename: str = "清单.json") -> None:
        """
        保存替换映射清单到JSON文件
        
        参数:
            tasks: 替换任务列表
            filename: 保存的文件名
        """
        try:
            # 转换为JSON格式
            json_data = []
            for task in tasks:
                # 通过角色ID获取角色和服装信息
                char_data = self.character_scraper.get_character_by_id(task.char_id)
                char_name = char_data.character if char_data else task.char_id
                costume_name = char_data.costume if char_data else "未知"
                
                json_data.append({
                    "char": char_name,
                    "costume": costume_name,
                    "char_id": task.char_id,
                    "type": task.type,
                    "replaceDir": task.replace_dir,
                    "dataName": task.data_name,
                    "downloadedDir": task.downloaded_dir,
                    "targetDir": task.target_dir,
                    "modName": task.mod_name,
                    "shouldExecute": task.should_execute
                })
            
            # 保存到文件
            mapping_file = self.project_root / filename
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"替换映射清单已保存到: {mapping_file}")
            
        except Exception as e:
            logger.error(f"保存替换映射清单失败: {e}")
    
    def process_updates(self, summary: UpdateSummary) -> Tuple[bool, list[ReplaceTask]]:
        """
        处理更新（下载资源和替换）
        
        参数:
            summary: 更新摘要
            
        返回:
            Tuple[bool, List[ReplaceTask]]: (是否成功处理, 替换任务列表)
        """
        logger.info("开始处理更新...")
        
        try:
            # 如果版本有变化，执行完整替换流程
            is_update_dir = False
            if summary.version_changed:
                logger.info("检测到版本更新，执行完整替换流程...")
                
                # 第一步：建立替换映射清单
                logger.info("🔍 第一步：建立替换映射清单")
                replace_tasks = self._build_replace_mapping()
                
                if not replace_tasks:
                    logger.warning("没有找到需要替换的任务")
                    return True,replace_tasks
                
                # 保存清单到文件
                # self._save_replace_mapping(replace_tasks, "完整替换清单.json")
                
                # 输出清单摘要
                logger.info("📋 替换任务摘要:")
                executed_count = 0
                for i, task in enumerate(replace_tasks, 1):
                    status = "✅ 执行" if task.should_execute else "⏭️ 跳过"
                    if task.should_execute:
                        executed_count += 1
                    
                    # 通过角色ID获取角色和服装信息用于显示
                    char_data = self.character_scraper.get_character_by_id(task.char_id)
                    char_name = char_data.character if char_data else task.char_id
                    costume_name = char_data.costume if char_data else "未知"
                    
                    logger.info(f"  {i}. {status} - {char_name}/{costume_name}/{task.type} (ID: {task.char_id})")
                    logger.info(f"     值: {task.idle_or_cutscene_value}")
                    logger.info(f"     资源: {task.data_name}")
                    logger.info(f"     Hash: {task.hash_id}")
                    logger.info(f"     MOD名称: {task.mod_name}")
                    if executed_count == 0:
                        logger.info("✅ 没有需要执行的替换任务")
                        return True,replace_tasks
                
                logger.info(f"✅ 完整替换映射清单建立完成 (执行: {executed_count}/{len(replace_tasks)})")
                
            elif summary.replace_dirs_to_update:
                is_update_dir = True
                logger.info("检测到文件更新，处理增量替换...")
                
                # 建立增量替换映射清单
                logger.info("🔍 建立增量替换映射清单")
                replace_tasks = self._build_replace_mapping(summary.replace_dirs_to_update)
                
                if not replace_tasks:
                    logger.warning("没有找到需要增量替换的任务")
                    return True,replace_tasks
                
                # 保存增量清单到文件
                # self._save_replace_mapping(replace_tasks, "增量替换清单.json")
                
                # 输出增量清单摘要
                logger.info("📋 增量替换任务摘要:")
                executed_count = 0
                for i, task in enumerate(replace_tasks, 1):
                    status = "✅ 执行" if task.should_execute else "⏭️ 跳过"
                    if task.should_execute:
                        executed_count += 1
                    
                    # 通过角色ID获取角色和服装信息用于显示
                    char_data = self.character_scraper.get_character_by_id(task.char_id)
                    char_name = char_data.character if char_data else task.char_id
                    costume_name = char_data.costume if char_data else "未知"
                    
                    logger.info(f"  {i}. {status} - {char_name}/{costume_name}/{task.type} (ID: {task.char_id})")
                    logger.info(f"     值: {task.idle_or_cutscene_value}")
                    logger.info(f"     资源: {task.data_name}")
                    logger.info(f"     Hash: {task.hash_id}")
                    logger.info(f"     MOD名称: {task.mod_name}")
                if executed_count == 0:
                    logger.info("✅ 没有需要执行的替换任务")
                    return True,replace_tasks
                
                logger.info(f"✅ 增量替换映射清单建立完成 (执行: {executed_count}/{len(replace_tasks)})")
                # if executed_count == 0:
                #     logger.info("✅ 没有需要执行的增量替换任务")
                #     return True,replace_tasks

            
            # 第二步：下载资源文件
            logger.info("📥 第二步：下载资源文件")
            success = self._download_resources(replace_tasks)
            if not success:
                logger.error("资源下载失败")
                return False,replace_tasks
            
            # 第三步：执行Unity资源替换
            logger.info("🔄 第三步：执行Unity资源替换")
            success = self._process_unity_resources(replace_tasks, is_update_dir)
            if not success:
                logger.error("Unity资源替换失败")
                return False,replace_tasks
            
            # 第四步：生成README文件（包含所有任务信息）
            logger.info("📝 第四步：生成README文件")
            self._generate_all_readme_files(replace_tasks)
            
            logger.info("✅ 更新处理完成")
            return True,replace_tasks
            
        except Exception as e:
            logger.error(f"处理更新失败: {e}")
            return False,replace_tasks
    
    def _download_resources(self, replace_tasks: List[ReplaceTask]) -> bool:
        """
        下载资源文件
        
        参数:
            replace_tasks: 替换任务列表
            
        返回:
            bool: 是否成功下载
        """
        try:
            # 获取所有需要下载的资源（去重），只处理需要执行的任务
            unique_resources = {}
            executable_tasks = [task for task in replace_tasks if task.should_execute]
            
            for task in executable_tasks:
                if task.data_name not in unique_resources:
                    unique_resources[task.data_name] = task
            
            total_tasks = len(replace_tasks)
            executable_count = len(executable_tasks)
            logger.info(f"总任务数: {total_tasks}, 需要执行: {executable_count}, 需要下载 {len(unique_resources)} 个唯一资源文件")
            
            if not unique_resources:
                logger.info("无需下载任何资源文件")
                return True
            
            # 逐个下载
            for i, (data_name, task) in enumerate(unique_resources.items(), 1):
                logger.info(f"[{i}/{len(unique_resources)}] 下载: {data_name}")
                
                try:
                    downloaded_path = self.data_downloader.download_data(data_name)
                    logger.info(f"✅ 下载完成: {downloaded_path}")
                except Exception as e:
                    logger.error(f"❌ 下载失败 {data_name}: {e}")
                    return False
            
            logger.info("🎉 所有资源下载完成")
            return True
            
        except Exception as e:
            logger.error(f"下载资源失败: {e}")
            return False

    def _process_unity_resources(self, replace_tasks: List[ReplaceTask], is_update_dir: bool) -> bool:
        """
        处理Unity资源替换
        
        参数:
            replace_tasks: 替换任务列表
            
        返回:
            bool: 是否成功处理
        """
        try:
            # 按目标目录分组任务，只处理需要执行的任务
            tasks_by_target = {}
            executable_tasks = [task for task in replace_tasks if task.should_execute]
            
            for task in executable_tasks:
                target_dir = task.target_dir
                if target_dir not in tasks_by_target:
                    tasks_by_target[target_dir] = []
                tasks_by_target[target_dir].append(task)
            
            total_tasks = len(replace_tasks)
            executable_count = len(executable_tasks)
            logger.info(f"总任务数: {total_tasks}, 需要执行: {executable_count}, 需要处理 {len(tasks_by_target)} 个目标文件")
            
            if not tasks_by_target:
                logger.info("无需处理任何Unity资源")
                return True
            
            # 逐个处理目标文件
            for i, (target_dir, group_tasks) in enumerate(tasks_by_target.items(), 1):
                logger.info(f"[{i}/{len(tasks_by_target)}] 处理目标: {target_dir}")
                
                # 获取源bundle文件路径（使用第一个任务的信息）
                first_task = group_tasks[0]
                source_bundle_path = str(self.downloaded_dir / first_task.data_name / "__data")
                # 收集所有替换目录
                replace_dirs = [task.replace_dir for task in group_tasks]
                
                # 生成目标路径
                target_path = str(self.project_root / target_dir)
                
                try:
                    # 使用Unity处理器的多目录替换功能
                    success = self.unity_processor.process_multiple_replace_dirs(
                        bundle_path=source_bundle_path,
                        replace_dirs=replace_dirs,
                        target_path=target_path
                    )
                    
                    if success:
                        logger.info(f"✅ 处理完成: {target_dir}")
                    else:
                        logger.error(f"❌ 处理失败: {target_dir}")
                        return False
                        
                except Exception as e:
                    logger.error(f"❌ 处理失败 {target_dir}: {e}")
                    return False
            
            logger.info("🎉 所有Unity资源处理完成")
            return True
            
        except Exception as e:
            logger.error(f"处理Unity资源失败: {e}")
            return False
    
    def _generate_all_readme_files(self, replace_tasks: List[ReplaceTask]) -> None:
        """
        为所有目标目录生成README文件（包含所有任务信息，无论是否执行）
        
        参数:
            replace_tasks: 所有替换任务列表
        """
        try:
            # 按目标目录分组所有任务（包括不执行的）
            tasks_by_target = {}
            for task in replace_tasks:
                target_dir = task.target_dir
                if target_dir not in tasks_by_target:
                    tasks_by_target[target_dir] = []
                tasks_by_target[target_dir].append(task)
            
            logger.info(f"生成 {len(tasks_by_target)} 个README文件")
            
            # 为每个目标目录生成README
            for target_dir, group_tasks in tasks_by_target.items():
                target_path = str(self.project_root / target_dir)
                self._create_mod_readme(target_path, group_tasks)
            
            logger.info("📝 所有README文件生成完成")
            
        except Exception as e:
            logger.error(f"生成README文件失败: {e}")
    
    def _create_mod_readme(self, target_path: str, tasks: List[ReplaceTask]) -> None:
        """
        在目标目录创建README文件
        
        参数:
            target_path: 目标路径
            tasks: 相关的替换任务列表
        """
        try:
            # 确保目标目录存在
            Path(target_path).parent.mkdir(parents=True, exist_ok=True)
            
            readme_path = Path(target_path).parent / "README.txt"
            
            # 统计执行状态
            executed_tasks = [task for task in tasks if task.should_execute]
            skipped_tasks = [task for task in tasks if not task.should_execute]
            
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("BD2 MOD资源包\n")
                f.write("=" * 30 + "\n\n")
                f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"总MOD数量: {len(tasks)}\n")
                f.write(f"已更新MOD: {len(executed_tasks)}\n")
                f.write(f"未更改MOD: {len(skipped_tasks)}\n\n")

                # 已更新的MOD
                if executed_tasks:
                    f.write("已更新的MOD:\n")
                    f.write("-" * 20 + "\n")
                    for i, task in enumerate(executed_tasks, 1):
                        # 通过角色ID获取角色和服装信息用于显示
                        char_data = self.character_scraper.get_character_by_id(task.char_id)
                        char_name = char_data.character if char_data else task.char_id
                        costume_name = char_data.costume if char_data else "未知"
                        
                        f.write(f"{i}. ✅ {task.mod_name}\n")
                        f.write(f"   角色ID: {task.char_id}\n")
                        f.write(f"   角色: {char_name}\n")
                        f.write(f"   服装: {costume_name}\n")
                        f.write(f"   类型: {task.type}\n")
                        f.write(f"   替换目录: {task.replace_dir}\n\n")
                
                # 跳过的MOD
                if skipped_tasks:
                    f.write("未更改的MOD:\n")
                    f.write("-" * 20 + "\n")
                    for i, task in enumerate(skipped_tasks, 1):
                        # 通过角色ID获取角色和服装信息用于显示
                        char_data = self.character_scraper.get_character_by_id(task.char_id)
                        char_name = char_data.character if char_data else task.char_id
                        costume_name = char_data.costume if char_data else "未知"
                        
                        f.write(f"{i}. ⏭️ {task.mod_name}\n")
                        f.write(f"   角色ID: {task.char_id}\n")
                        f.write(f"   角色: {char_name}\n")
                        f.write(f"   服装: {costume_name}\n")
                        f.write(f"   类型: {task.type}\n")
                        f.write(f"   替换目录: {task.replace_dir}\n")
                        f.write(f"   原因: 目录未在更新列表中\n\n")
                
                f.write("使用说明:\n")
                f.write("1. 将__data文件复制到游戏对应位置\n")
                f.write("2. 确保文件路径结构正确\n")
                f.write("3. 重新启动游戏以应用修改\n")
                f.write("4. 跳过的MOD需要手动触发更新才会应用\n\n")
                
                f.write("目录结构说明:\n")
                f.write("新的简化目录结构: 作者名/IDLE或CUTSCENE/MOD名称/\n")
                f.write("• MOD文件命名必须包含角色ID (如: char000101.atlas)\n")
                f.write("• 系统会从文件名自动识别角色和服装信息\n")
                f.write("• 支持的文件格式: .atlas, .modfile, .skel, .json\n")
                f.write("• 支持的角色ID格式: char*, illust_*, specialIllust*等\n")
            
            logger.info(f"📝 已生成README文件: {readme_path}")
            
        except Exception as e:
            logger.warning(f"创建README文件失败: {e}")
    
    def run(self) -> bool:
        """
        运行主流程
        
        返回:
            bool: 是否成功执行
        """
        try:
            logger.info("🎮 BD2资源替换工具启动")
            logger.info("=" * 50)
            
            # 检测版本和更新
            needs_update, summary = self.check_version_and_updates()
            
            # 输出检测结果
            logger.info("📊 检测结果摘要:")
            logger.info(f"  版本变化: {summary.version_changed}")
            if summary.old_version is not None and summary.new_version is not None:
                logger.info(f"  版本: {summary.old_version} -> {summary.new_version}")
            logger.info(f"  总替换目录数: {summary.total_replace_dirs}")
            logger.info(f"  需要更新的目录数: {len(summary.replace_dirs_to_update)}")
            
            if not needs_update:
                logger.info("✅ 无需更新，程序退出")
                return True
            
            logger.info("🔄 检测到更新，开始处理...")
            
            # 处理更新
            success = self.process_updates(summary)
            
            if success:
                logger.info("✅ 更新处理完成")
            else:
                logger.error("❌ 更新处理失败")
            
            return success
            
        except Exception as e:
            logger.error(f"主流程执行失败: {e}")
            return False


def main():
    """主函数"""
    try:
        manager = BD2ResourceManager()
        success = manager.run()
        return 0 if success else 1
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        return 1
    except Exception as e:
        logger.error(f"程序异常退出: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
