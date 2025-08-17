

<div align="center">

# 🎮 BD2 MOD Packer v2.0 - Brown Dust 2 自动化MOD管理系统

![BD2 Logo](https://img.shields.io/badge/BD2-MOD%20Manager-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Version](https://img.shields.io/badge/Version-2.0.0-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**🚀 全新架构的Brown Dust 2 MOD制作工具**

*工作区集中管理 | 模块化架构 | 命令行/GUI双界面 | 一键打包部署*

### 🌟 如果这个项目对您有帮助，请给我们一个Star或者[💕 赞助我们](#-支持我们)！

[![GitHub stars](https://img.shields.io/github/stars/laoxinH/bd2_auto_ab?style=social)](https://github.com/laoxinH/bd2_auto_ab)
[![GitHub forks](https://img.shields.io/github/forks/laoxinH/bd2_auto_ab?style=social)](https://github.com/laoxinH/bd2_auto_ab)

**🎮 让BD2 MOD制作变得专业而高效！**

*Made with ❤️ by BD2 MOD实验室*
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

BD2 MOD Packer v2.0 是专为《Brown Dust 2》游戏开发的新一代自动化MOD管理系统。基于全新的工作区集中化架构，提供了从MOD开发到打包部署的完整工作流程。

### 🚀 v2.0 重大更新

- **🏗️ 工作区集中化**: 全新的 `workspace/` 目录结构，统一管理所有MOD项目
- **📦 模块化重构**: 重新设计的 `bd2_mod_packer` 包架构，更好的代码组织
- **🖥️ 双界面支持**: 命令行界面 + 控制台界面，适应不同用户需求
- **⚙️ 统一配置**: 基于JSON的配置系统，所有设置集中管理
- **🔧 Python包化**: 支持 `pip install` 安装，更专业的分发方式

### 🌟 核心价值

- **专业化架构**: 采用现代Python项目标准架构，可维护性大大提升
- **工作区管理**: 支持多作者、多项目的工作区独立管理
- **智能处理**: 自动检测文件变更、智能缓存、版本管理
- **用户友好**: 统一的控制台界面和详细的错误提示

## ✨ 主要特性

### 🏗️ **自动化目录管理**
- 📊 **智能角色识别**: 从MOD文件名自动识别角色和服装信息
- 📁 **简化目录结构**: 新的三级目录结构：作者/类型/MOD名称
- 🔄 **增量更新**: 智能跳过已存在目录，支持增量初始化
- 🎭 **多格式支持**: 支持char*, illust_*, specialIllust*等多种ID格式

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
python main.py
```

### 🎯 三步完成MOD制作
1. **📋 选择 0** - 执行目录初始化，获取最新角色数据
2. **📁 放置MOD文件** - 将您的MOD文件放入对应角色目录
3. **📦 选择 1** - 执行MOD打包，自动生成可分发的MOD包

## 💻 安装配置

### 🔧 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10/11 (主要支持)
- **内存**: 建议 4GB 以上
- **存储**: 建议 2GB 以上空闲空间

### 📦 安装方式

#### 方法一：直接使用（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/laoxinH/bd2_auto_ab.git
cd bd2_auto_ab

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动程序
python main.py
```

### 🛠️ 环境配置

#### 代理配置

如果您处于需要代理的网络环境中，请修改 `config.json`：

```json
{
  "network": {
    "proxy_enabled": true,
    "proxy_http": "http://your-proxy:port",
    "proxy_https": "http://your-proxy:port"
  }
}
```

#### 依赖检查

程序提供了自动依赖检查功能：

```bash
python main.py --check
```
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

### 🖥️ 启动方式

#### 方法一：控制台界面（推荐新用户）

```bash
python main.py
```

#### 方法二：命令行模式（推荐高级用户）

```bash
# 列出所有工作区
python main.py --list

# 创建新的工作区
python main.py --create "我的MOD项目"

# 打包指定工作区
python main.py --workspace "我的MOD项目"

# 清理空文件夹
python main.py --cleanup

# 检查依赖环境
python main.py --check
```

### 📁 工作区结构说明

v2.0 采用全新的工作区集中化管理：

```
bd2_auto_ab/
├── workspace/                  # 🗂️ 工作区根目录
│   ├── mod_projects/           # 📦 MOD项目目录
│   │   ├── replace/            # 默认工作区
│   │   ├── laoxin的mod/        # 示例：多作者工作区
│   │   └── your_workspace/     # 您的自定义工作区
│   ├── sourcedata/             # 📥 原始游戏资源缓存
│   └── targetdata/             # 📤 处理后的MOD输出
├── bd2_mod_packer/             # 🔧 核心程序包
├── config.json                 # ⚙️ 配置文件
└── main.py                     # 🚀 程序入口
```

### 🎯 完整工作流程

#### 第一次使用

1. **🚀 启动程序**
   ```bash
   python main.py
   ```

2. **0️⃣ 创建工作区**
   - 选择菜单选项 "0" - 创建MOD工作目录
   - 输入工作区名称（如 "我的MOD"）  
   - 系统自动创建基础目录结构（IDLE/ 和 CUTSCENE/）

3. **📁 放置MOD文件**
   - 将您的MOD文件放入对应的工作区目录
   - 新结构：作者名/IDLE或CUTSCENE/MOD名称/
   - MOD文件名必须包含角色ID（如：char000101.atlas）

#### 日常MOD制作

1. **📁 管理MOD文件**
   - 在 `workspace/mod_projects/your_workspace/` 中组织您的MOD
   - 新结构：作者名/IDLE或CUTSCENE/MOD名称/
   - 支持多个作者、多种MOD类型的并行开发
   - MOD文件必须包含角色ID用于自动识别

2. **📦 一键打包**
   - 选择菜单选项 "1" - 执行MOD打包
   - 选择要打包的工作区
   - 系统自动识别角色信息并处理，输出到 `targetdata/`

3. **🧹 清理维护**
   - 定期使用选项 "3" 清理空文件夹
   - 保持工作区整洁

#### 命令行快速操作

对于熟练用户，可以直接使用命令行：

```bash
# 创建新工作区
python main.py --create "新项目名称"

# 列出所有工作区状态
python main.py --list

# 打包指定工作区
python main.py --workspace "项目名称"
```
   - 建议创建以MOD名称命名的子文件夹

2. **📦 执行打包**
   - 选择选项 `1`
   - 系统自动检测文件变更
   - 下载原始资源并执行替换
   - 生成完整的MOD包和说明文档

3. **📊 查看结果**
   - 在 `workspace/targetdata/` 目录查看生成的MOD包
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

BD2 MOD Packer v2.0 采用全新的工作区集中化架构：

```
bd2_auto_ab/                        # 项目根目录
├── � main.py                      # 🎯 统一程序入口
├── 📄 setup.py                     # 📦 Python包安装脚本
├── 📄 config.json                  # ⚙️ 统一配置文件
├── 📄 data.json                    # 📊 项目数据缓存
├── � requirements.txt             # 📋 依赖列表
│
├── 📦 bd2_mod_packer/              # 🔧 主程序包
│   ├── � core/                    # 核心业务逻辑
│   │   ├── � manager.py           # MOD管理器主类
│   │   ├── 📄 resource_manager.py  # 资源管理器
│   │   ├── � data_downloader.py   # 数据下载器
│   │   └── 📄 unity_processor.py   # Unity资源处理器
│   ├── � ui/                      # 用户界面
│   │   └── 📄 console.py           # 控制台界面
│   ├── 📁 config/                  # 配置管理
│   │   └── 📄 settings.py          # 配置设置
│   ├── 📁 utils/                   # 工具函数
│   │   └── � dependency_checker.py # 依赖检查器
│   └── 📁 api/                     # API接口
│       ├── 📄 cdn_api.py           # BD2 CDN API
│       └── 📄 character_scraper.py # 角色数据爬虫
│
├── 📁 workspace/                   # 🗂️ 工作区目录（v2.0核心）
│   ├── 📁 mod_projects/            # MOD项目工作区
│   │   ├── 📁 replace/             # 默认工作区
│   │   ├── 📁 laoxin的mod/         # 多作者工作区示例
│   │   └── 📁 {自定义工作区}/      # 用户自定义工作区
│   ├── 📁 sourcedata/              # 原始游戏资源缓存
│   └── 📁 targetdata/              # 处理后的MOD输出
│
├── � docs/                        # 📚 文档目录
│   ├── 📄 QUICKSTART.md            # 快速开始指南
│   ├── 📄 PROJECT_STRUCTURE.md     # 项目架构说明
│   ├── 📄 CONFIG_README.md         # 配置系统说明
│   ├── 📄 CHANGELOG.md             # 更新日志
│   └── 📄 PROJECT_OVERVIEW.md      # 项目概览
│
└── 📁 tests/                       # 🧪 测试文件
    ├── 📄 test_console.py          # 控制台测试
    └── 📄 test_new_features.py     # 新功能测试
```

### 🔧 v2.0架构亮点

- **🏗️ 工作区集中化**: workspace/ 统一管理所有MOD相关数据
- **📦 Python包化**: 标准Python包结构，支持pip安装
- **🔧 模块化设计**: 业务逻辑、界面、配置、工具清晰分离
- **🎯 统一入口**: main.py 提供一致的程序访问点
- **📊 多工作区支持**: 支持多个独立MOD项目并行开发

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
- � 基于ID的角色数据查找
- 📊 角色和服装数据解析  
- 💾 本地缓存管理
- 🏷️ 多种ID格式支持（char*, illust_*, specialIllust*等）

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
<summary><strong>Q: 角色ID识别失败怎么办？</strong></summary>

**A:** 检查MOD文件命名规范：

1. **文件名格式**:
   - 必须包含完整的角色ID：char000101, illust_dating001等
   - 支持的文件格式：.atlas, .modfile, .skel, .json
   - 避免在文件名中添加多余的字符

2. **支持的ID格式**:
   - char* 系列：char000101, char000102等
   - illust_* 系列：illust_dating001, illust_special002等  
   - specialIllust* 系列：specialIllust001, specialillust002等

3. **排查方法**:
   - 检查日志输出中的"提取到角色ID"信息
   - 确认文件名与预期ID格式匹配
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

**A:** 新的简化目录结构：

```
workspace/mod_projects/{工作目录名}/
├── {作者名1}/
│   ├── IDLE/                    # 立绘动画MOD
│   │   ├── {MOD名称1}/
│   │   │   ├── char000101.atlas      # 文件名包含角色ID
│   │   │   └── char000101.modfile
│   │   └── {MOD名称2}/
│   │       └── illust_dating001.atlas
│   └── CUTSCENE/                # 技能动画MOD
│       └── {MOD名称3}/
│           ├── char000102.skel
│           └── char000102.json
└── {作者名2}/
    └── IDLE/
        └── {MOD名称4}/
            └── specialIllust001.atlas

注意事项：
- MOD文件名必须包含角色ID (如: char000101, illust_dating001)
- 系统会从文件名自动识别角色和服装信息  
- 支持的文件格式: .atlas, .modfile, .skel, .json
- 支持的角色ID格式: char*, illust_*, specialIllust*, specialillust*
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
