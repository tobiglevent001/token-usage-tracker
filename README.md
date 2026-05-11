# Token Usage Tracker 💰

> AI 平台余额追踪器 — 实时监控多个 AI 服务的 Token 消耗和余额
>
> Real-time AI platform balance tracker for multiple AI services

[![CI](https://github.com/tobiglevent001/token-usage-tracker/actions/workflows/test.yml/badge.svg)](https://github.com/tobiglevent001/token-usage-tracker/actions/workflows/test.yml)
[![License](https://img.shields.io/github/license/tobiglevent001/token-usage-tracker)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

---

## ✨ 功能特性

- **📊 实时余额监控** — 自动查询各平台账户余额
- **🌐 多平台支持** — DeepSeek， Kimi/Moonshot， OpenAI 用量查询... 持续添加中
- **📝 日报生成** — 中/英双语报告，含消耗趋势和异常检测
- **🌐 Web 配置界面** — 可视化配置 API Key 和测试连接
- **⏰ 定时调度** — 支持每日自动抓取和报告生成
- **📈 历史趋势** — 自动保存历史数据，计算日均消耗
- **🔒 本地加密** — API 密钥安全本地存储

### 已支持平台

| 平台 | 余额查询 | 用量查询 | 实现状态 |
|------|---------|---------|---------|
| **DeepSeek** | ✅ `GET /user/balance` | — | 已验证 |
| **Kimi/Moonshot** | ✅ `GET /v1/users/me/balance` | — | 已验证 |
| **OpenAI** | — | ✅ 用量查询 | 需 Admin Key |
| 火山引擎/豆包 | ⚠️ 需签名 | ⚠️ 需签名 | 开发中 |
| 更多平台... | — | — | 欢迎 PR |

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/tobiglevent001/token-usage-tracker.git
cd token-usage-tracker

# Python 方式（推荐）
pip install -r requirements.txt
```

### 配置 API Key

```bash
cp config/auth.json.example config/auth.json
# 编辑 auth.json，填入你的 API Key
```

### 运行

```bash
# 方式一：命令行
python scripts/run.py

# 方式二：Web 配置界面
node index.js web
# 或
python config/web_config.py
# 然后浏览器访问 http://localhost:8888
```

---

## 📁 项目结构

```
token-usage-tracker/
├── index.js                    # Node.js 入口（CLI 包装器）
├── package.json                # Node.js 配置
├── requirements.txt            # Python 依赖
├── config/
│   ├── platforms.json          # 平台配置
│   ├── schedule.json           # 调度配置
│   ├── auth.json.example       # API Key 模板
│   └── web_config.py           # Web 配置服务（Flask）
├── scripts/
│   ├── run.py                  # 主入口 ⭐
│   ├── fetch_usage.py          # 余额抓取器
│   ├── generate_report.py      # 报告生成器
│   ├── scheduler.py            # 定时任务管理器
│   ├── anomaly_detector.py     # 异常检测
│   └── utils.py                # 工具函数
├── assets/
│   └── config_interface.html   # Web 配置前端
├── tests/
│   ├── test_fetch_usage.py     # 余额抓取测试
│   └── test_generate_report.py # 报告生成测试
└── output/                     # 输出目录（运行时生成）
```

---

## 📖 开发指南

```bash
# 运行测试
python -m pytest tests/ -v

# 启动开发环境
python scripts/run.py --lang both
```

更多信息见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 许可证

MIT License — 详见 [LICENSE](LICENSE)

## ⭐ 如果觉得有帮助，请给个 Star！
