import cv2
import os

# ==========================================================
# 配置：全用变量，不写死数字
# ==========================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))   # 路径相对脚本，从哪个目录启动都行
VIDEO_PATH = os.path.join(SCRIPT_DIR, "test_video.mp4")
SAVE_DIR = os.path.join(SCRIPT_DIR, "archive_frames")        # 抽帧保存目录
SAVE_EVERY = 30                    # 每多少帧存一张
FONT = cv2.FONT_HERSHEY_SIMPLEX
GREEN = (0, 255, 0)

os.makedirs(SAVE_DIR, exist_ok=True)

# ==========================================================
# 打开视频文件（不是摄像头，换成路径即可）
# ==========================================================
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("无法打开视频:", VIDEO_PATH)
    exit()

# 读视频元信息（可选，打印出来看）
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
print("视频总帧数: %d, 帧率: %.1f" % (total_frames, fps))

# ==========================================================
# 循环读帧 + 每 SAVE_EVERY 帧抽一张
# ==========================================================
frame_idx = 0          # 当前帧号（从 0 开始）
saved_count = 0        # 已保存张数

while True:
    ret, frame = cap.read()
    if not ret:                     # 视频读完，ret=False
        print("视频播放完毕")
        break

    # ---------- 每隔 SAVE_EVERY 帧存一张 ----------
    if frame_idx % SAVE_EVERY == 0:
        filename = os.path.join(SAVE_DIR, "frame_%06d.jpg" % frame_idx)
        cv2.imwrite(filename, frame)
        saved_count += 1
        print("已保存第 %d 张: %s" % (saved_count, filename))   # 实时打印

    # ---------- 画面叠加帧号，方便观察 ----------
    cv2.putText(frame, "Frame: %d" % frame_idx, (10, 30),
                FONT, 0.8, GREEN, 2)
    cv2.imshow("Archive (playing)", frame)

    # ---------- 按 q 可提前退出 ----------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("手动提前退出")
        break

    frame_idx += 1

# ==========================================================
# 统计并退出
# ==========================================================
print("=" * 40)
print("共处理帧数: %d" % frame_idx)
print("共保存张数: %d" % saved_count)
print("保存目录: %s" % os.path.abspath(SAVE_DIR))
print("=" * 40)

cap.release()
cv2.destroyAllWindows()