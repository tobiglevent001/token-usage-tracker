#!/usr/bin/env python3
"""用 Python 生成配置界面的截图预览（SVG 格式）"""
import json
from pathlib import Path

# 读取模型列表
SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"

# 读取已配置平台
platforms = []
config_file = CONFIG_DIR / "platforms.json"
if config_file.exists():
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
        platforms = config.get("platforms", [])

# 读取 auth
auth_file = CONFIG_DIR / "auth.json"
auth = {}
if auth_file.exists():
    with open(auth_file, 'r', encoding='utf-8') as f:
        auth = json.load(f)

# 模型列表
models = [
    ("DeepSeek Chat", "DeepSeek"),
    ("DeepSeek Coder", "DeepSeek"),
    ("通义千问 Max", "阿里云 / Alibaba"),
    ("通义千问 Plus", "阿里云 / Alibaba"),
    ("GLM-4", "智谱 AI / Zhipu"),
    ("文心一言 4.0", "百度 / Baidu"),
    ("腾讯混元 Pro", "腾讯 / Tencent"),
    ("豆包 Pro", "字节跳动 / ByteDance"),
    ("Kimi Moonshot", "月之暗面 / Moonshot"),
    ("GPT-4", "OpenAI"),
    ("GPT-4 Turbo", "OpenAI"),
    ("GPT-3.5 Turbo", "OpenAI"),
    ("Claude 3 Opus", "Anthropic"),
    ("Claude 3 Sonnet", "Anthropic"),
    ("Claude 3 Haiku", "Anthropic"),
    ("Gemini Pro", "Google"),
    ("Gemini Ultra", "Google"),
    ("Llama 3 70B", "Meta"),
    ("Mistral Large", "Mistral AI"),
]

# 生成 SVG
model_options = ""
for i, (name, provider) in enumerate(models):
    y = 140 + i * 22
    bg = "#fff" if i % 2 == 0 else "#f8f9fa"
    model_options += f'<rect x="30" y="{y-8}" width="540" height="20" fill="{bg}"/>'
    model_options += f'<text x="40" y="{y+4}" font-size="11" fill="#333">{name}</text>'
    model_options += f'<text x="260" y="{y+4}" font-size="11" fill="#666">{provider}</text>'

# 已配置平台
platform_rows = ""
if platforms:
    for i, p in enumerate(platforms):
        y = 620 + i * 35
        pid = p.get("id", "")
        pname = p.get("name", pid)
        provider = p.get("provider", "")
        key_masked = p.get("api_key_masked", "")
        if pid in auth:
            k = auth[pid]
            key_masked = k[:4] + "****" + k[-4:] if len(k) > 8 else "****"
        
        platform_rows += f'''
        <rect x="30" y="{y}" width="540" height="30" rx="6" fill="#f0f9f4" stroke="#c3e6cb" stroke-width="1"/>
        <text x="45" y="{y+18}" font-size="12" font-weight="600" fill="#333">{pname}</text>
        <text x="160" y="{y+18}" font-size="11" fill="#666">{provider}</text>
        <text x="280" y="{y+18}" font-size="10" fill="#999">endpoint hidden</text>
        <text x="430" y="{y+18}" font-size="10" fill="#28a745" font-family="monospace">🔑 {key_masked}</text>
        <rect x="510" y="{y+5}" width="50" height="20" rx="4" fill="#dc3545"/>
        <text x="520" y="{y+19}" font-size="10" fill="white">删除</text>
        '''
else:
    platform_rows = '<text x="300" y="640" font-size="14" fill="#999" text-anchor="middle">📭 暂无配置的平台</text>'

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 750" width="600" height="750">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea"/>
      <stop offset="100%" style="stop-color:#764ba2"/>
    </linearGradient>
  </defs>
  
  <!-- 背景 -->
  <rect width="600" height="750" fill="url(#bg)"/>
  
  <!-- 头部 -->
  <rect x="20" y="15" width="560" height="70" rx="12" fill="white"/>
  <text x="300" y="45" font-size="20" font-weight="bold" fill="#667eea" text-anchor="middle">🚀 Token Usage Tracker</text>
  <text x="300" y="68" font-size="12" fill="#666" text-anchor="middle">配置你的 AI 模型和 API Key，开始追踪 token 消耗</text>
  
  <!-- 添加平台区域 -->
  <rect x="20" y="95" width="560" height="490" rx="12" fill="white"/>
  <line x1="20" y1="125" x2="580" y2="125" stroke="#667eea" stroke-width="2"/>
  <text x="35" y="115" font-size="16" font-weight="bold" fill="#333">📊 添加平台 / Add Platform</text>
  
  <!-- 选择模型 -->
  <text x="35" y="145" font-size="12" font-weight="600" fill="#333">选择模型 / Select Model</text>
  <rect x="30" y="150" width="540" height="28" rx="6" fill="#f8f9fa" stroke="#e9ecef" stroke-width="1"/>
  <text x="40" y="168" font-size="11" fill="#999">-- 请选择模型 / Please select a model --</text>
  
  <!-- 模型列表（下拉展开效果） -->
  <rect x="30" y="182" width="540" height="{19 * 22 + 10}" rx="6" fill="white" stroke="#e9ecef" stroke-width="1"/>
  {model_options}
  
  <!-- API Key -->
  <text x="35" y="{140 + 19 * 22 + 30}" font-size="12" font-weight="600" fill="#333">API Key</text>
  <rect x="30" y="{140 + 19 * 22 + 35}" width="540" height="28" rx="6" fill="#f8f9fa" stroke="#e9ecef" stroke-width="1"/>
  <text x="40" y="{140 + 19 * 22 + 53}" font-size="11" fill="#999">输入你的 API Key (例如: sk-...)</text>
  
  <!-- 按钮 -->
  <rect x="30" y="{140 + 19 * 22 + 72}" width="90" height="32" rx="6" fill="#ffc107"/>
  <text x="50" y="{140 + 19 * 22 + 92}" font-size="12" font-weight="600" fill="#333">🧪 测试</text>
  
  <rect x="130" y="{140 + 19 * 22 + 72}" width="90" height="32" rx="6" fill="#667eea"/>
  <text x="145" y="{140 + 19 * 22 + 92}" font-size="12" font-weight="600" fill="white">💾 保存</text>
  
  <rect x="230" y="{140 + 19 * 22 + 72}" width="90" height="32" rx="6" fill="#dc3545"/>
  <text x="245" y="{140 + 19 * 22 + 92}" font-size="12" font-weight="600" fill="white">🗑️ 清空</text>
  
  <!-- 自定义模型链接 -->
  <text x="35" y="{140 + 19 * 22 + 118}" font-size="12" fill="#667eea" text-decoration="underline">+ 添加自定义模型 / Add Custom Model</text>
  
  <!-- 已配置平台 -->
  <rect x="20" y="590" width="560" height="140" rx="12" fill="white"/>
  <line x1="20" y1="620" x2="580" y2="620" stroke="#667eea" stroke-width="2"/>
  <text x="35" y="610" font-size="16" font-weight="bold" fill="#333">📋 已配置平台 / Configured Platforms</text>
  
  {platform_rows}
</svg>
'''

output_path = SKILL_DIR / "assets" / "config_preview.svg"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(svg)

print(f"截图已保存到: {output_path}")
