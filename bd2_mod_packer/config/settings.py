#!/usr/bin/env python3
"""
BD2项目统一配置文件

包含所有项目配置，包括：
- 网络代理设置
- API超时配置
- 日志配置
- 其他通用设置

使用方法:
    from config import get_config
    config = get_config()
    proxies = config.get_proxies()

作者: oldnew
日期: 2025-08-15
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class NetworkConfig:
    """网络配置"""
    # 代理设置
    proxy_enabled: bool = True
    proxy_http: str = ""
    proxy_https: str = ""
    
    # 超时设置
    request_timeout: float = 15.0
    download_timeout: float = 300.0
    
    # 重试设置
    max_retries: int = 3
    retry_delay: float = 1.0


@dataclass
class LogConfig:
    """日志配置"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    file_enabled: bool = False
    file_path: str = "logs/bd2_auto_ab.log"


@dataclass
class APIConfig:
    """API配置"""
    # 谷歌表格URL
    google_sheets_url: str = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQLmR_jafTkS65IOwboDbdCaUa9n2OUIT4_VLq2EU-9_alX5BBXmgj4T4IBJx-eWhBRkLnN9-pqM65R/pubhtml/sheet?headers=false&gid=269089981"
    
    # BD2 CDN设置
    bd2_base_url: str = "https://bd2-cdn.akamaized.net"
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


@dataclass
class ProjectConfig:
    """项目配置"""
    # 目录设置
    project_name: str = "BD2 Auto AB"
    version: str = "2.0.0"
    
    # Unity设置
    unity_version: str = "2022.3.22f1"
    
    # 并发设置
    max_workers: int = 4
    
    # MOD工作目录设置
    mod_workspaces: list = None  # MOD工作目录列表
    
    def __post_init__(self):
        """初始化后处理"""
        if self.mod_workspaces is None:
            self.mod_workspaces = ["replace"]  # 默认工作目录


