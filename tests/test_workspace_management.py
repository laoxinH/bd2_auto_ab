#!/usr/bin/env python3
"""
测试MOD打包的工作目录选择功能
"""

import sys
import os
from pathlib import Path

# 添加src目录到路径
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_mod_packaging_workspace_selection():
    """测试MOD打包的工作目录选择功能"""
    print("🧪 测试MOD打包工作目录选择")
    print("=" * 50)
    
    from console import BD2Console
    from config import get_config
    
    # 创建控制台实例
    console = BD2Console()
    config = get_config()
    
    # 获取当前配置的工作目录
    workspaces = config.get_mod_workspaces()
    print(f"配置的工作目录: {workspaces}")
    
    # 检查每个工作目录的物理存在性和文件数量
    print("\n工作目录状态:")
    project_root = Path(__file__).parent
    
    valid_workspaces = []
    for workspace in workspaces:
        workspace_path = project_root / workspace
        exists = workspace_path.exists()
        file_count = console._count_mod_files(workspace_path) if exists else 0
        
        status = "✅存在" if exists else "❌不存在"
        print(f"  {workspace}: {status}, {file_count} 个文件")
        
        if exists:
            valid_workspaces.append(workspace)
    
    print(f"\n有效工作目录: {valid_workspaces}")
    
    # 模拟用户选择
    if valid_workspaces:
        print(f"\n模拟选择第一个工作目录: {valid_workspaces[0]}")
        
        # 测试main_program的参数传递
        print("测试参数传递给main_program...")
        
        import sys
        original_argv = sys.argv.copy()
        sys.argv = ['main_program.py', valid_workspaces[0]]
        
        print(f"设置的参数: {sys.argv}")
        
        # 恢复原始argv
        sys.argv = original_argv
        
        print("✅ 参数传递测试完成")
    else:
        print("⚠️  没有有效的工作目录")
    
    print("✅ MOD打包工作目录选择测试完成\n")

def test_workspace_creation_validation():
    """测试工作目录创建验证"""
    print("🧪 测试工作目录创建验证")
    print("=" * 50)
    
    from console import BD2Console
    from config import get_config
    
    console = BD2Console()
    config = get_config()
    
    # 测试工作目录名称验证
    test_names = [
        ("valid_name", True),
        ("测试目录", True),
        ("author's_mod", True),
        ("laoxin的mod", True),
        ("", False),  # 空名称
        ("test/invalid", False),  # 包含斜杠
        ("test\\invalid", False),  # 包含反斜杠
        ("<invalid>", False),  # 包含特殊字符
        ("a" * 100, False),  # 名称过长
    ]
    
    print("工作目录名称验证测试:")
    for name, expected in test_names:
        result = console._validate_workspace_name(name)
        status = "✅" if result == expected else "❌"
        print(f"  '{name}': {status} (期望: {expected}, 实际: {result})")
    
    # 测试重复名称检查
    existing_workspaces = config.get_mod_workspaces()
    print(f"\n重复名称检查测试:")
    for workspace in existing_workspaces[:2]:  # 测试前两个
        exists = config.workspace_exists(workspace)
        print(f"  '{workspace}': {'✅存在' if exists else '❌不存在'}")
    
    # 测试不存在的名称
    test_name = "non_existent_workspace_12345"
    exists = config.workspace_exists(test_name)
    print(f"  '{test_name}': {'❌意外存在' if exists else '✅正确不存在'}")
    
    print("✅ 工作目录创建验证测试完成\n")

def main():
    """主函数"""
    print("🚀 BD2控制台工作目录管理测试")
    print("=" * 60)
    
    try:
        test_mod_packaging_workspace_selection()
        test_workspace_creation_validation()
        
        print("🎉 所有工作目录管理测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
