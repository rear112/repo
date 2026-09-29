import os

from cv_utils import cv_imread, ASSETS_DIR

path = os.path.join(ASSETS_DIR, "cat.jpg")
img = cv_imread(path)
assert img is not None, "读图失败"

# ==========================================================
# ★ 一行 numpy 切片缩小一半：隔一个取一个
# ==========================================================
small = img[::2, ::2]        # 行、列都每隔 2 取 1

print("原图 shape:", img.shape)
print("缩放后 shape:", small.shape)
# 例：(480, 640, 3) → (240, 320, 3)