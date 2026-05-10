# Token Usage Tracker 💰
## AI平台余额追踪器

> Real-time AI Platform Balance Tracker - Monitor your token consumption, spending, and budget across multiple AI services (OpenAI, Anthropic, Google, DeepSeek, etc.)
>
> 实时AI平台使用额度监控工具——追踪Token消耗、支出、预算，支持多个AI服务平台（OpenAI、Anthropic、Google、DeepSeek等）。

---

## ✨ 功能特性 | Features

### 🎯 核心能力

- **实时余额监控** - 实时追踪API额度消耗
- **多平台支持** - 同时监控 OpenAI、Anthropic、Google、DeepSeek、Kimi等
- **详细成本分析** - 按模型、日期、项目统计成本
- **预算告警** - 设置预算上限，超出自动告警
- **数据可视化** - 图表展示使用趋势和成本分布
- **导出报告** - 生成月度、年度使用报告
- **成本优化建议** - AI驱动的成本节省建议
- **Web配置界面** - 可视化配置API Key和预算

### Key Features
- **Real-time Balance Monitoring** - Live API usage tracking
- **Multi-Platform Support** - OpenAI, Anthropic, Google, DeepSeek, Kimi, etc.
- **Cost Analysis** - Detailed breakdown by model, date, project
- **Budget Alerts** - Automatic notifications when approaching limits
- **Data Visualization** - Charts and dashboards
- **Report Generation** - Export usage reports
- **Cost Optimization** - AI-powered savings recommendations
- **Web Dashboard** - Visual management interface

---

## 🚀 快速开始 | Quick Start

### 安装 | Installation

```bash
# 克隆项目
git clone https://github.com/tobiglevent001/token-usage-tracker.git
cd token-usage-tracker

# 安装依赖
npm install
# 或
pip install requests flask
```

### 基础使用 | Basic Usage

#### Node.js 版本

```javascript
const TokenTracker = require('./index.js');

// 初始化追踪器
const tracker = new TokenTracker({
  dbPath: './data',
  refreshInterval: 300000  // 5分钟更新一次
});

// 添加API密钥
await tracker.addApiKey({
  platform: 'openai',
  apiKey: 'sk-xxxxx',
  alias: 'Main Account'
});

// 获取实时余额
const balance = await tracker.getBalance('openai');
console.log(`OpenAI 余额: $${balance.available}`);

// 获取今日消耗
const todayUsage = await tracker.getUsageStats('today');
console.log(`今日消耗: $${todayUsage.total}`);
```

#### Python 版本

```bash
# 配置 API Key
cp config/auth.json.example config/auth.json
# 编辑 auth.json

# 运行追踪器
python scripts/run.py

# 启动Web配置界面
python config/web_config.py
# 访问 http://localhost:8888
```

### 配置 | Configuration

创建 `config.json`:

```json
{
  "trackedPlatforms": [
    "openai",
    "anthropic",
    "google",
    "deepseek",
    "kimi"
  ],
  "refreshInterval": 300000,
  "budgets": {
    "openai": {
      "monthly": 100,
      "daily": 5
    },
    "anthropic": {
      "monthly": 50,
      "daily": 2
    }
  },
  "alertThresholds": {
    "monthlyBudgetPercent": 80,
    "dailyBudgetPercent": 90
  },
  "notifications": {
    "email": true,
    "slack": false,
    "webhook": ""
  },
  "dataRetention": 365
}
```

---

## 📊 使用案例 | Use Cases

### 场景1：个人开发者成本控制

```
问题: 使用多个AI API，不知道每月花多少钱？
解决方案:
  ✓ 一览表显示所有API的实时余额
  ✓ 按天/周/月统计支出
  ✓ 预设预算，超支自动告警
  ✓ 对比不同模型成本差异
  
效果: 降低40%的API成本
```

### 场景2：AI创业公司成本管理

```
问题: 有10+员工，怎样追踪他们的API消耗？
解决方案:
  ✓ 为每个员工分配API Key
  ✓ 按人员/项目/部门统计成本
  ✓ 设置部门预算限额
  ✓ 每周自动生成成本报告
  
效果: 提高成本透明度，优化资源分配
```

### 场景3：AI应用运营优化

```
问题: 应该用GPT-4还是GPT-3.5-turbo？
解决方案:
  ✓ 记录不同模型的成本
  ✓ 分析精准度 vs 成本关系
  ✓ 给出模型选择建议
  ✓ 自动切换至成本最优模型
  
效果: 保持质量同时降低20%成本
```

---

## 📈 数据看板 | Dashboard

```
┌─────────────────────────────────────────────┐
│         AI Platform Balance Dashboard        │
├─────────────────────────────────────────────┤
│                                               │
│  OpenAI          余额: $450.32                │
│  ████████░░░░░░░ (预算: $500)                │
│  今月消耗: $49.68  (剩余27天)                │
│                                               │
│  Anthropic       余额: $125.45                │
│  ███░░░░░░░░░░░░ (预算: $200)                │
│  今月消耗: $74.55                            │
│                                               │
│  Google Gemini   余额: $300.00                │
│  ██████░░░░░░░░░ (预算: $400)                │
│  今月消耗: $100.00                           │
│                                               │
│  DeepSeek        余额: ¥76.17                 │
│  ███████░░░░░░░░ (预算: ¥100)                │
│  今月消耗: ¥23.83                            │
│                                               │
├─────────────────────────────────────────────┤
│  今日总消耗: $12.34                          │
│  预计月底: $387  (在预算内 ✓)                │
├─────────────────────────────────────────────┤
```

