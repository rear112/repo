import os

import cv2
import numpy as np

from cv_utils import cv_imread, cv_imwrite, ASSETS_DIR, OUTPUTS_DIR

path = os.path.join(ASSETS_DIR, "cat.jpg")
img = cv_imread(path)
assert img is not None, "读图失败"

# ==========================================================
# 1. 拆通道（BGR 顺序！）
# ==========================================================
b = img[:, :, 0]
g = img[:, :, 1]
r = img[:, :, 2]

# ==========================================================
# 2. 构造布尔掩码：蓝色明显高于其他通道
# ==========================================================
# 条件1：蓝色分量本身够大（够亮）
# 条件2：蓝比红明显大
# 条件3：蓝比绿明显大
mask = (b > 100) & (b > r + 30) & (b > g + 30)
# mask 是 shape=(H,W) 的布尔矩阵，True=保留，False=置灰

print("mask shape:", mask.shape, " dtype:", mask.dtype)
print("蓝色像素占比: %.2f%%" % (mask.sum() / mask.size * 100))

# ==========================================================
# 3. 构造灰度图作为"背景"
# ==========================================================
# 用加权公式转标准灰度（也可以简单用均值）
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # (H,W)
# 转成三通道，方便赋值
gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)   # (H,W,3)

# ==========================================================
# 4. 用布尔索引抠图：True 保留原色，False 用灰度
# ==========================================================
result = gray_3ch.copy()          # 先全置灰
result[mask] = img[mask]          # 再把蓝色区域的像素换回原色

# ★ 核心就是这两行：
#   result[mask]  → 取出所有 True 位置的像素
#   img[mask]     → 取出原图对应位置的像素
#   赋值回去     → 完成"按颜色筛选"

# ==========================================================
# 5. 显示与保存
# ==========================================================
cv2.imshow("Mask (white=blue pixels)", (mask * 255).astype(np.uint8))
cv2.imshow("Original", img)
cv2.imshow("Blue kept, others gray", result)
cv_imwrite(os.path.join(OUTPUTS_DIR, "blue_mask_result.jpg"), result)
cv_imwrite(os.path.join(OUTPUTS_DIR, "blue_mask.png"),
           (mask * 255).astype(np.uint8))

cv2.waitKey(0)
cv2.destroyAllWindows()