import cv2
import time
import os

# ==========================================================
# 1. 打开视频源（摄像头是幻影设备 → 用测试视频；修好后换回 cv2.VideoCapture(0)）
# ==========================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))   # 脚本所在目录（路径相对脚本，启动目录随便）
VIDEO_PATH = os.path.join(SCRIPT_DIR, "test_video.mp4")

cap = cv2.VideoCapture(VIDEO_PATH)

# 检查是否打开成功
if not cap.isOpened():
    print("无法打开视频源")
    exit()

# ==========================================================
# 2. 循环读帧 + 显示 + 算帧率
# ==========================================================
prev_time = time.time()        # 上一帧的时间戳

while True:
    # 读一帧：ret 是布尔值（成功与否），frame 是图像
    ret, frame = cap.read()

    if not ret:
        # 视频播完 → 回卷循环播放（摄像头模式不会走到这里）
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # ---------- 算实时帧率 ----------
    curr_time = time.time()
    dt = curr_time - prev_time          # 相邻两帧时间差（秒）
    fps = 1.0 / dt if dt > 0 else 0     # 帧率 = 1 / 时间差
    prev_time = curr_time

    # ---------- 把 FPS 画在画面上 ----------
    fps_text = "FPS: %.1f" % fps
    cv2.putText(frame, fps_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0), 2)

    # ---------- 显示 ----------
    cv2.imshow('Camera (press q to quit)', frame)

    # ---------- 按 q 退出 ----------
    # waitKey(1) 返回按键的 ASCII 码，没有按键返回 -1
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("退出")
        break

# ==========================================================
# 3. 释放资源
# ==========================================================
cap.release()                  # 释放摄像头
cv2.destroyAllWindows()        # 关闭所有窗口