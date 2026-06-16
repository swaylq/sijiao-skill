# 调研笔记（8 路汇总）· linear-algebra

> 参考样本：从线代正典蒸出以演示管线。完整 per-route 拆分见 `rust-learn` 样本；此处汇总。

- **1 知识地图 / 先修**：脊柱 向量 → 矩阵 → 消元 → 向量空间 → 基/维数 → 变换/行列式 → 特征值 → 对角化/正交 → SVD。来源：MIT 18.06 课程序 `[primary]`。
- **2 正典**：MIT 18.06 (Strang, OCW) · 《Introduction to Linear Algebra》(Strang) · 3Blue1Brown《Essence of LA》· Axler《Linear Algebra Done Right》(抽象/证明向，进阶)。三处以上独立推荐。
- **3 高手路径**：共识「先 3b1b 建直觉，再 18.06 练计算」；别一上来啃 Axler 的抽象。
- **4 刻意练习**：18.06 problem sets；每题手算 + numpy 验证；3b1b 直觉自测。环境：纸笔 + numpy。
- **5 卡点**：会算不懂义、张成/无关/基混淆、特征向量 scale、SVD 当黑箱。
- **6 评估**：novice = 能消元解系统；adv beginner = 会求基/维数/秩、读懂线性变换；competent = 能独立做特征分解/SVD/最小二乘并解释几何。
- **7 反馈**：MIT 18.06 答案对照 · math.stackexchange · 学校助教。AI 能批计算 + 直觉，严格证明逻辑找真人。
- **8 动机**：5h/周到胜任约 12-16 周；抽象段平台期，靠具体矩阵例子 + 间隔复习维持。
