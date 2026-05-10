#!/usr/bin/env python3
"""
定时任务管理器 / Scheduler Manager

设置和管理定时任务，每天自动生成并推送 token 消耗日报
Set up and manage scheduled tasks to automatically generate and deliver token usage reports daily
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

class SchedulerManager:
    """
    定时任务管理器
    Scheduler manager
    """
    
    def __init__(self, config_path: str = "config/schedule.json"):
        """
        初始化管理器
        Initialize manager
        
        Args:
            config_path: 配置文件路径 / Config file path
        """
        self.config = self._load_config(config_path)
    
    def create_automation(self) -> Dict:
        """
        创建自动化任务（用于 WorkBuddy 的 automation_update 工具）
        Create automation task (for WorkBuddy's automation_update tool)
        
        Returns:
            Dict: 自动化任务配置 / Automation task configuration
        """
        if not self.config["enabled"]:
            return {"error": "定时任务已禁用 / Scheduler is disabled"}
        
        schedule = self.config["schedule"]
        
        # 构建 rrule / Build rrule
        rrule = self._build_rrule(schedule)
        
        automation_config = {
            "name": "Token Usage Daily Report",
            "description": "Automatically generate and deliver token usage daily report",
            "scheduleType": "recurring",
            "rrule": rrule,
            "prompt": self._build_prompt(),
            "status": "ACTIVE"
        }
        
        return automation_config
    
    def _build_rrule(self, schedule: Dict) -> str:
        """
        构建 RRULE 字符串
        Build RRULE string
        
        Args:
            schedule: 调度配置 / Schedule configuration
            
        Returns:
            str: RRULE 字符串 / RRULE string
        """
        time_parts = schedule["time"].split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        
        rrule = f"RRULE:FREQ=DAILY;BYHOUR={hour};BYMINUTE={minute}"
        
        return rrule
    
    def _build_prompt(self) -> str:
        """
        构建执行提示词
        Build execution prompt
        
        Returns:
            str: 提示词 / Prompt
        """
        language = self.config["schedule"].get("language", "both")
        
        prompt = """Run the token-usage-tracker skill to:
1. Fetch token usage data from all enabled platforms
2. Generate daily report with summary and details
3. Save report to output/ directory

Use bilingual output (Chinese + English) if language is set to "both".
"""
        
        return prompt
    
    def print_instructions(self):
        """
        打印手动设置定时任务的说明
        Print instructions for manual scheduler setup
        """
        config = self.create_automation()
        
        print("=" * 60)
        print("定时任务配置说明 / Scheduler Configuration Instructions")
        print("=" * 60)
        print("\n请使用以下配置创建自动化任务：")
        print("Please use the following configuration to create an automation task:\n")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        print("\n使用方法 / Usage:")
        print("在 WorkBuddy 中使用 automation_update 工具创建定时任务")
        print("Use the automation_update tool in WorkBuddy to create scheduled task\n")
    
    def _load_config(self, path: str) -> Dict:
        """
        加载配置文件
        Load configuration file
        
        Args:
            path: 配置文件路径 / Config file path
            
        Returns:
            Dict: 配置数据 / Configuration data
        """
        full_path = Path(__file__).parent.parent / path
        
        if not full_path.exists():
            raise FileNotFoundError(f"配置文件不存在 / Config file not found: {full_path}")
        
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)


if __name__ == "__main__":
    print("=" * 60)
    print("定时任务管理器 / Scheduler Manager")
    print("=" * 60)
    
    manager = SchedulerManager()
    manager.print_instructions()
