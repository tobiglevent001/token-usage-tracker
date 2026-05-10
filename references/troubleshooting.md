# 故障排查指南 / Troubleshooting Guide

## 常见问题 / Common Issues

### 1. API 认证失败 / API Authentication Failed

**症状 / Symptoms**:
```
 ValueError: 缺少 API Key / Missing API key for deepseek
```

**原因 / Cause**:
- API Key 未设置或无效
- API Key not set or invalid

**解决 / Solution**:

```bash
# 检查环境变量 / Check environment variable
echo $DEEPSEEK_API_KEY

# 设置环境变量（Linux/Mac）/ Set environment variable (Linux/Mac)
export DEEPSEEK_API_KEY="your-api-key-here"

# 设置环境变量（Windows PowerShell）/ Set environment variable (Windows PowerShell)
$env:DEEPSEEK_API_KEY = "your-api-key-here"

# 永久设置（Windows）/ Permanent setting (Windows)
[System.Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "your-api-key-here", "User")
```

---

### 2. 浏览器抓取失败 / Browser Fetch Failed

**症状 / Symptoms**:
```
⚠️ 浏览器抓取尚未实现，返回模拟数据
⚠️ Browser fetch not yet implemented, returning mock data
```

**原因 / Cause**:
- `browser-use` skill 未安装
- 网站需要登录
- CSS 选择器失效

**解决 / Solution**:

1. **安装 browser-use skill**:
   ```bash
   # 使用 Skill 工具安装 / Install using Skill tool
   # 或在 skills 目录中手动安装 / Or manually install in skills directory
   ```

2. **手动登录后保存 cookies**:
   - 在 `config/auth.json` 中配置 cookie 文件路径
   - 使用 browser-use 登录并保存 session

3. **更新选择器 / Update selectors**:
   ```json
   {
     "selectors": {
       "total_tokens": "新的 CSS 选择器",
       "cost": "新的 CSS 选择器"
     }
   }
   ```

---

### 3. 报告生成失败 / Report Generation Failed

**症状 / Symptoms**:
```
FileNotFoundError: 数据文件不存在 / Data file not found
```

**原因 / Cause**:
- 数据文件不存在
- 使用模拟数据

**解决 / Solution**:

```bash
# 先抓取数据 / Fetch data first
python scripts/fetch_usage.py

# 查看输出目录 / Check output directory
ls -la output/

# 再生成报告 / Then generate report
python scripts/generate_report.py
```

---

### 4. 定时任务未触发 / Scheduled Task Not Triggered

**症状 / Symptoms**:
- 到达设定时间后未收到报告
- No report received at scheduled time

**原因 / Cause**:
- 定时任务未正确设置
- WorkBuddy 未运行

**解决 / Solution**:

1. **检查 automation 配置 / Check automation config**:
   ```bash
   # 查看当前自动化任务 / View current automations
   # 使用 automation_update 工具 / Use automation_update tool
   ```

2. **确保 WorkBuddy 在运行 / Ensure WorkBuddy is running**:
   - 定时任务需要 WorkBuddy 会话保持活跃
   - Scheduled tasks require active WorkBuddy session

3. **查看日志 / Check logs**:
   - 检查输出目录中的文件时间戳
   - Check file timestamps in output directory

---

### 5. 数据不准确 / Inaccurate Data

**症状 / Symptoms**:
- 报告中的数字与实际不符
- Numbers in report don't match actual usage

**原因 / Cause**:
- API 返回数据格式变化
- 统计口径不一致

**解决 / Solution**:

1. **检查原始数据 / Check raw data**:
   ```bash
   cat output/usage_data.json | python -m json.tool
   ```

2. **对比平台网页 / Compare with platform webpage**:
   - 登录平台官网查看实际用量
   - Login to platform website to check actual usage

3. **调整数据解析逻辑 / Adjust data parsing logic**:
   - 修改 `scripts/fetch_usage.py` 中的解析代码
   - Modify parsing code in `scripts/fetch_usage.py`

---

### 6. 中英文混合乱码 / Chinese-English Mixed Encoding Issue

**症状 / Symptoms**:
- 报告中中文显示为乱码
- Chinese characters displayed as garbled text in report

**原因 / Cause**:
- 文件编码不是 UTF-8
- File encoding is not UTF-8

**解决 / Solution**:

```bash
# 确保所有文件使用 UTF-8 编码 / Ensure all files use UTF-8 encoding
# 在 Python 中打开文件时指定 encoding / Specify encoding when opening files in Python
with open(file_path, "r", encoding="utf-8") as f:
    # ...
```

---

## 获取帮助 / Get Help

如果以上方法无法解决问题，请：

1. **查看完整日志 / Check full logs**:
   ```bash
   python scripts/fetch_usage.py 2>&1 | tee -a debug.log
   ```

2. **收集错误信息 / Collect error information**:
   - Python 版本 / Python version
   - 操作系统 / OS version
   - 完整的错误堆栈 / Full error stack trace

3. **提交 Issue / Submit Issue**:
   - 在 GitHub 仓库提交 issue
   - Submit issue on GitHub repository

---

*最后更新 / Last Updated: 2026-05-10*
