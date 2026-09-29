"""生成硬币计数练习图：灰底 + 若干亮"硬币"，含粘连和椒盐噪声。

用途：下午项目不用等实拍图，先生成合成图把流水线调通，
再换成实拍/网图验证泛化（提示：合成图上 Otsu 一定好使，实拍图不一定——这本身就是练习点）。
运行：python make_coin_image.py  →  输出 outputs/coins.png（含真值坐标，方便自己对数）
"""
import os
import random

import cv2
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRIPT_DIR, "outputs")
os.makedirs(OUT, exist_ok=True)

W, H = 800, 600
random.seed(7)          # 固定种子，每次生成同一张，方便复现调参
np.random.seed(7)

img = np.full((H, W), 60, dtype=np.uint8)                # 深灰背景
img += np.random.normal(0, 5, (H, W)).astype(np.uint8)   # 轻微高斯噪声

coins = []          # (cx, cy, r) 真值
attempts = 0
while len(coins) < 12 and attempts < 500:
    attempts += 1
    r = random.randint(25, 45)
    cx = random.randint(r + 5, W - r - 5)
    cy = random.randint(r + 5, H - r - 5)
    coins.append((cx, cy, r))                            # 允许粘连——这正是分水岭练习点

for cx, cy, r in coins:
    brightness = random.randint(150, 220)                # 硬币亮度略有差异，模拟光照
    cv2.circle(img, (cx, cy), r, brightness, -1)
    cv2.circle(img, (cx, cy), r, brightness - 40, 3)     # 边缘一圈暗一点，模拟立体感

# 椒盐噪声
mask = np.random.random((H, W))
img[mask < 0.001] = 255
img[mask > 0.999] = 0

ok, buf = cv2.imencode(".png", img)
buf.tofile(os.path.join(OUT, "coins.png"))

print("已生成:", os.path.join(OUT, "coins.png"))
print("硬币总数(真值):", len(coins))
for i, (cx, cy, r) in enumerate(sorted(coins), 1):
    print("  %2d: 中心(%4d, %4d) 半径 %d" % (i, cx, cy, r))
print("提示：你的流水线计数结果应等于 12。粘连的用 距离变换+分水岭 分开。")
