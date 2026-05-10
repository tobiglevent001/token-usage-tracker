#!/usr/bin/env python3
"""
Token 消耗数据抓取器 / Token Usage Data Fetcher

支持多种抓取方式：
1. 余额查询 API（DeepSeek, Kimi/Moonshot 等）
2. 用量查询 API（OpenAI Admin API 等）
3. 浏览器抓取（腾讯云 TokenHub 等）
"""

import json
import os
import requests
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

class BalanceFetcher:
    """
    AI 平台余额抓取器
    AI Platform Balance Fetcher
    """

    # 各平台的余额 API 配置
    BALANCE_APIS = {
        "deepseek": {
            "name": "DeepSeek",
            "name_en": "DeepSeek",
            "endpoint": "https://api.deepseek.com/user/balance",
            "method": "GET",
            "env_var": "DEEPSEEK_API_KEY",
            "currency": "CNY",
            "parser": "_parse_deepseek"
        },
        "moonshot": {
            "name": "Kimi/Moonshot",
            "name_en": "Kimi/Moonshot",
            "endpoint": "https://api.moonshot.ai/v1/users/me/balance",
            "method": "GET",
            "env_var": "MOONSHOT_API_KEY",
            "currency": "USD",
            "parser": "_parse_moonshot"
        },
        "openai_usage": {
            "name": "OpenAI",
            "name_en": "OpenAI",
            "endpoint": "https://api.openai.com/v1/organization/usage/completions",
            "method": "GET",
            "env_var": "OPENAI_ADMIN_API_KEY",
            "currency": "USD",
            "parser": "_parse_openai_usage",
            "requires_admin": True
        }
    }

    def __init__(self, auth_path: str = None):
        """
        初始化抓取器

        Args:
            auth_path: auth.json 文件路径
        """
        self.auth = self._load_auth(auth_path)
        self.results = []

    def _load_auth(self, auth_path: str = None) -> Dict:
        """加载认证信息"""
        if auth_path:
            full_path = Path(auth_path)
        else:
            full_path = Path(__file__).parent.parent / "config" / "auth.json"

        if full_path.exists():
            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _get_api_key(self, platform_id: str, env_var: str) -> Optional[str]:
        """
        获取 API Key（优先从 auth.json，其次从环境变量）
        """
        # 1. 从 auth.json 获取
        if platform_id in self.auth:
            return self.auth[platform_id]

        # 2. 从环境变量获取
        return os.getenv(env_var)

    def fetch_all(self, platforms: List[str] = None) -> List[Dict]:
        """
        抓取所有平台的余额数据

        Args:
            platforms: 要抓取的平台列表，None 表示全部

        Returns:
            List[Dict]: 抓取结果
        """
        self.results = []

        to_fetch = platforms if platforms else list(self.BALANCE_APIS.keys())

        for platform_id in to_fetch:
            if platform_id not in self.BALANCE_APIS:
                print(f"⚠️ 未知平台: {platform_id}")
                continue

            config = self.BALANCE_APIS[platform_id]

            try:
                print(f"正在抓取: {config['name']}...")
                data = self._fetch_platform(platform_id, config)
                self.results.append(data)
                print(f"✅ {config['name']}: 余额 {data.get('balance', 'N/A')} {config['currency']}")
            except Exception as e:
                print(f"❌ {config['name']}: {str(e)}")
                self.results.append({
                    "platform_id": platform_id,
                    "platform_name": config["name"],
                    "platform_name_en": config["name_en"],
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })

        return self.results

    def _fetch_platform(self, platform_id: str, config: Dict) -> Dict:
        """
        抓取单个平台的数据
        """
        api_key = self._get_api_key(platform_id, config["env_var"])

        if not api_key:
            raise ValueError(f"缺少 API Key: 请在 auth.json 或环境变量 {config['env_var']} 中设置")

        # 发送请求
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.get(
            config["endpoint"],
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            raise ValueError(f"API 返回错误 {response.status_code}: {response.text[:200]}")

        # 解析响应
        raw_data = response.json()
        parser = getattr(self, config["parser"])
        parsed = parser(raw_data, config)

        return {
            "platform_id": platform_id,
            "platform_name": config["name"],
            "platform_name_en": config["name_en"],
            "success": True,
            "timestamp": datetime.now().isoformat(),
            **parsed
        }

    def _parse_deepseek(self, data: Dict, config: Dict) -> Dict:
        """
        解析 DeepSeek 余额响应

        响应格式：
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
        """
        is_available = data.get("is_available", False)
        balance_infos = data.get("balance_infos", [])

        result = {
            "api_available": is_available,
            "currency": config["currency"],
            "balance": 0,
            "granted_balance": 0,
            "topped_up_balance": 0
        }

        if balance_infos:
            info = balance_infos[0]
            result["balance"] = float(info.get("total_balance", "0").replace(",", ""))
            result["granted_balance"] = float(info.get("granted_balance", "0").replace(",", ""))
            result["topped_up_balance"] = float(info.get("topped_up_balance", "0").replace(",", ""))

        return result

    def _parse_moonshot(self, data: Dict, config: Dict) -> Dict:
        """
        解析 Kimi/Moonshot 余额响应

        响应格式：
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
        """
        status_code = data.get("code", -1)
        balance_data = data.get("data", {})

        return {
            "api_available": status_code == 0,
            "currency": config["currency"],
            "balance": balance_data.get("available_balance", 0),
            "voucher_balance": balance_data.get("voucher_balance", 0),
            "cash_balance": balance_data.get("cash_balance", 0)
        }

    def _parse_openai_usage(self, data: Dict, config: Dict) -> Dict:
        """
        解析 OpenAI 用量响应

        注意：OpenAI 没有余额查询 API，只有用量查询
        需要使用 Admin API Key
        """
        buckets = data.get("data", [])

        total_input_tokens = 0
        total_output_tokens = 0
        total_requests = 0

        for bucket in buckets:
            for result in bucket.get("results", []):
                total_input_tokens += result.get("input_tokens", 0)
                total_output_tokens += result.get("output_tokens", 0)
                total_requests += result.get("num_model_requests", 0)

        return {
            "api_available": True,
            "currency": config["currency"],
            "balance": None,  # OpenAI 无余额查询
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "total_requests": total_requests,
            "note": "OpenAI 仅提供用量查询，无余额查询 API"
        }

    def save_results(self, output_path: str = "output/balance_data.json"):
        """保存抓取结果"""
        full_path = Path(__file__).parent.parent / output_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"✅ 结果已保存到: {full_path}")
        return str(full_path)

    def print_summary(self):
        """打印汇总信息"""
        print("\n" + "=" * 60)
        print("📊 Token 余额汇总 / Balance Summary")
        print("=" * 60)

        total_balance = 0

        for r in self.results:
            if r.get("success") and r.get("balance") is not None:
                balance = r["balance"]
                currency = r.get("currency", "CNY")
                total_balance += balance if currency == "CNY" else balance * 7.2

                print(f"  {r['platform_name']}: {balance:.2f} {currency}")

        print("-" * 40)
        print(f"  总计（CNY）: ¥{total_balance:.2f}")
        print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Token 余额抓取器 / Token Balance Fetcher")
    print("=" * 60)
    print()

    fetcher = BalanceFetcher()

    # 默认抓取 DeepSeek 和 Kimi（这两个最简单）
    print("📡 开始抓取余额数据...")
    results = fetcher.fetch_all(platforms=["deepseek", "moonshot"])

    # 打印汇总
    fetcher.print_summary()

    # 保存结果
    fetcher.save_results()

    print("\n📁 详细结果:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
