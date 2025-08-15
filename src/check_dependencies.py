#!/usr/bin/env python3
"""
BD2项目依赖检查脚本
检查所有必需的第三方库是否正确安装
"""

import sys

def check_dependencies():
    """检查所有依赖"""
    print('Python版本:', sys.version)
    print()

    # 检查所有依赖
    dependencies = [
        ('requests', 'HTTP请求库'),
        ('bs4', 'HTML解析库 (beautifulsoup4)'),
        ('lxml', 'XML解析器'),
        ('tqdm', '进度条库'),
        ('UnityPy', 'Unity资源处理库'),
        ('PIL', '图像处理库 (Pillow)'),
        ('blackboxprotobuf', 'Protobuf解析库'),
    ]

    print('📦 依赖检查结果:')
    print('-' * 50)

    missing = []
    installed = []
    
    for module, desc in dependencies:
        try:
            if module == 'bs4':
                import bs4
                print(f'✅ {module:20} - {desc}')
                installed.append(module)
            elif module == 'PIL':
                from PIL import Image
                print(f'✅ {module:20} - {desc}')
                installed.append(module)
            else:
                __import__(module)
                print(f'✅ {module:20} - {desc}')
                installed.append(module)
        except ImportError as e:
            print(f'❌ {module:20} - {desc} (缺失: {e})')
            missing.append(module)

    print()
    print(f'📊 统计: {len(installed)}个已安装, {len(missing)}个缺失')
    
    if missing:
        print(f'⚠️ 缺失依赖: {", ".join(missing)}')
        print('请运行以下命令安装:')
        
        # 提供安装建议
        install_commands = {
            'requests': 'pip install requests>=2.31.0',
            'bs4': 'pip install beautifulsoup4>=4.12.0',
            'lxml': 'pip install lxml>=4.9.0',
            'tqdm': 'pip install tqdm>=4.65.0',
            'UnityPy': 'pip install UnityPy>=1.20.0',
            'PIL': 'pip install Pillow>=10.0.0',
            'blackboxprotobuf': 'pip install blackboxprotobuf>=1.0.0',
        }
        
        for dep in missing:
            if dep in install_commands:
                print(f'  {install_commands[dep]}')
        
        print('\n或者一次性安装所有依赖:')
        print('  pip install -r requirements.txt')
        return False
    else:
        print('🎉 所有依赖都已正确安装！')
        
        # 显示已安装版本
        print('\n📋 已安装版本:')
        print('-' * 30)
        
        try:
            import requests
            print(f'requests: {requests.__version__}')
        except:
            pass
            
        try:
            import bs4
            print(f'beautifulsoup4: {bs4.__version__}')
        except:
            pass
            
        try:
            import lxml
            print(f'lxml: {lxml.__version__}')
        except:
            pass
            
        try:
            import tqdm
            print(f'tqdm: {tqdm.__version__}')
        except:
            pass
            
        try:
            import UnityPy
            print(f'UnityPy: {UnityPy.__version__}')
        except:
            pass
            
        try:
            from PIL import Image
            import PIL
            print(f'Pillow: {PIL.__version__}')
        except:
            pass
            
        try:
            import blackboxprotobuf
            print(f'blackboxprotobuf: {blackboxprotobuf.__version__}')
        except:
            pass
        
        return True

if __name__ == "__main__":
    success = check_dependencies()
    sys.exit(0 if success else 1)
