#!/usr/bin/env python3
"""
BD2 CDN API

BD2 CDN基础设施交互API类。
此类处理版本检测、资源URL生成以及从游戏内容分发网络检索数据。

作者: OLDNEW
日期: 2025-08-14
"""

import base64
import logging
import time
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
from functools import lru_cache

import blackboxprotobuf as bbpb
import requests


@dataclass
class BD2VersionInfo:
    """BD2版本信息数据类。"""
    version: str
    raw_data: Dict[str, Any]
    timestamp: float
    update_time: str

    def __str__(self) -> str:
        return f"BD2版本 {self.version}  更新时间 {self.update_time} (获取时间: {time.ctime(self.timestamp)} )"


@dataclass
class BD2ResourceInfo:
    """BD2资源信息数据类。"""
    data_name: str
    download_url: str
    version: str
    size: Optional[int] = None
    
    def __str__(self) -> str:
        size_str = f" ({self.size} 字节)" if self.size else ""
        return f"{self.data_name} v{self.version}{size_str}"


class BD2CDNAPIError(Exception):
    """BD2 CDN API自定义异常类。"""
    pass


class BD2CDNAPI:
    """
    BD2 CDN操作API类。
    
    此类提供了干净的接口用于:
    - 获取当前游戏版本
    - 生成资源下载URL
    - 检查资源大小
    - 缓存API响应以提升性能
    
    示例:
        api = BD2CDNAPI()
        version_info = api.get_version_info()
        resource_url = api.get_resource_url("catalog_alpha.json")
        size = api.get_resource_size("catalog_alpha.json")
    """
    
    # BD2 API 常量
    MAINTENANCE_URL = "https://mt.bd2.pmang.cloud/MaintenanceInfo"
    CDN_BASE_URL = "https://cdn.bd2.pmang.cloud/ServerData/Android/HD"
    
    # 默认API请求载荷
    DEFAULT_PAYLOAD = {
        "1": 2,
        "2": 4,
        "3": "1.78.18",  # 客户端版本
        "5": "10004|5063|WEB|KR|5321e432f133f7fbbd6d200a000c3aaddbbe62e3|1733413309371",
        "6": 5,
    }
    
    # protobuf编码的载荷模式
    PAYLOAD_SCHEMA = {
        "1": {"type": "int", "name": ""},
        "2": {"type": "int", "name": ""},
        "3": {"type": "bytes", "name": ""},
        "5": {"type": "bytes", "name": ""},
        "6": {"type": "int", "name": ""},
    }
    
    def __init__(self, 
                 proxies: Optional[Dict[str, str]] = None,
                 timeout: float = 30.0,
                 enable_logging: bool = True):
        """
        初始化BD2 CDN API客户端。
        
        参数:
            proxies: 可选的请求代理配置
            timeout: 请求超时时间（秒）
            enable_logging: 是否启用调试日志
        """
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        
        if enable_logging:
            logging.basicConfig(
                level=logging.INFO, 
                format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
            )
        
        # 配置会话
        self.session = requests.Session()
        if proxies:
            self.session.proxies.update(proxies)
            self.logger.info(f"BD2API代理: {proxies}")
        
        # 版本信息缓存以避免重复API调用
        self._version_cache: Optional[BD2VersionInfo] = None
        self._cache_ttl = 300  # 5分钟缓存
    
    @lru_cache(maxsize=32)
    def get_version_info(self, force_refresh: bool = False) -> BD2VersionInfo:
        """
        获取当前BD2游戏版本信息。
        
        参数:
            force_refresh: 强制刷新缓存的版本数据
            
        返回:
            BD2VersionInfo: 版本信息对象
            
        异常:
            BD2CDNAPIError: 如果API请求失败
        """
        current_time = time.time()
        
        # 检查缓存有效性
        if (not force_refresh and 
            self._version_cache and 
            (current_time - self._version_cache.timestamp) < self._cache_ttl):
            self.logger.debug("使用缓存的版本信息")
            return self._version_cache
        
        try:
            self.logger.info("从BD2 API获取版本信息...")
            
            # 编码请求载荷
            encoded_payload = base64.b64encode(
                bbpb.encode_message(self.DEFAULT_PAYLOAD, self.PAYLOAD_SCHEMA)
            )
            
            # 发送API请求
            response = self.session.post(
                self.MAINTENANCE_URL,
                data=encoded_payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # 解码响应
            response_data = response.json()
            if "data" not in response_data:
                raise BD2CDNAPIError("无效的API响应: 缺少'data'字段")
            
            decoded_data = bbpb.decode_message(base64.b64decode(response_data["data"]))
            raw_version_data = decoded_data[0]["1"]
            
            # 提取版本字符串
            version = str(raw_version_data["3"])[2:-1]
            update_time = str(raw_version_data["13"])[2:-1]
            # 创建版本信息对象
            version_info = BD2VersionInfo(
                version=version,
                raw_data=raw_version_data,
                update_time=update_time,
                timestamp=current_time
            )
            
            # 更新缓存
            self._version_cache = version_info
            
            self.logger.info(f"成功获取版本: {version}")
            return version_info
            
        except requests.RequestException as e:
            raise BD2CDNAPIError(f"获取版本时网络错误: {e}")
        except (KeyError, IndexError) as e:
            raise BD2CDNAPIError(f"解析API响应失败: {e}")
        except Exception as e:
            raise BD2CDNAPIError(f"意外错误: {e}")
    
    def get_resource_url(self, data_name: str) -> str:
        """
        为特定资源生成CDN下载URL。
        
        参数:
            data_name: 资源文件名称
            
        返回:
            str: 完整的下载URL
            
        异常:
            BD2CDNAPIError: 如果无法获取版本信息
        """
        try:
            version_info = self.get_version_info()
            url = f"{self.CDN_BASE_URL}/{version_info.version}/{data_name}"
            
            self.logger.debug(f"为 {data_name} 生成URL: {url}")
            return url
            
        except Exception as e:
            raise BD2CDNAPIError(f"生成资源URL失败: {e}")
    
    def get_resource_info(self, data_name: str) -> BD2ResourceInfo:
        """
        获取包含URL和大小的完整资源信息。
        
        参数:
            data_name: 资源文件名称
            
        返回:
            BD2ResourceInfo: 完整的资源信息
            
        异常:
            BD2CDNAPIError: 如果无法获取资源信息
        """
        try:
            version_info = self.get_version_info()
            url = self.get_resource_url(data_name)
            size = self.get_resource_size(data_name)
            
            return BD2ResourceInfo(
                data_name=data_name,
                download_url=url,
                version=version_info.version,
                size=size
            )
            
        except Exception as e:
            raise BD2CDNAPIError(f"获取资源信息失败: {e}")
    
    def get_resource_size(self, data_name: str) -> int:
        """
        不下载资源的情况下获取资源大小。
        
        参数:
            data_name: 资源文件名称
            
        返回:
            int: 大小（字节）
            
        异常:
            BD2CDNAPIError: 如果无法确定大小
        """
        try:
            url = self.get_resource_url(data_name)
            
            response = self.session.head(url, timeout=self.timeout)
            response.raise_for_status()
            
            size = int(response.headers.get('Content-Length', 0))
            
            self.logger.debug(f"资源 {data_name} 大小: {size} 字节")
            return size
            
        except requests.RequestException as e:
            raise BD2CDNAPIError(f"检查资源大小时网络错误: {e}")
        except (ValueError, TypeError) as e:
            raise BD2CDNAPIError(f"响应中的大小值无效: {e}")
    
    def check_resource_exists(self, data_name: str) -> bool:
        """
        检查CDN上是否存在资源。
        
        参数:
            data_name: 资源文件名称
            
        返回:
            bool: 如果资源存在返回True，否则返回False
        """
        try:
            url = self.get_resource_url(data_name)
            response = self.session.head(url, timeout=self.timeout)
            return response.status_code == 200
            
        except Exception:
            return False
    
    def get_resource_bundle_name_and_hash(self, idle_value: str) -> Optional[Tuple[str, str]]:
        """
        通过角色的idle值获取资源部名称。
        
        参数:
            idle_value: 角色的idle值（用于在catalog中查找bundleName）
            
        返回:
            Optional[str]: 资源部名称（readableName + .bundle后缀），如果未找到返回None
            
        异常:
            BD2CDNAPIError: 如果无法获取catalog文件或解析失败
        """
        try:
            # 获取版本信息以获得update_time
            version_info = self.get_version_info()
            update_time = version_info.update_time
            
            # 构建catalog文件的URL
            catalog_url = f"https://bd2-cdn.akamaized.net/ServerData/Android/SD/{update_time}/catalog_alpha_file_hash.json"
            
            self.logger.info(f"从catalog获取资源信息: {catalog_url}")
            
            # 下载catalog文件
            response = self.session.get(catalog_url, timeout=self.timeout)
            response.raise_for_status()
            
            catalog_data = response.json()
            
            # 在bundles中查找匹配的bundleName
            if "bundles" not in catalog_data:
                raise BD2CDNAPIError("catalog文件格式无效: 缺少'bundles'字段")
            
            for bundle in catalog_data["bundles"]:
                if bundle.get("bundleName") == idle_value:
                    readable_name = bundle.get("readableName")
                    hash_id = bundle.get("hash")
                    if readable_name:
                        # 提取资源部名称并添加.bundle后缀
                        # 例如: "common-char-atlas-group0_assets_atlas/char000502_battle.spriteatlasv2" 
                        # 提取: "common-char-atlas-group0_assets_atlas"
                        # if "/" in readable_name:
                        #     resource_name = readable_name.split("/")[0] + ".bundle"
                        # else:
                        resource_name = readable_name + ".bundle"
                        self.logger.info(f"找到资源名称: {resource_name}")
                        return resource_name, hash_id
            
            # 未找到匹配的idle值
            self.logger.warning(f"未找到idle值 '{idle_value}' 对应的资源")
            return None
            
        except requests.RequestException as e:
            raise BD2CDNAPIError(f"获取catalog文件时网络错误: {e}")
        except ValueError as e:
            raise BD2CDNAPIError(f"解析catalog JSON失败: {e}")
        except Exception as e:
            raise BD2CDNAPIError(f"获取资源部名称时发生意外错误: {e}")
    
    def list_common_resources(self) -> Dict[str, str]:
        """
        获取常见BD2资源及其URL的字典。
        
        返回:
            Dict[str, str]: 资源名称到URL的映射
        """
        common_resources = [
            "catalog_alpha.json",
            "common-skeleton-data_assets_all.bundle",
            "common-skeleton-data-group0_assets_all.bundle",
            "common-skeleton-data-group1_assets_all.bundle",
            "common-skeleton-data-group2_assets_all.bundle",
        ]
        
        return {
            resource: self.get_resource_url(resource) 
            for resource in common_resources
        }
    
    def get_api_status(self) -> Dict[str, Any]:
        """
        获取综合API状态信息。
        
        返回:
            Dict[str, Any]: 包含版本、缓存等的状态信息
        """
        try:
            version_info = self.get_version_info()
            cache_age = time.time() - version_info.timestamp if self._version_cache else None
            
            return {
                "api_accessible": True,
                "current_version": version_info.version,
                "cache_age_seconds": cache_age,
                "cache_valid": cache_age < self._cache_ttl if cache_age else False,
                "base_cdn_url": self.CDN_BASE_URL,
                "session_proxies": dict(self.session.proxies),
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "api_accessible": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    def clear_cache(self):
        """清除版本信息缓存。"""
        self._version_cache = None
        self.get_resource_url.cache_clear()
        self.logger.info("缓存已清除")


# 向后兼容的便捷函数
def create_default_api(proxies: Optional[Dict[str, str]] = None) -> BD2CDNAPI:
    """
    使用默认配置创建BD2CDNAPI实例。
    
    参数:
        proxies: 可选的代理配置
        
    返回:
        BD2CDNAPI: 配置好的API实例
    """
    return BD2CDNAPI(proxies=proxies)


def get_bd2_version(proxies: Optional[Dict[str, str]] = None) -> str:
    """
    快速获取当前BD2版本的函数。
    
    参数:
        proxies: 可选的代理配置
        
    返回:
        str: 当前游戏版本
    """
    api = create_default_api(proxies)
    return api.get_version_info().version


def get_bd2_resource_url(data_name: str, 
                        proxies: Optional[Dict[str, str]] = None) -> str:
    """
    快速获取资源下载URL的函数。
    
    参数:
        data_name: 资源名称
        proxies: 可选的代理配置
        
    返回:
        str: 下载URL
    """
    api = create_default_api(proxies)
    return api.get_resource_url(data_name)


def get_bundle_name_by_idle(idle_value: str,
                           proxies: Optional[Dict[str, str]] = None) -> Optional[str]:
    """
    快速通过idle值获取资源部名称的函数。
    
    参数:
        idle_value: 角色的idle值
        proxies: 可选的代理配置
        
    返回:
        Optional[str]: 资源部名称，如果未找到返回None
    """
    api = create_default_api(proxies)
    return api.get_resource_bundle_name(idle_value)


# 使用示例
if __name__ == "__main__":
    # 带代理配置的示例
    proxies = {
        'http': 'http://192.168.1.220:7897',
        'https': 'http://192.168.1.220:7897',
    }
    
    # 创建API实例
    api = BD2CDNAPI(proxies=proxies)
    
    try:
        # 获取版本信息
        print("🎮 BD2 CDN API 示例")
        print("=" * 50)
        
        version_info = api.get_version_info()
        print(f"📊 当前版本: {version_info}")
        
        # 获取资源URL
        catalog_url = api.get_resource_url("catalog_alpha.json")
        print(f"📁 目录URL: {catalog_url}")
        
        # 获取资源信息
        resource_info = api.get_resource_info("catalog_alpha.json")
        print(f"📋 资源信息: {resource_info}")
        
        # 检查API状态
        status = api.get_api_status()
        print(f"🔍 API状态: {status}")
        
        print("\n✅ API测试成功完成!")
        
    except BD2CDNAPIError as e:
        print(f"❌ API错误: {e}")
    except Exception as e:
        print(f"❌ 意外错误: {e}")
