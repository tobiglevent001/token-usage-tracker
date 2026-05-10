# AI 平台余额/用量查询 API 调研报告

## 调研时间：2026-05-10

---

## 📊 总览

| 平台 | 余额查询 API | 用量查询 API | 认证方式 | API 状态 |
|------|-------------|-------------|----------|----------|
| DeepSeek | ✅ 有 | ❌ 无公开 | Bearer Token | 已验证 |
| Kimi/Moonshot | ✅ 有 | ❌ 无公开 | Bearer Token | 已验证 |
| OpenAI | ❌ 无公开 | ✅ 有 | Admin API Key | 已验证 |
| 火山引擎/豆包 | ✅ 有 | ✅ 有 | 签名认证 v4 | 需签名 |
| Anthropic/Claude | ❌ 无公开 | ❌ 无公开 | 仅 Console | 不可用 |
| 阿里云通义千问 | ❌ 无公开 | ❌ 无公开 | 仅 Console | 不可用 |
| 智谱AI/GLM | ⚠️ 第三方 | ⚠️ 第三方 | 仅 Console | 不稳定 |
| MiniMax | ⚠️ 网页工具 | ⚠️ 网页工具 | 仅 Console | 不稳定 |
| Google Gemini | ❌ 无公开 | ❌ 无公开 | Cloud Console | 不可用 |
| Mistral | ❌ 无公开 | ❌ 无公开 | 仅 Console | 不可用 |

---

## 1. DeepSeek ✅ 已验证

### 余额查询 API

| 项目 | 值 |
|------|-----|
| **Endpoint** | `GET https://api.deepseek.com/user/balance` |
| **认证方式** | `Authorization: Bearer <API_KEY>` |
| **响应格式** | JSON |

**请求示例**：
```bash
curl -X GET 'https://api.deepseek.com/user/balance' \
  -H 'Authorization: Bearer sk-xxxxx'
```

**响应示例**：
```json
{
  "is_available": true,
  "balance_infos": [
    {
      "currency": "CNY",
      "total_balance": "110.00",
      "granted_balance": "10.00",
      "topped_up_balance": "100.00"
    }
  ]
}
```

**字段说明**：
| 字段 | 说明 |
|------|------|
| `is_available` | API 服务是否可用 |
| `currency` | 币种（CNY） |
| `total_balance` | 总余额（赠送 + 充值） |
| `granted_balance` | 赠送余额 |
| `topped_up_balance` | 充值余额 |

**注意**：余额字段类型为 `string`，使用时需转换为数字。

---

## 2. Kimi/Moonshot ✅ 已验证

### 余额查询 API

| 项目 | 值 |
|------|-----|
| **Endpoint** | `GET https://api.moonshot.ai/v1/users/me/balance` |
| **认证方式** | `Authorization: Bearer <API_KEY>` |
| **响应格式** | JSON |

**请求示例**：
```bash
curl -X GET "https://api.moonshot.ai/v1/users/me/balance" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**响应示例**：
```json
{
  "code": 0,
  "scode": "0x0",
  "status": true,
  "data": {
    "available_balance": 49.58894,
    "voucher_balance": 46.58893,
    "cash_balance": 3.00001
  }
}
```

**字段说明**：
| 字段 | 类型 | 说明 |
|------|------|------|
| `available_balance` | float | 可用余额（USD），≤ 0 时无法调用 API |
| `voucher_balance` | float | 代金券余额（USD） |
| `cash_balance` | float | 现金余额（USD），可为负 |

---

## 3. OpenAI ✅ 已验证（仅用量）

### 用量查询 API

| 项目 | 值 |
|------|-----|
| **Endpoint** | `GET https://api.openai.com/v1/organization/usage/completions` |
| **认证方式** | `Authorization: Bearer <ADMIN_API_KEY>` |
| **必需参数** | `start_time` (Unix timestamp) |
| **响应格式** | JSON |

**重要**：需要使用 **Admin API Key**（管理员密钥），在 https://platform.openai.com/settings/organization/admin-keys 获取。

**请求示例**：
```bash
curl -X GET "https://api.openai.com/v1/organization/usage/completions?start_time=1736616660" \
  -H "Authorization: Bearer YOUR_ADMIN_API_KEY" \
  -H "Content-Type: application/json"
```

**响应示例**：
```json
{
  "data": [
    {
      "object": "bucket",
      "start_time": 1736616660,
      "end_time": 1736640000,
      "results": [
        {
          "object": "organization.usage.completions.result",
          "input_tokens": 141201,
          "output_tokens": 9756,
          "num_model_requests": 470,
          "model": null
        }
      ]
    }
  ]
}
```

