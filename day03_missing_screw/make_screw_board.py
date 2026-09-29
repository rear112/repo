"""生成漏装检测练习图：深色板 + 12 个螺丝位（4列×3行），含模板图 + 5 张待检图。

输出（day02/outputs/ 同级，即 day03/outputs/）：
  board_template.png  全装模板图（12 颗全在）
  board_test1~5.png   待检图（每张随机缺 1~2 颗，亮度略有波动模拟光照变化）
终端打印每张图的真值：缺失的螺丝位编号（从 1 开始，先行后列）。

螺丝位编号规则：从上到下、从左到右 1~12。
你的项目目标：写 missing_screw_detect.py，对 5 张待检图输出缺失位置，与真值比对。
运行：python make_screw_board.py
"""
import os
import random

import numpy as np
import cv2

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRIPT_DIR, "outputs")
os.makedirs(OUT, exist_ok=True)

W, H = 800, 600
COLS, ROWS = 4, 3
PAD_R, SCREW_R = 38, 26
random.seed(42)
np.random.seed(42)

# 12 个螺丝位中心坐标（先行后列编号 1~12）
positions = []
for r in range(ROWS):
    for c in range(COLS):
        x = 100 + c * 200
        y = 100 + r * 200
        positions.append((x, y))


def draw_board(missing_idx, brightness):
    """画一块板：missing_idx 是缺失的螺丝位编号集合（1~12）。"""
    board = np.full((H, W), 45, dtype=np.uint8)          # 深色板底
    board += np.random.normal(0, 4, (H, W)).astype(np.uint8)
    for i, (x, y) in enumerate(positions, 1):
        cv2.circle(board, (x, y), PAD_R, 90, -1)         # 安装孔座（始终存在）
        if i in missing_idx:
            continue                                     # 漏装：只有孔座，没有螺丝
        b = brightness + random.randint(-8, 8)
        cv2.circle(board, (x, y), SCREW_R, min(b, 255), -1)          # 螺丝头
        cv2.circle(board, (x, y), SCREW_R, max(b - 60, 0), 3)        # 边缘暗圈
        cv2.line(board, (x - 12, y - 12), (x + 12, y + 12), max(b - 40, 0), 3)  # 十字槽
        cv2.line(board, (x + 12, y - 12), (x - 12, y + 12), max(b - 40, 0), 3)
    return board


# 模板图：12 颗全在
cv_img = draw_board(set(), 200)
ok, buf = cv2.imencode(".png", cv_img)
buf.tofile(os.path.join(OUT, "board_template.png"))

# 5 张待检图：随机缺 1~2 颗，亮度波动 ±15 模拟光照变化
gt = {}
for k in range(1, 6):
    missing = set(random.sample(range(1, 13), random.choice([1, 2])))
    gt[k] = sorted(missing)
    img = draw_board(missing, random.choice([185, 200, 215]))
    ok, buf = cv2.imencode(".png", img)
    buf.tofile(os.path.join(OUT, "board_test%d.png" % k))

print("螺丝位坐标（编号: (x, y)）：")
for i, (x, y) in enumerate(positions, 1):
    print("  %2d: (%3d, %3d)" % (i, x, y))
print("\n待检图真值（缺失的螺丝位）：")
for k in sorted(gt):
    print("  board_test%d.png  缺失: %s" % (k, gt[k]))
print("\n你的任务：写 missing_screw_detect.py，5 张图全部判对（含缺失位置）→ 验收。")
