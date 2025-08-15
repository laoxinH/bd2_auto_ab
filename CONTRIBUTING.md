# 🤝 贡献指南 (CONTRIBUTING)

感谢您对BD2 Auto AB项目的兴趣！我们欢迎各种形式的贡献。

## 📋 目录

- [如何贡献](#如何贡献)
- [开发环境配置](#开发环境配置)
- [代码规范](#代码规范)
- [提交指南](#提交指南)
- [问题报告](#问题报告)
- [功能建议](#功能建议)

## 如何贡献

### 💡 贡献方式

1. **🐛 报告Bug**: 发现问题并提供详细信息
2. **✨ 功能建议**: 提出新功能想法
3. **📝 改进文档**: 完善文档、添加示例
4. **💻 代码贡献**: 修复Bug、实现新功能
5. **🧪 测试**: 帮助测试新版本
6. **🌍 翻译**: 帮助翻译界面和文档

### 🎯 优先级任务

当前急需帮助的领域：

- [ ] **GUI界面开发**: tkinter或其他GUI框架
- [ ] **性能优化**: 大文件处理优化
- [ ] **错误处理**: 更完善的异常处理
- [ ] **文档完善**: 用户手册和开发文档
- [ ] **测试用例**: 单元测试和集成测试

## 开发环境配置

### 🔧 环境要求

- **Python**: 3.8 或更高版本
- **Git**: 版本控制工具
- **IDE**: 推荐 PyCharm 或 VS Code

### 📦 环境搭建

1. **克隆项目**
   ```bash
   git clone https://github.com/laoxinH/bd2_auto_ab.git
   cd bd2_auto_ab
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行测试**
   ```bash
   cd src
   python check_dependencies.py
   python console.py
   ```

### 🛠️ 开发工具

推荐的开发工具和配置：

```bash
# 代码格式化
pip install black isort

# 代码检查
pip install flake8 pylint

# 类型检查
pip install mypy
```

## 代码规范

### 🐍 Python代码规范

1. **PEP 8**: 遵循Python官方代码规范
2. **类型注解**: 为函数参数和返回值添加类型注解
3. **文档字符串**: 为所有公共函数和类添加docstring
4. **命名规范**:
   - 变量和函数: `snake_case`
   - 类名: `PascalCase`
   - 常量: `UPPER_CASE`

### 📝 文档规范

```python
def process_unity_bundle(bundle_path: str, output_path: str) -> bool:
    """
    处理Unity Bundle文件
    
    Args:
        bundle_path (str): Bundle文件路径
        output_path (str): 输出目录路径
    
    Returns:
        bool: 处理是否成功
    
    Raises:
        FileNotFoundError: 文件不存在
        PermissionError: 没有文件权限
    
    Example:
        >>> success = process_unity_bundle("input.bundle", "output/")
        >>> print(f"处理结果: {success}")
    """
    pass
```

### 🧪 测试规范

```python
import unittest
from pathlib import Path

class TestUnityProcessor(unittest.TestCase):
    
    def setUp(self):
        """测试前的准备工作"""
        self.test_data_path = Path("test_data")
        self.test_data_path.mkdir(exist_ok=True)
    
    def test_process_bundle(self):
        """测试Bundle处理功能"""
        # Arrange
        bundle_path = self.test_data_path / "test.bundle"
        
        # Act
        result = process_unity_bundle(str(bundle_path), "output/")
        
        # Assert
        self.assertTrue(result)
    
    def tearDown(self):
        """测试后的清理工作"""
        pass
```

## 提交指南

### 📋 Git工作流程

1. **创建分支**
   ```bash
   git checkout -b feature/new-feature
   # 或
   git checkout -b fix/bug-description
   ```

2. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

3. **推送分支**
   ```bash
   git push origin feature/new-feature
   ```

4. **创建Pull Request**

### 📝 提交信息规范

使用[约定式提交](https://conventionalcommits.org/zh-hans/)格式：

```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

**提交类型**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 添加测试
- `chore`: 构建过程或辅助工具的变动

**示例**:
```
feat(console): 添加依赖检查功能

- 添加依赖库状态检查
- 提供安装建议
- 支持版本信息显示

Closes #123
```

### 🔍 代码审查

Pull Request会经过以下审查：

1. **自动检查**:
   - 代码格式检查
   - 单元测试运行
   - 依赖安全检查

2. **人工审查**:
   - 代码质量评估
   - 功能完整性检查
   - 文档完整性检查

## 问题报告

### 🐛 Bug报告模板

提交Bug时请包含以下信息：

```markdown
## Bug描述
简要描述遇到的问题

## 复现步骤
1. 执行操作A
2. 点击按钮B
3. 查看结果C

## 预期结果
描述应该发生什么

## 实际结果
描述实际发生了什么

## 环境信息
- 操作系统: Windows 10
- Python版本: 3.9.0
- 项目版本: 1.2.0

## 额外信息
- 错误日志
- 截图（如适用）
- 配置文件内容
```

### 🔍 问题分类

使用标签来分类问题：

- `bug`: 程序错误
- `enhancement`: 功能增强
- `documentation`: 文档相关
- `question`: 使用问题
- `help wanted`: 需要帮助
- `good first issue`: 适合新手

## 功能建议

### 💡 功能请求模板

```markdown
## 功能描述
详细描述建议的新功能

## 使用场景
说明什么情况下需要这个功能

## 解决方案
描述您认为可行的实现方式

## 替代方案
描述您考虑过的其他解决方案

## 额外背景
提供任何其他相关信息
```

### 🎯 功能优先级

我们会根据以下标准评估功能请求：

1. **用户价值**: 对用户的帮助程度
2. **实现复杂度**: 开发和维护成本
3. **兼容性**: 与现有功能的兼容性
4. **社区需求**: 社区反馈和支持程度

## 社区规范

### 🤝 行为准则

- **尊重他人**: 保持友善和专业
- **建设性讨论**: 提供有价值的反馈
- **耐心帮助**: 协助新手解决问题
- **保持开放**: 接受不同的观点和建议

### 🏆 贡献者认可

- **代码贡献者**: 在README中列出
- **文档贡献者**: 在文档中署名
- **Bug报告者**: 在修复日志中感谢
- **功能建议者**: 在更新日志中提及

## 发布流程

### 📦 版本发布

1. **版本规划**: 确定新版本功能
2. **代码冻结**: 停止新功能开发
3. **测试验证**: 全面测试新版本
4. **文档更新**: 更新README和CHANGELOG
5. **版本发布**: 创建GitHub Release

### 🏷️ 版本号规则

遵循[语义化版本控制](https://semver.org/lang/zh-CN/)：

- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正


### 💬 讨论渠道

- **GitHub Issues**: 问题报告和功能建议
- **GitHub Discussions**: 一般讨论和问答

### 📚 学习资源

- [Python官方文档](https://docs.python.org/zh-cn/3/)
- [UnityPy文档](https://unitypy.readthedocs.io/)
- [Git教程](https://git-scm.com/book/zh/v2)

---

再次感谢您的贡献！您的每一个改进都让BD2 Auto AB变得更好。

*让我们一起构建更好的BD2 MOD制作体验！* 🎮✨
