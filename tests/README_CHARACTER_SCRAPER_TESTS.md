# Character Scraper 测试文档

## 📋 测试概览

这个文档描述了 `CharacterScraper` 类的测试套件，包括测试脚本、测试用例和使用方法。

## 🧪 测试脚本

### 1. 完整测试套件 (`test_character_scraper.py`)

全面的单元测试脚本，涵盖所有功能和边界情况。

**运行方式:**
```bash
python tests/test_character_scraper.py
```

**测试内容:**
- ✅ 网络连接和HTML获取
- ✅ HTML解析和数据提取
- ✅ Idle值查询
- ✅ Cutscene值查询
- ✅ 模糊匹配（大小写不敏感）
- ✅ ID查找功能
- ✅ 角色搜索功能
- ✅ 获取所有数据
- ✅ 错误处理
- ✅ 数据完整性检查

### 2. 快速测试脚本 (`quick_test_scraper.py`)

用于快速验证基本功能的简化脚本。

**运行方式:**
```bash
# 基本测试
python tests/quick_test_scraper.py

# 测试特定角色
python tests/quick_test_scraper.py "Lathel" "Homunculus"
```

## 📊 测试结果

### 最近测试结果

```
======================================================================
测试结果摘要
======================================================================
总测试数: 17
✅ 通过: 15
❌ 失败: 2
通过率: 88.2%
======================================================================
```

### 详细测试项

| 测试项 | 状态 | 说明 |
|-------|------|------|
| 测试1: 从网站获取HTML | ✅ PASS | 成功获取 1,040,151 字节 |
| 测试2: 解析HTML内容 | ✅ PASS | 解析 222 条角色数据 |
| 测试3: 获取idle值 | ✅ PASS | 成功查询多个角色 |
| 测试4: 获取cutscene值 | ✅ PASS | 成功查询多个角色 |
| 测试5: 模糊匹配 | ✅ PASS | 大小写不敏感匹配正常 |
| 测试6: 根据ID获取数据 | ✅ PASS | 三种ID查询方法都正常 |
| 测试7: 搜索角色 | ✅ PASS | 找到 7 个 Lathel 的服装变体 |
| 测试8: 获取所有数据 | ✅ PASS | 222 条数据，102 个角色 |
| 测试9: 错误处理 | ✅ PASS | 正确处理各种异常情况 |
| 测试10: 数据完整性 | ⚠️ PARTIAL | 部分数据缺少idle值 |

## 🔍 测试用例详解

### 用例1: 基本查询测试

```python
from bd2_mod_packer.api.character_scraper import CharacterScraper

scraper = CharacterScraper()

# 获取idle值
idle = scraper.get_idle("Lathel", "Homunculus")
print(f"Idle: {idle}")
# 输出: Idle: f919a627e69a0cec80b5db8bf61764ce

# 获取cutscene值
cutscene = scraper.get_cutscene("Lathel", "Homunculus")
print(f"Cutscene: {cutscene}")
# 输出: Cutscene: 195913fc7cf6887bec2a0aee49171a89
```

### 用例2: ID查找测试

```python
# 根据角色ID获取idle值
idle = scraper.get_idle_by_id("char000103")
print(f"Idle: {idle}")

# 根据角色ID获取完整数据
char_data = scraper.get_character_by_id("char000103")
print(f"角色: {char_data.character}")
print(f"服装: {char_data.costume}")
print(f"Idle: {char_data.idle}")
print(f"Cutscene: {char_data.cutscene}")
```

### 用例3: 模糊搜索测试

```python
# 搜索某个角色的所有服装
matches = scraper.search_characters("Lathel")
print(f"找到 {len(matches)} 个服装变体")

for match in matches:
    print(f"- {match.costume}")
    print(f"  ID: {match.char_id}")
    print(f"  Idle: {match.idle}")
    print(f"  Cutscene: {match.cutscene}")
```

### 用例4: 离线使用（本地HTML）

```python
# 从本地文件读取
with open("character_data.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 使用本地HTML查询
idle = scraper.get_idle("Lathel", "Homunculus", html=html_content)
cutscene = scraper.get_cutscene("Lathel", "Homunculus", html=html_content)
```

### 用例5: 错误处理测试

```python
try:
    # 查询不存在的角色
    idle = scraper.get_idle("不存在的角色", "不存在的服装")
except LookupError as e:
    print(f"未找到: {e}")
    # 输出错误信息和可用角色列表

try:
    # 查询不存在的ID
    idle = scraper.get_idle_by_id("char999999")
except LookupError as e:
    print(f"未找到ID: {e}")
```

## 🐛 已知问题

### 1. 部分数据缺少idle值

**现象:** 222条数据中有11条缺少idle值

**影响:** 这些角色无法通过 `get_idle()` 查询到有效值

**解决方案:** 
- 检查源网站数据是否完整
- 在代码中添加默认值处理

### 2. Idle值格式异常

**现象:** 部分idle值不是标准的MD5哈希格式

**影响:** 可能需要额外的格式验证

**解决方案:**
- 添加格式验证函数
- 支持多种格式的idle值

## 📝 编写新测试用例

如果需要添加新的测试用例，请按照以下模板：

```python
def test_new_feature(self):
    """测试新功能的描述"""
    test_name = "测试X: 新功能名称"
    
    if not self.test_html:
        self.log_failure(test_name, "没有可用的HTML内容")
        return
    
    try:
        # 测试代码
        result = self.scraper.new_method(...)
        
        if result == expected:
            self.log_success(test_name, "测试通过的说明")
        else:
            self.log_failure(test_name, "测试失败的原因")
            
    except Exception as e:
        self.log_failure(test_name, str(e))
```

## 🚀 持续集成

这些测试脚本可以集成到CI/CD流程中：

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python tests/test_character_scraper.py
```

## 📞 问题反馈

如果遇到测试失败或其他问题，请提供以下信息：

1. 测试脚本输出的完整日志
2. Python版本 (`python --version`)
3. 依赖包版本 (`pip list`)
4. 网络环境（是否使用代理）
5. 具体的测试用例和输入参数

## 📚 相关文档

- [Character Scraper API文档](../bd2_mod_packer/api/character_scraper.py)
- [项目使用说明](../docs/QUICKSTART.md)
- [项目结构](../docs/PROJECT_STRUCTURE.md)
