#!/usr/bin/env python3
"""
测试控制台程序的核心功能
"""

import sys
import os
from pathlib import Path

# 添加src目录到路径
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_config_management():
    """测试配置管理功能"""
    print("🧪 测试配置管理功能")
    print("=" * 50)
    
    from config import get_config
    
    config = get_config()
    
    # 测试获取工作目录
    workspaces = config.get_mod_workspaces()
    print(f"当前工作目录: {workspaces}")
    
    # 测试添加工作目录
    test_workspace = "test_workspace"
    if config.add_mod_workspace(test_workspace):
        print(f"✅ 成功添加工作目录: {test_workspace}")
    else:
        print(f"⚠️  工作目录已存在: {test_workspace}")
    
    # 测试检查工作目录存在性
    exists = config.workspace_exists(test_workspace)
    print(f"工作目录 '{test_workspace}' 存在: {exists}")
    
    # 显示更新后的工作目录
    updated_workspaces = config.get_mod_workspaces()
    print(f"更新后工作目录: {updated_workspaces}")
    
    print("✅ 配置管理功能测试完成\n")

def test_console_initialization():
    """测试控制台初始化"""
    print("🧪 测试控制台初始化")
    print("=" * 50)
    
    from console import BD2Console
    
    console = BD2Console()
    
    # 测试工作目录验证
    valid_names = ["test_dir", "laoxin的mod", "bikini_mods", "测试目录", "author_name_123"]
    invalid_names = ["", "test/dir", "test\\dir", "<invalid>", "*test*", "a" * 100]
    
    print("有效工作目录名称测试:")
    for name in valid_names:
        is_valid = console._validate_workspace_name(name)
        print(f"  '{name}': {'✅' if is_valid else '❌'}")
    
    print("\n无效工作目录名称测试:")
    for name in invalid_names:
        is_valid = console._validate_workspace_name(name)
        print(f"  '{name}': {'✅' if is_valid else '❌'}")
    
    print("✅ 控制台初始化测试完成\n")

def test_workspace_file_counting():
    """测试工作目录文件统计"""
    print("🧪 测试工作目录文件统计")
    print("=" * 50)
    
    from console import BD2Console
    
    console = BD2Console()
    
    # 测试现有工作目录
    project_root = Path(__file__).parent
    test_paths = [
        project_root / "replace",
        project_root / "laoxin的mod",
        project_root / "test_author_mod",
        project_root / "nonexistent_dir"
    ]
    
    for path in test_paths:
        count = console._count_mod_files(path)
        exists = "存在" if path.exists() else "不存在"
        print(f"  {path.name}: {count} 个文件 ({exists})")
    
    print("✅ 文件统计测试完成\n")

def main():
    """主函数"""
    print("🚀 BD2控制台功能测试")
    print("=" * 60)
    
    try:
        test_config_management()
        test_console_initialization()
        test_workspace_file_counting()
        
        print("🎉 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
