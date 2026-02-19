import pyttsx3
import subprocess
import os


# 1. 生成普通人声
def generate_normal_voice(text, output_file):
    print("1. 正在生成普通人类声音...")
    engine = pyttsx3.init()
    # 稍微调慢语速，机器人说话不宜太快
    engine.setProperty('rate', 140)
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    print(f"   普通声音已保存至: {output_file}")


# 2. 应用文档推荐的 DSP 配方
def apply_walle_dsp(input_file, output_file):
    print("2. 正在应用 SoX 变声算法 (环形调制 + 过载失真)...")
    # 这就是报告中提到的核心命令链
    sox_cmd = [
        "sox", input_file, output_file,
        "overdrive", "10",
        "echo", "0.8", "0.8", "5", "0.7",
        "synth", "sine", "fmod", "30"
    ]
    try:
        subprocess.run(sox_cmd, check=True)
        print(f"🎉 瓦利专属声音已生成: {output_file}")

        # 尝试在 Windows 下自动播放最终音频
        os.startfile(output_file)

    except FileNotFoundError:
        print("\n❌ 找不到 SoX！请确保你在 Windows 上安装了 SoX 并添加到了环境变量。")
    except Exception as e:
        print(f"\n❌ 处理出错: {e}")


if __name__ == "__main__":
    # 我们把你刚才跑通的句子拿来测试
    text = "你好，开发者！瓦利在这里…有什么要我做的吗？"

    normal_wav = "normal.wav"
    walle_wav = "walle.wav"

    # 确保之前没有残留文件干扰
    if os.path.exists(normal_wav): os.remove(normal_wav)
    if os.path.exists(walle_wav): os.remove(walle_wav)

    generate_normal_voice(text, normal_wav)
    apply_walle_dsp(normal_wav, walle_wav)