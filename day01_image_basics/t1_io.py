import os

import cv2
import numpy as np

from cv_utils import cv_imread, cv_imwrite, ASSETS_DIR

# ========== 1. 故意用 cv2.imread 读"真·中文路径"，观察坑 ==========
# 注意：assets/中文目录测试/cat.jpg 是真实存在的图。
# 上次实验的路径文件不存在，测的其实是"文件不存在"而不是"中文路径的坑"
cn_path = os.path.join(ASSETS_DIR, "中文目录测试", "cat.jpg")

img_bad = cv2.imread(cn_path)
print("【坑】cv2.imread 读中文路径结果:", img_bad)   # Windows 上 OpenCV 不支持中文路径 → None
img = cv_imread(cn_path)
print("【解决】cv_imread 读取结果:", None if img is None else "成功")

if img is None:
    print("图片还是没读到，检查路径/文件名是否正确")
    exit()

# ========== 3. 打印 shape 和 dtype（对应“第2步理论①”）==========
print("shape:", img.shape)   # 例如 (H, W, 3)，三维数组
print("dtype:", img.dtype)   # 通常是 uint8

# ========== 4. 显示 ==========
cv2.imshow('Original', img)
cv2.waitKey(0)

# ========== 5. 保存副本（中文路径也能存）==========
save_path = os.path.join(ASSETS_DIR, "中文目录测试", "副本_中文.jpg")   # 写进中文目录：中文路径的"写"也测到
cv_imwrite(save_path, img)
print("已保存副本:", save_path)

cv2.destroyAllWindows()