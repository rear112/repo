import os
import cv2
import numpy as np
from cv_utils import cv_imread, ASSETS_DIR,OUTPUTS_DIR,cv_imwrite

#=========== 1. 读图 ==========
path=os.path.join(ASSETS_DIR, "cat.jpg")
image = cv_imread(path)
assert image is not None, "读图失败"
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#============= 保存 =============
save_path=os.path.join(OUTPUTS_DIR, "gray_cat.jpg")
cv_imwrite(save_path, gray)


#=========== 直方图与 CLAHE —— "图太暗/光照不均先调什么"==========
eq = cv2.equalizeHist(gray)  # 直方图均衡化
clahe=cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))  # 创建 CLAHE 对象    
cl=clahe.apply(gray)  # 应用 CLAHE
cv_imwrite(os.path.join(OUTPUTS_DIR, "gray_cat_eq.jpg"), np.hstack([gray, eq, cl]))  # 拼接显示

#=========== 滤波 —— 去噪 ==========
gauss = cv2.GaussianBlur(gray, (5, 5), 0)
median = cv2.medianBlur(gray, 5)   
cv_imwrite(os.path.join(OUTPUTS_DIR, "gray_cat_filter.jpg"), np.hstack([gray, gauss, median]))  # 拼接显示

#========== 阈值 —— 二值化的三种姿势 ==========
_, th_fixed = cv2.threshold(gauss, 127, 255, cv2.THRESH_BINARY)          # 手动全局
_, th_otsu  = cv2.threshold(gauss, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # 自动全局
th_adap = cv2.adaptiveThreshold(gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 11, 2)                # 局部自适应
cv_imwrite(os.path.join(OUTPUTS_DIR, "gray_cat_threshold.jpg"), np.hstack([gray, th_otsu, th_adap]))  # 拼接显示

#========== 边缘检测 ==========
sobelx = cv2.Sobel(gauss, cv2.CV_64F, 1, 0, ksize=3)    # 水平方向梯度
sobelx = cv2.convertScaleAbs(sobelx)   # 取绝对值 + 缩放回 0~255 的 uint8
edges = cv2.Canny(gauss, 50, 150)                        # 低阈值50，高阈值150
cv_imwrite(os.path.join(OUTPUTS_DIR, "gray_cat_edges.jpg"), np.hstack([gray, sobelx, edges]))  # 拼接显示

#========== 形态学  ==========
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
opened  = cv2.morphologyEx(th_otsu, cv2.MORPH_OPEN,  kernel)   # 开=先腐蚀再膨胀：去小白点
closed  = cv2.morphologyEx(th_otsu, cv2.MORPH_CLOSE, kernel)   # 闭=先膨胀再腐蚀：填小黑洞
cv_imwrite(os.path.join(OUTPUTS_DIR, "gray_cat_morphology.jpg"), np.hstack([gray, opened, closed]))  # 拼接显示

#========== 轮廓 ==========
img_area = image.shape[0] * image.shape[1]     # 全图像素总数
cnts, hier = cv2.findContours(closed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
for i, c in enumerate(cnts):
    if hier[0][i][3] != -1:      # 只要顶层外轮廓，跳过洞边界（hier 四元组: [next, prev, first_child, parent]）
        continue
    area = cv2.contourArea(c)
    if area < 200 or area > img_area * 0.024:        # 太小是噪声，太大是结构框:
        continue
    x, y, w, h = cv2.boundingRect(c)
    (cx, cy), (rw, rh), ang = cv2.minAreaRect(c)
    box = cv2.boxPoints(((cx, cy), (rw, rh), ang)).astype(int)
    cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
    cv2.putText(image, "%.0f" % area, (int(x), int(y) - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
cv_imwrite(os.path.join(OUTPUTS_DIR, "gray_cat_contours.jpg"), image)
