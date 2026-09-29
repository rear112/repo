import os

import cv2
import numpy as np
import matplotlib.pyplot as plt

from cv_utils import cv_imread, ASSETS_DIR

# 读一张图（assets 素材，全项目统一从 ASSETS_DIR 取）
path = os.path.join(ASSETS_DIR, "cat.jpg")
img = cv_imread(path)
assert img is not None, "读图失败，检查路径"
print("图像 shape:", img.shape, "dtype:", img.dtype)

# ==========================================================
# 1. 打印某个像素的 BGR 值：img[100, 200]
# ==========================================================
pixel = img[100, 200]
print("像素 [100, 200] 的 BGR 值:", pixel)
print("  → B =", pixel[0], " G =", pixel[1], " R =", pixel[2])

# 为什么是“行在前”？
# OpenCV 图像是一个 numpy 数组，shape = (高度H, 宽度W, 通道C)
# img[y, x]  →  第 y 行、第 x 列
# 所以 img[100, 200] 表示“第100行、第200列”，即 y=100, x=200
# 顺序是 (行/高, 列/宽)，和数学里的 (x, y) 相反，容易搞混！

# 也可以分别取三个通道
print("B通道值:", img[100, 200, 0])
print("G通道值:", img[100, 200, 1])
print("R通道值:", img[100, 200, 2])

# ==========================================================
# 2. 裁剪 ROI：取图中间 1/4 区域并显示
# ==========================================================
h, w = img.shape[:2]          # 高、宽
# 中间 1/4：宽高各取一半，从 1/4 处开始
y1, y2 = h // 4, h * 3 // 4
x1, x2 = w // 4, w * 3 // 4
roi = img[y1:y2, x1:x2]       # 注意：切片是 [行范围, 列范围]
print("ROI shape:", roi.shape)

cv2.imshow('Original', img)
cv2.imshow('ROI (middle 1/4)', roi)
cv2.waitKey(0)

# ==========================================================
# 3. 通道拆分合并：split / merge
# ==========================================================
b, g, r = cv2.split(img)      # 拆成 3 个单通道（二维数组）
print("拆出的 B 通道 shape:", b.shape, "dtype:", b.dtype)   # (H, W)，二维

# 合并回去验证
merged = cv2.merge([b, g, r])
print("合并后是否与原图一致:", np.array_equal(img, merged))   # True

# 把蓝色通道单独显示成灰度图（单通道本身就是灰度图）
cv2.imshow('Blue Channel (gray)', b)
cv2.waitKey(0)

# 小技巧：只想显示蓝色，其余置0 → 得到一个"纯蓝"的图
only_blue = cv2.merge([b, np.zeros_like(g), np.zeros_like(r)])
cv2.imshow('Only Blue', only_blue)
cv2.waitKey(0)

cv2.destroyAllWindows()

# ==========================================================
# 4. BGR→RGB 后用 matplotlib 显示，对比 cv2.imshow
# ==========================================================
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 用 cv2.imshow 显示原图（OpenCV 认为数组是 BGR，所以颜色正常）
cv2.imshow('cv2.imshow (BGR treated as BGR)', img)

# 用 matplotlib 显示“没转换”的图 → 颜色会错（红蓝互换）
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title('matplotlib WITHOUT convert (BGR misread as RGB)')
plt.imshow(img)          # 直接把 BGR 当 RGB 显示 → 红蓝颠倒
plt.axis('off')

# 用 matplotlib 显示“转换后”的图 → 颜色正常
plt.subplot(1, 2, 2)
plt.title('matplotlib AFTER BGR->RGB')
plt.imshow(img_rgb)      # 正确转换后再显示 → 颜色正常
plt.axis('off')

plt.tight_layout()
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()