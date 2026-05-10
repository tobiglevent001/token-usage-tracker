---
name: token-usage-tracker
description: "追踪多个 AI 平台的余额和用量，生成每日汇总报告。支持 DeepSeek、Kimi/Moonshot 等平台的余额查询，自动生成中英文双语报告。当用户问 (1) 查看 token 余额, (2) 生成余额日报, (3) 配置 API Key, (4) 添加新平台 时使用。"
version: "2.0"
author: "Senior Developer (高级开发工程师)"
license: "MIT"
metadata:
  tags: [token-tracking, balance-query, cost-monitoring, daily-report]
  languages: [zh, en]
---

# Token Usage Tracker / Token 余额追踪器

## 概述

本 skill 自动查询多个 AI 平台的账户余额，生成每日汇总报告。

**核心功能**：
- 📊 **余额查询** — 支持 DeepSeek、Kimi/Moonshot 等平台
- 📝 **日报生成** — 中英文双语报告
- ⏰ **历史趋势** — 自动保存历史数据，计算消耗趋势
- 🌐 **Web 配置界面** — 可视化配置 API Key

---

## 何时使用

使用本 skill 当您：

1. **查看余额** → "查看我的 token 余额"
2. **生成日报** → "生成 token 余额日报"
3. **配置平台** → "打开配置界面添加 API Key"
4. **查看趋势** → "我的 token 消耗趋势"

---

## 快速开始

### 方法一：直接运行脚本

```bash
cd C:\Users\leven\.workbuddy\skills\token-usage-tracker
python scripts/run.py
```

### 方法二：通过对话调用

直接说："帮我查看 token 余额"

---

## 已支持平台

| 平台 | 余额查询 | API Endpoint | 响应数据 |
|------|---------|-------------|---------|
| **DeepSeek** | ✅ | `GET /user/balance` | CNY 余额（总余额、赠送、充值） |
| **Kimi/Moonshot** | ✅ | `GET /v1/users/me/balance` | USD 余额（可用、代金券、现金） |
| **OpenAI** | ⚠️ 用量 | `GET /v1/organization/usage/completions` | 需要 Admin API Key |

---

## 配置 API Key

### 方法一：编辑 auth.json

编辑 `config/auth.json`：

```json
{
  "deepseek": "sk-你的deepseek-key",
  "moonshot": "sk-你的kimi-key"
}
```

### 方法二：通过 Web 界面

1. 启动配置服务器：
   ```bash
   python config/web_config.py
   ```

2. 打开浏览器访问：`http://localhost:8888`

3. 选择模型，输入 API Key，点击保存

---

## 运行参数

```bash
python scripts/run.py                          # 默认抓取 deepseek + moonshot
python scripts/run.py --platforms deepseek    # 只抓取 DeepSeek
python scripts/run.py --lang zh               # 只生成中文报告
python scripts/run.py --lang en               # 只生成英文报告
```

---

## 输出文件

运行后会在 `output/` 目录生成：

| 文件 | 内容 |
|------|------|
| `balance_data.json` | 本次抓取的余额数据 |
| `balance_history.json` | 历史余额记录（用于趋势分析） |
| `report_*_zh.md` | 中文日报 |
| `report_*_en.md` | 英文日报 |

---

## 报告格式

### 示例报告

```markdown
# 📊 Token 余额日报 - 2026-05-10

## 💰 余额总览

| 项目 | 金额 |
|------|------|
| 人民币总额 | ¥76.29 |
| 美元总额 | $0.00 |

## 📋 平台明细

### 1. DeepSeek
| 项目 | 金额 |
|------|------|
| 总余额 | ¥76.29 |
| 充值余额 | ¥76.29 |
```

---

## 文件结构

```
token-usage-tracker/
├── SKILL.md                 # 本文件
├── config/
│   ├── auth.json           # API Key 存储
│   ├── platforms.json      # 平台配置
│   └── web_config.py       # Web 配置服务器
├── scripts/
│   ├── run.py              # 主入口脚本 ⭐
│   ├── fetch_usage.py      # 余额抓取
│   ├── generate_report.py  # 报告生成
│   └── anomaly_detector.py # 异常检测
├── assets/
│   └── config_interface.html # Web 配置界面
├── output/
│   ├── balance_data.json   # 余额数据
│   ├── balance_history.json # 历史记录
│   └── report_*.md         # 报告文件
└── references/
    └── api_balance_research.md # API 调研报告
```

---

## 常见问题

### 1. API Key 无效

检查 `config/auth.json` 中的 key 是否正确，或通过 Web 界面重新配置。

### 2. 报告显示"暂无历史数据"

需要连续运行 2 天以上才能生成趋势分析。

### 3. 某平台抓取失败

可能原因：
- API Key 未配置
- API Key 无效或过期
- 平台 API 服务不可用

---

## 下一步计划

- [ ] OpenAI Admin API 用量查询
- [ ] 火山引擎/豆包余额查询（需签名认证）
- [ ] 定时推送（automation_update）
- [ ] 浏览器抓取（腾讯云 TokenHub 等）
- [ ] HTML 可视化报告

---

*版本 2.0 · 2026-05-10*