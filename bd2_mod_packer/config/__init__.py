#!/usr/bin/env python3
"""
BD2 MOD Manager - 配置管理模块

包含所有配置相关的组件：
- 配置文件管理
- 设置项定义
- 配置验证
- 默认配置

作者: BD2 MOD实验室
日期: 2025-08-15
"""

# 配置组件导入将在重构完成后添加
from .settings import get_config,reload_config

__all__ = [
    'get_config',
    'reload_config',
]
