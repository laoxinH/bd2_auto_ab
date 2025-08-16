# BD2 MOD Packer v2.0 - 项目结构说明

## 📁 项目架构概览

BD2 MOD Packer v2.0 采用全新的工作区集中化架构和模块化设计，以下是完整的项目结构：

```
bd2_auto_ab/                        # 项目根目录
├── 📄 main.py                      # 🎯 主入口程序（新）
├── 📄 setup.py                     # 📦 Python包安装脚本（新）
├── 📄 requirements.txt             # 📋 依赖列表
├── 📄 config.json                  # ⚙️ 配置文件
├── 📄 data.json                    # � 项目数据缓存
├── 📄 README.md                    # 📖 项目说明
├── 📄 LICENSE                      # 📜 许可证
│
├── 📦 bd2_mod_packer/              # 🔧 主程序包（重构）
│   ├── 📄 __init__.py              # 包初始化
│   │
│   ├── 📁 core/                    # 🔧 核心业务逻辑
│   │   ├── 📄 __init__.py
│   │   ├── 📄 manager.py           # 🎯 MOD管理器主类
│   │   ├── 📄 data_downloader.py   # 📥 数据下载器
│   │   ├── 📄 resource_manager.py  # 📦 资源管理器
│   │   ├── 📄 unity_processor.py   # 🎨 Unity资源处理器
│   │   └── 📄 main_program.py      # 📜 兼容性主程序
│   │
│   ├── 📁 ui/                      # 🖥️ 用户界面
│   │   ├── 📄 __init__.py
│   │   └── 📄 console.py           # 🎛️ 控制台界面
│   │
│   ├── 📁 config/                  # ⚙️ 配置管理
│   │   ├── 📄 __init__.py
│   │   └── 📄 settings.py          # ⚙️ 配置设置和管理
│   │
│   ├── 📁 utils/                   # 🛠️ 工具函数
│   │   ├── 📄 __init__.py
│   │   └── 📄 dependency_checker.py # 🔍 依赖检查器
│   │
│   └── 📁 api/                     # 🌐 API接口
│       ├── 📄 __init__.py
│       ├── 📄 cdn_api.py           # 🌐 BD2 CDN API
│       └── 📄 character_scraper.py  # 📊 角色数据爬虫
│
├── 📁 workspace/                   # 🗂️ 工作区目录（新架构核心）
│   ├── 📁 mod_projects/            # 📦 MOD项目工作区
│   │   ├── 📁 replace/             # 默认工作区
│   │   │   ├── � {角色名}/
│   │   │   │   ├── � {服装名}/
│   │   │   │   │   ├── 📁 CUTSCENE/ # 技能动画资源
│   │   │   │   │   └── 📁 IDLE/     # 立绘动画资源
│   │   │   │   └── ...
│   │   │   └── ...
│   │   ├── � laoxin的mod/         # 示例：多作者工作区
│   │   └── 📁 {自定义工作区}/      # 用户自定义工作区
│   │
│   ├── 📁 sourcedata/              # 📥 原始游戏资源缓存
│   │   ├── � common-skeleton-data_assets_all.bundle/
│   │   ├── 📁 common-skeleton-data-group*_assets_all.bundle/
│   │   └── ...
│   │
│   └── 📁 targetdata/              # 📤 处理后的MOD输出
│       ├── 📁 replace/
│       │   └── 📁 {时间戳}/        # 按时间归档的输出
│       └── 📁 {工作区名}/
│           └── 📁 {时间戳}/
│
├── 📁 scripts/                     # 📜 脚本文件
│   └── 📄 {辅助脚本}.py
│
├── 📁 tests/                       # 🧪 测试文件
│   ├── 📄 test_console.py          # 控制台测试
│   ├── 📄 test_new_features.py     # 新功能测试
│   └── ...
│
└── 📁 docs/                        # 📚 文档目录
    ├── 📄 QUICKSTART.md            # 快速开始指南
    ├── 📄 CONFIG_README.md         # 配置系统说明
    ├── 📄 CONTRIBUTING.md          # 贡献指南
    ├── 📄 CHANGELOG.md             # 更新日志
    ├── 📄 PROJECT_OVERVIEW.md      # 项目概览
    ├── 📄 PROJECT_STRUCTURE.md     # 本文档
    ├── 📄 UPGRADE_GUIDE.md         # 升级指南
    └── 📄 使用说明_多作者支持.md    # 多作者支持说明
```

## 🔧 架构说明

### 🎯 核心变化

#### 1. **工作区集中化** (`workspace/`)
- **统一管理**: 所有MOD相关数据都在 `workspace/` 目录下
- **多项目支持**: `mod_projects/` 支持多个独立工作区
- **清晰分离**: 源数据、项目文件、输出结果分别管理

