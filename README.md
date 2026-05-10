# Token Usage Tracker

> 🚀 追踪多个 AI 平台的账户余额，自动生成每日汇总报告

## 功能特性

- ✅ **余额查询** — 支持 DeepSeek、Kimi/Moonshot 等平台
- ✅ **日报生成** — 中英文双语 Markdown 报告
- ✅ **历史趋势** — 自动保存历史数据，计算消耗趋势
- ✅ **Web 配置界面** — 32 个模型，可视化配置 API Key

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/tobiglevent001/token-usage-tracker.git
cd token-usage-tracker

# 安装依赖
pip install requests flask

# 配置 API Key
cp config/auth.json.example config/auth.json
# 编辑 auth.json，填入你的 API Key

# 运行
python scripts/run.py
```

## 已支持平台

| 平台 | 余额查询 | API Endpoint |
|------|---------|--------------|
| DeepSeek | ✅ | `GET /user/balance` |
| Kimi/Moonshot | ✅ | `GET /v1/users/me/balance` |
| OpenAI | ⚠️ 用量 | 需要 Admin API Key |

## 项目结构

```
token-usage-tracker/
├── SKILL.md                 # Skill 说明文档
├── config/
│   ├── auth.json.example    # API Key 配置示例
│   └── web_config.py        # Web 配置服务器
├── scripts/
│   ├── run.py               # 主入口脚本
│   ├── fetch_usage.py       # 余额抓取
│   └── generate_report.py  # 报告生成
├── assets/
│   └── config_interface.html # Web 配置界面
└── docs/
    └── 开发总结.md           # 开发文档
```

## 使用方式

### 命令行

```bash
python scripts/run.py                          # 默认抓取所有平台
python scripts/run.py --platforms deepseek    # 只抓取 DeepSeek
python scripts/run.py --lang zh               # 只生成中文报告
```

### Web 配置界面

```bash
python config/web_config.py
# 打开 http://localhost:8888
```

## 示例报告

```markdown
# 📊 Token 余额日报 - 2026-05-10

## 💰 余额总览

| 项目 | 金额 |
|------|------|
| 人民币总额 | ¥76.17 |
| 美元总额 | $0.00 |

## 📋 平台明细

### 1. DeepSeek
| 项目 | 金额 |
|------|------|
| 总余额 | ¥76.17 |
| 充值余额 | ¥76.17 |
```

## License

MIT