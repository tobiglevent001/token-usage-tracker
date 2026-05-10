#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token Usage Tracker - Web Configuration Interface
提供可视化的配置界面，让用户可以轻松配置模型和 API Key
"""

from flask import Flask, request, jsonify, send_from_directory
import json
import os
import urllib.request
import urllib.error
from pathlib import Path

app = Flask(__name__)

# 配置文件路径
SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"
CONFIG_DIR.mkdir(exist_ok=True)

PLATFORMS_CONFIG = CONFIG_DIR / "platforms.json"
AUTH_CONFIG = CONFIG_DIR / "auth.json"

# 支持的模型列表（按主流程度排序，与前端保持一致）
SUPPORTED_MODELS = [
    # 国内主流模型
    {"id": "deepseek-chat", "name": "DeepSeek Chat", "provider": "DeepSeek 深度求索", "api_endpoint": "https://api.deepseek.com/v1/chat/completions", "api_key_env": "DEEPSEEK_API_KEY"},
    {"id": "deepseek-coder", "name": "DeepSeek Coder", "provider": "DeepSeek 深度求索", "api_endpoint": "https://api.deepseek.com/v1/chat/completions", "api_key_env": "DEEPSEEK_API_KEY"},
    {"id": "deepseek-reasoner", "name": "DeepSeek R1", "provider": "DeepSeek 深度求索", "api_endpoint": "https://api.deepseek.com/v1/chat/completions", "api_key_env": "DEEPSEEK_API_KEY"},
    {"id": "qwen-max", "name": "通义千问 Max", "provider": "阿里云 Alibaba", "api_endpoint": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "api_key_env": "DASHSCOPE_API_KEY"},
    {"id": "qwen-plus", "name": "通义千问 Plus", "provider": "阿里云 Alibaba", "api_endpoint": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "api_key_env": "DASHSCOPE_API_KEY"},
    {"id": "qwen-turbo", "name": "通义千问 Turbo", "provider": "阿里云 Alibaba", "api_endpoint": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "api_key_env": "DASHSCOPE_API_KEY"},
    {"id": "glm-4", "name": "GLM-4", "provider": "智谱AI Zhipu", "api_endpoint": "https://open.bigmodel.cn/api/paas/v4/chat/completions", "api_key_env": "GLM_API_KEY"},
    {"id": "glm-4-flash", "name": "GLM-4 Flash", "provider": "智谱AI Zhipu", "api_endpoint": "https://open.bigmodel.cn/api/paas/v4/chat/completions", "api_key_env": "GLM_API_KEY"},
    {"id": "ernie-4.0", "name": "文心一言 4.0", "provider": "百度 Baidu", "api_endpoint": "https://aip.baidu.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro", "api_key_env": "ERNIE_API_KEY"},
    {"id": "ernie-3.5", "name": "文心一言 3.5", "provider": "百度 Baidu", "api_endpoint": "https://aip.baidu.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions", "api_key_env": "ERNIE_API_KEY"},
    {"id": "hunyuan-pro", "name": "腾讯混元 Pro", "provider": "腾讯 Tencent", "api_endpoint": "https://hunyuan.tencentcloudapi.com", "api_key_env": "HUNYUAN_API_KEY"},
    {"id": "doubao-pro-32k", "name": "豆包 Pro 32K", "provider": "字节跳动 ByteDance", "api_endpoint": "https://ark.cn-beijing.volces.com/api/v3/chat/completions", "api_key_env": "DOUBAO_API_KEY"},
    {"id": "doubao-pro-128k", "name": "豆包 Pro 128K", "provider": "字节跳动 ByteDance", "api_endpoint": "https://ark.cn-beijing.volces.com/api/v3/chat/completions", "api_key_env": "DOUBAO_API_KEY"},
    {"id": "moonshot-v1-8k", "name": "Kimi v1 8K", "provider": "月之暗面 Moonshot", "api_endpoint": "https://api.moonshot.cn/v1/chat/completions", "api_key_env": "MOONSHOT_API_KEY"},
    {"id": "moonshot-v1-32k", "name": "Kimi v1 32K", "provider": "月之暗面 Moonshot", "api_endpoint": "https://api.moonshot.cn/v1/chat/completions", "api_key_env": "MOONSHOT_API_KEY"},
    {"id": "minimax-abab6.5", "name": "MiniMax abab6.5", "provider": "MiniMax", "api_endpoint": "https://api.minimax.chat/v1/text/chatcompletion_v2", "api_key_env": "MINIMAX_API_KEY"},
    {"id": "spark-v3.5", "name": "讯飞星火 v3.5", "provider": "科大讯飞 iFlytek", "api_endpoint": "https://spark-api.xf-yun.com/v3.5/chat", "api_key_env": "SPARK_API_KEY"},
    # 国际主流模型
    {"id": "gpt-4o", "name": "GPT-4o", "provider": "OpenAI", "api_endpoint": "https://api.openai.com/v1/chat/completions", "api_key_env": "OPENAI_API_KEY"},
    {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "OpenAI", "api_endpoint": "https://api.openai.com/v1/chat/completions", "api_key_env": "OPENAI_API_KEY"},
    {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "provider": "OpenAI", "api_endpoint": "https://api.openai.com/v1/chat/completions", "api_key_env": "OPENAI_API_KEY"},
    {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "OpenAI", "api_endpoint": "https://api.openai.com/v1/chat/completions", "api_key_env": "OPENAI_API_KEY"},
    {"id": "o1-preview", "name": "o1 Preview", "provider": "OpenAI", "api_endpoint": "https://api.openai.com/v1/chat/completions", "api_key_env": "OPENAI_API_KEY"},
    {"id": "o1-mini", "name": "o1 Mini", "provider": "OpenAI", "api_endpoint": "https://api.openai.com/v1/chat/completions", "api_key_env": "OPENAI_API_KEY"},
    {"id": "claude-3.5-sonnet", "name": "Claude 3.5 Sonnet", "provider": "Anthropic", "api_endpoint": "https://api.anthropic.com/v1/messages", "api_key_env": "ANTHROPIC_API_KEY"},
    {"id": "claude-3-opus", "name": "Claude 3 Opus", "provider": "Anthropic", "api_endpoint": "https://api.anthropic.com/v1/messages", "api_key_env": "ANTHROPIC_API_KEY"},
    {"id": "claude-3-haiku", "name": "Claude 3 Haiku", "provider": "Anthropic", "api_endpoint": "https://api.anthropic.com/v1/messages", "api_key_env": "ANTHROPIC_API_KEY"},
    {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "provider": "Google", "api_endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent", "api_key_env": "GEMINI_API_KEY"},
    {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "provider": "Google", "api_endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent", "api_key_env": "GEMINI_API_KEY"},
    {"id": "llama-3.1-70b", "name": "Llama 3.1 70B", "provider": "Meta (via Together)", "api_endpoint": "https://api.together.xyz/v1/chat/completions", "api_key_env": "TOGETHER_API_KEY"},
    {"id": "llama-3.1-405b", "name": "Llama 3.1 405B", "provider": "Meta (via Together)", "api_endpoint": "https://api.together.xyz/v1/chat/completions", "api_key_env": "TOGETHER_API_KEY"},
    {"id": "mistral-large", "name": "Mistral Large", "provider": "Mistral AI", "api_endpoint": "https://api.mistral.ai/v1/chat/completions", "api_key_env": "MISTRAL_API_KEY"},
    {"id": "mistral-medium", "name": "Mistral Medium", "provider": "Mistral AI", "api_endpoint": "https://api.mistral.ai/v1/chat/completions", "api_key_env": "MISTRAL_API_KEY"},
]


def load_config():
    """加载配置"""
    if PLATFORMS_CONFIG.exists():
        with open(PLATFORMS_CONFIG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"platforms": []}


def save_config(config):
    """保存配置"""
    with open(PLATFORMS_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_auth():
    """加载认证信息"""
    if AUTH_CONFIG.exists():
        with open(AUTH_CONFIG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_auth(auth):
    """保存认证信息"""
    with open(AUTH_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(auth, f, ensure_ascii=False, indent=2)


def test_api_connection(model_config, api_key):
    """实际调用 API 测试连接"""
    endpoint = model_config["api_endpoint"]
    provider = model_config.get("provider", "")
    model_id = model_config["id"]
    timeout = 15  # 秒

    try:
        # Anthropic 格式
        if "Anthropic" in provider:
            payload = json.dumps({
                "model": model_id,
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hi"}]
            }).encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01"
                }
            )

        # Google Gemini 格式
        elif "Google" in provider:
            url = endpoint + "?key=" + api_key
            payload = json.dumps({
                "contents": [{"parts": [{"text": "Hi"}]}],
                "generationConfig": {"maxOutputTokens": 10}
            }).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json"}
            )

        # OpenAI 兼容格式（大部分国内模型也用这个格式）
        else:
            payload = json.dumps({
                "model": model_id,
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hi"}]
            }).encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + api_key
                }
            )

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            return True, f"连接成功！状态码: {status}，模型: {model_config['name']}"

    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8")
            err_json = json.loads(error_body)
            err_msg = ""
            if "error" in err_json:
                err_msg = err_json["error"].get("message", "")
            elif "message" in err_json:
                err_msg = err_json["message"]
            if err_msg:
                return False, f"API 返回错误 {e.code}: {err_msg}"
        except Exception:
            pass
        if e.code == 401:
            return False, f"API Key 无效（401 未授权），请检查 Key 是否正确"
        elif e.code == 429:
            return False, f"请求频率限制（429），Key 有效但请求过快，请稍后重试"
        elif e.code == 403:
            return False, f"访问被拒绝（403），Key 可能没有该模型的权限"
        else:
            return False, f"API 返回错误 {e.code}: {e.reason}"

    except urllib.error.URLError as e:
        return False, f"网络错误: {str(e.reason)}"

    except Exception as e:
        return False, f"测试异常: {str(e)}"


@app.route('/')
def index():
    """配置界面首页"""
    return send_from_directory(SKILL_DIR / "assets", "config_interface.html")


@app.route('/api/models', methods=['GET'])
def get_models():
    """获取支持的模型列表"""
    return jsonify(SUPPORTED_MODELS)


@app.route('/api/config', methods=['GET'])
def get_config():
    """获取当前配置"""
    config = load_config()
    auth = load_auth()

    # 不返回完整的 API Key，只返回前4位和后4位
    for platform in config.get("platforms", []):
        platform_id = platform.get("id")
        if platform_id in auth:
            api_key = auth[platform_id]
            if len(api_key) > 8:
                platform["api_key_masked"] = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
            else:
                platform["api_key_masked"] = "*" * len(api_key)

    return jsonify(config)


@app.route('/api/config', methods=['POST'])
def update_config():
    """更新配置"""
    data = request.json
    config = load_config()
    auth = load_auth()

    # 更新平台配置
    if "platforms" in data:
        for platform in data["platforms"]:
            platform_id = platform.get("id")

            # 保存 API Key 到 auth.json
            if "api_key" in platform and platform["api_key"]:
                auth[platform_id] = platform["api_key"]

            # 移除 api_key 字段，不保存在 platforms.json 中
            if "api_key" in platform:
                del platform["api_key"]

        config["platforms"] = data["platforms"]

    save_config(config)
    save_auth(auth)

    return jsonify({"success": True, "message": "配置已保存 / Config saved"})


@app.route('/api/test', methods=['POST'])
def test_connection():
    """测试 API 连接（实际调用 API）"""
    data = request.json
    model_id = data.get("model_id")
    api_key = data.get("api_key")

    # 查找模型配置
    model_config = next((m for m in SUPPORTED_MODELS if m["id"] == model_id), None)

    if not model_config:
        return jsonify({"success": False, "message": "不支持的模型: " + str(model_id)})

    if not api_key:
        return jsonify({"success": False, "message": "API Key 不能为空"})

    # 实际调用 API 测试
    success, message = test_api_connection(model_config, api_key)

    return jsonify({"success": success, "message": message})


@app.route('/api/config/delete', methods=['POST'])
def delete_platform():
    """删除平台配置"""
    data = request.json
    platform_id = data.get("platform_id")

    config = load_config()
    config["platforms"] = [p for p in config.get("platforms", []) if p.get("id") != platform_id]
    save_config(config)

    # 同时删除 auth 中的 key
    auth = load_auth()
    if platform_id in auth:
        del auth[platform_id]
        save_auth(auth)

    return jsonify({"success": True, "message": "已删除 / Deleted"})


@app.route('/api/custom-model', methods=['POST'])
def add_custom_model():
    """添加自定义模型"""
    data = request.json

    required_fields = ["id", "name", "provider", "api_endpoint", "api_key_env"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"success": False, "message": "缺少必填字段: " + field})

    # 检查 ID 是否已存在
    if any(m["id"] == data["id"] for m in SUPPORTED_MODELS):
        return jsonify({"success": False, "message": "模型 ID 已存在: " + data["id"]})

    # 添加到模型列表
    SUPPORTED_MODELS.append({
        "id": data["id"],
        "name": data["name"],
        "provider": data["provider"],
        "api_endpoint": data["api_endpoint"],
        "api_key_env": data["api_key_env"],
        "custom": True
    })

    return jsonify({"success": True, "message": "自定义模型已添加: " + data["name"]})


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Token Usage Tracker - 配置界面")
    print("=" * 60)
    print("📍 访问地址: http://localhost:8888")
    print("📊 内置模型: {} 个".format(len(SUPPORTED_MODELS)))
    print("=" * 60 + "\n")

    app.run(host='0.0.0.0', port=8888, debug=False)
