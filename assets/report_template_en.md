━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Token Usage Daily Report - {{date}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【Summary】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total Today: ¥{{total_cost_cny}} (${{total_cost_usd}})
• vs Yesterday: {{trend_arrow}} {{change_percent}}%
• Month Total: ¥{{month_total_cny}} (${{month_total_usd}})
• Budget Used: {{budget_percent}}% (Budget: ¥{{budget_cny}})

【Platform Details】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% for platform in platforms %}
{{loop.index}}. {{platform.name_en}}
   • Tokens: {{"{0:,d}".format(platform.tokens)}}
   • Cost: ¥{{"%.2f"|format(platform.cost_cny)}} (${{"%.2f"|format(platform.cost_usd)}})
   • Requests: {{"{0:,d}".format(platform.requests)}}
{% endfor %}

【Alerts】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% if alerts %}
{% for alert in alerts %}
⚠️ {{alert.message_en}}
{% endfor %}
{% else %}
✅ No anomalies
{% endif %}

【Trend Analysis】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 7-day Average: ¥{{"%.2f"|format(week_avg_cny)}} (${{"%.2f"|format(week_avg_usd)}})
• 30-day Average: ¥{{"%.2f"|format(month_avg_cny)}} (${{"%.2f"|format(month_avg_usd)}})
• Predicted Month-end: ¥{{"%.2f"|format(predicted_total_cny)}} (${{"%.2f"|format(predicted_total_usd)}})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: {{generated_at}} | Data Source: {{data_sources}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
