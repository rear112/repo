import os
import numpy as np
import cv2
from cv_utils import cv_imread, ASSETS_DIR, OUTPUTS_DIR, cv_imwrite
import json
import sys
import glob

Path = os.path.join(OUTPUTS_DIR, "board_template.png")
ROI_SIZE = 60
AREA_THRESHOLD = 800
JSON_PATH = 'screw_positions.json'
# ========== 函数1：提取模板坐标 ==========
def extract_template(Path, json_path):
    #=========== 读图 ==========
    image = cv_imread(Path)
    assert image is not None, "读图失败"

    #========== 预处理 ==========
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gauss = cv2.GaussianBlur(gray, (5, 5), 0)
    _, th_otsu = cv2.threshold(gauss, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #========= 轮廓=========
    contours, _ = cv2.findContours(th_otsu, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #=========筛选=========
    screw_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 2000 < area < 3000:  # 螺丝孔面积范围
            screw_contours.append(cnt)

    centers = []
    
    for cnt in screw_contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centers.append((cx, cy))
    if len(centers) == 0:
        print("未找到任何螺丝位，请检查阈值和面积范围")
        return

    #先按y排序
    centers.sort(key=lambda p: p[1])
    rows = []
    current_row = [centers[0]]
    for p in centers[1:]:
        if abs(p[1] - current_row[-1][1]) < 30:  # 同一行，Y差小于30
            current_row.append(p)
        else:
            rows.append(current_row)
            current_row = [p]
    rows.append(current_row)
    print(f"分行数: {len(rows)}")
    for i, row in enumerate(rows):
        print(f"第 {i+1} 行: {len(row)} 个点")
    numbered = []
    idx = 1
    for row in rows:
        row.sort(key=lambda p: p[0])
        for (x, y) in row:
            numbered.append({"id": idx, "x": x, "y": y})
            idx += 1

    #可视化验证 + 保存 JSON
    vis = image.copy()
    for item in numbered:
        cv2.circle(vis, (item['x'], item['y']), 5, (0, 0, 255), -1)
        cv2.putText(vis, str(item['id']), (item['x']+10, item['y']-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    with open(json_path, 'w') as f:
        json.dump(numbered, f, indent=2)
    print(f"已保存 {len(numbered)} 个坐标到 {json_path}")

    cv2.imshow('template', vis)
    cv2.waitKey(0)

# ========== 函数2：检测缺件 ==========
def detect_missing(image_path, positions, visualize=True):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    missing = []
    r = ROI_SIZE // 2

    for item in positions:
        x, y = item['x'], item['y']

        x1 = max(0, x - r)
        y1 = max(0, y - r)
        x2 = min(gray.shape[1], x + r)
        y2 = min(gray.shape[0], y + r)

        roi = gray[y1:y2, x1:x2]
        # 固定阈值而非 Otsu：缺失位 ROI 里只有孔座(90)+底板(45)，Otsu 会把噪声切成两班导致误判
        # 依据：螺丝最暗≈177、孔座 90、底板 45 → 150 站在 90 与 177 的空隙里
        _, roi_binary = cv2.threshold(roi, 150, 255, cv2.THRESH_BINARY)
        white_area = cv2.countNonZero(roi_binary)

        if white_area < AREA_THRESHOLD:
            missing.append(item['id'])

    name = os.path.basename(image_path)
    print(f"{name}: {'NG, 缺失螺丝位 ' + str(missing) if missing else 'OK'}")

    vis = img.copy()
    for item in positions:
        color = (0, 0, 255) if item['id'] in missing else (0, 255, 0)
        cv2.circle(vis, (item['x'], item['y']), 20, color, 2)
        cv2.putText(vis, str(item['id']), (item['x']-10, item['y']-25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    out_name = 'result_' + os.path.basename(image_path)
    cv_imwrite(os.path.join(OUTPUTS_DIR, out_name), vis)

    return missing



if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'detect'
    if mode == 'extract':
        extract_template(Path, 'screw_positions.json')

    elif mode == 'detect':
        with open(JSON_PATH, 'r') as f:
            positions = json.load(f)
            # 读取 outputs 文件夹下所有 png
        image_paths = sorted(glob.glob(os.path.join(OUTPUTS_DIR, 'board_test*.png')))

        for path in image_paths:
            detect_missing(path, positions, visualize=False)