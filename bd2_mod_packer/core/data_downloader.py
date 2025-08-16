#!/usr/bin/env python3
"""
BD2 数据下载器

此模块处理从BD2的CDN下载游戏数据文件。

作者: OLDNEW
日期: 2025-08-14
"""

import logging
import os
from typing import Optional

import requests
import tqdm

from ..api import BD2CDNAPI, BD2CDNAPIError


# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
logger = logging.getLogger(__name__)

# 获取脚本所在目录的父目录（项目根目录）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 导入配置
try:
    from config import get_config
    _config_available = True
except ImportError:
    _config_available = False
    # 如果配置模块不可用，提供默认代理配置
    DEFAULT_PROXIES = None


class BD2DataDownloader:
    """
    BD2资源数据下载器。

    此类提供了一个干净的接口，用于下载游戏数据文件，
    使用BD2CDNAPI进行URL生成和版本管理。
    """
    
    def __init__(self, 
                 proxies: Optional[dict] = None,
                 output_dir: Optional[str] = None,
                 timeout: float = 30.0):
        """
        初始化数据下载器。
        
        参数:
            proxies: 请求的代理配置
            output_dir: 下载的基础目录（默认为项目的sourcedata目录）
            timeout: 请求超时时间（秒）
        """
        # 设置代理配置
        if proxies is not None:
            self.proxies = proxies
        elif _config_available:
            # 从配置文件获取代理
            config = get_config()
            self.proxies = config.get_proxies()
        else:
            # 使用默认代理配置
            self.proxies = DEFAULT_PROXIES
            
        self.output_dir = output_dir or os.path.join(project_root, "sourcedata")
        self.timeout = timeout
        
        # 初始化API和会话
        self.api = BD2CDNAPI(proxies=self.proxies, timeout=timeout)
        self.session = requests.Session()
        if self.proxies:
            self.session.proxies.update(self.proxies)
            logger.info(f"BD2资源下载代理: {self.proxies}")
        
        logger.info(f"BD2数据下载器已初始化，输出目录: {self.output_dir}")
    
    def download_data(self, data_name: str, show_progress: bool = True) -> str:
        """
        从BD2 CDN下载数据文件。
        
        参数:
            data_name: 要下载的数据文件名称
            show_progress: 是否显示下载进度条
            
        返回:
            str: 下载文件的路径
            
        异常:
            BD2CDNAPIError: 如果下载失败
        """
        try:
            # 获取资源信息
            resource_info = self.api.get_resource_info(data_name)
            
            logger.info(f"正在下载 {resource_info}")
            
            # 准备输出路径
            output_path = os.path.join(self.output_dir, data_name, "__data")
            
            # 检查文件是否已存在，如果存在且大小一致则跳过下载
            if os.path.exists(output_path):
                local_size = os.path.getsize(output_path)
                server_size = resource_info.size
                
                if local_size == server_size:
                    logger.info(f"文件已存在且大小一致({local_size} 字节)，跳过下载: {output_path}")
                    return output_path
                else:
                    logger.info(f"文件已存在但大小不一致(本地:{local_size}, 服务器:{server_size})，将重新下载: {output_path}")
            
            # 如需要则创建目录
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            logger.info(f"输出目录: {os.path.dirname(output_path)}")
            
            # 开始下载并显示进度条
            response = self.session.get(resource_info.download_url, stream=True, timeout=self.timeout)
            response.raise_for_status()
            
            total_size = resource_info.size or int(response.headers.get('content-length', 0))
            
            if show_progress:
                progress_bar = tqdm.tqdm(
                    desc=os.path.basename(output_path),
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                )
            
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        size = f.write(chunk)
                        if show_progress:
                            progress_bar.update(size)
            
            if show_progress:
                progress_bar.close()
            
            logger.info(f"✅ 已下载 {data_name} 到 {output_path}")
            return output_path
            
        except requests.RequestException as e:
            raise BD2CDNAPIError(f"{data_name} 下载失败: {e}")
        except OSError as e:
            raise BD2CDNAPIError(f"文件系统错误: {e}")
        except Exception as e:
            raise BD2CDNAPIError(f"下载 {data_name} 时发生意外错误: {e}")
    
    def get_data_size(self, data_name: str) -> int:
        """
        在不下载的情况下获取数据文件的大小。
        
        参数:
            data_name: 数据文件名称
            
        返回:
            int: 大小（字节）
        """
        try:
            size = self.api.get_resource_size(data_name)
            logger.info(f"📊 {data_name} 大小: {size:,} 字节 ({size/1024/1024:.2f} MB)")
            return size
        except Exception as e:
            raise BD2CDNAPIError(f"获取 {data_name} 大小失败: {e}")
    
    def check_data_exists(self, data_name: str) -> bool:
        """
        检查CDN上是否存在数据文件。
        
        参数:
            data_name: 数据文件名称
            
        返回:
            bool: 如果文件存在返回True
        """
        return self.api.check_resource_exists(data_name)
    
    def download_multiple(self, data_names: list, show_progress: bool = True) -> dict:
        """
        下载多个数据文件。
        
        参数:
            data_names: 数据文件名称列表
            show_progress: 是否显示进度条
            
        返回:
            dict: data_name到下载路径或错误的映射
        """
        results = {}
        
        logger.info(f"📦 开始批量下载 {len(data_names)} 个文件")
        
        for i, data_name in enumerate(data_names, 1):
            logger.info(f"[{i}/{len(data_names)}] 正在处理 {data_name}")
            
            try:
                path = self.download_data(data_name, show_progress)
                results[data_name] = {"status": "success", "path": path}
            except Exception as e:
                logger.error(f"❌ 下载 {data_name} 失败: {e}")
                results[data_name] = {"status": "error", "error": str(e)}
        
        success_count = sum(1 for r in results.values() if r["status"] == "success")
        logger.info(f"✅ 批量下载完成: {success_count}/{len(data_names)} 成功")
        
        return results
    
    def get_status(self) -> dict:
        """
        获取下载器状态信息。
        
        返回:
            dict: 状态信息
        """
        api_status = self.api.get_api_status()
        
        return {
            "output_directory": self.output_dir,
            "proxies_configured": bool(self.proxies),
            "api_status": api_status,
            "timeout": self.timeout
        }


