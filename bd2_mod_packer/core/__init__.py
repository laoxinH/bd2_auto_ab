#!/usr/bin/env python3
"""
BD2 MOD Manager - 核心模块

包含系统的核心业务逻辑：
- MOD管理器
- 资源处理器
- 数据下载器
- 工作区管理

作者: BD2 MOD实验室
日期: 2025-08-15
"""

# 核心组件导入将在重构完成后添加
# 导入主要类和函数
from .manager import BD2ModManager
from .resource_manager import BD2ResourceManager
from .data_downloader import BD2DataDownloader
from .unity_processor import UnityResourceProcessor
from .main_program import BD2MainProgram

__all__ = [
    'BD2ModManager',
    'BD2ResourceManager',
    'BD2DataDownloader',
    'UnityResourceProcessor',
    'BD2MainProgram'
]


