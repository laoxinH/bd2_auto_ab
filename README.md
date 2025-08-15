# BD2自动化系统使用指南

## 🎯 系统概述

BD2自动化MOD打包系统是一个完整的《BD2》游戏资源管理解决方案，提供从角色目录初始化到MOD打包的全自动化流程。

## 📦 系统架构

### 核心组件
- **统一配置系统** (`config.py`) - 集中管理所有配置
- **配置管理器** (`config_manager.py`) - 可视化配置修改工具
- **统一控制台** (`console.py`) - 用户友好的主界面
- **目录初始化器** (`initialize_directories.py`) - 自动创建角色目录
- **MOD打包器** (`main_program.py`) - 资源替换和打包功能

## 🚀 快速开始

### 1. 启动统一控制台
```bash
cd src
python console.py
```

### 2. 选择功能
- **选项0**: 目录初始化 - 从谷歌表格获取角色数据并创建目录结构
- **选项1**: MOD打包 - 检测更新的资源并进行打包替换
- **选项2**: 显示帮助信息
- **选项3**: 退出程序

## ⚙️ 配置管理

### 配置文件位置
- 主配置文件: `config.json`
- 自动生成: 首次运行时自动创建默认配置

### 配置管理器
```bash
cd src
python config_manager.py
```

#### 可配置项目
1. **网络设置**
   - 代理启用/禁用
   - HTTP/HTTPS代理地址
   - 超时时间设置
   - 重试次数配置

2. **日志设置**
   - 日志级别
   - 输出格式
   - 文件记录选项

3. **API设置**
   - 谷歌表格URL
   - BD2基础URL
   - 用户代理字符串

4. **项目设置**
   - 项目名称和版本
   - Unity版本
   - 最大工作线程数

## 📁 目录结构

```
bd2_auto_ab/
├── config.json              # 配置文件
├── src/                     # 源代码目录
│   ├── config.py           # 配置系统
│   ├── config_manager.py   # 配置管理器
│   ├── console.py          # 统一控制台
│   ├── initialize_directories.py  # 目录初始化
│   ├── main_program.py             # MOD打包主程序
│   └── ...
├── sourcedata/             # 源数据目录
├── targetdata/             # 目标数据目录
└── replace/                # 替换文件目录
```

## 🔧 常见配置

### 代理设置
```json
{
  "network": {
    "proxy_enabled": true,
    "proxy_http": "http://192.168.1.220:7897",
    "proxy_https": "http://192.168.1.220:7897"
  }
}
```

### 禁用代理
```json
{
  "network": {
    "proxy_enabled": false
  }
}
```

### 日志配置
```json
{
  "log": {
    "level": "INFO",
    "file_enabled": true,
    "file_path": "logs/bd2_auto_ab.log"
  }
}
```

## 🎮 使用流程

### 第一次使用
1. 启动统一控制台: `python console.py`
2. 选择"0 - 执行目录初始化"
3. 等待从谷歌表格下载角色数据
4. 系统自动创建所有角色目录结构

### 日常使用
1. 将新的角色资源放入对应的`replace/角色名称/服装名称/MOD名称`目录，其中MOD名称目录需要自行建立
2. 启动统一控制台: `python console.py`
3. 选择"1 - 执行MOD打包"
4. 系统自动检测更新并打包

### 配置修改
1. 启动配置管理器: `python config_manager.py`
2. 根据菜单选择要修改的配置项
3. 修改完成后自动保存

## 🛠️ 高级功能

### 配置系统API
```python
from config import get_config

config = get_config()
proxies = config.get_proxies()
network_config = config.network
```

### 直接运行组件
```bash
# 仅目录初始化
python initialize_directories.py

# 仅MOD打包
python main_program.py

# 配置管理
python config_manager.py
```

## 🐛 故障排除

### 常见问题

1. **网络连接失败**
   - 检查代理设置是否正确
   - 尝试禁用代理后重试
   - 确认网络连接正常

2. **配置文件损坏**
   - 删除`config.json`文件
   - 重新运行程序自动生成默认配置

3. **目录权限问题**
   - 确保对工作目录有读写权限
   - 以管理员身份运行程序

### 错误日志
- 程序运行时会显示详细的错误信息
- 可以启用文件日志记录更多调试信息

## 📞 其他说明

如果遇到问题，请检查：
1. Python环境是否正确安装
2. 依赖包是否完整
3. 配置文件格式是否正确
4. 网络连接是否正常

---

🎉 **享受自动化的BD2 MOD资源管理体验！**