---

## 📊 成本分析示例 | Cost Analysis Example

### 每日消耗趋势

```
今天        5:30am    8:45am    2:15pm    7:30pm
OpenAI      $2.10     $1.45     $3.20     $1.95
Anthropic   $0.80     $0.40     $1.10     $0.50
Google      $0.50     $0.30     $0.80     $0.40
DeepSeek    ¥2.50     ¥1.80     ¥3.20     ¥1.50
────────────────────────────────────────
日总计      $3.40     $2.15     $5.10     $2.85
```

### 模型成本对比

```
模型                  今月成本    占比    每请求成本
GPT-4               $32.50     32%     $0.028
GPT-3.5-turbo       $18.20     18%     $0.002
Claude-3-Opus       $25.10     25%     $0.015
Claude-3-Sonnet     $15.40     15%     $0.008
Google Gemini-Pro   $9.80      10%     $0.001
```

### 成本节省建议

```
🎯 优化建议:

1. 将18%的GPT-4调用切换到GPT-3.5-turbo
   预计节省: $5.85/月

2. 为非核心任务使用Gemini-Pro
   预计节省: $8.20/月

3. 使用缓存减少重复请求
   预计节省: $3.40/月

───────────────────────
总计节省潜力: $17.45/月 (17.4%)
```

---

## 📚 API 文档 | API Documentation

### `getBalance(platform)`

获取特定平台的实时余额

**参数:**
- `platform` (string): 'openai' | 'anthropic' | 'google' | 'deepseek' | 'kimi' | 'azure'

**返回:**
```javascript
{
  platform: string,
  available: number,        // 可用余额（美元或当地货币）
  usage: number,           // 本月已用
  percentage: number,      // 使用百分比
  resetDate: date,         // 下次重置日期
  currency: string,        // 货币代码
  lastUpdated: timestamp
}
```

### `getUsageStats(period)`

获取使用统计

**参数:**
- `period` (string): 'today' | 'week' | 'month' | 'custom'

**返回:**
```javascript
{
  totalSpent: number,
  byPlatform: { openai: 45.20, deepseek: 12.50, ... },
  byModel: { 'gpt-4': 32.50, 'claude-3': 25.10, ... },
  byProject: { project_a: 25.10, ... },
  trend: array,
  comparison: { yesterday: -10%, lastMonth: +5% }
}
```

### `setBudgetAlert(config)`

设置预算告警

---

## 🔔 告警机制 | Alert System

```
告警类型：

🔴 严重告警 (Critical)
   - 已超过月度预算
   - 立即发送通知

🟠 警告告警 (Warning)
   - 达到预算的80%
   - 每小时检查一次

🟡 信息告警 (Info)
   - 达到预算的60%
   - 每日检查一次

📊 趋势告警 (Trend)
   - 本周消耗比上周增加50%以上
   - 可能有异常使用
```

---

## 💾 数据导出 | Export Options

```bash
# 导出本月报告 (PDF)
tracker.exportReport('month', 'pdf');

# 导出使用详情 (CSV)
tracker.exportUsageDetails('csv');

# 导出成本分析 (Excel)
tracker.exportAnalysis('xlsx');

# 导出账单 (JSON)
tracker.exportBilling('json');
```

---

## 🔒 安全性 | Security

✅ **本地存储** - API密钥存储在本地，加密处理
✅ **不收集日志** - 不保存API请求详情
✅ **定期清理** - 自动删除过期数据
✅ **访问控制** - 支持用户认证

---

## 📁 项目结构 | Project Structure

```
token-usage-tracker/
├── README.md                    # 本文件
├── LICENSE                      # MIT许可证
├── index.js / run.py           # 主入口
├── config/
│   ├── config.json             # 配置文件
│   ├── auth.json.example       # API密钥配置示例
│   └── web_config.py           # Web配置服务器
├── scripts/
│   ├── fetch_usage.py          # 余额抓取脚本
│   └── generate_report.py      # 报告生成脚本
├── assets/
│   └── dashboard.html          # Web仪表盘
└── data/
    └── history/                # 历史数据存储
```

---

## 🤝 贡献指南 | Contributing

欢迎提交 Issues 和 Pull Requests！

---

## 📄 许可证 | License

MIT License - 详见 LICENSE 文件

---

## 💬 常见问题 | FAQ

**Q: API密钥安全吗？**
A: 完全安全。密钥本地加密存储，不会上传任何服务器。

**Q: 支持哪些平台？**
A: 目前支持OpenAI、Anthropic、Google、DeepSeek、Kimi。更多平台持续添加中。

**Q: 数据更新有延迟吗？**
A: 最新数据延迟<5分钟，基于各平台API的更新速度。

**Q: 可以离线使用吗？**
A: 可以！使用本地缓存数据，但无法获取最新余额。

**Q: 支持多用户吗？**
A: 支持！可以为不同成员分配API Key，分别追踪。

---

## 📞 联系方式 | Contact

- GitHub Issues: [报告问题](https://github.com/tobiglevent001/token-usage-tracker/issues)
- 讨论区: [加入讨论](https://github.com/tobiglevent001/token-usage-tracker/discussions)

---

**⭐ 如果觉得有帮助，请给个Star！**
