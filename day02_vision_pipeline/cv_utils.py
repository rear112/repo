"""day01 公共工具模块：中文路径读写 + 目录约定。

企业级习惯：工具函数只放一处，全项目 import，绝不复制粘贴。
升级方向（Day 9 会用到）：读图失败抛异常而不是静默返回 None + logging。
"""
import os

import cv2
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))    # day01/
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)                 # E:\jiqivison
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")          # 测试素材（只进不改）
OUTPUTS_DIR = os.path.join(SCRIPT_DIR, "outputs")          # 运行产出
os.makedirs(OUTPUTS_DIR, exist_ok=True)


def cv_imread(path):
    """读取图像（支持中文路径）。失败返回 None，调用方必须检查。"""
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)


def cv_imwrite(path, img):
    """保存图像（支持中文路径）。返回是否成功。"""
    ext = '.' + path.rsplit('.', 1)[-1]
    ok, buf = cv2.imencode(ext, img)
    if ok:
        buf.tofile(path)
    return ok