# 向后兼容性函数
def get_bd2_cdn(data_name: str) -> tuple:
    """
    用于向后兼容性的遗留函数。
    
    参数:
        data_name: 数据文件名称
        
    返回:
        tuple: (url, data_name)
    """
    # 获取代理配置
    if _config_available:
        config = get_config()
        proxies = config.get_proxies()
    else:
        proxies = DEFAULT_PROXIES
        
    api = BD2CDNAPI(proxies=proxies)
    url = api.get_resource_url(data_name)
    return url, data_name


def download_data(data_name: str) -> str:
    """
    用于向后兼容性的遗留函数。
    
    参数:
        data_name: 数据文件名称
        
    返回:
        str: 下载文件的路径
    """
    downloader = BD2DataDownloader()
    return downloader.download_data(data_name)


def get_data_size(data_name: str) -> int:
    """
    用于向后兼容性的遗留函数。
    
    参数:
        data_name: 数据文件名称
        
    返回:
        int: 大小（字节）
    """
    downloader = BD2DataDownloader()
    return downloader.get_data_size(data_name)


# 使用示例和测试
if __name__ == "__main__":
    print("🎮 BD2数据下载器测试")
    print("=" * 50)
    
    try:
        # 创建下载器
        downloader = BD2DataDownloader()
        
        # 显示状态
        status = downloader.get_status()
        print(f"📊 下载器状态:")
        print(f"   输出目录: {status['output_directory']}")
        print(f"   API版本: {status['api_status'].get('current_version', '未知')}")
        print(f"   API可访问: {status['api_status']['api_accessible']}")
        
        # 使用小文件测试
        test_file = "catalog_alpha.json"
        
        print(f"\n🔍 检查 {test_file}...")
        if downloader.check_data_exists(test_file):
            size = downloader.get_data_size(test_file)
            print(f"✅ 文件存在，大小: {size:,} 字节")
            
            # 取消注释以实际下载
            # print(f"📥 正在下载 {test_file}...")
            # path = downloader.download_data(test_file)
            # print(f"✅ 已下载到: {path}")
        else:
            print(f"❌ 文件 {test_file} 未找到")
        
        print("\n✅ 测试成功完成!")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
