"""
测试 generate_report.py
Test generate_report.py

测试报告生成功能
Test report generation functionality
"""

import unittest
from unittest.mock import patch, MagicMock
import json
from pathlib import Path
import sys
import os

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate_report import ReportGenerator


class TestReportGenerator(unittest.TestCase):
    """测试报告生成器 / Test Report Generator"""

    def setUp(self):
        """测试前准备"""
        self.mock_data = [
            {
                "platform_id": "deepseek",
                "platform_name": "DeepSeek",
                "platform_name_en": "DeepSeek",
                "success": True,
                "currency": "CNY",
                "balance": 110.00,
                "granted_balance": 10.00,
                "topped_up_balance": 100.00,
                "timestamp": "2026-05-10T07:00:00"
            },
            {
                "platform_id": "moonshot",
                "platform_name": "Kimi/Moonshot",
                "platform_name_en": "Kimi/Moonshot",
                "success": True,
                "currency": "USD",
                "balance": 49.59,
                "voucher_balance": 46.59,
                "cash_balance": 3.00,
                "timestamp": "2026-05-10T07:00:00"
            }
        ]

    @patch('generate_report.ReportGenerator._load_data')
    @patch('generate_report.ReportGenerator._load_history')
    def test_generate_zh_report(self, mock_history, mock_load):
        """测试生成中文报告"""
        mock_load.return_value = self.mock_data
        mock_history.return_value = {"entries": []}

        generator = ReportGenerator()
        reports = generator.generate(language="zh")

        self.assertIn("zh", reports)
        report_zh = reports["zh"]

        # 检查关键信息
        self.assertIn("余额日报", report_zh)
        self.assertIn("DeepSeek", report_zh)
        self.assertIn("Kimi/Moonshot", report_zh)
        self.assertIn("人民币总额", report_zh)
        self.assertIn("美元总额", report_zh)

    @patch('generate_report.ReportGenerator._load_data')
    @patch('generate_report.ReportGenerator._load_history')
    def test_generate_en_report(self, mock_history, mock_load):
        """测试生成英文报告"""
        mock_load.return_value = self.mock_data
        mock_history.return_value = {"entries": []}

        generator = ReportGenerator()
        reports = generator.generate(language="en")

        self.assertIn("en", reports)
        report_en = reports["en"]

        # 检查关键信息
        self.assertIn("Balance Report", report_en)
        self.assertIn("DeepSeek", report_en)
        self.assertIn("Kimi/Moonshot", report_en)
        self.assertIn("CNY Total", report_en)
        self.assertIn("USD Total", report_en)

    @patch('generate_report.ReportGenerator._load_data')
    @patch('generate_report.ReportGenerator._load_history')
    def test_generate_bilingual(self, mock_history, mock_load):
        """测试生成双语报告"""
        mock_load.return_value = self.mock_data
        mock_history.return_value = {"entries": []}

        generator = ReportGenerator()
        reports = generator.generate(language="both")

        self.assertIn("zh", reports)
        self.assertIn("en", reports)
        self.assertEqual(len(reports), 2)

    @patch('generate_report.ReportGenerator._load_data')
    @patch('generate_report.ReportGenerator._load_history')
    def test_trend_with_history(self, mock_history, mock_load):
        """测试带历史数据的趋势分析"""
        mock_load.return_value = self.mock_data
        mock_history.return_value = {
            "entries": [
                {"date": "2026-05-08", "total_cny": 130.00, "total_usd": 55.00},
                {"date": "2026-05-09", "total_cny": 120.00, "total_usd": 52.00},
                {"date": "2026-05-10", "total_cny": 110.00, "total_usd": 49.59},
            ]
        }

        generator = ReportGenerator()
        reports = generator.generate(language="zh")

        report_zh = reports["zh"]
        self.assertIn("消耗趋势", report_zh)

    @patch('generate_report.ReportGenerator._load_data')
    @patch('generate_report.ReportGenerator._load_history')
    def test_save_reports(self, mock_history, mock_load):
        """测试保存报告到文件"""
        mock_load.return_value = self.mock_data
        mock_history.return_value = {"entries": []}

        generator = ReportGenerator()
        reports = generator.generate(language="both")

        with patch.object(generator, 'save', return_value=["file1.md", "file2.md"]) as mock_save:
            saved = generator.save(reports)
            self.assertEqual(len(saved), 2)

    @patch('generate_report.ReportGenerator._load_data')
    @patch('generate_report.ReportGenerator._load_history')
    def test_failed_platform_handling(self, mock_history, mock_load):
        """测试失败平台的报告处理"""
        data_with_error = [
            {
                "platform_id": "deepseek",
                "platform_name": "DeepSeek",
                "platform_name_en": "DeepSeek",
                "success": False,
                "error": "API Key not configured",
                "timestamp": "2026-05-10T07:00:00"
            }
        ]
        mock_load.return_value = data_with_error
        mock_history.return_value = {"entries": []}

        generator = ReportGenerator()
        reports = generator.generate(language="zh")

        self.assertIn("抓取失败", reports["zh"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
