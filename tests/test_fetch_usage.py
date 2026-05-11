"""
测试 fetch_usage.py
Test fetch_usage.py

测试 Token 消耗数据抓取功能
Test token usage data fetching functionality
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import os
import sys
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from fetch_usage import BalanceFetcher


class TestBalanceFetcher(unittest.TestCase):
    """测试 Balance Fetcher / Test Balance Fetcher"""

    def setUp(self):
        """测试前准备"""
        self.mock_auth = {
            "deepseek": "sk-test-deepseek-key",
            "moonshot": "sk-test-moonshot-key"
        }

    @patch('fetch_usage.BalanceFetcher._load_auth')
    @patch('fetch_usage.requests.get')
    def test_fetch_deepseek_success(self, mock_get, mock_load_auth):
        """测试 DeepSeek 余额查询成功"""
        mock_load_auth.return_value = self.mock_auth

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "is_available": True,
            "balance_infos": [
                {
                    "currency": "CNY",
                    "total_balance": "110.00",
                    "granted_balance": "10.00",
                    "topped_up_balance": "100.00"
                }
            ]
        }
        mock_get.return_value = mock_response

        fetcher = BalanceFetcher()
        result = fetcher._fetch_platform("deepseek", fetcher.BALANCE_APIS["deepseek"])

        self.assertTrue(result["success"])
        self.assertEqual(result["balance"], 110.00)
        self.assertEqual(result["granted_balance"], 10.00)
        self.assertEqual(result["topped_up_balance"], 100.00)

    @patch('fetch_usage.BalanceFetcher._load_auth')
    @patch('fetch_usage.requests.get')
    def test_fetch_moonshot_success(self, mock_get, mock_load_auth):
        """测试 Kimi/Moonshot 余额查询成功"""
        mock_load_auth.return_value = self.mock_auth

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 0,
            "scode": "0x0",
            "status": True,
            "data": {
                "available_balance": 49.58894,
                "voucher_balance": 46.58893,
                "cash_balance": 3.00001
            }
        }
        mock_get.return_value = mock_response

        fetcher = BalanceFetcher()
        result = fetcher._fetch_platform("moonshot", fetcher.BALANCE_APIS["moonshot"])

        self.assertTrue(result["success"])
        self.assertEqual(result["balance"], 49.58894)
        self.assertEqual(result["voucher_balance"], 46.58893)

    @patch('fetch_usage.BalanceFetcher._load_auth')
    def test_fetch_without_api_key(self, mock_load_auth):
        """测试缺少 API Key 时报错"""
        mock_load_auth.return_value = {}

        fetcher = BalanceFetcher()
        results = fetcher.fetch_all(platforms=["deepseek"])

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0]["success"])
        self.assertIn("API Key", results[0].get("error", ""))

    @patch('fetch_usage.BalanceFetcher._load_auth')
    def test_fetch_all_no_platforms(self, mock_load_auth):
        """测试空平台列表"""
        mock_load_auth.return_value = self.mock_auth
        fetcher = BalanceFetcher()
        results = fetcher.fetch_all(platforms=[])
        self.assertEqual(len(results), 0)

    @patch('fetch_usage.BalanceFetcher._load_auth')
    @patch('fetch_usage.requests.get')
    def test_fetch_openai_usage(self, mock_get, mock_load_auth):
        """测试 OpenAI 用量查询"""
        mock_load_auth.return_value = {"openai_usage": "sk-admin-test-key"}

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "object": "bucket",
                    "start_time": 1736616660,
                    "end_time": 1736640000,
                    "results": [
                        {
                            "input_tokens": 141201,
                            "output_tokens": 9756,
                            "num_model_requests": 470
                        }
                    ]
                }
            ]
        }
        mock_get.return_value = mock_response

        fetcher = BalanceFetcher()
        result = fetcher._fetch_platform("openai_usage", fetcher.BALANCE_APIS["openai_usage"])

        self.assertTrue(result["success"])
        self.assertEqual(result["input_tokens"], 141201)
        self.assertEqual(result["output_tokens"], 9756)

    @patch('fetch_usage.BalanceFetcher._load_auth')
    @patch('fetch_usage.requests.get')
    def test_api_error_handling(self, mock_get, mock_load_auth):
        """测试 API 错误返回处理"""
        mock_load_auth.return_value = self.mock_auth

        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = '{"error": "invalid_api_key"}'
        mock_get.return_value = mock_response

        fetcher = BalanceFetcher()
        result = fetcher.fetch_all(platforms=["deepseek"])

        self.assertFalse(result[0]["success"])


class TestSaveResults(unittest.TestCase):
    """测试结果保存功能"""

    @patch('fetch_usage.BalanceFetcher._load_auth')
    @patch('fetch_usage.json.dump')
    @patch('fetch_usage.open', new_callable=unittest.mock.mock_open)
    def test_save_results(self, mock_file, mock_dump, mock_load_auth):
        """测试保存结果到 JSON"""
        mock_load_auth.return_value = {"deepseek": "sk-test"}

        fetcher = BalanceFetcher()
        # 模拟保存空结果
        fetcher.results = [{"test": "data"}]
        path = fetcher.save_results("output/test.json")
        self.assertIn("output/test.json", path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
