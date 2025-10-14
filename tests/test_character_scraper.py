#!/usr/bin/env python3
"""
Brown Dust 2 Character Scraper 测试脚本

这个脚本测试 CharacterScraper 类的所有主要功能，包括：
- 从网站获取数据
- 解析HTML内容
- 模糊匹配查找
- ID查找功能
- 错误处理

运行方式:
    python tests/test_character_scraper.py
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from bd2_mod_packer.api.character_scraper import CharacterScraper, CharacterData


class TestCharacterScraper:
    """CharacterScraper 测试类"""
    
    def __init__(self):
        self.scraper = CharacterScraper()
        self.passed = 0
        self.failed = 0
        self.test_html = None
        
    def log_success(self, test_name: str, message: str = ""):
        """记录成功的测试"""
        self.passed += 1
        status = "✅ PASS"
        print(f"{status} | {test_name}")
        if message:
            print(f"       └─ {message}")
    
    def log_failure(self, test_name: str, error: str):
        """记录失败的测试"""
        self.failed += 1
        status = "❌ FAIL"
        print(f"{status} | {test_name}")
        print(f"       └─ 错误: {error}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 70)
        print("Brown Dust 2 Character Scraper 测试套件")
        print("=" * 70)
        print()
        
        # 测试1: 网络连接测试
        self.test_fetch_html()
        
        # 测试2: HTML解析测试
        self.test_parse_rows()
        
        # 测试3: 获取idle值
        self.test_get_idle()
        
        # 测试4: 获取cutscene值
        self.test_get_cutscene()
        
        # 测试5: 模糊匹配测试
        self.test_fuzzy_matching()
        
        # 测试6: ID查找测试
        self.test_get_by_id()
        
        # 测试7: 搜索角色功能
        self.test_search_characters()
        
        # 测试8: 获取所有数据
        self.test_get_all_data()
        
        # 测试9: 错误处理
        self.test_error_handling()
        
        # 测试10: 数据完整性检查
        self.test_data_integrity()
        
        # 测试11: 指定ID获取完整角色信息
        self.test_specific_char_id()
        
        # 输出测试结果摘要
        self.print_summary()
    
    def test_fetch_html(self):
        """测试从网站获取HTML"""
        test_name = "测试1: 从网站获取HTML"
        try:
            html = self.scraper.fetch_html()
            if html and len(html) > 1000:  # 确保获取到了足够的内容
                self.test_html = html  # 保存以供后续测试使用
                self.log_success(test_name, f"成功获取 {len(html)} 字节的HTML内容")
            else:
                self.log_failure(test_name, "HTML内容太短，可能获取失败")
        except Exception as e:
            self.log_failure(test_name, str(e))
            # 如果网络测试失败，尝试从本地文件读取
            self.try_load_local_html()
    
    def try_load_local_html(self):
        """尝试从本地文件加载HTML（备用方案）"""
        test_html_path = project_root / "文档.html"
        if test_html_path.exists():
            try:
                with open(test_html_path, "r", encoding="utf-8") as f:
                    self.test_html = f.read()
                print("       └─ 提示: 使用本地HTML文件进行测试")
            except Exception:
                pass
    
    def test_parse_rows(self):
        """测试HTML解析功能"""
        test_name = "测试2: 解析HTML内容"
        if not self.test_html:
            self.log_failure(test_name, "没有可用的HTML内容")
            return
        
        try:
            rows = self.scraper.parse_rows(self.test_html)
            if rows and len(rows) > 0:
                self.log_success(test_name, f"成功解析 {len(rows)} 条角色数据")
                # 显示前3条数据作为示例
                print(f"       └─ 前3条数据示例:")
                for i, row in enumerate(rows[:3], 1):
                    print(f"          {i}. {row.character} - {row.costume} (ID: {row.char_id})")
            else:
                self.log_failure(test_name, "未能解析到任何数据")
        except Exception as e:
            self.log_failure(test_name, str(e))
    
    def test_get_idle(self):
        """测试获取idle值"""
        test_name = "测试3: 获取idle值"
        if not self.test_html:
            self.log_failure(test_name, "没有可用的HTML内容")
            return
        
        test_cases = [
            ("Lathel", "Homunculus"),
            ("Celia", "The Curse"),
        ]
        
        for character, costume in test_cases:
            try:
                idle_value = self.scraper.get_idle(character, costume, html=self.test_html)
                self.log_success(
                    f"{test_name} - {character}/{costume}",
                    f"Idle = {idle_value}"
                )
            except LookupError:
                # 如果找不到，尝试搜索相似的角色
                try:
                    matches = self.scraper.search_characters(character, html=self.test_html)
                    if matches:
                        suggestion = matches[0]
                        self.log_failure(
                            f"{test_name} - {character}/{costume}",
                            f"未找到精确匹配。建议: {suggestion.character}/{suggestion.costume}"
                        )
                    else:
                        self.log_failure(
                            f"{test_name} - {character}/{costume}",
                            f"未找到匹配的角色"
                        )
                except Exception:
                    self.log_failure(
                        f"{test_name} - {character}/{costume}",
                        "未找到匹配项"
                    )
            except Exception as e:
                self.log_failure(f"{test_name} - {character}/{costume}", str(e))
    
    def test_get_cutscene(self):
        """测试获取cutscene值"""
        test_name = "测试4: 获取cutscene值"
        if not self.test_html:
            self.log_failure(test_name, "没有可用的HTML内容")
            return
        
        test_cases = [
            ("Lathel", "Homunculus"),
            ("Celia", "The Curse"),
        ]
        
        for character, costume in test_cases:
            try:
                cutscene_value = self.scraper.get_cutscene(character, costume, html=self.test_html)
                self.log_success(
                    f"{test_name} - {character}/{costume}",
                    f"Cutscene = {cutscene_value}"
                )
            except LookupError:
                self.log_failure(
                    f"{test_name} - {character}/{costume}",
                    "未找到匹配项"
                )
            except Exception as e:
                self.log_failure(f"{test_name} - {character}/{costume}", str(e))
    
    def test_fuzzy_matching(self):
        """测试模糊匹配功能"""
        test_name = "测试5: 模糊匹配"
        if not self.test_html:
            self.log_failure(test_name, "没有可用的HTML内容")
            return
        
        # 测试大小写不敏感
        try:
            rows = self.scraper.parse_rows(self.test_html)
            if rows:
                first_char = rows[0]
                # 测试不同大小写
                idle1 = self.scraper.get_idle(
                    first_char.character.upper(),
                    first_char.costume.upper(),
                    html=self.test_html
                )
                idle2 = self.scraper.get_idle(
                    first_char.character.lower(),
                    first_char.costume.lower(),
                    html=self.test_html
                )
                
                if idle1 == idle2:
                    self.log_success(
                        test_name,
                        f"大小写不敏感匹配正常 ({first_char.character}/{first_char.costume})"
                    )
                else:
                    self.log_failure(
                        test_name,
                        "大小写不敏感匹配失败"
                    )
            else:
                self.log_failure(test_name, "没有可用的测试数据")
        except Exception as e:
            self.log_failure(test_name, str(e))
    
    def test_get_by_id(self):
        """测试根据ID获取数据"""
        test_name = "测试6: 根据ID获取数据"
        if not self.test_html:
            self.log_failure(test_name, "没有可用的HTML内容")
            return
        
        try:
            rows = self.scraper.parse_rows(self.test_html)
            # 找到第一个有ID的角色
            char_with_id = None
            for row in rows:
                if row.char_id:
                    char_with_id = row
                    break
            
            if not char_with_id:
                self.log_failure(test_name, "没有找到带ID的角色数据")
                return
            
            # 测试get_idle_by_id
            idle = self.scraper.get_idle_by_id(char_with_id.char_id, html=self.test_html)
            if idle == char_with_id.idle or str(idle) == str(char_with_id.idle):
                self.log_success(
                    f"{test_name} - get_idle_by_id",
                    f"ID: {char_with_id.char_id}, Idle: {idle}"
                )
            else:
                self.log_failure(
                    f"{test_name} - get_idle_by_id",
                    f"返回值不匹配: 期望 {char_with_id.idle}, 得到 {idle}"
                )
            
            # 测试get_cutscene_by_id
            cutscene = self.scraper.get_cutscene_by_id(char_with_id.char_id, html=self.test_html)
            if cutscene == char_with_id.cutscene or str(cutscene) == str(char_with_id.cutscene):
                self.log_success(
                    f"{test_name} - get_cutscene_by_id",
                    f"ID: {char_with_id.char_id}, Cutscene: {cutscene}"
                )
            else:
                self.log_failure(
                    f"{test_name} - get_cutscene_by_id",
                    f"返回值不匹配: 期望 {char_with_id.cutscene}, 得到 {cutscene}"
                )
            
            # 测试get_character_by_id
            char_data = self.scraper.get_character_by_id(char_with_id.char_id, html=self.test_html)
            if char_data and char_data.char_id == char_with_id.char_id:
                self.log_success(
                    f"{test_name} - get_character_by_id",
                    f"成功获取完整数据: {char_data.character}/{char_data.costume}"
                )
            else:
                self.log_failure(
                    f"{test_name} - get_character_by_id",
                    "未能正确获取角色数据"
                )
                
        except Exception as e:
            self.log_failure(test_name, str(e))
    
    def test_search_characters(self):
        """测试搜索角色功能"""
        test_name = "测试7: 搜索角色"
        if not self.test_html:
            self.log_failure(test_name, "没有可用的HTML内容")
            return
        
        try:
            rows = self.scraper.parse_rows(self.test_html)
            if not rows:
                self.log_failure(test_name, "没有可用的测试数据")
                return
            
            # 搜索第一个角色
            first_char_name = rows[0].character
            matches = self.scraper.search_characters(first_char_name, html=self.test_html)
            
            if matches:
                self.log_success(
                    test_name,
                    f"找到 {len(matches)} 个 '{first_char_name}' 的服装变体"
                )
                # 显示前3个匹配项
                for i, match in enumerate(matches[:3], 1):
                    print(f"       └─ {i}. {match.costume} (Idle: {match.idle}, Cutscene: {match.cutscene})")
            else:
                self.log_failure(test_name, f"未找到 '{first_char_name}' 的任何数据")
                
        except Exception as e:
            self.log_failure(test_name, str(e))
    
    def test_get_all_data(self):
        """测试获取所有数据"""
        test_name = "测试8: 获取所有数据"
        if not self.test_html:
            self.log_failure(test_name, "没有可用的HTML内容")
            return
        
        try:
            all_data = self.scraper.get_all_data(html=self.test_html)
            if all_data and len(all_data) > 10:  # 期望至少有10条数据
                # 统计信息
                unique_characters = len(set(d.character for d in all_data))
                chars_with_id = sum(1 for d in all_data if d.char_id)
                
                self.log_success(
                    test_name,
                    f"获取 {len(all_data)} 条数据，{unique_characters} 个独立角色，{chars_with_id} 条有ID"
                )
            else:
                self.log_failure(test_name, f"数据量不足: 仅获取到 {len(all_data) if all_data else 0} 条")
        except Exception as e:
            self.log_failure(test_name, str(e))
    
    def test_error_handling(self):
        """测试错误处理"""
        test_name = "测试9: 错误处理"
        
        # 测试不存在的角色
        try:
            self.scraper.get_idle("不存在的角色XYZ123", "不存在的服装ABC456", html=self.test_html or "<html></html>")
            self.log_failure(f"{test_name} - 不存在的角色", "应该抛出LookupError")
        except LookupError:
            self.log_success(f"{test_name} - 不存在的角色", "正确抛出LookupError")
        except Exception as e:
            self.log_failure(f"{test_name} - 不存在的角色", f"抛出了错误的异常类型: {type(e).__name__}")
        
        # 测试空HTML
        try:
            self.scraper.get_idle("任意角色", "任意服装", html="<html></html>")
            self.log_failure(f"{test_name} - 空HTML", "应该抛出ValueError")
        except (ValueError, LookupError):
            self.log_success(f"{test_name} - 空HTML", "正确处理空HTML")
        except Exception as e:
            self.log_failure(f"{test_name} - 空HTML", f"抛出了错误的异常类型: {type(e).__name__}")
        
        # 测试不存在的ID
        try:
            self.scraper.get_idle_by_id("char999999", html=self.test_html or "<html></html>")
            self.log_failure(f"{test_name} - 不存在的ID", "应该抛出LookupError")
        except LookupError:
            self.log_success(f"{test_name} - 不存在的ID", "正确抛出LookupError")
        except Exception as e:
            self.log_failure(f"{test_name} - 不存在的ID", f"抛出了错误的异常类型: {type(e).__name__}")
    
    def test_data_integrity(self):
        """测试数据完整性"""
        test_name = "测试10: 数据完整性检查"
        if not self.test_html:
            self.log_failure(test_name, "没有可用的HTML内容")
            return
        
        try:
            all_data = self.scraper.get_all_data(html=self.test_html)
            
            # 检查必需字段
            missing_character = sum(1 for d in all_data if not d.character)
            missing_costume = sum(1 for d in all_data if not d.costume)
            missing_idle = sum(1 for d in all_data if not d.idle)
            
            issues = []
            if missing_character > 0:
                issues.append(f"{missing_character}条缺少角色名")
            if missing_costume > 0:
                issues.append(f"{missing_costume}条缺少服装名")
            if missing_idle > 0:
                issues.append(f"{missing_idle}条缺少idle值")
            
            if not issues:
                self.log_success(test_name, "所有数据完整性检查通过")
            else:
                self.log_failure(test_name, "；".join(issues))
            
            # 检查idle值格式
            invalid_idle = []
            for d in all_data[:50]:  # 检查前50条
                if d.idle and not (isinstance(d.idle, int) or d.idle.isdigit() or d.idle.strip() == ""):
                    invalid_idle.append(f"{d.character}/{d.costume}: '{d.idle}'")
            
            if not invalid_idle:
                self.log_success(f"{test_name} - Idle格式", "Idle值格式正确")
            else:
                self.log_failure(
                    f"{test_name} - Idle格式",
                    f"发现 {len(invalid_idle)} 个格式异常的idle值"
                )
                
        except Exception as e:
            self.log_failure(test_name, str(e))
    
    def test_specific_char_id(self):
        """测试通过指定ID获取完整角色信息"""
        test_name = "测试11: 获取指定ID(char004101)的完整信息"
        if not self.test_html:
            self.log_failure(test_name, "没有可用的HTML内容")
            return
        
        target_id = "char004101"
        
        try:
            # 获取完整角色数据
            char_data = self.scraper.get_character_by_id(target_id, html=self.test_html)
            
            if char_data:
                self.log_success(
                    test_name,
                    f"成功获取角色信息"
                )
                # 显示详细信息
                print(f"       └─ 角色名称: {char_data.character}")
                print(f"       └─ 服装名称: {char_data.costume}")
                print(f"       └─ 角色ID: {char_data.char_id}")
                print(f"       └─ Idle值: {char_data.idle}")
                print(f"       └─ Cutscene值: {char_data.cutscene}")
                
                # 验证数据完整性
                if not char_data.character:
                    self.log_failure(f"{test_name} - 数据验证", "角色名称为空")
                elif not char_data.costume:
                    self.log_failure(f"{test_name} - 数据验证", "服装名称为空")
                elif not char_data.idle:
                    self.log_failure(f"{test_name} - 数据验证", "Idle值为空")
                else:
                    self.log_success(f"{test_name} - 数据验证", "所有必需字段都存在")
                
                # 测试通过ID获取idle和cutscene的方法
                try:
                    idle_by_id = self.scraper.get_idle_by_id(target_id, html=self.test_html)
                    cutscene_by_id = self.scraper.get_cutscene_by_id(target_id, html=self.test_html)
                    
                    # 验证返回值一致性
                    if str(idle_by_id) == str(char_data.idle):
                        self.log_success(f"{test_name} - Idle一致性", "get_idle_by_id返回值匹配")
                    else:
                        self.log_failure(
                            f"{test_name} - Idle一致性",
                            f"不匹配: get_idle_by_id={idle_by_id}, char_data.idle={char_data.idle}"
                        )
                    
                    if str(cutscene_by_id) == str(char_data.cutscene):
                        self.log_success(f"{test_name} - Cutscene一致性", "get_cutscene_by_id返回值匹配")
                    else:
                        self.log_failure(
                            f"{test_name} - Cutscene一致性",
                            f"不匹配: get_cutscene_by_id={cutscene_by_id}, char_data.cutscene={char_data.cutscene}"
                        )
                        
                except Exception as e:
                    self.log_failure(f"{test_name} - 一致性测试", str(e))
                    
            else:
                self.log_failure(test_name, f"未找到ID为 '{target_id}' 的角色")
                
                # 尝试查找相似的ID
                all_data = self.scraper.get_all_data(html=self.test_html)
                similar_ids = [d.char_id for d in all_data if d.char_id and 'char004' in d.char_id]
                if similar_ids:
                    print(f"       └─ 提示: 找到相似的ID: {similar_ids[:5]}")
                    
        except LookupError as e:
            self.log_failure(test_name, f"未找到指定ID: {e}")
            
            # 显示可用的ID示例
            try:
                all_data = self.scraper.get_all_data(html=self.test_html)
                available_ids = [d.char_id for d in all_data if d.char_id and 'char004' in d.char_id]
                if available_ids:
                    print(f"       └─ 可用的char004xxx ID: {available_ids[:10]}")
            except Exception:
                pass
                
        except Exception as e:
            self.log_failure(test_name, str(e))
    
    def print_summary(self):
        """打印测试结果摘要"""
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print()
        print("=" * 70)
        print("测试结果摘要")
        print("=" * 70)
        print(f"总测试数: {total}")
        print(f"✅ 通过: {self.passed}")
        print(f"❌ 失败: {self.failed}")
        print(f"通过率: {pass_rate:.1f}%")
        print("=" * 70)
        
        if self.failed == 0:
            print("🎉 所有测试通过！")
        else:
            print("⚠️  部分测试失败，请检查上面的详细信息")


def main():
    """主函数"""
    tester = TestCharacterScraper()
    tester.run_all_tests()
    
    # 返回退出码（用于CI/CD）
    return 0 if tester.failed == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