#### 2. **模块化重构** (`bd2_mod_packer/`)
- **业务逻辑分离**: core 目录包含所有核心业务逻辑
- **界面分离**: ui 目录专门处理用户交互
- **配置统一**: config 目录统一管理所有配置
- **工具集中**: utils 目录包含通用工具函数
- **API抽象**: api 目录处理外部API调用

#### 3. **Python包化** (`setup.py`)
- **标准安装**: 支持 `pip install` 安装
- **命令行工具**: 安装后可直接使用 `bd2ab` 命令
- **依赖管理**: 自动处理依赖关系

### 📦 模块详解

#### Core 模块 (`bd2_mod_packer/core/`)

- **manager.py**: MOD管理器主类
  - 工作区创建、删除、管理
  - MOD打包和处理流程协调
  - 统一的错误处理和日志记录

- **resource_manager.py**: 资源管理器
  - Unity AssetBundle处理
  - 文件变更检测和版本管理
  - 批量资源处理和优化

- **data_downloader.py**: 数据下载器
  - BD2 CDN 资源下载
  - 网络请求和重试机制
  - 进度显示和错误恢复

- **unity_processor.py**: Unity资源处理器
  - 纹理格式转换
  - AssetBundle 修改和重打包
  - 资源优化和压缩

#### UI 模块 (`bd2_mod_packer/ui/`)

- **console.py**: 统一控制台界面
  - 菜单驱动的用户交互
  - 美观的ASCII艺术界面
  - 智能错误处理和用户反馈

#### Config 模块 (`bd2_mod_packer/config/`)

- **settings.py**: 配置管理系统
  - JSON配置文件自动生成和加载
  - 工作区路径管理
  - 网络代理和超时配置
  - 配置热重载支持

#### Utils 模块 (`bd2_mod_packer/utils/`)

- **dependency_checker.py**: 依赖检查器
  - Python环境检测
  - 依赖库版本验证
  - 自动修复建议

#### API 模块 (`bd2_mod_packer/api/`)

- **cdn_api.py**: BD2 CDN API接口
  - 游戏资源URL构建
  - API请求封装
  - 错误处理和重试

- **character_scraper.py**: 角色数据爬虫
  - Google Sheets数据获取
  - 角色信息解析
  - 数据缓存和更新

### 🗂️ 工作区架构

#### mod_projects/ 结构
```
mod_projects/
├── replace/                    # 默认工作区
│   ├── Celia/                 # 角色目录
│   │   ├── Default/           # 默认服装
│   │   │   ├── CUTSCENE/      # 技能动画
│   │   │   └── IDLE/          # 立绘动画
│   │   └── Custom_Outfit/     # 自定义服装
│   │       ├── CUTSCENE/
│   │       └── IDLE/
│   └── Morpeah/               # 其他角色
│       └── ...
├── 作者A的MOD/                # 多作者支持
└── 作者B的MOD/
```

#### targetdata/ 输出结构
```
targetdata/
├── replace/
│   ├── 2025-08-16(143022)/    # 时间戳目录
│   │   ├── 角色1/
│   │   └── 角色2/
│   └── 2025-08-16(150430)/    # 另一次打包
└── 作者A的MOD/
    └── 2025-08-16(160000)/
```

## 🔄 与v1.x的对比

| 特性 | v1.x | v2.0 |
|------|------|------|
| 架构 | 单文件脚本 | 模块化Python包 |
| 工作区管理 | 单一replace目录 | 多工作区支持 |
| 配置管理 | 硬编码 | JSON配置文件 |
| 安装方式 | 手动依赖 | pip install |
| 界面 | 命令行参数 | 控制台 + CLI |
| 项目组织 | 平铺文件 | 标准Python包结构 |
| 多作者支持 | 不支持 | 原生支持 |

## 🚀 使用方式

### 开发模式
```bash
# 直接运行
python main.py

# 命令行模式
python main.py --workspace replace
python main.py --list
```

### 安装模式
```bash
# 安装为Python包
pip install -e .

# 使用命令
bd2-mod-manager
bd2ab
```

