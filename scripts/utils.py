#!/usr/bin/env python3
"""
工具函数 / Utility Functions

提供通用的工具函数
Provide common utility functions
"""

import json
from typing import Dict, Any
from datetime import datetime

def load_json_file(file_path: str, default: Any = None) -> Dict:
    """
    加载 JSON 文件
    Load JSON file
    
    Args:
        file_path: 文件路径 / File path
        default: 默认值（文件不存在时返回）/ Default value (returned if file not found)
    
    Returns:
        Dict: JSON 数据 / JSON data
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        if default is not None:
            return default
        raise

def save_json_file(file_path: str, data: Any, indent: int = 2):
    """
    保存 JSON 文件
    Save JSON file
    
    Args:
        file_path: 文件路径 / File path
        data: 要保存的数据 / Data to save
        indent: 缩进空格数 / Indentation spaces
    """
    import os
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

def format_currency(amount: float, currency: str = "CNY") -> str:
    """
    格式化货币金额
    Format currency amount
    
    Args:
        amount: 金额 / Amount
        currency: 货币类型 / Currency type (CNY or USD)
    
    Returns:
        str: 格式化后的金额字符串 / Formatted currency string
    """
    if currency == "CNY":
        return f"¥{amount:.2f}"
    elif currency == "USD":
        return f"${amount:.2f}"
    return f"{amount:.2f}"

def calculate_percent_change(old_value: float, new_value: float) -> float:
    """
    计算百分比变化
    Calculate percent change
    
    Args:
        old_value: 旧值 / Old value
        new_value: 新值 / New value
    
    Returns:
        float: 百分比变化 / Percent change
    """
    if old_value == 0:
        return 100.0 if new_value > 0 else 0.0
    
    return ((new_value - old_value) / old_value) * 100

def get_trend_arrow(percent_change: float) -> str:
    """
    获取趋势箭头
    Get trend arrow
    
    Args:
        percent_change: 百分比变化 / Percent change
    
    Returns:
        str: 趋势箭头符号 / Trend arrow symbol
    """
    if percent_change > 0:
        return "↑"
    elif percent_change < 0:
        return "↓"
    return "→"

def timestamp_to_iso(timestamp: float = None) -> str:
    """
    时间戳转换为 ISO 格式
    Convert timestamp to ISO format
    
    Args:
        timestamp: 时间戳（默认当前时间）/ Timestamp (default: current time)
    
    Returns:
        str: ISO 格式时间字符串 / ISO format time string
    """
    if timestamp is None:
        return datetime.now().isoformat()
    return datetime.fromtimestamp(timestamp).isoformat()

def iso_to_readable(iso_str: str, language: str = "zh") -> str:
    """
    ISO 时间转换为可读格式
    Convert ISO time to readable format
    
    Args:
        iso_str: ISO 格式时间字符串 / ISO format time string
        language: 语言 / Language ("zh" or "en")
    
    Returns:
        str: 可读的时间字符串 / Readable time string
    """
    dt = datetime.fromisoformat(iso_str)
    
    if language == "zh":
        return dt.strftime("%Y年%m月%d日 %H:%M:%S")
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    # 示例用法 / Example usage
    print("=" * 60)
    print("工具函数测试 / Utility Functions Test")
    print("=" * 60)
    
    # 测试货币格式化 / Test currency formatting
    print(f"\n货币格式化 / Currency formatting:")
    print(f"  ¥{format_currency(1234.56, 'CNY')}")
    print(f"  {format_currency(1234.56, 'USD')}")
    
    # 测试百分比变化 / Test percent change
    print(f"\n百分比变化 / Percent change:")
    print(f"  100 -> 120: {calculate_percent_change(100, 120):+.2f}%")
    print(f"  100 -> 80: {calculate_percent_change(100, 80):+.2f}%")
    
    # 测试趋势箭头 / Test trend arrow
    print(f"\n趋势箭头 / Trend arrow:")
    print(f"  +20%: {get_trend_arrow(20)}")
    print(f"  -20%: {get_trend_arrow(-20)}")
    print(f"  0%: {get_trend_arrow(0)}")
    
    print(f"\n" + "=" * 60)
