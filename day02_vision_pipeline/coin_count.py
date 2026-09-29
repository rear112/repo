
# ============================================================
# 硬币计数 —— 分水岭版
# ------------------------------------------------------------
# 选型理由：
#   硬币"粘连/重叠"时，直接 findContours 会把多个硬币算成 1 个块。
#   用"距离变换 + 分水岭"能把粘连处切开，冲 12/12。
#
# 适用：
#   - 目标粘连严重、非圆或圆但不规则
#   - 需要"按区域"拆分
#
# 关键调参：
#   FG_RATIO = 0.7    # 种子阈值系数：调大→拆开（数多），调小→合并（数少）
#
# 风险：
#   - 参数敏感，粘连太严重可能仍拆不开
#   - 比 Hough 慢
# ============================================================import os
import numpy as np
from cv_utils import cv_imread, ASSETS_DIR, OUTPUTS_DIR, cv_imwrite
import cv2

path = os.path.join(OUTPUTS_DIR, "coins.png")
#=========== 读图 ==========
image = cv_imread(path)
assert image is not None, "读图失败"
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gauss = cv2.GaussianBlur(gray, (5, 5), 0)#滤波

# 硬币通常比背景亮，用 BINARY 让硬币变白
_, th_otsu = cv2.threshold(gauss, 0, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#========== 形态学  ==========
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
opened  = cv2.morphologyEx(th_otsu, cv2.MORPH_OPEN,  kernel)   # 开=先腐蚀再膨胀：去小白点
closed  = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)   # 闭=先膨胀再腐蚀：填小黑洞   

# ==========================================================
# 分水岭拆粘连
# ==========================================================

# 1) 确定背景：膨胀
sure_bg = cv2.dilate(closed, kernel, iterations=3)

# 2) 距离变换：找硬币中心
dist = cv2.distanceTransform(closed, cv2.DIST_L2, 5)

 #3) 确定前景：距离的峰（硬币中心）
_, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
sure_fg = np.uint8(sure_fg)

# 4) 不确定区域
unknown = cv2.subtract(sure_bg, sure_fg)

# 5) 标记连通域
_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1              # 背景 = 1
markers[unknown == 255] = 0        # 未知 = 0

# 6) 分水岭
markers = cv2.watershed(image, markers)

#========= 轮廓 ==========
img_area = image.shape[0] * image.shape[1]     # 全图像素总数
count = 0
vis=image.copy()
vis[markers == -1] = (0, 0, 255)   # 分割边界标红
for label in np.unique(markers):
    if label <= 1:                 # 0=未知, 1=背景
        continue
    mask = np.uint8(markers == label) * 255
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        continue
    c = max(cnts, key=cv2.contourArea)
    area = cv2.contourArea(c)
    # 面积筛选（上限放宽到 0.1）
    if area < 200 or area > img_area * 0.1:
        continue
    count += 1
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(vis, "#%d" % count, (int(x), int(y) - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
print("硬币总数：", count)
cv_imwrite(os.path.join(OUTPUTS_DIR, "coins_count.jpg"), vis)
cv_imwrite(os.path.join(OUTPUTS_DIR, "coins_dist.jpg"),
           cv2.normalize(dist, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8))