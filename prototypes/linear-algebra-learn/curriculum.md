# linear-algebra — 学习路径

## 阶段：novice

### 向量与向量运算  `(vectors)`
- 目标（understand）：把向量同时理解成『一列数』和『空间中的箭头』
- 目标（apply）：手算向量加法、数乘，并画出几何意义
- 练习（drill）：给定 5 组向量，手算 2u-3v 并在坐标纸画出，再用 numpy 验证

### 矩阵入门：矩阵-向量乘法是线性组合  `(matrices-basics)`
- 先修：vectors
- 目标（understand）：解释 Ax 是 A 的列向量按 x 加权的线性组合
- 练习（drill）：对 3 个 Ax，分别用『行点积』和『列线性组合』两种方式各算一遍，结果一致

### 矩阵运算：乘法、转置、逆  `(matrix-operations)`
- 先修：matrices-basics
- 目标（apply）：手算矩阵乘法，理解它是复合线性变换
- 目标（understand）：说清逆矩阵在解什么问题
- 练习（drill）：手算两个 2x2 矩阵乘积；求一个 2x2 的逆并验证 A·A⁻¹=I

### 线性方程组与高斯消元  `(linear-systems)`
- 先修：matrix-operations
- 目标（apply）：用高斯消元把 Ax=b 化成行阶梯形求解
- 目标（analyze）：判断方程组解的三种情况（唯一/无穷/无解）
- 练习（drill）：手动消元解一个 3x3 系统；构造一个无解和一个无穷解的例子各一个
- 里程碑：手解一个 3 元方程组并解释解的结构 — 会了的标志：能独立消元到行阶梯形并判断解的情况

## 阶段：advanced_beginner

### 行列式  `(determinants)`
- 先修：matrix-operations
- 目标（understand）：把行列式理解成面积/体积缩放因子
- 目标（apply）：手算 2x2、3x3 行列式
- 练习（drill）：手算 3 个 3x3 行列式；解释 det=0 时变换把空间压扁了

### 向量空间与子空间  `(vector-spaces)`
- 先修：linear-systems
- 目标（remember）：复述向量空间/子空间的判定条件
- 目标（apply）：识别列空间、零空间
- 练习（drill）：给定矩阵 A，求出 C(A) 和 N(A) 的一组生成向量

### 张成与线性无关  `(span-independence)`
- 先修：vector-spaces
- 目标（analyze）：判断一组向量是否线性无关、张成什么空间
- 练习（drill）：对 4 组向量判定线性相关性，相关的写出一个非平凡线性组合等于零

### 线性变换  `(linear-transformations)`
- 先修：matrix-operations, vector-spaces
- 目标（understand）：把矩阵理解为线性变换，读出它对基向量做了什么
- 练习（drill）：写出旋转 90°、剪切、缩放各自的 2x2 矩阵，并验证对 (1,0)/(0,1) 的作用

### 基、维数与秩  `(basis-dimension)`
- 先修：span-independence
- 目标（apply）：求子空间的一组基和维数
- 目标（analyze）：用秩联系四个基本子空间的维数
- 练习（drill）：给定 A，求 rank、列空间和零空间的基与维数，验证秩-零化度定理

## 阶段：competent

### 特征值与特征向量  `(eigenvalues)`
- 先修：determinants, linear-transformations
- 目标（apply）：用特征多项式求特征值，再求特征向量
- 目标（understand）：解释特征向量是变换中方向不变的向量
- 练习（drill）：对一个 2x2 矩阵手算特征值和特征向量，numpy 验证

### 正交性、投影与 Gram-Schmidt  `(orthogonality)`
- 先修：basis-dimension
- 目标（apply）：求一个向量到子空间的投影
- 目标（apply）：用 Gram-Schmidt 正交化一组基
- 练习（drill）：把 R³ 中两个向量 Gram-Schmidt 正交化；求 b 到某平面的投影

### 对角化与基变换  `(diagonalization)`
- 先修：eigenvalues, basis-dimension
- 目标（apply）：把可对角化矩阵写成 A=PDP⁻¹
- 目标（apply）：用对角化算矩阵幂 Aⁿ
- 练习（drill）：对角化一个 2x2 矩阵并用它算 A⁵，与直接连乘对照

### SVD 与应用：最小二乘 / PCA  `(svd-applications)`
- 先修：diagonalization, orthogonality
- 目标（understand）：解释 SVD 把任意矩阵分解成旋转-缩放-旋转
- 目标（create）：用最小二乘拟合一条直线 / 用 PCA 找主方向
- 练习（project）：对一个 2D 点集用最小二乘拟合直线，再手动+numpy 做一次 PCA 找主方向，解释两者关系
- 里程碑：对一个真实 2D 数据集做最小二乘 + PCA，解释每一步的几何意义 — 会了的标志：能独立从数据走到 SVD/特征分解并解释结果，不只是调 numpy
