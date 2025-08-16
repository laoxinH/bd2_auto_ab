# 📜 Scripts 目录使用说明

这个目录用于存放打包完成后自动执行的脚本。

## 🚀 功能特性

- **自动调用**: MOD打包成功完成后，系统会自动遍历此目录并执行所有脚本
- **多语言支持**: 支持Python、批处理、Shell、PowerShell等多种脚本类型
- **参数传递**: 脚本会接收打包结果信息作为参数
- **智能跳过**: 如果没有执行实际的打包任务（如"无需更新"），则不会调用脚本

## 📋 支持的脚本类型

| 扩展名 | 脚本类型 | 执行方式 |
|--------|----------|----------|
| `.py` | Python脚本 | `python script.py` |
| `.bat`, `.cmd` | Windows批处理 | `script.bat` |
| `.sh` | Shell脚本 | `bash script.sh` |
| `.ps1` | PowerShell脚本 | `powershell -File script.ps1` |
| `.exe` | 可执行文件 | `script.exe` |

## 📦 参数格式

每个脚本都会收到以下参数：

1. **结果文件路径** (字符串): JSON格式的临时文件路径，包含详细的打包信息
2. **工作区名称** (字符串): 执行打包的工作区名称
3. **MOD数量** (整数): 工作区中的MOD数量

### JSON结果文件格式

```json
{
  "package_time": "2025-08-16 13:30:30",
  "workspace_name": "replace",
  "mod_count": 6,
  "mod_list": ["Celia", "Eleaneer", "Elise", "Morpeah", "Venaka", "Ventana"]
}
```

## 🎯 示例脚本

### Python脚本示例

```python
#!/usr/bin/env python3
import sys
import json

# 接收参数
result_file = sys.argv[1]
workspace_name = sys.argv[2] 
mod_count = int(sys.argv[3])

# 读取详细信息
with open(result_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"打包完成: {workspace_name}, 共{mod_count}个MOD")
for mod in data['mod_list']:
    print(f"  - {mod}")
```

### 批处理脚本示例

```batch
@echo off
REM %1 = 结果文件路径
REM %2 = 工作区名称  
REM %3 = MOD数量

echo 打包完成通知
echo 工作区: %2
echo MOD数量: %3
echo 详细信息请查看: %1

REM 这里可以添加你的处理逻辑
REM 比如发送邮件、上传文件、清理临时文件等
```

## 📁 目录结构

```
scripts/
├── README.md                     # 本说明文件
├── example_post_package.py       # Python示例脚本
├── smart_notification.py         # 智能通知脚本
├── test_script.bat              # 批处理测试脚本
├── logs/                        # 脚本生成的日志目录
│   └── package_log_20250816.txt
└── stats/                       # 统计信息目录
    └── package_stats.jsonl
```

## ⚙️ 执行机制

1. **触发条件**: 只有在实际执行了MOD打包任务时才会调用脚本
2. **执行顺序**: 按文件名字母顺序依次执行
3. **错误处理**: 单个脚本失败不会影响其他脚本的执行
4. **超时保护**: 每个脚本最多执行5分钟，超时会被终止
5. **工作目录**: 脚本在scripts目录中执行

## 🔧 使用建议

### 脚本命名规范
- 使用有意义的名称，如 `01_backup.py`, `02_notification.bat`
- 数字前缀可以控制执行顺序
- 避免使用中文和特殊字符

### 最佳实践
- 在脚本中添加适当的错误处理
- 记录脚本执行日志以便调试
- 避免执行耗时过长的操作
- 测试脚本在不同情况下的表现

### 常见用例
- 📧 发送打包完成通知
- 💾 备份重要文件到云端
- 📊 记录打包统计信息
- 🧹 清理临时文件
- 🔄 触发其他系统的同步操作

## 🚨 注意事项

1. **权限问题**: 确保脚本有足够的执行权限
2. **路径问题**: 使用绝对路径避免路径错误
3. **编码问题**: Windows批处理建议使用GBK编码
4. **依赖问题**: 脚本可能依赖的外部工具要确保已安装
5. **安全问题**: 不要在脚本中包含敏感信息

## 🔍 调试技巧

- 查看主程序日志了解脚本是否被调用
- 在脚本中添加日志输出便于调试
- 可以手动执行脚本进行测试
- 使用`python main.py --workspace test`进行测试

## 📞 技术支持

如有问题，请参考主程序的日志输出或联系开发团队。
