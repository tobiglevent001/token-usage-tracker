#!/usr/bin/env python3
"""
报告生成器 / Report Generator

根据抓取的余额数据生成汇总报告
Generate summary report from fetched balance data
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class ReportGenerator:
    """
    报告生成器
    Report generator
    """

    def __init__(self, data_path: str = "output/balance_data.json",
                 history_path: str = "output/balance_history.json"):
        """
        初始化生成器

        Args:
            data_path: 当前余额数据文件路径
            history_path: 历史余额数据文件路径
        """
        self.data = self._load_data(data_path)
        self.history = self._load_history(history_path)
        self.report_data = {}

    def generate(self, language: str = "both") -> Dict[str, str]:
        """
        生成报告

        Args:
            language: 语言选项 ("zh", "en", "both")

        Returns:
            Dict[str, str]: 生成的报告
        """
        self._process_data()

        reports = {}
        if language in ["zh", "both"]:
            reports["zh"] = self._generate_zh_report()
        if language in ["en", "both"]:
            reports["en"] = self._generate_en_report()

        return reports

    def save(self, reports: Dict[str, str], output_dir: str = "output") -> List[str]:
        """保存报告到文件"""
        output_path = Path(__file__).parent.parent / output_dir
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = []

        for lang, content in reports.items():
            filename = output_path / f"report_{timestamp}_{lang}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            saved_files.append(str(filename))
            print(f"✅ 报告已保存: {filename}")

        return saved_files

    def _process_data(self):
        """处理原始数据"""
        total_cny = 0
        total_usd = 0
        platforms = []

        for item in self.data:
            if not item.get("success"):
                platforms.append({
                    "name": item.get("platform_name", item.get("platform_id", "Unknown")),
                    "name_en": item.get("platform_name_en", ""),
                    "error": item.get("error", "Unknown error"),
                    "success": False
                })
                continue

            balance = item.get("balance")
            currency = item.get("currency", "CNY")

            if balance is None:
                # OpenAI 等没有余额的平台，显示用量
                platforms.append({
                    "name": item.get("platform_name", ""),
                    "name_en": item.get("platform_name_en", ""),
                    "success": True,
                    "balance": None,
                    "currency": currency,
                    "note": item.get("note", ""),
                    "input_tokens": item.get("input_tokens", 0),
                    "output_tokens": item.get("output_tokens", 0),
                    "total_requests": item.get("total_requests", 0)
                })
                continue

            if currency == "CNY":
                total_cny += balance
            elif currency == "USD":
                total_usd += balance

            platform_info = {
                "name": item.get("platform_name", ""),
                "name_en": item.get("platform_name_en", ""),
                "success": True,
                "balance": balance,
                "currency": currency,
                "granted_balance": item.get("granted_balance", 0),
                "topped_up_balance": item.get("topped_up_balance", 0),
                "voucher_balance": item.get("voucher_balance", 0),
                "cash_balance": item.get("cash_balance", 0),
            }
            platforms.append(platform_info)

        # 计算趋势（从历史数据）
        trend = self._calculate_trend()

        self.report_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "total_cny": total_cny,
            "total_usd": total_usd,
            "total_cny_all": total_cny + total_usd * 7.2,
            "platforms": platforms,
            "trend": trend,
            "generated_at": datetime.now().isoformat()
        }

    def _calculate_trend(self) -> Dict:
        """从历史数据计算趋势"""
        if not self.history:
            return {
                "has_data": False,
                "message": "暂无历史数据，将在下次运行后生成趋势分析"
            }

        entries = self.history.get("entries", [])
        if len(entries) < 2:
            return {
                "has_data": False,
                "message": "需要至少 2 天数据才能计算趋势"
            }

        # 获取最近的记录
        recent = sorted(entries, key=lambda x: x.get("date", ""), reverse=True)[:7]

        balances = [e.get("total_cny", 0) for e in recent if e.get("total_cny") is not None]

        if len(balances) < 2:
            return {"has_data": False, "message": "数据不足"}

        # 计算日均消耗
        daily_change = balances[0] - balances[-1]
        days = len(balances)
        avg_daily = daily_change / days if days > 0 else 0

        return {
            "has_data": True,
            "daily_change": daily_change,
            "avg_daily": avg_daily,
            "last_balance": balances[0],
            "days_count": days
        }

    def _generate_zh_report(self) -> str:
        """生成中文报告"""
        d = self.report_data

        report = f"""# 📊 Token 余额日报 - {d['date']}

