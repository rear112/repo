import cv2
import time
import os

# ==========================================================
# 配置：全用变量，不写死
# ==========================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))   # 本文件所在目录（防坑：路径相对脚本而不是相对运行位置）
# 摄像头是幻影设备开不了 → 先用测试视频；修好后把 VIDEO_PATH 换回 0，即 cv2.VideoCapture(0)
VIDEO_PATH = os.path.join(SCRIPT_DIR, "test_video.mp4")
SAVE_DIR = os.path.join(SCRIPT_DIR, "snapshots")   # 截图保存目录
FPS_WINDOW = 30                 # 滑动平均窗口大小
FONT = cv2.FONT_HERSHEY_SIMPLEX
GREEN = (0, 255, 0)

os.makedirs(SAVE_DIR, exist_ok=True)   # 目录不存在就创建

# ==========================================================
# 打开摄像头
# ==========================================================
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("无法打开视频源")
    exit()

# ==========================================================
# 循环：读帧 + 算 FPS（滑动平均）+ 按键
# ==========================================================
prev_time = time.time()
fps_list = []                   # 存最近 N 帧的 fps，用于滑动平均

while True:
    ret, frame = cap.read()
    if not ret:
        # 视频源播完了 → 回卷到第 0 帧循环播放（换回摄像头模式后这里不会走到）
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # ---------- 算瞬时 FPS ----------
    curr_time = time.time()
    dt = curr_time - prev_time
    prev_time = curr_time
    fps = 1.0 / dt if dt > 0 else 0.0

    # ---------- 滑动平均 ----------
    fps_list.append(fps)
    if len(fps_list) > FPS_WINDOW:
        fps_list.pop(0)
    avg_fps = sum(fps_list) / len(fps_list)

    # ---------- 把 FPS 画到画面 ----------
    cv2.putText(frame, "FPS: %.1f" % avg_fps, (10, 30),
                FONT, 0.8, GREEN, 2)

    # ---------- 显示 ----------
    cv2.imshow("webcam_demo (s=shot, q=quit)", frame)

    # ---------- 按键处理 ----------
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):                 # 退出
        print("退出")
        break
    elif key == ord('s'):               # 截图
        ts = time.strftime("%Y%m%d_%H%M%S")        # 时间戳
        filename = os.path.join(SAVE_DIR, "shot_%s.jpg" % ts)
        cv2.imwrite(filename, frame)
        print("已截图:", filename)

# ==========================================================
# 释放资源
# ==========================================================
cap.release()
cv2.destroyAllWindows()