import os

import cv2
import numpy as np

from cv_utils import cv_imread, cv_imwrite, ASSETS_DIR, OUTPUTS_DIR

# 读图
path = os.path.join(ASSETS_DIR, "cat.jpg")
img = cv_imread(path)
assert img is not None, "读图失败"
h, w = img.shape[:2]
print("原图 shape:", img.shape)

# ==========================================================
# 1. cv2.resize：缩到 0.5 倍 和 放大 2 倍
# ==========================================================
# 方式一：指定缩放比例 fx, fy
small = cv2.resize(img, None, fx=0.5, fy=0.5)
large = cv2.resize(img, None, fx=2.0, fy=2.0)

# 方式二：指定目标尺寸 (宽, 高) —— 注意是 (W, H)！
small2 = cv2.resize(img, (w // 2, h // 2))
large2 = cv2.resize(img, (w * 2, h * 2))

print("缩小后 shape:", small.shape)   # 高宽都减半
print("放大后 shape:", large.shape)   # 高宽都翻倍

cv2.imshow('Small 0.5x', small)
cv2.imshow('Large 2x', large)

# ==========================================================
# 2. cv2.flip：水平、垂直翻转
# ==========================================================
flip_h = cv2.flip(img, 1)    # 水平翻转（左右镜像）
flip_v = cv2.flip(img, 0)    # 垂直翻转（上下镜像）
flip_both = cv2.flip(img, -1)  # 同时水平+垂直（旋转180°）

cv2.imshow('Flip Horizontal (1)', flip_h)
cv2.imshow('Flip Vertical (0)', flip_v)
cv2.imshow('Flip Both (-1)', flip_both)

# ==========================================================
# 3. warpAffine 平移：自己构造 2×3 矩阵
# ==========================================================
tx, ty = 100, 50              # 向右移100像素，向下移50像素

# 平移矩阵 M = [[1, 0, tx],
#               [0, 1, ty]]
M_translate = np.float32([[1, 0, tx],
                          [0, 1, ty]])

# 注意 dsize=(宽, 高)，不是 (高, 宽)！
translated = cv2.warpAffine(img, M_translate, (w, h))

cv2.imshow('Translated', translated)

# 小实验：如果想平移后不裁掉，输出画布开大一点
canvas = cv2.warpAffine(img, M_translate, (w + tx, h + ty))
cv2.imshow('Translated (bigger canvas)', canvas)

# ==========================================================
# 4. getRotationMatrix2D + warpAffine：绕中心旋转 30°
# ==========================================================
center = (w // 2, h // 2)      # 旋转中心 (x, y)
angle = 30                     # 逆时针 30°（正数=逆时针）
scale = 1.0                    # 缩放比例

M_rotate = cv2.getRotationMatrix2D(center, angle, scale)
print("旋转矩阵 shape:", M_rotate.shape)   # (2, 3)
print("旋转矩阵:\n", M_rotate)

rotated = cv2.warpAffine(img, M_rotate, (w, h))
cv2.imshow('Rotated 30 deg', rotated)

# ==========================================================
# 保存结果（可选，用中文路径安全的写法）
# ==========================================================
cv_imwrite(os.path.join(OUTPUTS_DIR, "resize_small.jpg"), small)
cv_imwrite(os.path.join(OUTPUTS_DIR, "flip_h.jpg"), flip_h)
cv_imwrite(os.path.join(OUTPUTS_DIR, "translated.jpg"), translated)
cv_imwrite(os.path.join(OUTPUTS_DIR, "rotated.jpg"), rotated)

cv2.waitKey(0)
cv2.destroyAllWindows()