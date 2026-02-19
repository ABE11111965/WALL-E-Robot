import time


class VirtualServo:
    def __init__(self, name, initial_angle=90.0):
        self.name = name
        self.current_angle = initial_angle
        self.target_angle = initial_angle
        self.start_angle = initial_angle

    def set_target(self, angle):
        """设定新的目标角度，并记录当前角度作为插值起点"""
        self.start_angle = self.current_angle
        self.target_angle = angle


class WalleKinematics:
    def __init__(self):
        # 初始化 WALL-E 的核心关节 (假设 90 度为中位/中立姿态)
        # 颈部云台机制 (Pan-Tilt)
        self.neck_pan = VirtualServo("颈部水平 (Pan)")
        self.neck_tilt = VirtualServo("颈部俯仰 (Tilt)")

        # 双目独立运动系统
        self.eye_left = VirtualServo("左眼")
        self.eye_right = VirtualServo("右眼")

        # 手臂
        self.arm_left = VirtualServo("左臂")
        self.arm_right = VirtualServo("右臂")

        self.servos = [self.neck_pan, self.neck_tilt, self.eye_left, self.eye_right, self.arm_left, self.arm_right]

    def apply_emotion(self, emotion):
        """
        基于语义的情感演绎映射逻辑 (参考工程报告 6.2)
        """
        print(f"\n[运动学引擎] 接收到情感指令: {emotion.upper()}，正在计算目标姿态...")

        if emotion == "happy":
            # 仰视, 外侧上扬(倒八字), 手臂张开
            self.neck_tilt.set_target(130.0)
            self.eye_left.set_target(120.0)
            self.eye_right.set_target(60.0)
            self.arm_left.set_target(140.0)
            self.arm_right.set_target(40.0)

        elif emotion == "sad":
            # 低头, 外侧下垂(八字), 手臂垂下
            self.neck_tilt.set_target(40.0)
            self.eye_left.set_target(60.0)
            self.eye_right.set_target(120.0)
            self.arm_left.set_target(40.0)
            self.arm_right.set_target(140.0)

        elif emotion == "curious":
            # 侧头, 眼睛一高一低, 手臂前伸
            self.neck_pan.set_target(60.0)
            self.eye_left.set_target(110.0)
            self.eye_right.set_target(110.0)
            self.arm_left.set_target(110.0)
            self.arm_right.set_target(110.0)

        else:  # neutral 恢复中立
            for servo in self.servos:
                servo.set_target(90.0)

    def cubic_ease_in_out(self, t):
        """缓动函数：保证舵机起步和停止时的平滑度"""
        if t < 0.5:
            return 4.0 * t * t * t
        else:
            p = 2.0 * t - 2.0
            return 0.5 * p * p * p + 1.0

    def execute_movement(self, duration=1.0):
        """
        执行动作插值循环。
        duration: 动作完成所需的总时间(秒)
        """
        fps = 50.0  # 控制循环频率应高于50Hz
        steps = int(duration * fps)
        sleep_time = 1.0 / fps

        print("\n--- 动作执行轨迹 (模拟 PCA9685 PWM 信号输出) ---")
        for step in range(steps + 1):
            t = step / float(steps)  # 归一化时间 0.0 -> 1.0
            eased_t = self.cubic_ease_in_out(t)

            # 清屏并打印当前帧的状态 (模拟终端UI)
            output = f"帧 [{step:02d}/{steps}] t={eased_t:.2f} | "
            for servo in self.servos:
                # 线性插值公式: current = start + (target - start) * eased_t
                servo.current_angle = servo.start_angle + (servo.target_angle - servo.start_angle) * eased_t
                output += f"{servo.name}: {servo.current_angle:>5.1f}° | "

            # 加上 \r 覆盖上一行，形成动画效果
            print(output, end="\r")
            time.sleep(sleep_time)
        print("\n--- 动作执行完毕 ---\n")


if __name__ == "__main__":
    robot_body = WalleKinematics()

    # 模拟从刚才的大脑逻辑中接收到了 "curious" 标签
    robot_body.apply_emotion("curious")
    robot_body.execute_movement(duration=1.5)  # 用 1.5 秒完成这个动作

    time.sleep(1)

    # 模拟情绪变化为 "happy"
    robot_body.apply_emotion("happy")
    robot_body.execute_movement(duration=1.0)