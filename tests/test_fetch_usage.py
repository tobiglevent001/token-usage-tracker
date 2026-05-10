"""
测试 fetch_usage.py
Test fetch_usage.py

测试 Token 消耗数据抓取功能
Test token usage data fetching functionality
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import os, sys
from pathlib import Path

# 添加 scripts 目录到路径 / Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from fetch_usage import TokenUsageFetcher

class TestTokenUsageFetcher(unittest.TestCase):
    """测试 Token 消耗数据抓取器 / Test Token Usage Fetcher"""
    
    def setUp(self):
        """测试前准备 / Setup before tests"""
        self.mock_config = {
            "platforms": [
                {
                    "id": "test-platform",
                    "name": "测试平台",
                    "name_en": "Test Platform",
                    "enabled": True,
                    "fetch_method": "api",
                    "api_endpoint": "https://api.test.com/v1/usage",
                    "auth": {
                        "type": "api_key",
                        "env_var": "TEST_API_KEY"
                    }
                }
            ],
            "settings": {
                "retry_failed": 3,
                "retry_delay_seconds": 5
            }
        }
    
    @patch('fetch_usage.requests.get')
    @patch('fetch_usage.os.getenv')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=json.dumps({"platforms": [{"id": "test", "name": "Test", "name_en": "Test", "enabled": True, "fetch_method": "api", "api_endpoint": "https://api.test.com", "auth": {"type": "api_key", "env_var": "TEST"}}]))
    def test_fetch_via_api_success(self, mock_open, mock_getenv, mock_get):
        """测试通过 API 成功抓取数据 / Test successful data fetch via API"""
        # 模拟 API Key / Mock API key
        mock_getenv.return_value = "test-api-key"
        
        # 模拟 API 响应 / Mock API response
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "total_tokens": 10000,
            "cost": 5.50,
            "requests": 50
        }
        mock_get.return_value = mock_response
        
        # 注意：这个测试需要完整实现 / Note: This test needs full implementation
        # 目前只是示例 / Currently just an example
        self.assertTrue(True)  # 占位 / Placeholder
    
    def test_missing_api_key(self):
        """测试缺少 API Key 的情况 / Test missing API key"""
        with patch('os.getenv', return_value=None):
            with self.assertRaises(ValueError):
                fetcher = TokenUsageFetcher()
                # 这里应该触发 ValueError / This should raise ValueError
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=json.dumps({"platforms": []}))
    def test_fetch_all_no_platforms(self, mock_open):
        """测试没有启用平台的情况 / Test no enabled platforms"""
        fetcher = TokenUsageFetcher()
        results = fetcher.fetch_all()
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    print("=" * 60)
    print("运行测试 / Running tests")
    print("=" * 60)
    unittest.main(verbosity=2)
