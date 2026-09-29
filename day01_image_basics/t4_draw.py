import os

import cv2
import numpy as np

from cv_utils import cv_imread, cv_imwrite, ASSETS_DIR, OUTPUTS_DIR

# 读图
path = os.path.join(ASSETS_DIR, "cat.jpg")
img = cv_imread(path)
assert img is not None, "读图失败"
h, w = img.shape[:2]
print("图像尺寸: W=%d, H=%d" % (w, h))

# ==========================================================
# 统一样式参数（全用变量，不写死数字）
# ==========================================================
GREEN = (0, 255, 0)      # BGR 绿色
RED   = (0, 0, 255)      # BGR 红色
THICKNESS = 3            # 线宽
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1.2
FONT_COLOR = (255, 255, 255)   # 白色字
FONT_THICKNESS = 2

# ==========================================================
# 1. 矩形框（模拟检测框）：位置由变量控制
# ==========================================================
# 用"相对比例"定义框的位置，这样换张图也能用
x1_ratio, y1_ratio = 0.25, 0.25   # 左上角占全图的比例
x2_ratio, y2_ratio = 0.75, 0.75   # 右下角占全图的比例

# 换算成像素坐标
x1, y1 = int(w * x1_ratio), int(h * y1_ratio)
x2, y2 = int(w * x2_ratio), int(h * y2_ratio)

# 画矩形：参数是 (图, 左上角(x,y), 右下角(x,y), 颜色, 线宽)
cv2.rectangle(img, (x1, y1), (x2, y2), GREEN, THICKNESS)

# ==========================================================
# 2. 圆：圆心和半径也用变量
# ==========================================================
cx_ratio, cy_ratio = 0.5, 0.5        # 圆心在图像中心
radius_ratio = 0.15                  # 半径占宽度的比例

cx, cy = int(w * cx_ratio), int(h * cy_ratio)
radius = int(w * radius_ratio)

# 画圆：参数是 (图, 圆心(x,y), 半径, 颜色, 线宽)
cv2.circle(img, (cx, cy), radius, RED, THICKNESS)

# ==========================================================
# 3. 写文字（中文会乱码，用英文）
# ==========================================================
label = "Cat 0.98"                   # 用英文，避免乱码
text_ratio_x, text_ratio_y = 0.25, 0.20   # 文字位置比例

text_x, text_y = int(w * text_ratio_x), int(h * text_ratio_y)

# 画文字：参数是 (图, 文字, 位置(x,y), 字体, 缩放, 颜色, 线宽)
cv2.putText(img, label, (text_x, text_y), FONT,
            FONT_SCALE, FONT_COLOR, FONT_THICKNESS)

# 小优化：给文字加个背景条，更清晰（可选）
(text_w, text_h), baseline = cv2.getTextSize(label, FONT, FONT_SCALE, FONT_THICKNESS)
cv2.rectangle(img,
              (text_x, text_y - text_h - baseline),
              (text_x + text_w, text_y + baseline),
              GREEN, -1)              # 线宽 -1 = 填充
cv2.putText(img, label, (text_x, text_y), FONT,
            FONT_SCALE, (0, 0, 0), FONT_THICKNESS)   # 黑色字

# ==========================================================
# 显示 + 保存
# ==========================================================
cv2.imshow('Detection Result', img)
cv_imwrite(os.path.join(OUTPUTS_DIR, "detection_result.jpg"), img)

cv2.waitKey(0)
cv2.destroyAllWindows()