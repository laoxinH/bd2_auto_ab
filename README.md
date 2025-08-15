

<div align="center">

# 🎮 BD2 Auto AB - Brown Dust 2 自动化MOD打包系统

![BD2 Logo](https://img.shields.io/badge/BD2-MOD%20Manager-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**🚀 一站式Brown Dust 2MOD制作工具**

*自动化角色目录管理 | Unity资源替换 | 智能MOD打包*
### 🌟 如果这个项目对您有帮助，请给我们一个Star或者[💕 赞助我们](#-支持我们)！

[![GitHub stars](https://img.shields.io/github/stars/laoxinH/bd2_auto_ab?style=social)](https://github.com/laoxinH/bd2_auto_ab)
[![GitHub forks](https://img.shields.io/github/forks/laoxinH/bd2_auto_ab?style=social)](https://github.com/laoxinH/bd2_auto_ab)

**🎮 让BD2 MOD制作变得简单而高效！**

*Made with ❤️ by MOD实验室*
</div>

## 📋 目录

- [🎯 项目简介](#-项目简介)
- [✨ 主要特性](#-主要特性)
- [🚀 快速开始](#-快速开始)
- [💻 安装配置](#-安装配置)
- [🎮 使用指南](#-使用指南)
- [⚙️ 配置管理](#️-配置管理)
- [📁 项目结构](#-项目结构)
- [🔧 开发者指南](#-开发者指南)
- [❓ 常见问题](#-常见问题)
- [🤝 贡献指南](#-贡献指南)
- [🌐 相关链接](#-相关链接)

## 🎯 项目简介

BD2 Auto AB 是一个专为《Brown Dust 2》游戏开发的自动化资源管理系统。它提供了从角色数据获取、目录结构初始化到MOD资源打包的完整自动化流程，让MOD制作变得简单高效。

### 🌟 核心价值
- **自动化流程**: 一键完成从数据获取到MOD打包的全过程
- **智能管理**: 自动检测更新、版本管理、智能缓存
- **用户友好**: 统一控制台界面，无需复杂命令行操作
- **高度可配置**: 灵活的配置系统，支持代理、超时等个性化设置

## ✨ 主要特性

### 🏗️ **自动化目录管理**
- 📊 **智能数据获取**: 自动从Google Sheets获取最新角色数据
- 📁 **目录结构生成**: 自动创建标准化的MOD目录结构
- 🔄 **增量更新**: 智能跳过已存在目录，支持增量初始化
- 🎭 **多服装支持**: 完整支持角色的所有服装变体

### 🎨 **Unity资源处理**
- 🔧 **Unity Bundle支持**: 完整的Unity AssetBundle读取和修改
- 🖼️ **纹理替换**: 支持各种图像格式的纹理替换
- ⚡ **高性能处理**: 多线程并行处理，大幅提升处理速度
- 💾 **智能缓存**: 避免重复下载和处理相同资源

### 📦 **智能MOD打包**
- 🔍 **变更检测**: 自动检测MOD文件变更，仅处理更新内容
- 📋 **详细报告**: 生成完整的MOD打包报告和使用说明
- 🔒 **版本管理**: 自动版本控制和冲突检测
- 📄 **README生成**: 自动生成MOD安装和使用文档

### 🎛️ **统一控制台**
- 🖥️ **友好界面**: 直观的菜单驱动界面，无需记忆命令
- 🔧 **依赖检查**: 一键检查Python环境和依赖库状态
- ⚙️ **配置管理**: 可视化配置修改和管理工具
- 📊 **实时反馈**: 详细的进度显示和状态信息

### 🌐 **网络和配置**
- 🔄 **代理支持**: 完整的HTTP/HTTPS代理配置支持
- ⏱️ **智能重试**: 网络超时和重试机制
- 📝 **配置热更新**: 运行时配置修改，无需重启
- 🛡️ **错误恢复**: 完善的错误处理和恢复机制

## 🚀 快速开始

### 📥 一键启动
```bash
# 克隆项目
git clone https://github.com/laoxinH/bd2_auto_ab.git
cd bd2_auto_ab

# 安装依赖
pip install -r requirements.txt

# 启动控制台
cd src
python console.py
```

### 🎯 三步完成MOD制作
1. **📋 选择 0** - 执行目录初始化，获取最新角色数据
2. **📁 放置MOD文件** - 将您的MOD文件放入对应角色目录
3. **📦 选择 1** - 执行MOD打包，自动生成可分发的MOD包

## 💻 安装配置

### 🔧 系统要求
- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10/11, macOS, Linux
- **内存**: 建议 4GB 以上
- **磁盘空间**: 至少 2GB 可用空间
- **网络**: 稳定的互联网连接

### 📦 依赖安装

#### 方法一：自动安装（推荐）
```bash
pip install -r requirements.txt
```

#### 方法二：手动安装
```bash
pip install requests>=2.31.0
pip install beautifulsoup4>=4.12.0
pip install lxml>=4.9.0
pip install tqdm>=4.65.0
pip install UnityPy>=1.20.0
pip install Pillow>=10.0.0
pip install blackboxprotobuf>=1.0.0
```

#### 方法三：使用国内镜像
```bash
# 清华大学镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 阿里云镜像源
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### ✅ 环境验证
```bash
# 使用内置依赖检查工具
cd src
python console.py
# 选择选项 2 进行依赖环境检查
```

## 🎮 使用指南

### 🖥️ 统一控制台界面

启动控制台后，您将看到以下主菜单：

```
┌─────────────────────────────────────────────────────────────┐
│                          主菜单                             │
├─────────────────────────────────────────────────────────────┤
│  0️⃣  执行目录初始化 - 从谷歌表格创建角色目录结构           │
│  1️⃣  执行MOD打包   - 检测更新并打包替换资源               │
│  2️⃣  依赖环境检查 - 检查Python依赖库安装状态              │
│  3️⃣  显示帮助信息 - 查看详细使用说明                      │
│  4️⃣  退出程序     - 安全退出控制台                        │
└─────────────────────────────────────────────────────────────┘
```

### 📁 目录结构说明

系统会自动创建以下标准化目录结构：

```
bd2_auto_ab/
├── replace/                    # MOD替换文件目录
│   ├── {角色名}/
│   │   ├── {服装名}/
│   │   │   ├── CUTSCENE/      # 技能动画资源
│   │   │   │   └── {MOD名}/   # 您的MOD文件夹
│   │   │   └── IDLE/          # 立绘动画资源
│   │   │       └── {MOD名}/   # 您的MOD文件夹
├── sourcedata/                 # 原始游戏资源缓存
├── targetdata/                 # 处理后的MOD输出
├── config.json                 # 配置文件
└── requirements.txt           # 依赖清单
```

### � 完整工作流程

#### 第一次使用
1. **🚀 启动系统**
   ```bash
   cd src
   python console.py
   ```

2. **📋 初始化目录**
   - 选择选项 `0`
   - 系统自动从Google Sheets获取角色数据
   - 创建完整的目录结构

3. **🔧 检查环境**
   - 选择选项 `2`
   - 验证所有依赖库安装状态
   - 确保系统配置正确

#### 日常MOD制作
1. **📁 放置MOD文件**
   - 将您的MOD文件放入对应的角色/服装/类型目录
   - 建议创建以MOD名称命名的子文件夹

2. **📦 执行打包**
   - 选择选项 `1`
   - 系统自动检测文件变更
   - 下载原始资源并执行替换
   - 生成完整的MOD包和说明文档

3. **📊 查看结果**
   - 在 `targetdata/` 目录查看生成的MOD包
   - 阅读自动生成的README文件
   - 按说明安装和测试MOD

## ⚙️ 配置管理

### 🔧 配置工具

系统提供专门的配置管理工具：

```bash
cd src
python config_manager.py
```

### ⚡ 关键配置项

#### 🌐 网络配置
```json
{
  "network": {
    "proxy_enabled": true,              // 是否启用代理
    "proxy_http": "http://127.0.0.1:7890",  // HTTP代理地址
    "proxy_https": "http://127.0.0.1:7890", // HTTPS代理地址
    "request_timeout": 15.0,            // 请求超时时间(秒)
    "download_timeout": 300.0,          // 下载超时时间(秒)
    "max_retries": 3,                   // 最大重试次数
    "retry_delay": 1.0                  // 重试延迟(秒)
  }
}
```

#### 📝 日志配置
```json
{
  "log": {
    "level": "INFO",                    // 日志级别
    "file_enabled": false,              // 是否保存到文件
    "file_path": "logs/bd2_auto_ab.log" // 日志文件路径
  }
}
```

### 🔄 配置修改方式

1. **🖥️ 可视化管理**（推荐）
   ```bash
   python config_manager.py
   ```

2. **✏️ 直接编辑**
   - 编辑项目根目录的 `config.json` 文件
   - 确保JSON格式正确

3. **⚡ 热更新**
   - 配置修改后立即生效
   - 无需重启程序

## 📁 项目结构

```
bd2_auto_ab/
├── 📁 src/                     # 源代码目录
│   ├── 🖥️ console.py           # 统一控制台主程序
│   ├── ⚙️ config.py            # 配置管理系统
│   ├── 🔧 config_manager.py    # 配置管理工具
│   ├── 📋 initialize_directories.py  # 目录初始化器
│   ├── 📦 main_program.py      # MOD打包主程序
│   ├── 🌐 BD2CDNAPI.py         # BD2 CDN API接口
│   ├── 📥 BD2DataDownloader.py # 数据下载器
│   ├── 🎨 UnityResourceProcessor.py  # Unity资源处理器
│   ├── 🕷️ CharacterScraper.py   # 角色数据抓取器
│   └── 🔍 check_dependencies.py # 依赖检查工具
├── 📁 replace/                 # MOD替换文件目录
├── 📁 sourcedata/              # 原始游戏资源缓存
├── 📁 targetdata/              # 处理后的MOD输出
├── 📄 config.json              # 主配置文件
├── 📄 requirements.txt         # Python依赖清单
├── 📄 data.json                # 项目数据缓存
└── 📄 README.md                # 项目说明文档
```

## 🔧 开发者指南

### 🏗️ 核心模块架构

#### 1. **统一配置系统** (`config.py`)
- 🔄 单例模式配置管理
- 📁 JSON配置文件自动生成
- ⚡ 热重载配置支持

#### 2. **Unity资源处理** (`UnityResourceProcessor.py`)
- 🎨 Unity Bundle文件解析
- 🖼️ 纹理格式转换和替换
- 💾 资源缓存和优化

#### 3. **网络模块** (`BD2CDNAPI.py`, `BD2DataDownloader.py`)
- 🌐 BD2 CDN API封装
- 📥 多线程下载支持
- 🔄 自动重试和错误恢复

#### 4. **数据处理** (`CharacterScraper.py`)
- 🕷️ Google Sheets数据抓取
- 📊 角色和服装数据解析
- 💾 本地缓存管理

### 🧪 测试和调试

#### 运行测试套件
```bash
# 依赖检查测试
python check_dependencies.py

# 控制台功能测试
python ../test_console_features.py

# 配置系统测试
python config_manager.py
```

#### 调试模式
```bash
# 启用详细日志
# 修改config.json中的log.level为"DEBUG"
```

### 🔌 扩展开发

#### 添加新的配置选项
1. 在 `config.py` 中定义新的数据类
2. 更新默认配置生成逻辑
3. 在 `config_manager.py` 中添加管理界面

#### 添加新的资源处理器
1. 继承 `UnityResourceProcessor` 基类
2. 实现特定的资源处理逻辑
3. 注册到主处理流程中

## ❓ 常见问题

### 🔧 环境和安装问题

<details>
<summary><strong>Q: Python版本不兼容怎么办？</strong></summary>

**A:** 系统要求Python 3.8或更高版本。请升级Python或使用pyenv管理多版本：

```bash
# 检查Python版本
python --version

# 使用pyenv安装新版本
pyenv install 3.11.0
pyenv local 3.11.0
```
</details>

<details>
<summary><strong>Q: 依赖安装失败怎么解决？</strong></summary>

**A:** 常见解决方案：

```bash
# 1. 更新pip
python -m pip install --upgrade pip

# 2. 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 3. 逐个安装依赖
pip install requests beautifulsoup4 lxml tqdm UnityPy Pillow blackboxprotobuf
```
</details>

### 🌐 网络和代理问题

<details>
<summary><strong>Q: 无法访问Google Sheets怎么办？</strong></summary>

**A:** 配置代理或使用本地缓存：

1. **配置代理**:
   ```bash
   cd src
   python config_manager.py
   # 启用代理并设置正确的代理地址
   ```

2. **使用本地缓存**:
   - 系统会自动缓存已获取的数据
   - 离线模式下可以使用之前的缓存
</details>

<details>
<summary><strong>Q: 下载游戏资源时超时怎么办？</strong></summary>

**A:** 调整超时配置：

```json
{
  "network": {
    "download_timeout": 600.0,  // 增加到10分钟
    "max_retries": 5,           // 增加重试次数
    "retry_delay": 2.0          // 增加重试间隔
  }
}
```
</details>

### 🎮 MOD制作问题

<details>
<summary><strong>Q: MOD文件应该放在哪里？</strong></summary>

**A:** 标准目录结构：

```
replace/
├── {角色名}/
│   ├── {服装名}/
│   │   ├── CUTSCENE/
│   │   │   └── {您的MOD名}/    # 技能动画MOD
│   │   │       ├── texture.png
│   │   │       └── ...
│   │   └── IDLE/
│   │       └── {您的MOD名}/    # 立绘动画MOD
│   │           ├── texture.png
│   │           └── ...
```
</details>

<details>
<summary><strong>Q: 支持哪些图像格式？</strong></summary>

**A:** 支持的格式：
- **输入格式**: PNG, JPG, JPEG, BMP, TGA
- **输出格式**: Unity RGBA32 纹理格式
- **建议**: 使用PNG格式以保持透明度
</details>

### 🐛 错误排查

<details>
<summary><strong>Q: "配置文件损坏"错误？</strong></summary>

**A:** 重置配置文件：

```bash
# 删除损坏的配置文件
rm config.json

# 重新运行程序，自动生成新配置
python console.py
```
</details>

<details>
<summary><strong>Q: Unity资源处理失败？</strong></summary>

**A:** 检查和解决：

1. **确认文件格式**: 只支持Unity Bundle格式
2. **检查文件权限**: 确保有读写权限
3. **清理缓存**: 删除 `sourcedata/` 目录重新下载
4. **查看详细日志**: 设置日志级别为DEBUG
</details>

## 🤝 贡献指南

### 💡 如何贡献

我们欢迎各种形式的贡献：

1. **🐛 报告Bug**: 在Issues中详细描述问题
2. **✨ 功能建议**: 提出新功能想法和改进建议
3. **📝 文档改进**: 完善文档、添加示例
4. **💻 代码贡献**: 修复Bug、实现新功能

### 📋 开发流程

1. **🍴 Fork项目**
2. **🌿 创建特性分支**: `git checkout -b feature/amazing-feature`
3. **💻 提交更改**: `git commit -m 'Add amazing feature'`
4. **📤 推送分支**: `git push origin feature/amazing-feature`
5. **🔄 创建Pull Request**

### 📏 代码规范

- 🐍 遵循PEP 8 Python代码规范
- 📝 添加详细的文档字符串
- 🧪 为新功能编写测试
- 📊 保持代码覆盖率

### 🏷️ 版本规范

项目遵循语义化版本控制：
- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

---

## 🌐 相关链接

### 🏠 官方网站
- **🔗 MOD实验室官方网站**: [https://www.modwu.com/](https://www.modwu.com/)
  - 更多MOD资源和教程
  - 社区交流和技术支持
  - 最新的游戏MOD资讯

### 💝 支持我们

如果这个项目对您有帮助，您可以通过以下方式支持我们的持续开发：

- **🎯 实验室官方捐赠渠道**: [https://www.modwu.com/?p=549](https://www.modwu.com/?p=549)
- **⚡ 爱发电捐赠渠道**: [https://afdian.com/a/oldnew/plan](https://afdian.com/a/oldnew/plan)

您的支持将帮助我们：
- 🔧 持续改进和优化工具
- 📚 完善文档和教程
- 🆕 开发更多实用功能
- 🎮 支持更多游戏MOD制作

---

🎉 **享受自动化的BD2 MOD资源管理体验！**
