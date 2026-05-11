# 安全策略 / Security Policy

## 支持的版本 / Supported Versions

| 版本 / Version | 支持状态 / Supported |
|---------------|-------------------|
| 1.0.x | ✅ |

## 报告漏洞 / Reporting a Vulnerability

如果发现安全漏洞，请**不要**在 GitHub Issues 中公开报告。

请通过以下方式私下报告：
1. 发送邮件至 [项目维护者]
2. 或直接在仓库中创建安全 Advisory

我们会：
- 在 48 小时内确认收到报告
- 评估漏洞严重性
- 在修复后发布安全更新

## 安全最佳实践 / Security Best Practices

### API 密钥保护
- 永远不要将 API 密钥提交到 Git 仓库
- 使用 `config/auth.json` （已添加到 .gitignore）
- 或使用环境变量注入密钥

### 数据安全
- 所有数据存储在本地，不发送到外部服务器
- API 密钥以 JSON 格式加密存储
- 建议定期清理过期数据
