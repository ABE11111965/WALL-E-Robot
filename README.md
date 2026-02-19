# WALL-E-Robot: An Embodied AI Agent based on LLM and Edge Computing
> 基于多模态大模型与边缘计算的具身智能机器人系统

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Gemini API](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-orange.svg)](https://aistudio.google.com/)
[![Status](https://img.shields.io/badge/Status-Simulation%20Stage-brightgreen.svg)]()

## 📖 项目简介 (Introduction)
本项目旨在构建一个具有情感交互能力的具身智能机器人（以 WALL-E 为物理载体）。系统摒弃了传统的本地有限状态机交互，利用云端大语言模型（LLM）作为认知核心，结合数字信号处理（DSP）与逆运动学（Inverse Kinematics），在树莓派边缘节点上实现“语音-语义-情感-姿态”的端到端闭环反馈。

目前项目已完成 **软件仿真与数字孪生层 (Digital Twin Stage)** 的构建，正在向物理硬件层进行移植。

## 🏗️ 系统架构 (System Architecture)
系统采用高度解耦的模块化设计，分为三大核心子系统：

1. **认知引擎层 (Cognitive Engine):** - 接入 Gemini 多模态大模型，利用结构化输出（JSON Format）将自然语言解析为文本回复与枚举类情感标签 (e.g., `happy`, `curious`)。
2. **声学表现层 (Acoustic DSP):**
   - 结合 TTS 引擎与 SoX (Sound eXchange) 音频处理链。
   - 运用环形调制 (Ring Modulation) 与过载失真 (Overdrive) 算法，实时渲染出具有金属质感的机器人口音。
3. **运动学执行层 (Kinematics & Actuation):**
   - 构建虚拟舵机组，通过三次缓入缓出 (Cubic Ease-In-Out) 贝塞尔插值算法，将抽象情感标签映射为平滑的物理运动轨迹。

## 📂 核心代码结构 (Repository Structure)
```text
WALL-E-Robot/
├── simulation/                 # 数字孪生与软件仿真模块
│   ├── walle_brain.py          # LLM 认知与情感解析逻辑
│   ├── walle_voice.py          # TTS 与 SoX DSP 变声管道
│   ├── walle_kinematics.py     # 逆运动学与三次缓动物理引擎
│   └── walle_master.py         # 多线程并发调度主程序 (Main Loop)
├── hardware/                   # [WIP] 硬件驱动与部署模块
├── 3d_models/                  # [WIP] 打印结构件 STL 文件
└── README.md
