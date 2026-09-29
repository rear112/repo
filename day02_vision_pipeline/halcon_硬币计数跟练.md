# 晚上加练 · Halcon 硬币计数（OpenCV → HDevelop 方言转换）

> 前提：HDevelop 装好、license 激活、`read_image + dev_display` 验证通过。
> 目标：用 Halcon 重做硬币计数，产出 `coin_counting.hdev`，体会"同一个问题两种工具"。
> **纪律不变：程序自己敲**，下面给的是算子地图和骨架，不是答案。

---

## 一、算子对照表（背下来，面试要考）

| 你在 OpenCV 里写的 | Halcon 对应算子 | 备注 |
|---|---|---|
| `cv_imread` | `read_image` | 路径用正斜杠 `/`，别用中文路径 |
| `cv2.cvtColor(GRAY)` | `rgb1_to_gray`（或直接读灰度） | 读彩图后转灰度 |
| `cv2.GaussianBlur` | `gauss_filter` | 半径给 2~3 |
| `cv2.threshold(OTSU)` | `threshold` | **没有 Otsu！** 用交互窗口拖出灰度直方图手选区间，或 `auto_threshold` |
| `THRESH_BINARY / _INV` | `threshold` 的最后一个参数：`'light'` / `'dark'` | Halcon 直接选亮/暗，极性思路一致 |
| `cv2.morphologyEx(OPEN)` | `opening_circle` / `opening_rectangle` | 结构元素是"圆半径"，不是 kernel 矩阵 |
| `cv2.findContours` | `connection` | **一步把连通域拆开**，比 OpenCV 更直接 |
| `cv2.contourArea + if 筛选` | `select_shape` | 一行完成：按 area 区间筛选，这是 Halcon 最香的算子 |
| `len(cnts)` / 计数 | `count_obj` | 直接数区域个数 |

## 二、骨架（自己补全参数）

```
* 1. 读图（注意路径分隔符）
read_image (Image, 'E:/jiqivison/day02/outputs/coins.png')

* 2. 转灰度 + 滤波（自己查算子：双击工具栏算子窗口，F1 看文档）

* 3. 阈值分割：硬币是亮的 → 选 'light'，灰度区间先用交互阈值窗口看直方图再定

* 4. 开运算去噪（opening_circle，半径自己试 1~5）

* 5. 拆连通域：connection

* 6. 按面积筛选硬币：select_shape（想一想面积下限和上限给多少——参考你 OpenCV 里的 200 和 0.024*全图）

* 7. 计数：count_obj，配合 dev_display 和_DISP 語句把结果画出来查看
```

## 三、HDevelop 界面生存指南

- **算子窗口**（右下）：所有算子按类分组，双击插入到程序；**选中算子按 F1 = 官方文档**，参数含义、例子全在里面——今晚遇到不会的算子一律先 F1
- **图形窗口**：`dev_display (变量)` 显示图像；选中区域变量双击可以放大看
- **交互阈值**：工具栏 Filters → Threshold 有交互助手，拖滑块看直方图选灰度区间，选完把数值抄进 `threshold` 算子——这就是 Halcon 调参比 OpenCV 舒服的地方
- **运行**：F5 全跑，F6 单步——单步配合图形窗口，就是 Halcon 版的"边跑边看"
- 保存：File → Save As → `coin_counting.hdev`（存到 day02/ 下）

## 四、验收点（明早检查）

1. `coin_counting.hdev` 计数结果 = 你 OpenCV 霍夫版的数量（12）
2. 能口头回答：
   - Halcon 的 `threshold` 和 OpenCV 的 Otsu 思路差异？（Halcon 交互选区间 vs OpenCV 自动算法）
   - `connection` 和 `findContours` 返回的东西有什么本质不同？（区域 region vs 边界点集——这就是 Halcon 区域运算快的原因）
   - `select_shape` 一行顶 OpenCV 几行？为什么工业界爱用 Halcon？
3. 如果卡住超过 1 小时：把卡住的算子和报错截图发我