> 生成时间：{d['time']}

---

## 💰 余额总览

| 项目 | 金额 |
|------|------|
| 人民币总额 | **¥{d['total_cny']:.2f}** |
| 美元总额 | **${d['total_usd']:.2f}** |
| 折合人民币 | **¥{d['total_cny_all']:.2f}** |

"""

        # 趋势
        trend = d.get("trend", {})
        if trend.get("has_data"):
            arrow = "↓" if trend["daily_change"] < 0 else "↑"
            report += f"""
## 📈 消耗趋势

| 项目 | 数值 |
|------|------|
| 近 {trend['days_count']} 天变化 | {arrow} ¥{abs(trend['daily_change']):.2f} |
| 日均消耗 | ¥{abs(trend['avg_daily']):.2f}/天 |
| 最近余额 | ¥{trend['last_balance']:.2f} |

"""
        else:
            report += f"\n> ℹ️ {trend.get('message', '暂无趋势数据')}\n\n"

        # 平台明细
        report += """## 📋 平台明细

"""
        for i, p in enumerate(d['platforms'], 1):
            if not p.get("success"):
                report += f"### {i}. {p['name']}\n"
                report += f"❌ 抓取失败：{p.get('error', '未知错误')}\n\n"
                continue

            if p.get("balance") is None:
                report += f"### {i}. {p['name']}\n"
                report += f"- 📊 输入 Tokens: {p.get('input_tokens', 0):,}\n"
                report += f"- 📊 输出 Tokens: {p.get('output_tokens', 0):,}\n"
                report += f"- 📊 请求数: {p.get('total_requests', 0):,}\n"
                if p.get("note"):
                    report += f"- ℹ️ {p['note']}\n"
                report += "\n"
                continue

            currency = p.get("currency", "CNY")
            symbol = "¥" if currency == "CNY" else "$"
            balance = p["balance"]

            report += f"### {i}. {p['name']}\n"
            report += f"| 项目 | 金额 |\n|------|------|\n"
            report += f"| **总余额** | **{symbol}{balance:.2f}** |\n"

            if currency == "CNY":
                if p.get("granted_balance"):
                    report += f"| 赠送余额 | {symbol}{p['granted_balance']:.2f} |\n"
                if p.get("topped_up_balance"):
                    report += f"| 充值余额 | {symbol}{p['topped_up_balance']:.2f} |\n"
            elif currency == "USD":
                if p.get("voucher_balance"):
                    report += f"| 代金券 | {symbol}{p['voucher_balance']:.2f} |\n"
                if p.get("cash_balance"):
                    report += f"| 现金 | {symbol}{p['cash_balance']:.2f} |\n"

            report += "\n"

        report += f"---\n*报告由 Token Usage Tracker 自动生成 · {d['generated_at']}*\n"

        return report

    def _generate_en_report(self) -> str:
        """生成英文报告"""
        d = self.report_data

        report = f"""# 📊 Token Balance Report - {d['date']}

> Generated at: {d['time']}

---

## 💰 Balance Overview

| Item | Amount |
|------|--------|
| CNY Total | **¥{d['total_cny']:.2f}** |
| USD Total | **${d['total_usd']:.2f}** |
| Total (CNY) | **¥{d['total_cny_all']:.2f}** |