**常用参数**：
| 参数 | 说明 |
|------|------|
| `start_time` | 开始时间（Unix 秒级时间戳）**必填** |
| `end_time` | 结束时间 |
| `bucket_width` | 时间桶宽度：`1m`/`1h`/`1d` |
| `models` | 模型列表过滤 |
| `group_by` | 分组字段，如 `["model"]` |

**注意**：OpenAI 没有直接的余额查询 API，需要在 https://platform.openai.com/settings/organization/billing/overview 查看。

---

## 4. 火山引擎/豆包 ✅ 已验证（需签名）

### 余额查询 API

| 项目 | 值 |
|------|-----|
| **Service** | `billing` |
| **Action** | `QueryBalanceAcct` |
| **Version** | `2022-01-01` |
| **认证方式** | 签名认证 v4（Access Key + Secret Key） |

**API Explorer**：
https://api.volcengine.com/api-explorer/?action=QueryBalanceAcct&groupName=资金服务&serviceCode=billing&version=2022-01-01

**注意**：火山引擎 API 需要签名认证，实现较复杂。建议使用火山引擎 SDK。

---

## 5. Anthropic/Claude ❌ 无公开 API

- 余额和用量查询需要通过 Console：https://console.anthropic.com/
- 无公开的余额查询或用量查询 API endpoint
- 第三方平台（如 UsageBox）提供监控集成，但需要额外配置

---

## 6. 阿里云通义千问/DashScope ❌ 无公开 API

- 余额需要在阿里云控制台查看：https://dashscope.console.aliyun.com/
- API 调用会返回每次请求的 token 使用量（在 `usage` 字段），但无累计用量查询 API
- 无公开的余额查询 endpoint

---

## 7. 智谱AI/GLM ⚠️ 不稳定

- 官方无公开的余额查询 API
- 存在第三方查询工具：
  - https://check.glmbigmodel.me/
  - http://glm-check.618987.xyz/
- 这些工具可能不稳定，不建议在生产环境依赖

---

## 8. MiniMax ⚠️ 不稳定

- 官方无公开的余额查询 API
- 存在第三方网页工具：https://minimax-usage.vercel.app/
- Token Plan 用量需要在订阅管理页面查看

---

## 9. Google Gemini ❌ 无公开 API

- 用量和配额需要通过 Google Cloud Console 查看
- 无直接的余额查询 API
- Gemini API 免费层有配额限制，但需要在 Cloud Console 监控

---

## 10. Mistral ❌ 无公开 API

- 余额和用量需要在 https://console.mistral.ai/ 查看
- 无公开的余额查询 API

---

## 🔧 实现优先级建议

### Phase 1：立即可实现（1-2小时）

| 平台 | 难度 | 说明 |
|------|------|------|
| DeepSeek | ⭐ 简单 | 直接 GET 请求，Bearer Token 认证 |
| Kimi/Moonshot | ⭐ 简单 | 直接 GET 请求，Bearer Token 认证 |

### Phase 2：需要额外配置（2-4小时）

| 平台 | 难度 | 说明 |
|------|------|------|
| OpenAI | ⭐⭐ 中等 | 需要 Admin API Key，参数较多 |
| 火山引擎/豆包 | ⭐⭐⭐ 复杂 | 需要实现签名认证 v4 |

### Phase 3：需要浏览器抓取（未来）

| 平台 | 难度 | 说明 |
|------|------|------|
| Anthropic/Claude | ⭐⭐⭐⭐ | 需要 browser-use 抓取 Console |
| 阿里云通义千问 | ⭐⭐⭐⭐ | 需要 browser-use 抓取 Console |
| 智谱AI/GLM | ⭐⭐⭐ | 可尝试第三方工具，但不稳定 |

---

## 📝 实现建议

### 推荐实现顺序

1. **先做 DeepSeek + Kimi** — 这两个最简单，10分钟内可完成
2. **再做 OpenAI** — 需要 Admin Key，但认证方式简单
3. **火山引擎最后** — 签名认证复杂，建议用 SDK

### 代码架构建议

```python
# 统一接口设计
class BalanceFetcher:
    def fetch(self, platform_id: str) -> Dict:
        if platform_id == "deepseek":
            return self._fetch_deepseek()
        elif platform_id == "moonshot":
            return self._fetch_moonshot()
        elif platform_id == "openai":
            return self._fetch_openai_usage()
        # ...

    def _fetch_deepseek(self) -> Dict:
        # GET https://api.deepseek.com/user/balance
        pass

    def _fetch_moonshot(self) -> Dict:
        # GET https://api.moonshot.ai/v1/users/me/balance
        pass
```

---

*调研完成时间：2026-05-10*