class BD2Config:
    """BD2项目配置管理器"""
    
    def __init__(self, config_file: str = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，如果不提供则使用默认路径
        """
        self.project_root = Path(__file__).parent.parent.parent
        self.config_file = Path(config_file) if config_file else self.project_root / "config.json"
        
        # 默认配置
        self.network = NetworkConfig()
        self.log = LogConfig()
        self.api = APIConfig()
        self.project = ProjectConfig()
        
        # 加载配置文件
        self.load_config()
        
        # 设置日志
        self._setup_logging()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"配置加载完成: {self.config_file}")
    
    def load_config(self) -> None:
        """从配置文件加载配置"""
        if not self.config_file.exists():
            print(f"配置文件不存在，创建默认配置: {self.config_file}")
            self.save_config()
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # 更新配置
            if 'network' in config_data:
                for key, value in config_data['network'].items():
                    if hasattr(self.network, key):
                        setattr(self.network, key, value)
            
            if 'log' in config_data:
                for key, value in config_data['log'].items():
                    if hasattr(self.log, key):
                        setattr(self.log, key, value)
            
            if 'api' in config_data:
                for key, value in config_data['api'].items():
                    if hasattr(self.api, key):
                        setattr(self.api, key, value)
            
            if 'project' in config_data:
                for key, value in config_data['project'].items():
                    if hasattr(self.project, key):
                        setattr(self.project, key, value)
                        
        except Exception as e:
            print(f"加载配置文件失败: {e}，使用默认配置")
    
    def save_config(self) -> None:
        """保存配置到文件"""
        try:
            # 确保配置目录存在
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            config_data = {
                "network": asdict(self.network),
                "log": asdict(self.log),
                "api": asdict(self.api),
                "project": asdict(self.project)
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def _setup_logging(self) -> None:
        """设置日志配置"""
        # 转换日志级别
        level = getattr(logging, self.log.level.upper(), logging.INFO)
        
        handlers = [logging.StreamHandler()]
        
        # 如果启用文件日志
        if self.log.file_enabled:
            log_file = Path(self.log.file_path)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
        
        logging.basicConfig(
            level=level,
            format=self.log.format,
            datefmt=self.log.date_format,
            handlers=handlers,
            force=True  # 强制重新配置
        )
    
    def get_proxies(self) -> Optional[Dict[str, str]]:
        """
        获取代理配置
        
        Returns:
            代理配置字典，如果未启用代理则返回None
        """
        if not self.network.proxy_enabled:
            return None

        if self.network.proxy_http == "" and self.network.proxy_https == "":
            return None

        return {
            'http': self.network.proxy_http,
            'https': self.network.proxy_https
        }
    
    def get_requests_config(self) -> Dict[str, Any]:
        """
        获取requests请求配置
        
        Returns:
            requests配置字典
        """
        config = {
            'timeout': self.network.request_timeout,
            'headers': {
                'User-Agent': self.api.user_agent
            }
        }
        
        proxies = self.get_proxies()
        if proxies:
            config['proxies'] = proxies
        
        return config
    
    def update_proxy(self, enabled: bool, http_proxy: str = None, https_proxy: str = None) -> None:
        """
        更新代理设置
        
        Args:
            enabled: 是否启用代理
            http_proxy: HTTP代理地址
            https_proxy: HTTPS代理地址
        """
        self.network.proxy_enabled = enabled
        
        if http_proxy:
            self.network.proxy_http = http_proxy
        
        if https_proxy:
            self.network.proxy_https = https_proxy
        
        # 保存配置
        self.save_config()
        
        # 重新设置日志（如果日志配置也有变化）
        self._setup_logging()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"代理设置已更新: enabled={enabled}")
    
    def get_all_config(self) -> Dict[str, Any]:
        """获取所有配置"""
        return {
            "network": asdict(self.network),
            "log": asdict(self.log),
            "api": asdict(self.api),
            "project": asdict(self.project)
        }
    
    def add_mod_workspace(self, workspace_name: str) -> bool:
        """
        添加MOD工作目录
        
        Args:
            workspace_name: 工作目录名称
            
        Returns:
            是否添加成功
        """
        if workspace_name in self.project.mod_workspaces:
            return False
        
        self.project.mod_workspaces.append(workspace_name)
        self.save_config()
        
        if hasattr(self, 'logger'):
            self.logger.info(f"已添加MOD工作目录: {workspace_name}")
        
        return True
    
    def remove_mod_workspace(self, workspace_name: str) -> bool:
        """
        移除MOD工作目录
        
        Args:
            workspace_name: 工作目录名称
            
        Returns:
            是否移除成功
        """
        if workspace_name not in self.project.mod_workspaces:
            return False
        
        # 保留至少一个工作目录
        if len(self.project.mod_workspaces) <= 1:
            return False
        
        self.project.mod_workspaces.remove(workspace_name)
        self.save_config()
        
        if hasattr(self, 'logger'):
            self.logger.info(f"已移除MOD工作目录: {workspace_name}")
        
        return True
    
    def get_mod_workspaces(self) -> list:
        """
        获取所有MOD工作目录
        
        Returns:
            工作目录列表
        """
        return self.project.mod_workspaces.copy()
    
    def workspace_exists(self, workspace_name: str) -> bool:
        """
        检查工作目录是否存在于配置中
        
        Args:
            workspace_name: 工作目录名称
            
        Returns:
            是否存在
        """
        return workspace_name in self.project.mod_workspaces
    
    def get_workspace_root(self) -> Path:
        """
        获取工作区根目录
        
        Returns:
            工作区根目录路径
        """
        return self.project_root / "workspace"
    
    def get_mod_projects_dir(self) -> Path:
        """
        获取MOD项目目录
        
        Returns:
            MOD项目目录路径
        """
        return self.get_workspace_root() / "mod_projects"
    
    def get_sourcedata_dir(self) -> Path:
        """
        获取源数据目录
        
        Returns:
            源数据目录路径
        """
        return self.get_workspace_root() / "sourcedata"
    
    def get_targetdata_dir(self) -> Path:
        """
        获取目标数据目录
        
        Returns:
            目标数据目录路径
        """
        return self.get_workspace_root() / "targetdata"
    
    def get_mod_workspace_path(self, workspace_name: str) -> Path:
        """
        获取指定MOD工作区的完整路径
        
        Args:
            workspace_name: 工作区名称
            
        Returns:
            工作区完整路径
        """
        return self.get_mod_projects_dir() / workspace_name


# 全局配置实例
_config_instance: Optional[BD2Config] = None


def get_config(config_file: str = None) -> BD2Config:
    """
    获取配置实例（单例模式）
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        配置实例
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = BD2Config(config_file)
    
    return _config_instance


def reload_config(config_file: str = None) -> BD2Config:
    """
    重新加载配置
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        新的配置实例
    """
    global _config_instance
    _config_instance = BD2Config(config_file)
    return _config_instance


# 便捷函数
def get_proxies() -> Optional[Dict[str, str]]:
    """获取代理配置"""
    return get_config().get_proxies()


def get_requests_config() -> Dict[str, Any]:
    """获取requests配置"""
    return get_config().get_requests_config()


if __name__ == "__main__":
    # 测试配置
    config = get_config()
    
    print("=== BD2项目配置 ===")
    print(f"代理设置: {config.get_proxies()}")
    print(f"请求配置: {config.get_requests_config()}")
    print(f"项目信息: {config.project.project_name} v{config.project.version}")
    
    # 显示所有配置
    import json
    print("\n=== 完整配置 ===")
    print(json.dumps(config.get_all_config(), indent=2, ensure_ascii=False))
