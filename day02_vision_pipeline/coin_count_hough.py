# ============================================================
# 硬币计数 —— 霍夫圆检测版（HoughCircles）
# ------------------------------------------------------------
# 选型理由：
#   硬币是"圆"，HoughCircles 直接检测圆，对粘连/重叠最直接。
#
# 适用：
#   - 目标接近正圆（硬币、孔、圆点）
#   - 粘连严重、分水岭拆不开时的"备用方案"
#
# 关键调参：
#   param2 = 30    # 累加器阈值：调小→检更多（易误检），调大→检更少（易漏检）
#   minDist = 50   # 圆心最小距离：防止一个圆被检多次
#   minRadius/maxRadius = 20/80   # 半径范围，按实际硬币大小设
#
# 返回值注意：
#   circles 是 np.float32，画圆前要：
#       circles = np.uint16(np.around(circles))
#       for i in circles[0, :]: ...
#   （也可 .T 转置解包）
# ============================================================
import os
import numpy as np
from cv_utils import cv_imread, ASSETS_DIR, OUTPUTS_DIR, cv_imwrite
import cv2

# ========== 读图 + 灰度 + 滤波 ==========
path = os.path.join(OUTPUTS_DIR, "coins.png")
image = cv_imread(path)
assert image is not None, "读图失败"
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# HoughCircles 前先高斯滤波，去噪、减少误检
gauss = cv2.GaussianBlur(gray, (5, 5), 0)

# ========== HoughCircles ==========
circles = cv2.HoughCircles(
    gauss,
    cv2.HOUGH_GRADIENT,
    dp=1,              # 累加器分辨率（1=原分辨率）
    minDist=20,        # 圆心最小距离（防止一个圆被检多次）
    param1=100,        # Canny 高阈值（内部用）
    param2=30,         # ★ 累加器阈值：调小→检更多，调大→检更少
    minRadius=20,      # 最小半径
    maxRadius=80       # 最大半径
)

# ========== 画圆 + 计数 ==========
vis = image.copy()
count = 0

if circles is not None:
    # ★ 返回值是 np.float32，先四舍五入转 uint16，再 .T 转置解包
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:          # [0,:] 取第一组，[x, y, r]
        count += 1
        cv2.circle(vis, (i[0], i[1]), i[2], (0, 255, 0), 2)   # 画圆
        cv2.circle(vis, (i[0], i[1]), 2, (0, 0, 255), 3)      # 画圆心
        cv2.putText(vis, "#%d" % count, (i[0] - 10, i[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

print("HoughCircles 硬币总数：", count)
cv_imwrite(os.path.join(OUTPUTS_DIR, "coins_hough.jpg"), vis)