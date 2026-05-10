# 贡献指南 | Contributing Guide

感谢您对 Token Usage Tracker 的关注！欢迎提交 Issue 和 Pull Request。

## 🤝 如何贡献

### 报告 Bug 🐛

如果您发现了 Bug，请提交 Issue：

1. 使用清晰的标题描述问题
2. 详细描述复现步骤
3. 说明预期行为和实际行为
4. 包含系统信息（OS、Node版本等）

### 提议新功能 ✨

1. 先检查是否已有相关 Issue
2. 在新 Issue 中详细描述功能
3. 解释为什么这个功能很重要
4. 提供使用示例

### 提交代码 💻

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📋 代码规范

- 遵循现有代码风格
- 添加注释说明复杂逻辑
- 为新功能编写测试
- 更新相关文档

## 📚 开发环境设置

```bash
# 克隆项目
git clone https://github.com/yourusername/token-usage-tracker.git
cd token-usage-tracker

# 安装依赖
npm install

# 启动开发环境
npm run dev

# 运行测试
npm test
```

## 📝 提交信息格式

```
feat: 新增功能描述
fix: Bug修复描述
docs: 文档更新
style: 代码风格调整
refactor: 代码重构
test: 测试相关
chore: 构建配置等
```

## 🚀 发布流程

1. 更新版本号 (package.json)
2. 更新 CHANGELOG.md
3. 创建 Release
4. 发布到 npm

---

感谢所有贡献者的支持！❤️
