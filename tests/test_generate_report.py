"""
测试 generate_report.py
Test generate_report.py

测试报告生成功能
Test report generation functionality
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from pathlib import Path
import sys

# 添加 scripts 目录到路径 / Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate_report import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    """测试报告生成器 / Test Report Generator"""
    
    def setUp(self):
        """测试前准备 / Setup before tests"""
        self.mock_data = [
            {
                "platform_id": "deepseek",
                "platform_name": "DeepSeek",
                "platform_name_en": "DeepSeek",
                "success": True,
                "data": {
                    "total_tokens": 12100,
                    "cost": 4.30,
                    "requests": 89
                },
                "timestamp": "2026-05-10T07:00:00"
            },
            {
                "platform_id": "tencent-tokenhub",
                "platform_name": "腾讯云 TokenHub",
                "platform_name_en": "Tencent Cloud TokenHub",
                "success": True,
                "data": {
                    "total_tokens": 15230,
                    "cost": 8.20,
                    "requests": 123
                },
                "timestamp": "2026-05-10T07:00:00"
            }
        ]
    
    @patch('generate_report.ReportGenerator._load_data')
    def test_generate_zh_report(self, mock_load):
        """测试生成中文报告 / Test generating Chinese report"""
        mock_load.return_value = self.mock_data
        
        generator = ReportGenerator()
        generator.report_data = generator._process_data_for_test(self.mock_data)
        report_zh = generator._generate_zh_report()
        
        # 检查报告包含关键信息 / Check report contains key info
        self.assertIn("Token 消耗日报", report_zh)
        self.assertIn("DeepSeek", report_zh)
        self.assertIn("腾讯云 TokenHub", report_zh)
        self.assertIn("汇总", report_zh)
        self.assertIn("明细", report_zh)
    
    @patch('generate_report.ReportGenerator._load_data')
    def test_generate_en_report(self, mock_load):
        """测试生成英文报告 / Test generating English report"""
        mock_load.return_value = self.mock_data
        
        generator = ReportGenerator()
        generator.report_data = generator._process_data_for_test(self.mock_data)
        report_en = generator._generate_en_report()
        
        # 检查报告包含关键信息 / Check report contains key info
        self.assertIn("Token Usage Daily Report", report_en)
        self.assertIn("DeepSeek", report_en)
        self.assertIn("Tencent Cloud TokenHub", report_en)
        self.assertIn("Summary", report_en)
        self.assertIn("Platform Details", report_en)
    
    @patch('generate_report.ReportGenerator._load_data')
    def test_generate_bilingual(self, mock_load):
        """测试生成双语报告 / Test generating bilingual report"""
        mock_load.return_value = self.mock_data
        
        generator = ReportGenerator()
        reports = generator.generate(language="both")
        
        # 检查生成了两种语言的报告 / Check both language reports generated
        self.assertIn("zh", reports)
        self.assertIn("en", reports)
        self.assertEqual(len(reports), 2)
    
    def test_save_reports(self):
        """测试保存报告 / Test saving reports"""
        # 创建模拟报告 / Create mock reports
        reports = {
            "zh": "# 测试中文报告 / Test Chinese Report",
            "en": "# Test English Report"
        }
        
        generator = ReportGenerator()
        
        # 模拟保存 / Mock save
        with patch('pathlib.Path.open', unittest.mock.mock_open()) as mock_file:
            saved_files = generator.save(reports, output_dir="output")
            
            # 检查文件数量 / Check file count
            self.assertEqual(len(saved_files), 2)


if __name__ == '__main__':
    print("=" * 60)
    print("运行测试 / Running tests")
    print("=" * 60)
    unittest.main(verbosity=2)
