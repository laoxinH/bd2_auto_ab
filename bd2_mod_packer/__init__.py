#!/usr/bin/env python3
"""
BD2 MOD Manager - Brown Dust 2 自动化MOD管理系统

这是一个专为《Brown Dust 2》游戏开发的自动化资源管理系统，
提供从角色数据获取、目录结构初始化到MOD资源打包的完整自动化流程。

主要功能模块：
- core: 核心业务逻辑
- ui: 用户界面
- config: 配置管理
- utils: 工具函数
- api: API接口

作者: BD2 MOD实验室
版本: 2.0.0
日期: 2025-08-15
"""

__version__ = "2.0.0"
__author__ = "BD2 MOD实验室"
__email__ = "bd2lab@example.com"
__description__ = "Brown Dust 2 自动化MOD管理系统"

# 导入主要类和函数
from .core.manager import BD2ModManager
from .ui.console import BD2Console
from .config.settings import BD2Config

__all__ = [
    'BD2ModManager',
    'BD2Console',
    'BD2Config',
]
