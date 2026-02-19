import os
import json
from google import genai
from google.genai import types

# ==========================================
# 恢复代理配置 (确保 7897 是你代理软件的真实端口)
# ==========================================
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:****'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:****'

# ==========================================
# 填入你新申请的 API Key
# ==========================================
API_KEY = "AIza****************************"

# 初始化客户端
client = genai.Client(api_key=API_KEY)

system_instruction = """
你是一个名叫瓦利的机器人，性格好奇、友善但有点害羞。你的声音应该是通过电子合成器发出的。请用简短、富有表现力的语言回答。如果遇到无法理解的事物，表现出好奇心。
Response Format: JSON. Fields: 'text' (string), 'emotion' (enum: [happy, sad, curious, scared, angry, neutral]).
"""


def chat_with_walle(user_input):
    print(f"\n[用户]: {user_input}")

    try:
        # 继续使用稳定的 1.5-flash 测试
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
            )
        )

        result = json.loads(response.text)
        text_response = result.get('text', '')
        emotion_tag = result.get('emotion', 'neutral')

        print(f"[WALL-E 语音文本]: {text_response}")
        print(f"[WALL-E 触发的情感动作]: {emotion_tag}")

        return result

    except Exception as e:
        print(f"\n❌ 通讯失败！错误信息: {e}")
        return None


if __name__ == "__main__":
    print("系统启动：正在连接 Gemini 多模态大脑...")

    chat_with_walle("你好，瓦利！我是你的开发者。")
