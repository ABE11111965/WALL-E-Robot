import os
import json
import pyttsx3
import subprocess
import threading
from google import genai
from google.genai import types

# 引入你刚才写好的运动学模块
from simulation.walle_kinematics import WalleKinematics

# ==========================================
# 1. 大脑配置 (直连模式，无代理)
# ==========================================
API_KEY = "AIzaSyCR6E1QEthuGzgLID8MX9U2hy0QsBpcM90"
client = genai.Client(api_key=API_KEY)

system_instruction = """
你是一个名叫瓦利的机器人，性格好奇、友善但有点害羞。你的声音应该是通过电子合成器发出的。请用简短、富有表现力的语言回答。如果遇到无法理解的事物，表现出好奇心。
Response Format: JSON. Fields: 'text' (string), 'emotion' (enum: [happy, sad, curious, scared, angry, neutral]).
"""


# ==========================================
# 2. 发声管道配置
# ==========================================
def generate_and_play_walle_voice(text):
    normal_wav = "temp_normal.wav"
    walle_wav = "temp_walle.wav"

    if os.path.exists(normal_wav): os.remove(normal_wav)
    if os.path.exists(walle_wav): os.remove(walle_wav)

    try:
        # TTS生成
        engine = pyttsx3.init()
        engine.setProperty('rate', 140)
        engine.save_to_file(text, normal_wav)
        engine.runAndWait()

        # SoX DSP处理
        sox_cmd = ["sox", normal_wav, walle_wav, "overdrive", "10", "echo", "0.8", "0.8", "5", "0.7", "synth", "sine",
                   "fmod", "30"]
        subprocess.run(sox_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 播放声音
        os.startfile(walle_wav)
    except Exception as e:
        pass  # 仿真阶段忽略次要音频报错


# ==========================================
# 3. 主循环与并发调度
# ==========================================
def main():
    print("==================================================")
    print("🤖 WALL-E 具身智能引擎 [完全体仿真版] 已上线")
    print("包含：Gemini 云端大脑 | DSP 变声 | 运动学并发引擎")
    print("==================================================")

    # 初始化虚拟机器人的身体
    robot_body = WalleKinematics()

    while True:
        user_input = input("\n[开发者 (输入 'q' 退出)]: ")

        if user_input.lower() in ['q', 'quit', 'exit']:
            print("系统关闭。晚安，瓦利。")
            break
        if not user_input.strip():
            continue

        try:
            # --- 思考阶段 ---
            print("🧠 瓦利正在思考...")
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

            print(f"\n[决定情绪]: {emotion_tag.upper()}")
            print(f"[输出文本]: {text_response}\n")

            # --- 执行阶段 (并发多线程) ---
            # 1. 开启一个独立的后台线程去处理并播放音频
            voice_thread = threading.Thread(target=generate_and_play_walle_voice, args=(text_response,))
            voice_thread.start()

            # 2. 主线程同时执行舵机的物理缓动计算
            robot_body.apply_emotion(emotion_tag)
            robot_body.execute_movement(duration=1.5)

            # 等待声音播放完毕再进入下一轮对话
            voice_thread.join()

        except Exception as e:
            print(f"\n❌ 系统异常: {e}")


if __name__ == "__main__":
    main()