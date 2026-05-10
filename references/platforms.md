# 支持的平台 / Supported Platforms

本文档列出 `token-usage-tracker` 目前支持的平台及配置方法。

This document lists platforms currently supported by `token-usage-tracker` and how to configure them.

---

## 已支持平台 / Supported Platforms

### 1. DeepSeek

| 属性 / Attribute | 值 / Value |
|-------------------|--------|
| 名称（中文） / Name (Chinese) | DeepSeek |
| 名称（英文） / Name (English) | DeepSeek |
| 抓取方式 / Fetch Method | `api` |
| 需要 API Key | 是 / Yes |
| 环境变量 / Env Variable | `DEEPSEEK_API_KEY` |
| 免费额度 / Free Tier | 有 / Yes |

**配置示例 / Configuration Example**:

```json
{
  "id": "deepseek",
  "name": "DeepSeek",
  "name_en": "DeepSeek",
  "enabled": true,
  "fetch_method": "api",
  "api_endpoint": "https://api.deepseek.com/v1/usage",
  "auth": {
    "type": "api_key",
    "env_var": "DEEPSEEK_API_KEY"
  }
}
```

**获取 API Key / Get API Key**:
1. 访问 https://platform.deepseek.com/
2. 登录 / Login
3. 进入 API Keys 页面
4. 创建新 Key / Create new key

---

### 2. 腾讯云 TokenHub (Tencent Cloud TokenHub)

| 属性 / Attribute | 值 / Value |
|-------------------|--------|
| 名称（中文） / Name (Chinese) | 腾讯云 TokenHub |
| 名称（英文） / Name (English) | Tencent Cloud TokenHub |
| 抓取方式 / Fetch Method | `browser` |
| 需要登录 | 是 / Yes |
| Cookies 文件 | `config/tencent_cookies.json` |
| 免费额度 | 取决于具体服务 / Depends on service |

**配置示例 / Configuration Example**:

```json
{
  "id": "tencent-tokenhub",
  "name": "腾讯云 TokenHub",
  "name_en": "Tencent Cloud TokenHub",
  "enabled": true,
  "fetch_method": "browser",
  "url": "https://console.cloud.tencent.com/tokenhub/tokenplan",
  "selectors": {
    "total_tokens": ".token-total",
    "cost": ".cost-amount"
  },
  "auth": {
    "type": "cookie",
    "cookie_file": "config/tencent_cookies.json"
  }
}
```

**注意事项 / Notes**:
- 需要安装 `browser-use` skill
- Requires `browser-use` skill installation
- 网页结构变化后需要更新选择器
- Update selectors after webpage structure changes

---

## 待支持平台 / Platforms To Support

### OpenAI

| 属性 / Attribute | 值 / Value |
|-------------------|--------|
| 名称（中文） / Name (Chinese) | OpenAI |
| 名称（英文） / Name (English) | OpenAI |
| 抓取方式 / Fetch Method | `api` |
| 需要 API Key | 是 / Yes |
| 环境变量 / Env Variable | `OPENAI_API_KEY` |
| 免费额度 / Free Tier | 无 / No |

**配置示例 / Configuration Example**:

```json
{
  "id": "openai",
  "name": "OpenAI",
  "name_en": "OpenAI",
  "enabled": false,
  "fetch_method": "api",
  "api_endpoint": "https://api.openai.com/v1/usage",
  "auth": {
    "type": "api_key",
    "env_var": "OPENAI_API_KEY"
  }
}
```

---

### Anthropic (Claude)

| 属性 / Attribute | 值 / Value |
|-------------------|--------|
| 名称（中文） / Name (Chinese) | Anthropic (Claude) |
| 名称（英文） / Name (English) | Anthropic (Claude) |
| 抓取方式 / Fetch Method | `api` |
| 需要 API Key | 是 / Yes |
| 环境变量 / Env Variable | `ANTHROPIC_API_KEY` |

---

## 添加新平台 / Adding New Platform

### 方法 1：API 方式 / Method 1: API Method

如果平台提供 API，在 `config/platforms.json` 中添加：

1. 获取 API 文档 / Get API documentation
2. 获取 API Key / Get API key
3. 添加到配置文件 / Add to config file

### 方法 2：Browser 方式 / Method 2: Browser Method

如果平台只有网页，使用 browser-use：

1. 手动登录并保存 cookies
2. 检查网页 HTML 结构，获取 CSS 选择器
3. 添加到配置文件 / Add to config file

---

## 贡献新平台支持 / Contributing New Platform Support

如果你成功添加了新平台，请提交 Pull Request！

If you successfully added a new platform, please submit a Pull Request!

**需要包含 / Should include**:
- 配置文件示例 / Example config
- 抓取脚本（如需要）/ Fetch script (if needed)
- 文档更新 / Documentation update

---

*最后更新 / Last Updated: 2026-05-10*