这种新架构使得项目更加专业化、模块化，同时保持了向后兼容性和用户友好性。
│   └── 📄 test_workspace_management.py # 工作区管理测试
│
├── 📁 docs/                        # 📚 文档目录
│   ├── 📄 CHANGELOG.md             # 更新日志
│   ├── 📄 CONFIG_README.md         # 配置说明
│   ├── 📄 CONTRIBUTING.md          # 贡献指南
│   ├── 📄 PROJECT_OVERVIEW.md      # 项目概览
│   ├── 📄 QUICKSTART.md            # 快速开始
│   └── 📄 使用说明_多作者支持.md    # 多作者支持说明
│
├── 📁 scripts/                     # 📝 脚本文件目录
│
├── 📁 workspaces/                  # 🏗️ MOD工作区目录
│   ├── 📁 replace/                 # 默认工作区
│   └── 📁 laoxin的mod/             # 用户自定义工作区
│
├── 📁 sourcedata/                  # 📊 源数据缓存
├── 📁 targetdata/                  # 🎯 目标数据输出
└── 📁 venv2/                       # 🐍 虚拟环境
```

## 🔧 核心模块说明

### 📦 bd2_mod_manager - 主包

整个项目的核心包，采用模块化设计，便于维护和扩展。

#### 🔧 core/ - 核心业务逻辑

| 文件 | 说明 | 主要功能 |
|------|------|----------|
| `manager.py` | MOD管理器主类 | 统一的工作区管理接口 |
| `data_downloader.py` | 数据下载器 | 从BD2 CDN下载游戏数据 |
| `resource_manager.py` | 资源管理器 | Unity资源文件管理 |
| `unity_processor.py` | Unity处理器 | Unity资源解析和替换 |
| `workspace_initializer.py` | 工作区初始化器 | 创建MOD工作区目录结构 |

#### 🖥️ ui/ - 用户界面

| 文件 | 说明 | 主要功能 |
|------|------|----------|
| `console.py` | 控制台界面 | 交互式菜单和用户输入处理 |

#### ⚙️ config/ - 配置管理

| 文件 | 说明 | 主要功能 |
|------|------|----------|
| `settings.py` | 配置设置 | 配置文件读写、默认配置管理 |

#### 🛠️ utils/ - 工具函数

| 文件 | 说明 | 主要功能 |
|------|------|----------|
| `dependency_checker.py` | 依赖检查器 | 检查Python依赖库安装状态 |

#### 🌐 api/ - API接口

| 文件 | 说明 | 主要功能 |
|------|------|----------|
| `cdn_api.py` | CDN API | BD2 CDN接口封装 |
| `character_scraper.py` | 角色爬虫 | 从谷歌表格获取角色数据 |

## 🎯 入口点说明

### 📄 main.py - 统一入口

新版本的统一入口程序，支持：

- **控制台模式**: `python main.py`
- **命令行模式**: `python main.py --workspace <name>`
- **功能调用**: `python main.py --list`, `--cleanup`, `--check`

### 📜 src/ - 兼容性支持

保留旧版本的文件结构，确保向后兼容：

- `main_program.py`: 旧版主程序，MOD打包核心逻辑
- `config_manager.py`: 旧版配置管理器

## 🏗️ 工作区结构

每个MOD工作区都遵循标准的目录结构：

```
工作区名/
├── 角色名1/
│   ├── 服装名1/
│   │   ├── CUTSCENE/           # 技能动画资源
│   │   │   └── MOD文件
│   │   └── IDLE/               # 立绘动画资源
│   │       └── MOD文件
│   └── 服装名2/
│       ├── CUTSCENE/
│       └── IDLE/
└── 角色名2/
    └── ...
```

## 📊 数据流程

### 1. 初始化流程
```
用户输入工作区名 → 配置保存 → 获取角色数据 → 创建目录结构
```

### 2. MOD打包流程
```
选择工作区 → 扫描MOD文件 → 下载原始资源 → Unity资源替换 → 生成输出
```

### 3. 配置管理流程
```
读取config.json → 解析配置 → 验证设置 → 应用配置
```

## 🔄 版本兼容性

### v2.0 新特性
- ✅ 模块化架构
- ✅ 统一入口程序
- ✅ 增强的工作区管理
- ✅ 命令行支持
- ✅ 改进的MOD统计

### 向后兼容
- ✅ 保留原有配置文件格式
- ✅ 支持旧版工作区结构
- ✅ 兼容现有MOD文件

## 🛠️ 开发指南

### 添加新功能
1. 在对应模块中添加功能代码
2. 更新`__init__.py`导入
3. 在`main.py`中添加命令行支持
4. 在`console.py`中添加菜单选项

### 修改配置
1. 在`settings.py`中添加配置项
2. 更新默认配置
3. 处理配置向后兼容

### 添加测试
1. 在`tests/`目录中添加测试文件
2. 使用标准的unittest框架
3. 确保测试覆盖新功能

## 📈 未来规划

### 短期目标
- [ ] GUI界面开发
- [ ] 更多MOD类型支持
- [ ] 自动更新功能

### 长期目标
- [ ] 插件系统
- [ ] 云端同步
- [ ] 社区MOD库

---

*此文档描述BD2 Auto AB v2.0的项目结构，如有疑问请参考其他文档或提交Issue。*
