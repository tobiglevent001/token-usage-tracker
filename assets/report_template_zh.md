━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Token 消耗日报 - {{date}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【汇总 / Summary】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 今日总消耗 / Total Today: ¥{{total_cost_cny}}
• 昨日对比 / vs Yesterday: {{trend_arrow}} {{change_percent}}%
• 本月累计 / Month Total: ¥{{month_total_cny}}
• 预算执行 / Budget Used: {{budget_percent}}% (预算 / Budget ¥{{budget_cny}})

【平台明细 / Platform Details】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% for platform in platforms %}
{{loop.index}}. {{platform.name}}
   • Tokens: {{"{0:,d}".format(platform.tokens)}}
   • 消耗 / Cost: ¥{{"%.2f"|format(platform.cost_cny)}} (${{"%.2f"|format(platform.cost_usd)}})
   • 请求数 / Requests: {{"{0:,d}".format(platform.requests)}}
{% endfor %}

【异常告警 / Alerts】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% if alerts %}
{% for alert in alerts %}
⚠️ {{alert.message}}
{% endfor %}
{% else %}
✅ 无异常 / No anomalies
{% endif %}

【趋势分析 / Trend Analysis】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 7日平均 / 7-day Average: ¥{{"%.2f"|format(week_avg_cny)}} (${{"%.2f"|format(week_avg_usd)}})
• 30日平均 / 30-day Average: ¥{{"%.2f"|format(month_avg_cny)}} (${{"%.2f"|format(month_avg_usd)}})
• 预测月末 / Predicted Month-end: ¥{{"%.2f"|format(predicted_total_cny)}} (${{"%.2f"|format(predicted_total_usd)}})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
生成时间 / Generated: {{generated_at}} | 数据来源 / Data Source: {{data_sources}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
