# API 参考文档 / API Reference

本文档提供各平台 API 的详细参考信息。

This document provides detailed API reference information for each platform.

---

## DeepSeek API

### Base URL
```
https://api.deepseek.com/v1
```

### 认证 / Authentication
```
Headers:
  Authorization: Bearer {{DEEPSEEK_API_KEY}}
  Content-Type: application/json
```

### 端点 / Endpoints

#### 1. 获取用量统计 / Get Usage Statistics

**请求 / Request**:
```http
GET /v1/usage
Host: api.deepseek.com
Authorization: Bearer sk-xxxxx
```

**响应 / Response**:
```json
{
  "object": "list",
  "data": [
    {
      "id": "usage-123",
      "object": "usage",
      "created": 1715328000,
      "tokens": 15230,
      "cost": 8.20,
      "currency": "CNY",
      "model": "deepseek-chat",
      "requests": 123
    }
  ],
  "total_tokens": 15230,
  "total_cost": 8.20
}
```

**字段说明 / Field Description**:
| 字段 / Field | 类型 / Type | 说明 / Description |
|---------------|------------|-------------------|
| `tokens` | integer | Token 使用量 / Token usage |
| `cost` | float | 费用 / Cost |
| `currency` | string | 货币单位（CNY/USD) / Currency unit |
| `model` | string | 模型名称 / Model name |
| `requests` | integer | 请求数 / Number of requests |

---

## OpenAI API

### Base URL
```
https://api.openai.com/v1
```

### 认证 / Authentication
```
Headers:
  Authorization: Bearer {{OPENAI_API_KEY}}
  Content-Type: application/json
```

### 端点 / Endpoints

#### 1. 获取用量统计 / Get Usage Statistics

**请求 / Request**:
```http
GET /v1/usage?start_date=2026-05-01&end_date=2026-05-10
Host: api.openai.com
Authorization: Bearer sk-xxxxx
```

**响应 / Response**:
```json
{
  "object": "list",
  "data": [
    {
      "date": "2026-05-10",
      "tokens": 12500,
      "cost": 15.50,
      "model": "gpt-4o"
    }
  ],
  "total_tokens": 12500,
  "total_cost": 15.50
}
```

---

## 腾讯云 API (Tencent Cloud API)

### 认证方式 / Authentication Method
使用腾讯云 SDK 或签名认证 / Use Tencent Cloud SDK or signature authentication

### 示例 / Example
```python
from tencentcloud.common import credential
from tencentcloud.faceid.v20180301 import faceid_client, models

cred = credential.Credential("secret_id", "secret_key")
```

**注意 / Note**: 腾讯云 TokenHub 可能需要通过浏览器抓取，暂无官方 API。  
*Tencent Cloud TokenHub may require browser scraping, no official API available yet.*

---

## 错误代码 / Error Codes

| HTTP 状态码 / HTTP Status | 说明 / Description | 解决方法 / Solution |
|--------------------------|-------------------|----------------------|
| 401 Unauthorized | API Key 无效 / Invalid API Key | 检查 API Key / Check API Key |
| 403 Forbidden | 权限不足 / Insufficient permissions | 检查账号权限 / Check account permissions |
| 429 Too Many Requests | 请求限流 / Rate limited | 实现重试机制 / Implement retry mechanism |
| 500 Internal Server Error | 服务器错误 / Server error | 稍后重试 / Retry later |

---

## 速率限制 / Rate Limits

| 平台 / Platform | 限制 / Limit | 说明 / Description |
|---------------|----------|-------------------|
| DeepSeek | 10 req/min | 每分钟 10 次请求 / 10 requests per minute |
| OpenAI | 20 req/min | 每分钟 20 次请求 / 20 requests per minute |
| 腾讯云 / Tencent Cloud | 取决于服务 / Depends on service | 查看具体服务限制 / Check specific service limits |

---

*最后更新 / Last Updated: 2026-05-10*
