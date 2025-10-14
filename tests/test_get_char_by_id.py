#!/usr/bin/env python3
"""
测试通过指定角色ID获取完整信息的独立脚本

运行方式:
    python tests/test_get_char_by_id.py
    python tests/test_get_char_by_id.py char004101
    python tests/test_get_char_by_id.py char004101 char000103
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from bd2_mod_packer.api.character_scraper import CharacterScraper


def test_character_by_id(char_id: str):
    """测试通过ID获取角色信息"""
    print("=" * 70)
    print(f"测试角色ID: {char_id}")
    print("=" * 70)
    
    scraper = CharacterScraper()
    
    try:
        # 获取HTML数据
        print("\n📥 正在获取数据...")
        html = scraper.fetch_html()
        print(f"✅ 成功获取 {len(html):,} 字节的HTML内容")
        
        # 方法1: 使用 get_character_by_id 获取完整数据
        print(f"\n🔍 方法1: 使用 get_character_by_id('{char_id}')")
        char_data = scraper.get_character_by_id(char_id, html=html)
        
        if char_data:
            print("✅ 成功获取角色数据:")
            print(f"   ├─ 角色名称: {char_data.character}")
            print(f"   ├─ 服装名称: {char_data.costume}")
            print(f"   ├─ 角色ID: {char_data.char_id}")
            print(f"   ├─ Idle值: {char_data.idle}")
            print(f"   └─ Cutscene值: {char_data.cutscene}")
            
            # 方法2: 使用 get_idle_by_id
            print(f"\n🔍 方法2: 使用 get_idle_by_id('{char_id}')")
            idle_value = scraper.get_idle_by_id(char_id, html=html)
            print(f"✅ Idle值: {idle_value}")
            
            # 方法3: 使用 get_cutscene_by_id
            print(f"\n🔍 方法3: 使用 get_cutscene_by_id('{char_id}')")
            cutscene_value = scraper.get_cutscene_by_id(char_id, html=html)
            print(f"✅ Cutscene值: {cutscene_value}")
            
            # 验证一致性
            print("\n🔬 数据一致性验证:")
            idle_match = str(idle_value) == str(char_data.idle)
            cutscene_match = str(cutscene_value) == str(char_data.cutscene)
            
            if idle_match and cutscene_match:
                print("✅ 所有方法返回的数据一致")
            else:
                if not idle_match:
                    print(f"⚠️  Idle值不一致:")
                    print(f"   get_character_by_id: {char_data.idle}")
                    print(f"   get_idle_by_id: {idle_value}")
                if not cutscene_match:
                    print(f"⚠️  Cutscene值不一致:")
                    print(f"   get_character_by_id: {char_data.cutscene}")
                    print(f"   get_cutscene_by_id: {cutscene_value}")
            
            # 使用角色名和服装名查询（验证双向查询）
            print(f"\n🔄 反向验证: 使用角色名和服装名查询")
            try:
                idle_by_name = scraper.get_idle(char_data.character, char_data.costume, html=html)
                cutscene_by_name = scraper.get_cutscene(char_data.character, char_data.costume, html=html)
                
                if str(idle_by_name) == str(char_data.idle):
                    print(f"✅ 通过名称查询的Idle值匹配")
                else:
                    print(f"⚠️  通过名称查询的Idle值不匹配: {idle_by_name}")
                
                if str(cutscene_by_name) == str(char_data.cutscene):
                    print(f"✅ 通过名称查询的Cutscene值匹配")
                else:
                    print(f"⚠️  通过名称查询的Cutscene值不匹配: {cutscene_by_name}")
                    
            except Exception as e:
                print(f"⚠️  反向验证失败: {e}")
            
            print("\n" + "=" * 70)
            print("✅ 测试完成")
            print("=" * 70)
            return True
            
        else:
            print(f"❌ 未找到ID为 '{char_id}' 的角色")
            
            # 尝试搜索相似的ID
            all_data = scraper.get_all_data(html=html)
            prefix = char_id[:8] if len(char_id) >= 8 else char_id
            similar_ids = [d.char_id for d in all_data if d.char_id and d.char_id.startswith(prefix)]
            
            if similar_ids:
                print(f"\n💡 找到 {len(similar_ids)} 个相似的ID (前缀: {prefix}):")
                for i, sid in enumerate(similar_ids[:10], 1):
                    char = next((d for d in all_data if d.char_id == sid), None)
                    if char:
                        print(f"   {i}. {sid} - {char.character}/{char.costume}")
            
            return False
            
    except LookupError as e:
        print(f"❌ 未找到指定ID: {e}")
        return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    # 如果没有提供命令行参数，使用默认ID
    if len(sys.argv) > 1:
        char_ids = sys.argv[1:]
    else:
        char_ids = ["char004101"]  # 默认测试ID
    
    print("🧪 Brown Dust 2 - 通过ID获取角色信息测试")
    print()
    
    success_count = 0
    for char_id in char_ids:
        result = test_character_by_id(char_id)
        if result:
            success_count += 1
        print()
    
    # 显示总结
    if len(char_ids) > 1:
        print("=" * 70)
        print("测试总结")
        print("=" * 70)
        print(f"总测试数: {len(char_ids)}")
        print(f"✅ 成功: {success_count}")
        print(f"❌ 失败: {len(char_ids) - success_count}")
        print("=" * 70)
    
    return 0 if success_count == len(char_ids) else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
