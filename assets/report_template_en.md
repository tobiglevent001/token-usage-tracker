---
┌─────────────────────────────────────────────┐
│ Token Balance Report - {{date}}            │
│ Generated: {{generated_at}}                 │
└─────────────────────────────────────────────┘

📊 Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Today: ${{total_cost_usd}}
  vs Yesterday: {{trend_arrow}} {{change_percent}}%
  Month Total: ${{month_total_usd}}
  Budget Used: {{budget_percent}}% (Budget: ${{budget_usd}})

📋 Platform Details
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% for platform in platforms %}
{{loop.index}}. {{platform.name}}
   • Tokens: {{"{:0,d}".format(platform.tokens)}}
   • Cost: ¥{{"{:.2f}".format(platform.cost_cny)}} (${{"{:.2f}".format(platform.cost_usd)}})
   • Requests: {{"{:0,d}".format(platform.requests)}}
{% endfor %}

📈 Trend Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7-day Average: ¥{{"{:.2f}".format(week_avg_cny)}} (${{"{:.2f}".format(week_avg_usd)}})
  30-day Average: ¥{{"{:.2f}".format(month_avg_cny)}} (${{"{:.2f}".format(month_avg_usd)}})
  Predicted Month-end: ¥{{"{:.2f}".format(predicted_total_cny)}} (${{"{:.2f}".format(predicted_total_usd)}})

---
Generated: {{generated_at}} | Data Source: {{data_sources}}
