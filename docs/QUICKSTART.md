# 🚀 BD2 MOD Packer v2.0 快速开始指南

欢迎使用BD2 MOD Packer v2.0！本指南将帮助您快速上手新架构的MOD制作工具。

## 📦 快速安装

### 方法一：直接使用（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/laoxinH/bd2_auto_ab.git
cd bd2_auto_ab

# 2. 安装依赖
pip install -r requirements.txt

# 3. 立即开始
python main.py
```

### 方法二：Python包安装

```bash
# 安装为Python包
pip install -e .

# 使用命令启动
bd2-mod-manager
```

## 🎯 5分钟上手

### 步骤 1: 启动程序

```bash
python main.py
```

您将看到欢迎界面和主菜单：

```
╔══════════════════════════════════════════════════════════════╗
║                    BD2 MOD packer v2.0                      ║
║               Brown Dust 2 自动化MOD打包系统                  ║
╚══════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────┐
│                          主菜单                             │
├─────────────────────────────────────────────────────────────┤
│  0️⃣  创建MOD工作目录 - 设置和初始化新的MOD工作环境          │
│  1️⃣  执行MOD打包     - 选择工作目录并打包替换资源          │
│  2️⃣  删除MOD工作目录 - 删除指定的MOD工作目录               │
│  3️⃣  清理空文件夹   - 清理工作目录中的空文件夹             │
│  4️⃣  依赖环境检查   - 检查Python依赖库安装状态             │
│  5️⃣  显示帮助信息   - 查看详细使用说明                     │
│  6️⃣  退出程序       - 安全退出控制台                       │
└─────────────────────────────────────────────────────────────┘
```

### 步骤 2: 创建工作区

选择选项 `0` 创建新的MOD工作目录：

```
请输入工作区名称: 我的第一个MOD
✅ 工作区创建成功！
```

### 步骤 3: 放置MOD文件

将您的MOD文件放入：
```
workspace/mod_projects/我的第一个MOD/
├── 角色名/
│   ├── 服装名/
│   │   ├── CUTSCENE/     # 技能动画MOD
│   │   └── IDLE/         # 立绘动画MOD
```

### 步骤 4: 打包MOD

选择选项 `1` 执行MOD打包：

```
📋 可用的MOD工作目录:
  1. 我的第一个MOD (发现 3 个MOD)
  2. replace (发现 6 个MOD)

请选择要打包的工作目录: 1
✅ MOD打包完成！
```

输出文件将保存在：
```
workspace/targetdata/我的第一个MOD/2025-08-16(143022)/
```

## 🔧 进阶使用

### 命令行模式

v2.0支持强大的命令行操作：

```bash
# 列出所有工作区
python main.py --list

# 直接打包指定工作区
python main.py --workspace "我的第一个MOD"

# 清理所有空文件夹
python main.py --cleanup

# 检查依赖环境
python main.py --check
```

### 多工作区管理

v2.0支持同时管理多个独立的MOD项目：

```bash
workspace/mod_projects/
├── 我的第一个MOD/        # 个人项目
├── 团队项目A/            # 协作项目
├── 实验性MOD/            # 测试项目
└── 发布版MOD/            # 正式版本
```

每个工作区完全独立，互不干扰！

### 配置自定义

编辑 `config.json` 文件自定义设置：

```json
{
  "network": {
    "proxy_enabled": true,
    "proxy_http": "http://your-proxy:port"
  },
  "project": {
    "max_workers": 8,
    "mod_workspaces": ["工作区1", "工作区2"]
  }
}
```

## 🎨 实战示例

### 示例：制作Celia角色MOD

1. **创建专用工作区**
   ```bash
   python main.py
   # 选择 0，输入 "Celia定制MOD"
   ```

2. **组织MOD文件**
   ```
   workspace/mod_projects/Celia定制MOD/
   └── Celia/
       └── Descendant of the Great Witch/
           ├── CUTSCENE/
           │   └── 我的技能动画MOD/
           └── IDLE/
               └── 我的立绘MOD/
   ```

3. **一键打包**
   ```bash
   python main.py --workspace "Celia定制MOD"
   ```

4. **查看结果**
   ```
   workspace/targetdata/Celia定制MOD/2025-08-16(150000)/
   ├── 角色文件夹/
   └── 处理日志.txt
   ```

## 🛠️ 故障排除

### 常见问题

**Q: 提示"No module named 'bd2_mod_packer'"**
```bash
# 确保在项目根目录运行
cd bd2_auto_ab
python main.py
```

**Q: 网络连接失败**
```bash
# 检查代理设置
python main.py --check
# 或编辑 config.json 中的网络配置
```

**Q: 工作区创建失败**
```bash
# 检查权限和磁盘空间
# 确保workspace目录可写
```

**Q: MOD文件找不到**
```bash
# 确认文件路径结构正确
# 参考: workspace/mod_projects/{工作区名}/{角色}/{服装}/{类型}/
```

### 获取帮助

- 📖 **详细文档**: [README.md](../README.md)
- 🏗️ **架构说明**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- 🔧 **配置指南**: [CONFIG_README.md](CONFIG_README.md)
- 🐛 **问题报告**: [GitHub Issues](https://github.com/laoxinH/bd2_auto_ab/issues)

## 🎯 下一步

现在您已经掌握了基础使用，可以：

1. **📚 深入学习**: 阅读完整的[README文档](../README.md)
2. **🔧 自定义配置**: 查看[配置说明](CONFIG_README.md)
3. **👥 参与社区**: 查看[贡献指南](CONTRIBUTING.md)
4. **🚀 探索高级功能**: 了解所有命令行选项和配置选项

---

**🎮 享受您的MOD制作之旅！**

如果遇到任何问题，请不要犹豫在GitHub上提出Issue，我们很乐意帮助您！
