#!/usr/bin/env python3
"""
Token Usage Tracker - 主入口脚本 / Main Entry Script

一条命令完成：抓取余额 → 生成报告
One command: fetch balance → generate report

用法 / Usage:
    python scripts/run.py              # 抓取所有已配置平台
    python scripts/run.py --platforms deepseek moonshot  # 指定平台
    python scripts/run.py --lang zh     # 只生成中文报告
"""

import sys
import json
import argparse
from pathlib import Path

# 添加脚本目录到 path
sys.path.insert(0, str(Path(__file__).parent))

from fetch_usage import BalanceFetcher
from generate_report import ReportGenerator


def main():
    parser = argparse.ArgumentParser(description="Token Usage Tracker")
    parser.add_argument("--platforms", nargs="+", default=None,
                        help="要抓取的平台列表 (默认: deepseek, moonshot)")
    parser.add_argument("--lang", default="both",
                        choices=["zh", "en", "both"],
                        help="报告语言 (默认: both)")
    parser.add_argument("--auth", default=None,
                        help="auth.json 文件路径")
    parser.add_argument("--no-history", action="store_true",
                        help="不保存历史数据")
    args = parser.parse_args()

    print("=" * 60)
    print("🚀 Token Usage Tracker")
    print("=" * 60)
    print()

    # 1. 抓取余额数据
    print("📡 [1/3] 抓取余额数据...")
    fetcher = BalanceFetcher(auth_path=args.auth)

    platforms = args.platforms if args.platforms else ["deepseek", "moonshot"]
    results = fetcher.fetch_all(platforms=platforms)

    if not results:
        print("❌ 没有抓取到任何数据，请检查配置")
        sys.exit(1)

    # 保存抓取结果
    fetcher.save_results()

    # 2. 生成报告
    print()
    print("📝 [2/3] 生成报告...")
    generator = ReportGenerator()
    reports = generator.generate(language=args.lang)
    saved_files = generator.save(reports)

    # 3. 保存历史数据
    if not args.no_history:
        print()
        print("💾 [3/3] 保存历史数据...")
        generator.save_history(
            total_cny=generator.report_data.get("total_cny", 0),
            total_usd=generator.report_data.get("total_usd", 0)
        )

    # 打印汇总
    print()
    fetcher.print_summary()

    print()
    print("📄 报告文件:")
    for f in saved_files:
        print(f"   → {f}")

    print()
    print("=" * 60)
    print("✅ 完成！/ Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
