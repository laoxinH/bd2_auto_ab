#!/usr/bin/env python3
"""
Character Scraper 快速测试脚本

这是一个简化版的测试脚本，用于快速验证 CharacterScraper 的基本功能。
适合在开发过程中快速检查功能是否正常。

运行方式:
    python tests/quick_test_scraper.py
    
    # 或者测试特定角色
    python tests/quick_test_scraper.py "Lathel" "Homunculus"
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from bd2_mod_packer.api.character_scraper import CharacterScraper


def print_separator():
    print("-" * 60)


def quick_test(character=None, costume=None):
    """快速测试功能"""
    print("=" * 60)
    print("Character Scraper 快速测试")
    print("=" * 60)
    
    scraper = CharacterScraper()
    
    try:
        print("\n📥 正在获取数据...")
        html = scraper.fetch_html()
        print(f"✅ 成功获取 {len(html):,} 字节的HTML内容")
        
        print("\n📊 解析角色数据...")
        all_data = scraper.get_all_data(html=html)
        unique_chars = len(set(d.character for d in all_data))
        print(f"✅ 解析成功: {len(all_data)} 条数据，{unique_chars} 个角色")
        
        # 如果指定了角色和服装，测试查询
        if character and costume:
            print_separator()
            print(f"\n🔍 查询: {character} / {costume}")
            
            try:
                idle = scraper.get_idle(character, costume, html=html)
                cutscene = scraper.get_cutscene(character, costume, html=html)
                
                print(f"✅ Idle值: {idle}")
                print(f"✅ Cutscene值: {cutscene}")
                
            except LookupError as e:
                print(f"❌ 未找到匹配: {e}")
                
                # 尝试搜索相似的角色
                print(f"\n🔍 搜索相似角色...")
                matches = scraper.search_characters(character, html=html)
                if matches:
                    print(f"找到 {len(matches)} 个匹配的服装:")
                    for i, match in enumerate(matches[:5], 1):
                        print(f"  {i}. {match.costume}")
                        print(f"     └─ Idle: {match.idle}")
                        print(f"     └─ Cutscene: {match.cutscene}")
        else:
            # 显示示例数据
            print_separator()
            print("\n📝 数据示例 (前5条):")
            for i, data in enumerate(all_data[:5], 1):
                print(f"\n{i}. {data.character} - {data.costume}")
                print(f"   └─ ID: {data.char_id}")
                print(f"   └─ Idle: {data.idle}")
                print(f"   └─ Cutscene: {data.cutscene}")
        
        # 测试ID查找功能
        print_separator()
        print("\n🔑 测试ID查找功能...")
        
        # 找一个有ID的角色
        test_char = next((d for d in all_data if d.char_id), None)
        if test_char:
            try:
                idle_by_id = scraper.get_idle_by_id(test_char.char_id, html=html)
                char_data = scraper.get_character_by_id(test_char.char_id, html=html)
                
                print(f"✅ ID查找测试成功")
                print(f"   测试ID: {test_char.char_id}")
                print(f"   角色: {char_data.character}")
                print(f"   服装: {char_data.costume}")
                print(f"   Idle: {idle_by_id}")
            except Exception as e:
                print(f"❌ ID查找失败: {e}")
        
        print_separator()
        print("\n✅ 所有快速测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    # 从命令行参数获取角色和服装
    character = sys.argv[1] if len(sys.argv) > 1 else None
    costume = sys.argv[2] if len(sys.argv) > 2 else None
    
    exit_code = quick_test(character, costume)
    sys.exit(exit_code)
