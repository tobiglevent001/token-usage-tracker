#!/usr/bin/env python3
"""
异常检测器 / Anomaly Detector

检测 token 消耗异常并生成告警
Detect abnormal token usage and generate alerts
"""

import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class AnomalyDetector:
    """
    异常检测器
    Anomaly detector
    """
    
    def __init__(self, threshold_percent: float = 20.0):
        """
        初始化检测器
        Initialize detector
        
        Args:
            threshold_percent: 异常阈值百分比 / Anomaly threshold percentage
        """
        self.threshold_percent = threshold_percent
        self.alerts = []
    
    def detect(self, current_data: Dict, historical_data: List[Dict]) -> List[Dict]:
        """
        检测异常
        Detect anomalies
        
        Args:
            current_data: 当前数据 / Current data
            historical_data: 历史数据 / Historical data
            
        Returns:
            List[Dict]: 告警列表 / Alert list
        """
        self.alerts = []
        
        if not historical_data:
            return self.alerts
        
        # 计算历史平均值 / Calculate historical average
        avg_usage = self._calculate_average(historical_data)
        
        # 检测每个平台的异常 / Detect anomalies for each platform
        for platform_id, current_usage in current_data.items():
            if platform_id in avg_usage:
                avg = avg_usage[platform_id]
                percent_change = ((current_usage - avg) / avg) * 100 if avg > 0 else 0
                
                if abs(percent_change) > self.threshold_percent:
                    alert = {
                        "platform_id": platform_id,
                        "current_usage": current_usage,
                        "average_usage": avg,
                        "percent_change": round(percent_change, 2),
                        "severity": "high" if abs(percent_change) > 50 else "medium"
                    }
                    self.alerts.append(alert)
        
        return self.alerts
    
    def generate_alert_messages(self, platforms: Dict[str, Dict], language: str = "both") -> Dict[str, List[str]]:
        """
        生成告警消息
        Generate alert messages
        
        Args:
            platforms: 平台信息字典 / Platform info dictionary
            language: 语言选项 / Language option
            
        Returns:
            Dict[str, List[str]]: 告警消息字典 / Alert messages dictionary
        """
        messages = {"zh": [], "en": []}
        
        for alert in self.alerts:
            platform = platforms.get(alert["platform_id"], {})
            platform_name = platform.get("name", alert["platform_id"])
            platform_name_en = platform.get("name_en", alert["platform_id"])
            
            if language in ["zh", "both"]:
                direction = "增长" if alert["percent_change"] > 0 else "下降"
                messages["zh"].append(
                    f"{platform_name} 消耗异常{direction} ({alert['percent_change']:+.2f}%)"
                )
            
            if language in ["en", "both"]:
                direction = "increase" if alert["percent_change"] > 0 else "decrease"
                messages["en"].append(
                    f"{platform_name_en} usage {direction} ({alert['percent_change']:+.2f}%)"
                )
        
        return messages
    
    def _calculate_average(self, historical_data: List[Dict]) -> Dict[str, float]:
        """
        计算历史平均使用量
        Calculate historical average usage
        
        Args:
            historical_data: 历史数据 / Historical data
            
        Returns:
            Dict[str, float]: 平台ID -> 平均值 / Platform ID -> Average value
        """
        totals = {}
        counts = {}
        
        for entry in historical_data:
            for platform_id, usage in entry.items():
                if platform_id not in totals:
                    totals[platform_id] = 0.0
                    counts[platform_id] = 0
                
                totals[platform_id] += usage
                counts[platform_id] += 1
        
        return {
            platform_id: totals[platform_id] / counts[platform_id]
            for platform_id in totals
        }


if __name__ == "__main__":
    print("=" * 60)
    print("异常检测器 / Anomaly Detector")
    print("=" * 60)
    
    # 示例数据 / Example data
    current = {
        "deepseek": 150.0,
        "tencent-tokenhub": 80.0
    }
    
    historical = [
        {"deepseek": 100.0, "tencent-tokenhub": 70.0},
        {"deepseek": 110.0, "tencent-tokenhub": 75.0},
        {"deepseek": 105.0, "tencent-tokenhub": 72.0}
    ]
    
    detector = AnomalyDetector(threshold_percent=20.0)
    alerts = detector.detect(current, historical)
    
    if alerts:
        print("\n⚠️ 检测到异常 / Anomalies detected:")
        messages = detector.generate_alert_messages(
            {"deepseek": {"name": "DeepSeek", "name_en": "DeepSeek"}},
            language="both"
        )
        
        for msg in messages["zh"]:
            print(f"  - {msg}")
    else:
        print("\n✅ 无异常 / No anomalies")