"""

        trend = d.get("trend", {})
        if trend.get("has_data"):
            arrow = "↓" if trend["daily_change"] < 0 else "↑"
            report += f"""
## 📈 Usage Trend

| Item | Value |
|------|-------|
| {trend['days_count']}-day change | {arrow} ¥{abs(trend['daily_change']):.2f} |
| Avg daily spend | ¥{abs(trend['avg_daily']):.2f}/day |
| Latest balance | ¥{trend['last_balance']:.2f} |

"""
        else:
            report += f"\n> ℹ️ {trend.get('message', 'No trend data yet')}\n\n"

        report += """## 📋 Platform Details

"""
        for i, p in enumerate(d['platforms'], 1):
            if not p.get("success"):
                report += f"### {i}. {p['name_en']}\n"
                report += f"❌ Failed: {p.get('error', 'Unknown error')}\n\n"
                continue

            if p.get("balance") is None:
                report += f"### {i}. {p['name_en']}\n"
                report += f"- 📊 Input Tokens: {p.get('input_tokens', 0):,}\n"
                report += f"- 📊 Output Tokens: {p.get('output_tokens', 0):,}\n"
                report += f"- 📊 Requests: {p.get('total_requests', 0):,}\n"
                if p.get("note"):
                    report += f"- ℹ️ {p['note']}\n"
                report += "\n"
                continue

            currency = p.get("currency", "CNY")
            symbol = "¥" if currency == "CNY" else "$"
            balance = p["balance"]

            report += f"### {i}. {p['name_en']}\n"
            report += f"| Item | Amount |\n|------|--------|\n"
            report += f"| **Total Balance** | **{symbol}{balance:.2f}** |\n"

            if currency == "CNY":
                if p.get("granted_balance"):
                    report += f"| Granted | {symbol}{p['granted_balance']:.2f} |\n"
                if p.get("topped_up_balance"):
                    report += f"| Topped Up | {symbol}{p['topped_up_balance']:.2f} |\n"
            elif currency == "USD":
                if p.get("voucher_balance"):
                    report += f"| Voucher | {symbol}{p['voucher_balance']:.2f} |\n"
                if p.get("cash_balance"):
                    report += f"| Cash | {symbol}{p['cash_balance']:.2f} |\n"

            report += "\n"

        report += f"---\n*Auto-generated by Token Usage Tracker · {d['generated_at']}*\n"

        return report

    def _load_data(self, path: str) -> List[Dict]:
        """加载余额数据"""
        full_path = Path(__file__).parent.parent / path

        if not full_path.exists():
            print(f"⚠️ 数据文件不存在: {full_path}")
            return []

        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_history(self, path: str) -> Dict:
        """加载历史数据"""
        full_path = Path(__file__).parent.parent / path

        if not full_path.exists():
            return {"entries": []}

        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_history(self, total_cny: float, total_usd: float):
        """保存历史记录（供趋势分析）"""
        history = self._load_history("output/balance_history.json")

        today = datetime.now().strftime("%Y-%m-%d")

        # 检查今天是否已有记录
        entries = history.get("entries", [])
        today_entry = next((e for e in entries if e.get("date") == today), None)

        if today_entry:
            today_entry["total_cny"] = total_cny
            today_entry["total_usd"] = total_usd
            today_entry["updated_at"] = datetime.now().isoformat()
        else:
            entries.append({
                "date": today,
                "total_cny": total_cny,
                "total_usd": total_usd,
                "created_at": datetime.now().isoformat()
            })

        history["entries"] = entries

        full_path = Path(__file__).parent.parent / "output" / "balance_history.json"
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        print(f"✅ 历史数据已保存: {full_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("📊 报告生成器 / Report Generator")
    print("=" * 60)

    generator = ReportGenerator()
    reports = generator.generate(language="both")

    for lang, content in reports.items():
        print(f"\n--- {lang.upper()} ---")
        print(content[:500] + "...")

    generator.save(reports)
