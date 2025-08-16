#!/usr/bin/env python3
"""
BD2 MOD Manager - API模块

包含所有外部API交互组件：
- BD2 CDN API
- 谷歌表格API
- 网络请求处理
- API响应解析

作者: BD2 MOD实验室
日期: 2025-08-15
"""

# 暴露依赖
from .cdn_api import BD2CDNAPI,BD2CDNAPIError
from .character_scraper import CharacterScraper, CharacterData

__all__ = [
    'BD2CDNAPI',
    'BD2CDNAPIError',
    'CharacterScraper',
    'CharacterData',
]
