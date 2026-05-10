# 🚀 快速开始指南 | Quick Start Guide

## 5分钟快速上手

### 第1步：安装

```bash
# 克隆项目
git clone https://github.com/tobiglevent001/token-usage-tracker.git
cd token-usage-tracker

# 安装依赖 (选择一个)
npm install      # Node.js 方式
# 或
pip install -r requirements.txt  # Python 方式
```

### 第2步：获取 API 密钥

1. **OpenAI**: https://platform.openai.com/api-keys
2. **Anthropic**: https://console.anthropic.com/account/keys
3. **Google**: https://aistudio.google.com/app/apikey
4. **DeepSeek**: https://platform.deepseek.com/api_keys
5. **Kimi**: https://platform.moonshot.cn/console/api-keys

### 第3步：配置和运行

#### 方式A：使用 Web 界面（推荐）

```bash
# 启动 Web 配置面板
python config/web_config.py

# 打开浏览器访问
http://localhost:8888
```

然后：
1. 在 "API密钥" 选项卡中添加您的密钥
2. 在 "预算设置" 选项卡中设置预算
3. 在 "告警设置" 中配置告警

#### 方式B：命令行方式

```bash
# 添加 OpenAI 密钥
node index.js add openai sk-xxxxxxxxxxxxx

# 添加更多平台
node index.js add anthropic sk-ant-xxxxxxxxxxxxx

# 启动监控
node index.js start
```

### 第4步：查看实时余额

访问 `assets/dashboard.html` 查看：
- 📊 各平台实时余额
- 📈 消费趋势图表
- 💡 成本分析建议
- 🔔 告警通知

---

## 常见问题

**Q: 我的 API 密钥安全吗？**  
A: 完全安全！密钥仅存储在本地，采用加密存储，不会上传任何服务器。

**Q: 多久更新一次余额？**  
A: 默认每5分钟更新一次，可在配置中调整。

**Q: 支持多用户吗？**  
A: 支持！可为不同团队成员分配不同的 API 密钥。

**Q: 可以离线使用吗？**  
A: 可以，使用本地缓存数据，但无法获取最新余额。

---

## 下一步

- 📖 [完整文档](README.md)
- 🔧 [配置说明](CONFIG.md)
- 🐛 [报告问题](https://github.com/tobiglevent001/token-usage-tracker/issues)
- 💬 [加入讨论](https://github.com/tobiglevent001/token-usage-tracker/discussions)

---

**需要帮助？** 提交 Issue 或在 Discussions 中提问！
