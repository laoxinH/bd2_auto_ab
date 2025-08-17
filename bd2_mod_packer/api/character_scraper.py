#!/usr/bin/env python3
"""
Brown Dust 2 Character Idle Scraper

从 https://browndust2modding.pages.dev/characters 网站提取角色idle值的工具类。
支持直接从网站获取数据，也支持解析本地HTML文件。

使用示例:
    from character_idle_scraper                            # 这是一个被rowspan影响的行，使用当前角色信息
                            if id_or_costume.startswith(('char', 'illust_', 'specialIllust', 'specialillust')):
                                # 这行有新的ID，说明是同一角色的不同服装变体
                                current_char_id = id_or_costume.strip()
                                costume = costume_or_idle.strip()
                                idle = idle_or_cutscene.strip()
                                cutscene = cutscene_or_next.strip()
                            else:
                                # 普通的服装行
                                costume = id_or_costume.strip()
                                idle = costume_or_idle.strip()
                                cutscene = idle_or_cutscene.strip()acterIdleScraper
    
    # 创建scraper实例
    scraper = CharacterIdleScraper()
    
    # 从网站获取idle值
    idle_value = scraper.get_idle("Lathel", "Homunculus")
    print(f"Idle value: {idle_value}")
    
    # 从网站获取cutscene值
    cutscene_value = scraper.get_cutscene("Lathel", "Homunculus")
    print(f"Cutscene value: {cutscene_value}")
    
    # 或从本地HTML文件获取数据
    with open("webpage.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    idle_value = scraper.get_idle("Lathel", "Homunculus", html=html_content)
    cutscene_value = scraper.get_cutscene("Lathel", "Homunculus", html=html_content)
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional, Tuple, Dict
import re
import requests
from bs4 import BeautifulSoup, Tag

# 导入配置
try:
    from ..config import get_config
    _config_available = True
except ImportError:
    _config_available = False


DEFAULT_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQLmR_jafTkS65IOwboDbdCaUa9n2OUIT4_VLq2EU-9_alX5BBXmgj4T4IBJx-eWhBRkLnN9-pqM65R/pubhtml/sheet?headers=false&gid=269089981"


def _norm(s: str) -> str:
    """标准化字符串：转小写并去除多余空白"""
    return re.sub(r"\s+", " ", s or "").strip().lower()


def _maybe_to_int(s: str):
    """如果字符串是纯数字，转换为int，否则返回原字符串"""
    t = s.strip()
    if re.fullmatch(r"[+-]?\d+", t):
        try:
            return int(t)
        except Exception:
            return t
    return t


@dataclass(frozen=True)
class CharacterData:
    """角色数据结构"""
    character: str
    costume: str
    idle: str
    cutscene: str = ""  # cutscene字段
    char_id: str = ""  # 角色ID字段 (如: char000101)

    def __str__(self):
        return f"Character: '{self.character}', Costume: '{self.costume}', ID: '{self.char_id}', Idle: '{self.idle}', Cutscene: '{self.cutscene}'"


class CharacterScraper:
    """
    Brown Dust 2 角色 Idle 值提取器
    
    功能特性：
    - 🌐 支持直接从网站获取最新数据
    - 📄 支持解析本地HTML文件（离线使用）
    - 🔍 智能模糊匹配（精确 → 前缀 → 子串匹配）
    - 🧠 自动处理复杂的表格结构（rowspan等）
    - ⚡ 内置缓存提高性能
    - 🛡️ 完善的错误处理
    """
    
    def __init__(self, url: str = DEFAULT_URL, *, timeout: float = 15.0, user_agent: Optional[str] = None, proxies: Optional[Dict[str, str]] = None):
        """
        初始化scraper
        
        Args:
            url: 目标网站URL
            timeout: 请求超时时间（秒）
            user_agent: 自定义User-Agent
            proxies: 代理配置，如果不提供且配置文件可用则自动获取
        """
        self.url = url
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        )

        # 设置代理
        # 设置代理配置
        if proxies is not None:
            self.proxies = proxies
        elif _config_available:
            # 从配置文件获取代理
            config = get_config()
            self.proxies = config.get_proxies()
        else:
            self.proxies = None



    @lru_cache(maxsize=4)
    def fetch_html(self) -> str:
        """
        从网站获取HTML内容（带缓存）
        
        Returns:
            HTML内容字符串
            
        Raises:
            requests.RequestException: 网络请求失败
        """
        request_kwargs = {
            'headers': {"User-Agent": self.user_agent}, 
            'timeout': self.timeout
        }
        
        # 添加代理配置
        if self.proxies:
            request_kwargs['proxies'] = self.proxies
        
        resp = requests.get(self.url, **request_kwargs)
        resp.raise_for_status()
        return resp.text

    def parse_rows(self, html: str) -> List[CharacterData]:
        """
        解析HTML内容，提取角色数据
        
        Args:
            html: HTML内容字符串
            
        Returns:
            角色数据列表
        """
        soup = BeautifulSoup(html, "lxml")
        tables = soup.find_all("table")
        if not tables:
            return []

        rows: List[CharacterData] = []
        for table in tables:
            try:
                tbody = table.find("tbody")
                if not tbody:
                    continue
                
                trs = tbody.find_all("tr")
                if len(trs) < 3:
                    continue
                
                # 构建考虑rowspan的表格矩阵
                matrix = self._build_table_matrix(trs[2:])  # 跳过表头和空行
                
                # 从矩阵中提取数据，需要跟踪当前角色名和ID
                current_character = ""
                current_char_id = ""
                
                for row_data in matrix:
                    if len(row_data) >= 5:
                        # 跳过行号列（列0）
                        character_cell = row_data[1] if len(row_data) > 1 else ""
                        id_or_costume = row_data[2] if len(row_data) > 2 else ""
                        costume_or_idle = row_data[3] if len(row_data) > 3 else ""
                        idle_or_cutscene = row_data[4] if len(row_data) > 4 else ""
                        cutscene_or_next = row_data[5] if len(row_data) > 5 else ""
                        
                        # 判断是否是新的角色行（有角色名）
                        if character_cell.strip():
                            current_character = character_cell.strip()
                            
                            # 从配置获取有效的ID前缀
                            valid_prefixes = self._get_valid_id_prefixes()
                            
                            # 判断数据类型：如果第二列看起来像ID，则调整列位置
                            if self._is_valid_id(id_or_costume, valid_prefixes):
                                current_char_id = id_or_costume.strip()
                                costume = costume_or_idle.strip()
                                idle = idle_or_cutscene.strip()
                                cutscene = cutscene_or_next.strip()
                            else:
                                # 角色名存在但没有ID，这种情况下第二列应该是服装
                                current_char_id = ""
                                costume = id_or_costume.strip()
                                idle = costume_or_idle.strip()
                                cutscene = idle_or_cutscene.strip()
                        else:
                            # 这是一个被rowspan影响的行，使用当前角色信息
                            valid_prefixes = self._get_valid_id_prefixes()
                            if self._is_valid_id(id_or_costume, valid_prefixes):
                                # 这行有新的ID，说明是同一角色的不同服装变体
                                current_char_id = id_or_costume.strip()
                                costume = costume_or_idle.strip()
                                idle = idle_or_cutscene.strip()
                                cutscene = cutscene_or_next.strip()
                            else:
                                # 普通的服装行
                                costume = id_or_costume.strip()
                                idle = costume_or_idle.strip()
                                cutscene = idle_or_cutscene.strip()
                        
                        # 只有当有角色名和服装时才添加数据
                        if current_character and costume:
                            rows.append(CharacterData(
                                character=current_character,
                                costume=costume,
                                idle=idle,
                                cutscene=cutscene,
                                char_id=current_char_id
                            ))
                    
            except Exception as e:
                print(f"解析表格时出错: {e}")
                continue
        
        return rows

    def _build_table_matrix(self, trs: List[Tag]) -> List[List[str]]:
        """构建考虑rowspan的表格矩阵"""
        matrix = []
        rowspan_tracker = {}  # 跟踪rowspan: {col_index: (remaining_rows, value)}
        
        for tr in trs:
            cells = tr.find_all(["td", "th"])
            row_data = []
            cell_index = 0
            
            for col_index in range(20):  # 假设最多20列够用
                # 检查这一列是否被之前的rowspan占用
                if col_index in rowspan_tracker:
                    remaining, value = rowspan_tracker[col_index]
                    row_data.append(value)
                    if remaining > 1:
                        rowspan_tracker[col_index] = (remaining - 1, value)
                    else:
                        del rowspan_tracker[col_index]
                else:
                    # 使用当前单元格
                    if cell_index < len(cells):
                        cell = cells[cell_index]
                        value = self._cell_text(cell)
                        row_data.append(value)
                        
                        # 检查rowspan
                        rowspan = cell.get('rowspan')
                        if rowspan and int(rowspan) > 1:
                            rowspan_tracker[col_index] = (int(rowspan) - 1, value)
                        
                        cell_index += 1
                    else:
                        row_data.append("")
                
                # 如果行数据已经足够长，可以跳出
                if len(row_data) >= 10:
                    break
            
            matrix.append(row_data)
        
        return matrix

    def _cell_text(self, cell: Tag) -> str:
        """提取单元格文本内容"""
        # 优先使用特殊属性
        for attr in ("data-value", "data-id", "title", "aria-label"):
            v = cell.get(attr)
            if v:
                return str(v)
        
        # 获取普通文本
        text = cell.get_text(" ", strip=True)
        
        # 如果为空，尝试特定标签
        if not text:
            for tag_name in ("code", "span", "div"):
                tag = cell.find(tag_name)
                if tag:
                    text = tag.get_text(" ", strip=True)
                    if text:
                        break
        
        return text

    def get_idle(self, character: str, costume: str, *, html: Optional[str] = None):
        """
        获取指定角色和服装的idle值
        
        Args:
            character: 角色名称
            costume: 服装名称  
            html: 可选的HTML内容，如果不提供则从网站获取
            
        Returns:
            idle值（字符串或整数）
            
        Raises:
            ValueError: 解析失败
            LookupError: 未找到匹配项
        """
        html_text = html if html is not None else self.fetch_html()
        rows = self.parse_rows(html_text)
        
        if not rows:
            raise ValueError("未能在页面中解析到有效的角色数据")

        n_char = _norm(character)
        n_cos = _norm(costume)

        def match_score(row: CharacterData) -> Tuple[int, int]:
            """计算匹配分数"""
            rc, rs = _norm(row.character), _norm(row.costume)
            
            def one(a: str, b: str) -> int:
                if a == b:
                    return 2  # 精确匹配
                if a.startswith(b) or b.startswith(a):
                    return 1  # 前缀匹配
                if a in b or b in a:
                    return 0  # 子串匹配
                return -1  # 不匹配

            return one(rc, n_char), one(rs, n_cos)

        # 查找最佳匹配
        best: Optional[Tuple[int, int, CharacterData]] = None
        for r in rows:
            sc = match_score(r)
            if sc[0] < 0 or sc[1] < 0:
                continue
            
            cand = (sc[0] + sc[1], max(sc), r)
            if best is None or cand > best:
                best = cand

        if best is None:
            # 提供有用的调试信息
            available_chars = list(set(row.character for row in rows[:20]))
            available_costumes = list(set(row.costume for row in rows[:20]))
            raise LookupError(
                f"未找到匹配项: character='{character}', costume='{costume}'\n"
                f"可用角色示例: {available_chars[:5]}\n"
                f"可用服装示例: {available_costumes[:5]}"
            )

        idle_value = best[2].idle
        return _maybe_to_int(idle_value)

    def get_cutscene(self, character: str, costume: str, *, html: Optional[str] = None):
        """
        获取指定角色和服装的cutscene值
        
        Args:
            character: 角色名称
            costume: 服装名称  
            html: 可选的HTML内容，如果不提供则从网站获取
            
        Returns:
            cutscene值（字符串或整数）
            
        Raises:
            ValueError: 解析失败
            LookupError: 未找到匹配项
        """
        html_text = html if html is not None else self.fetch_html()
        rows = self.parse_rows(html_text)
        
        if not rows:
            raise ValueError("未能在页面中解析到有效的角色数据")

        n_char = _norm(character)
        n_cos = _norm(costume)

        def match_score(row: CharacterData) -> Tuple[int, int]:
            """计算匹配分数"""
            rc, rs = _norm(row.character), _norm(row.costume)
            
            def one(a: str, b: str) -> int:
                if a == b:
                    return 2  # 精确匹配
                if a.startswith(b) or b.startswith(a):
                    return 1  # 前缀匹配
                if a in b or b in a:
                    return 0  # 子串匹配
                return -1  # 不匹配

            return one(rc, n_char), one(rs, n_cos)

        # 查找最佳匹配
        best: Optional[Tuple[int, int, CharacterData]] = None
        for r in rows:
            sc = match_score(r)
            if sc[0] < 0 or sc[1] < 0:
                continue
            
            cand = (sc[0] + sc[1], max(sc), r)
            if best is None or cand > best:
                best = cand

        if best is None:
            # 提供有用的调试信息
            available_chars = list(set(row.character for row in rows[:20]))
            available_costumes = list(set(row.costume for row in rows[:20]))
            raise LookupError(
                f"未找到匹配项: character='{character}', costume='{costume}'\n"
                f"可用角色示例: {available_chars[:5]}\n"
                f"可用服装示例: {available_costumes[:5]}"
            )

        cutscene_value = best[2].cutscene
        return _maybe_to_int(cutscene_value)

    def get_all_data(self, *, html: Optional[str] = None) -> List[CharacterData]:
        """
        获取所有角色数据
        
        Args:
            html: 可选的HTML内容，如果不提供则从网站获取
            
        Returns:
            所有角色数据的列表
        """
        html_text = html if html is not None else self.fetch_html()
        return self.parse_rows(html_text)

    def search_characters(self, character_name: str, *, html: Optional[str] = None) -> List[CharacterData]:
        """
        搜索指定角色的所有服装
        
        Args:
            character_name: 角色名称（支持模糊匹配）
            html: 可选的HTML内容
            
        Returns:
            匹配的角色数据列表
        """
        all_data = self.get_all_data(html=html)
        n_char = _norm(character_name)
        
        matches = []
        for data in all_data:
            rc = _norm(data.character)
            if n_char in rc or rc in n_char:
                matches.append(data)
        
        return matches

    def get_idle_by_id(self, char_id: str, *, html: Optional[str] = None):
        """
        根据角色ID获取idle值
        
        Args:
            char_id: 角色ID (如: char000101, char000102)
            html: 可选的HTML内容，如果不提供则从网站获取
            
        Returns:
            idle值（字符串或整数）
            
        Raises:
            ValueError: 解析失败
            LookupError: 未找到匹配的ID
        """
        html_text = html if html is not None else self.fetch_html()
        rows = self.parse_rows(html_text)
        
        if not rows:
            raise ValueError("未能在页面中解析到有效的角色数据")

        # 标准化ID，移除前缀并比较
        normalized_id = char_id.lower().strip()
        
        # 查找匹配的ID
        for row in rows:
            if row.char_id.lower().strip() == normalized_id:
                return _maybe_to_int(row.idle)
        
        # 如果没找到精确匹配，提供有用的调试信息
        available_ids = [row.char_id for row in rows[:10] if row.char_id]
        raise LookupError(
            f"未找到匹配的角色ID: '{char_id}'\n"
            f"可用ID示例: {available_ids[:5]}"
        )

    def get_cutscene_by_id(self, char_id: str, *, html: Optional[str] = None):
        """
        根据角色ID获取cutscene值
        
        Args:
            char_id: 角色ID (如: char000101, char000102)
            html: 可选的HTML内容，如果不提供则从网站获取
            
        Returns:
            cutscene值（字符串或整数）
            
        Raises:
            ValueError: 解析失败
            LookupError: 未找到匹配的ID
        """
        html_text = html if html is not None else self.fetch_html()
        rows = self.parse_rows(html_text)
        
        if not rows:
            raise ValueError("未能在页面中解析到有效的角色数据")

        # 标准化ID，移除前缀并比较
        normalized_id = char_id.lower().strip()
        
        # 查找匹配的ID
        for row in rows:
            if row.char_id.lower().strip() == normalized_id:
                return _maybe_to_int(row.cutscene)
        
        # 如果没找到精确匹配，提供有用的调试信息
        available_ids = [row.char_id for row in rows[:10] if row.char_id]
        raise LookupError(
            f"未找到匹配的角色ID: '{char_id}'\n"
            f"可用ID示例: {available_ids[:5]}"
        )

    def get_character_by_id(self, char_id: str, *, html: Optional[str] = None) -> Optional[CharacterData]:
        """
        根据角色ID获取完整的角色数据
        
        Args:
            char_id: 角色ID (如: char000101, char000102)
            html: 可选的HTML内容，如果不提供则从网站获取
            
        Returns:
            匹配的角色数据，如果未找到则返回None
        """
        html_text = html if html is not None else self.fetch_html()
        rows = self.parse_rows(html_text)
        
        if not rows:
            return None

        # 标准化ID，移除前缀并比较
        normalized_id = char_id.lower().strip()
        
        # 查找匹配的ID
        for row in rows:
            if row.char_id.lower().strip() == normalized_id:
                return row
        
        return None
    
    def _get_valid_id_prefixes(self) -> list:
        """
        获取有效的ID前缀列表
        
        Returns:
            ID前缀列表
        """
        try:
            if _config_available:
                config = get_config()
                return config.get_character_id_prefixes()
        except Exception:
            pass
        
        # 如果配置不可用，使用默认前缀
        return [
            "char",
            "illust_dating", 
            "illust_talk",
            "illust_special",
            "specialillust",
            "specialIllust",
            "npc",
            "storypack"
        ]
    
    def _is_valid_id(self, test_id: str, valid_prefixes: list) -> bool:
        """
        检查给定ID是否匹配任何有效前缀
        
        Args:
            test_id: 要检查的ID
            valid_prefixes: 有效前缀列表
            
        Returns:
            是否匹配
        """
        if not test_id or not valid_prefixes:
            return False
        
        test_id = test_id.strip()
        for prefix in valid_prefixes:
            if test_id.startswith(prefix):
                return True
        return False


__all__ = ["CharacterScraper", "CharacterData"]


if __name__ == "__main__":
    # 简单的使用示例
    scraper = CharacterScraper()
    
    try:
        # 测试从本地HTML文件读取
        with open("文档.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        idle_value = scraper.get_cutscene("Celia", "The Curse", html=html_content)
        print(f"Celia + The Curse cutscene = {idle_value}")
        
        # 测试新的cutscene功能
        cutscene_value = scraper.get_cutscene("Lathel", "Homunculus", html=html_content)
        print(f"Lathel + Homunculus Cutscene = {cutscene_value}")
        
        # 获取Lathel的所有服装
        lathel_data = scraper.search_characters("Celia", html=html_content)
        print(f"\nCelia的所有服装 ({len(lathel_data)}个):")
        for data in lathel_data:
            print(f"  - {data.costume}: ID={data.char_id}, Idle={data.idle}, Cutscene={data.cutscene}")
        
        # 测试基于ID的查找功能
        print(f"\n=== 测试ID查找功能 ===")
        try:
            # 测试根据ID获取idle值
            idle_by_id = scraper.get_idle_by_id("char000101", html=html_content)
            print(f"char000101 的 idle = {idle_by_id}")
            
            # 测试根据ID获取cutscene值
            cutscene_by_id = scraper.get_cutscene_by_id("char000101", html=html_content)
            print(f"char000101 的 cutscene = {cutscene_by_id}")
            
            # 测试获取完整角色数据
            character_data = scraper.get_character_by_id("char000102", html=html_content)
            if character_data:
                print(f"char000102 的完整数据: {character_data}")
            else:
                print("char000102 未找到")
                
        except Exception as e:
            print(f"ID查找测试失败: {e}")
            
    except FileNotFoundError:
        print("请确保文档.html文件存在")
        
        # 如果文件不存在，尝试从网站获取数据
        print("尝试从网站获取数据...")
        try:
            idle_value = scraper.get_idle("Lathel", "Homunculus")
            print(f"Lathel + Homunculus Idle = {idle_value}")
            
            cutscene_value = scraper.get_cutscene("Lathel", "Homunculus")
            print(f"Lathel + Homunculus Cutscene = {cutscene_value}")
            
        except Exception as e:
            print(f"从网站获取数据失败: {e}")
            
    except Exception as e:
        print(f"错误: {e}")
