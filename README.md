<div align="center">

# 🎓 私教.skill &nbsp;[![Tweet](https://img.shields.io/badge/share%20on-Twitter%2FX-000000?style=flat-square&logo=x)](https://twitter.com/intent/tweet?text=%E7%A7%81%E6%95%99.skill%20%E2%80%94%20%E8%BE%93%E5%85%A5%E4%BB%BB%E4%BD%95%E6%83%B3%E5%AD%A6%E7%9A%84%E6%8A%80%E8%83%BD%EF%BC%8C%E8%92%B8%E9%A6%8F%E5%87%BA%E4%B8%80%E4%B8%AA%E5%B8%A6%E4%BD%A0%E4%BB%8E%200%20%E5%AD%A6%E4%BC%9A%E5%AE%83%E7%9A%84%E6%9C%89%E7%8A%B6%E6%80%81%E7%A7%81%E6%95%99%E3%80%82&url=https%3A%2F%2Fgithub.com%2Fswaylq%2Fsijiao-skill&hashtags=ClaudeCode%2CAIAgent%2C%E7%A7%81%E6%95%99skill%2C%E5%BC%80%E6%BA%90)

### 输入任何想学的技能，蒸馏出一个**带你从 0 学会它**的有状态私教

> *「大师替你做这一行的判断。私教.skill 把你训练成能自己做判断的人。」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![tests](https://img.shields.io/badge/tests-35%20passing-brightgreen)](tests/)

<br>

[同事.skill](https://github.com/titanwings/colleague-skill) 把**一个人**蒸成 AI。<br>
[大师.skill](https://github.com/swaylq/master-skill) 把**一整行的认知**蒸成 AI —— **授人以鱼**。<br>

但还有一件比「替你做」更重要的事 ——<br>
**让你自己变成会的人。**

<br>

告诉它你想学什么，<br>
它跑完 **8 路调研**、按学习科学蒸出一条从 0 到「胜任」的路径，<br>
生成一个**记得你学到哪、按你水平自适应出题批改**的私教 skill。<br>

<br>

> **它跟「ChatGPT 给我列个学习计划」的本质差别：**<br>
> **那是一张一次性的纸；这是一个记得你、陪你练、知道你卡在哪的私教。**

<br>

[🚀 安装](#-安装) · [✨ 私教长什么样](#-私教长什么样) · [🧠 它蒸了什么](#-它蒸了什么) · [🔍 凭什么信它](#-凭什么相信它蒸出来的东西) · [⭐ 样本](#-已蒸馏的样本) · [🧬 三代谱系](#-三代谱系)

[**English README →**](README_en.md)

</div>

---

> 📊 &nbsp;**v0.1** — 元 skill + 工具引擎（**35 测试全绿**，纯标准库零依赖）+ **4 个端到端样本**（rust / 线性代数 / 英语阅读 / 减肥，共 **53 模块**）跑通。每个样本的先修图都经引擎拓扑校验、课程由引擎渲染。
>
> 🧬 &nbsp;**家族第三代** — 站在 同事 / 大师 肩膀上，把元 skill 框架从「蒸专家」翻转成「**教你成为专家**」。
>
> 🎯 &nbsp;**天花板诚实标到「胜任」** — 私教带你到「能独立做常规任务」，精通/专家靠之后多年真实实践。不告诉你局限的 skill 不值得信任。

---

## ✨ 私教长什么样

> 不是搜索引擎，也不是一张学习计划。是「一个记得你、陪你练的私教此刻在你旁边」。

#### 🦀 场景 1 · Rust（读档 → 间隔复习 → 打薄弱点 → 苏格拉底）

```
你    ❯ 继续学 rust

私教  ❯ 读档：你在「借用与引用」(mastery 0.55)，上次卡在
       &mut 与 & 同时存在的报错。今天先清一个到期复习，再啃这个坎。

       【检索练习 · 借用三原则】不许翻书：
       同一作用域，要么 ___ 个 &，要么 ___ 个 &mut，两者 ___ 共存。

你    ❯ 任意多个 &，或者一个 &mut，不能同时

私教  ❯ ✅ 记住了，下次复习排到 6 天后。现在上今天的坎，这段过不了编译：

         let mut v = vec![1,2,3];
         let first = &v[0];
         v.push(4);            // ← 编译器在这里报错
         println!("{first}");

       先别看答案：first 借走了 v 的不可变引用，push 要 &mut v，
       这正违反你刚背的哪一条？
```

#### 📐 场景 2 · 线性代数（诊断是「直觉缺口」而非基础问题，先建几何图像再算）

```
你    ❯ 学线性代数，但我一看到特征值就懵

私教  ❯ 读档：你卡在 eigenvalues，但前置的行列式、线性变换都过了 (mastery 0.8+)，
       所以不是基础问题，是缺几何图像。先别算特征多项式。

       一句话建图像：特征向量 = 这个矩阵『变换』作用下方向不变、只被拉伸的向量；
       特征值 = 拉伸倍数。

       看 [[2,0],[0,3]]：它把 x 轴拉 2 倍、y 轴拉 3 倍。
       不用算——你能直接说出它的两个特征向量和特征值吗？

你    ❯ (1,0) 特征值 2，(0,1) 特征值 3

私教  ❯ ✅ 这就是几何本质。现在换一个非对角矩阵，从「方向不变」反推……
```

#### 📖 场景 3 · 英语阅读（AI 现场生成贴合水平的句子，打「逐字翻译」的老毛病）

```
你    ❯ 继续练英语阅读

私教  ❯ 读档：你在「长难句」(mastery 0.45)，老毛病是逐字翻译。先练找主干。

       【现场生成 · 贴你水平的句子】先找主谓宾，别翻译：
       "The startup that the investors had backed quietly
        collapsed after its only customer left."

你    ❯ 主干是 The startup collapsed？

私教  ❯ ✅ 对！中间 that…backed 是定语从句修饰 startup，after… 是状语。
       你抓住主干了 —— 这正是要练的。再给一个嵌套更深的……
```

**四件 ChatGPT 学习计划做不到的事**：读档定位 → 间隔复习到期项 → 打你已知的薄弱点 → 苏格拉底式逼你自己想。每次都接着上次，不重问「你学到哪了」。

---

## 🧠 它蒸了什么

一条**按学习科学搭的路径**，不是资料堆。每个生成的 `{技能}-learn` 是自包含目录，分三层：

| 层 | 文件 | 装了什么 |
|----|------|---------|
| 📚 **课程层** | `curriculum.json` / `.md` | 先修排序、Dreyfus 分段的模块。每个带 Bloom 分层目标 + 正典资源 + **可评估练习** + 里程碑 + 「会了的标志」 |
| 🧑‍🏫 **教学层** | `SKILL.md` | 私教本体：读档 → 定位 → 讲解→范例→撤支架→独立练 → 出题批改 |
| 🗂️ **档案层** | `learner-state.json` | 你的进度 / 错题 / **SM-2 间隔重复排程** / 打卡（私人，不进 git） |

提炼遵循 5 条学习科学（[`references/pedagogy-framework.md`](references/pedagogy-framework.md)）：

| 原则 | 落地 |
|------|------|
| **Dreyfus 五段** | 切分课程阶段；天花板定在「胜任」 |
| **Bloom 分类** | 每个目标定认知层级（记忆→理解→应用→分析→评价→创造） |
| **刻意练习** | 每模块必有「可产出可评估结果」的练习，不是「读完这本书」 |
| **间隔重复 + 检索练习** | 档案排程哪些该复习；每次开课先清到期项 |
| **合意难度** | worked-example → 逐步撤支架 → 独立练 |

---

## 🔍 凭什么相信它蒸出来的东西

> 一个学习路径装上来，怎么知道它不是随手编的？

每个生成的 skill 过一套**学习特化质检**（[`prompts/quality_check.md`](prompts/quality_check.md)）：

- ✅ **先修图无环且有据** — `validate_dag` 必须返回空；每条「先学 A 再学 B」挂得到来源
- ✅ **每个模块都有可评估练习** — 不是「多看书」，是「输出能被判对错的任务」
- ✅ **「会了」的标志是行为化的** — 「能独立做 X」，不是「理解了 X」
- ✅ **来源一手** — 正典资源 ≥3 处独立推荐；拒绝 SEO「十大学习法」软文 / 内容农场
- ✅ **天花板诚实** — `dreyfus_ceiling ≤ competent`，不准吹「成为专家」

**本仓 4 个样本的硬数字**：53 模块全部经引擎拓扑校验、课程由引擎渲染、`learner-state` 示例 schema 验证通过，35 个测试覆盖工具引擎。

### 诚实边界（家族 DNA）

- **天花板 = 胜任**：精通/专家靠之后多年真实实践 —— 明说，不吹。
- AI 教不了的（手艺/身体/社交的真实反馈）**诚实标注**转上传/线下/真人，不假装能批改（如 `english-reading` 明标「只管阅读，不含听说写」）。
- 资源/工具 3-6 月衰减，先修图 + 教学法不衰减（`update 私教 X` 增量刷新）。

---

## ⚡ 安装

```bash
# Claude Code
git clone https://github.com/swaylq/sijiao-skill.git ~/.claude/skills/sijiao-skill
```

<details>
<summary><b>🛠️ 其他 host</b></summary>

<br>

| Host | 路径 |
|------|------|
| 🟣 Claude Code | `~/.claude/skills/sijiao-skill` |
| 🔵 OpenClaw | `~/.openclaw/skills/sijiao-skill` |
| ⚫ Codex | `~/.codex/skills/sijiao-skill` |
| 🟠 Hermit | `~/.hermit/skills/sijiao-skill` |

装一个**生成出来的** `{技能}-learn` 到某 host：

```bash
python3 tools/install.py install --host <claude|openclaw|codex|hermit> --source ./prototypes/rust-learn
python3 tools/install.py list-hosts
```

</details>

---

## 🚀 用法

装好 私教.skill 的 agent 里，直接说：

```
> 学 rust              # 没装过 → 触发蒸一个 rust-learn
> 继续学 rust           # 已有 → 读档接着教
> 考我 rust 所有权       # 触发对应模块的检索练习
> update 私教 rust      # 半年后增量刷新资源/工具
```

它先跟你确认 5 件事（技能、现有水平、目标、每周时间、locale），然后启动 **8 路并行调研** → 按学习科学蒸馏 → 生成三层私教目录。30-60 分钟后你拿到一个 `{技能}-learn`，装到任意 agent 立刻开课。

---

## ⭐ 已蒸馏的样本

每个都是端到端跑过的样本，三层齐全、先修图经引擎校验。调研留痕完全透明，可追溯每个模块从哪来。

| 技能 | 类型 | 模块 | 天花板 | 路径 |
|------|------|------|--------|------|
| **Rust 编程** | 硬技术（认知甜区） | 15 | 胜任 | [rust-learn/](prototypes/rust-learn/) |
| **线性代数** | 认知 / 数学 | 13 | 胜任 | [linear-algebra-learn/](prototypes/linear-algebra-learn/) |
| **英语阅读理解** | 语言 · 认知甜区 | 12 | 胜任 | [english-reading-learn/](prototypes/english-reading-learn/) |
| **减肥（科学减脂）** | 生理 · 行为（诚实降级 · ⚠️ 非医疗建议） | 13 | 胜任 | [weight-loss-learn/](prototypes/weight-loss-learn/) |

> 甜区起步（认知/知识型先跑通）；**减肥样本是第一个非认知技能**，展示框架碰到生理/行为时怎么「诚实降级」——AI 教不了的（实际摄入 / 动作 / 医学情况）标注转自报 / 线下 / 医生。<br>
> 想学不在列表里的？装上 私教.skill，说「学 XXX」就行。

---

## 🔬 工作原理

```
0  技能澄清       ← 收窄过粗的技能 + 探测水平/目标/时间/技能类型
1  8 路并行调研    ← 知识地图 / 正典 / 高手路径 / 刻意练习 / 卡点 / 评估 / 反馈 / 动机
   ─ 调研评审关卡
2  框架蒸馏        ← 建先修 DAG → Dreyfus 分段 → 填模块 → 三重验证（先修有据/资源被独立推荐/练习可评估）
   ─ 蒸馏评审关卡
3  写出 skill      ← curriculum_builder 校验+渲染课程；生成私教 SKILL.md + 档案 schema
4  质检           ← 10 项学习特化 rubric + validation gate（一票否决：黑名单源/环/无练习/吹专家）
5  双 agent 精炼   ← 优化「激活即开课」+ 自适应是否真用了档案
```

详见 [SKILL.md](SKILL.md)，方法论看 [references/pedagogy-framework.md](references/pedagogy-framework.md)。

---

## 🧬 三代谱系

同源，逐层放大：

- **[同事.skill](https://github.com/titanwings/colleague-skill)** — 蒸一个**具体的人**做什么。
- **[大师.skill](https://github.com/swaylq/master-skill)** — 蒸**一整行**的认知 + 工作流 + 工具（**授人以鱼**）。
- **🎓 私教.skill** — 蒸**一条让你自己学会的路**（**授人以渔**）。

前两代都在「让 agent 替你做」，私教.skill 第一个把目标翻转成「**让你自己会做**」。

---

## 📂 项目结构

```
sijiao-skill/
├── SKILL.md                  # 元 skill：8 路调研 → 蒸课程 → 生成私教
├── prompts/                  # intake + 8 路调研 + 来源规范 + synthesis + quality_check
├── references/               # pedagogy-framework（学习科学核心）+ skill-template（产物模板）
├── tools/                    # curriculum_builder · learner_state · install · self_test（纯标准库）
├── prototypes/               # 4 个端到端样本：rust / 线性代数 / 英语阅读 / 减肥（53 模块）
└── tests/                    # 35 个测试
```

---

## 📄 路线图

| 版本 | 内容 | 状态 |
|------|------|------|
| v0.1 | 元 skill + 工具引擎 + **4 个样本**（rust / 线性代数 / 英语阅读 / 减肥）+ 打包 | ✅ |
| v1.x | 质检自动化（quality_check.py / validation_gate.py）+ source_verifier + 增量刷新 update_skill.py | 🔲 |
| v2.x | 官网（点开就能试学）+「名师教学风格」sub-skill + cli/ 练习套件 + PyPI | 🔲 |

详见 [ROADMAP.md](ROADMAP.md)。

---

## 📜 许可证

MIT — 随便用，随便改，随便造。

<div align="center">

<br>

**🧬 同事.skill** 蒸一个**具体的人**做什么。<br>
**🎓 大师.skill** 蒸**一整行**的认知 —— 授人以鱼。<br>
**📖 私教.skill** 蒸**一条让你自己学会的路** —— 授人以渔。<br>

<br>

*把「学会一门技能」这件事，蒸馏成一个记得你、陪你练的私教。*

<br>

MIT License © [swaylq](https://github.com/swaylq) · 中文 README · [English](README_en.md)

</div>

---

## ⭐ Star History

<a href="https://www.star-history.com/#swaylq/sijiao-skill&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=swaylq/sijiao-skill&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=swaylq/sijiao-skill&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=swaylq/sijiao-skill&type=Date" />
 </picture>
</a>
