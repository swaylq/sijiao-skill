# 线性代数 教学法笔记

基于 `../../../references/pedagogy-framework.md`。

## 双视角并进
线代最大的坑是「会算不懂意义」。每个概念走两条线：**几何直觉**（3Blue1Brown）先建图像，
**计算**（Strang 18.06）再落手算。算完必问「这一步几何上发生了什么」。

## 卡点地图（route 5）
- 机械消元、不知道在干嘛 → `linear-systems` 强调「每步对应什么」。
- 混淆「张成集 / 线性无关 / 基」→ `span-independence` + `basis-dimension` 用反例区分。
- 特征向量的 sign / scale 任意 → `eigenvalues` 明确「方向不变，长度任意」。
- 把 SVD 当黑箱 → `svd-applications` 强制手推一个小例子。

## 间隔重复清单（进 spaced_queue）
向量空间判定 · 秩-零化度定理 · 行列式=体积缩放 · 特征值定义 · 投影公式。

## 节奏（route 8）
5 小时/周，到「胜任」约 **12-16 周**。抽象段（向量空间 → 基）是平台期，多用具体矩阵例子落地，
别停在符号操作。
