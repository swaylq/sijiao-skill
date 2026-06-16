<div align="center">

# 🎓 学习.skill

### 输入任何想学的技能，蒸馏出一个**带你从 0 学会它**的私教

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![tests](https://img.shields.io/badge/tests-35%20passing-brightgreen)](tests/)

<br>

[同事.skill](https://github.com/titanwings/colleague-skill) 把**一个人**蒸成 AI。<br>
[女娲.skill](https://github.com/alchaincyf/nuwa-skill) 把**任何人的思维**蒸成 AI。<br>
[大师.skill](https://github.com/swaylq/master-skill) 把**一整行的认知**蒸成 AI——**授人以鱼**。<br>

但还有一件比「替你做」更重要的事——<br>
**让你自己变成会的人。**

<br>

大师替你做这一行的判断，<br>
**学习.skill 把你训练成能自己做判断的人——授人以渔。**

<br>

告诉它你想学什么，<br>
它跑完 8 路调研、按学习科学蒸出一条从 0 到「胜任」的路径，<br>
生成一个**记得你学到哪、按你水平自适应出题批改**的私教 skill。<br>

[🚀 安装](#-安装) · [✨ 私教长什么样](#-私教长什么样) · [🧠 它蒸了什么](#-它蒸了什么) · [⭐ 样本](#-已蒸馏的样本) · [English](README_en.md)

</div>

---

> 📊 &nbsp;**v0.1** — 元 skill + 工具引擎（35 测试全绿）+ **3 个端到端样本**（rust / 线性代数 / 英语阅读，共 40 模块）跑通。
>
> 🧬 &nbsp;**家族第四代** — 站在 同事 / 女娲 / 大师 肩膀上，把元 skill 框架从「蒸专家」翻转成「教你成为专家」。

---

## ✨ 私教长什么样

> 不是「给我列个学习计划」（那种 ChatGPT 一句话就给）。是一个**记得你、陪你练**的私教。

```
你    ❯ 继续学 rust

私教  ❯ 读档：你在「借用与引用」(mastery 0.55)，上次卡在
       &mut 与 & 同时存在的报错。今天先清一个到期复习，再啃这个坎。

       【检索练习 · 借用三原则】不许翻书，背一遍：
       同一作用域，要么 ___ 个 &，要么 ___ 个 &mut，两者 ___ 共存。

你    ❯ 任意多个 &，或者一个 &mut，不能同时

私教  ❯ ✅ 记住了，下次复习排到 6 天后。现在上今天的坎，这段过不了编译：

         let mut v = vec![1,2,3];
         let first = &v[0];
         v.push(4);            // ← 编译器在这里报错
         println!("{first}");

       先别看答案：first 借走了 v 的不可变引用，push 要一个 &mut v，
       这正违反你刚背的哪一条？
```

它做了四件 ChatGPT 学习计划做不到的事：**读档定位** → **间隔复习到期项** → **打到你已知的薄弱点** → **苏格拉底式逼你自己想**。每次都接着上次，不重问「你学到哪了」。

---

## 🧠 它蒸了什么

每个生成的 `{技能}-learn` 是一个自包含目录，分三层：

- 📚 **课程层** `curriculum.json` / `curriculum.md` — 先修排序、Dreyfus 分段的模块。每个带：学习目标（Bloom 分层）+ 正典资源 + **可评估练习** + 里程碑项目 + 「你会了的标志」。
- 🧑‍🏫 **教学层** `SKILL.md` — 私教本体：读档 → 定位 → 讲解→范例→撤支架→独立练 → 出题批改。
- 🗂️ **档案层** `learner-state.json` — 你的进度 / 错题 / **SM-2 间隔重复排程** / 打卡（私人，不进 git）。

蒸的不是资料堆，是**一条按学习科学搭的路**：Dreyfus 五段切分阶段 · Bloom 定目标层级 · 刻意练习（每模块必有可评估练习）· 间隔重复 + 检索练习 · 合意难度（worked-example → 撤支架）。方法论见 [`references/pedagogy-framework.md`](references/pedagogy-framework.md)。

### 诚实边界（家族 DNA）

- **天花板 = 胜任**：私教带你到「能独立做常规任务」，精通/专家靠之后多年真实实践——明说，不吹「成为专家」。
- AI 教不了的（手艺/身体/社交的真实反馈）**诚实标注**转上传/线下/真人，不假装能批改。
- 资源/工具 3-6 月衰减，先修图 + 教学法不衰减（`update 学习 X` 增量刷新）。

---

## ⚡ 安装

```bash
# Claude Code
git clone https://github.com/swaylq/learn-skill.git ~/.claude/skills/learn-skill
```

<details>
<summary><b>🛠️ 其他 host</b></summary>

<br>

```bash
python3 tools/install.py install --host <claude|openclaw|codex|hermit> --source <生成的 {技能}-learn 目录>
python3 tools/install.py list-hosts
```

</details>

---

## 🚀 用法

装好 learn-skill 的 agent 里，直接说：

```
> 学 rust              # 没装过 → 触发蒸一个 rust-learn
> 继续学 rust           # 已有 → 读档接着教
> 考我 rust 所有权       # 触发对应模块的检索练习
> update 学习 rust      # 半年后增量刷新资源/工具
```

它先跟你确认（技能、现有水平、目标、每周时间、locale），然后启动 **8 路并行调研** → 按学习科学蒸馏 → 生成三层私教目录。

---

## ⭐ 已蒸馏的样本

| 技能 | 类型 | 模块 | 路径 |
|------|------|------|------|
| **Rust 编程** | 硬技术（认知甜区） | 15（novice→competent） | [prototypes/rust-learn/](prototypes/rust-learn/) |
| **线性代数** | 认知 / 数学 | 13（novice→competent） | [prototypes/linear-algebra-learn/](prototypes/linear-algebra-learn/) |
| **英语阅读理解** | 语言 · 认知甜区 | 12（novice→competent） | [prototypes/english-reading-learn/](prototypes/english-reading-learn/) |

> 想学不在列表里的？装上 learn-skill，说「学 XXX」就行。

---

## 🔬 工作原理

```
0  技能澄清       ← 收窄过粗的技能 + 探测水平/目标/时间/技能类型
1  8 路并行调研    ← 知识地图 / 正典 / 高手路径 / 刻意练习 / 卡点 / 评估 / 反馈 / 动机
   ─ 调研评审关卡
2  框架蒸馏        ← 建先修 DAG → Dreyfus 分段 → 填模块 → 三重验证
   ─ 蒸馏评审关卡
3  写出 skill      ← curriculum_builder 校验+渲染课程；生成私教 + 档案 schema
4  质检           ← 10 项学习特化 rubric + validation gate
5  双 agent 精炼   ← 优化「激活即开课」+ 自适应是否真用了档案
```

详见 [SKILL.md](SKILL.md)。

---

## 📂 项目结构

```
learn-skill/
├── SKILL.md                  # 元 skill：8 路调研 → 蒸课程 → 生成私教
├── prompts/                  # intake + 8 路调研 + synthesis + quality_check
├── references/               # pedagogy-framework（学习科学核心）+ skill-template
├── tools/                    # curriculum_builder · learner_state · install · self_test
├── prototypes/               # 3 个端到端样本：rust / 线性代数 / 英语阅读
└── tests/                    # 35 个测试（纯标准库，零依赖）
```

---

## 📄 路线图

| 版本 | 内容 | 状态 |
|------|------|------|
| v0.1 | 元 skill + 工具引擎 + **3 个甜区样本**（rust / 线性代数 / 英语阅读）+ 打包 | ✅ |
| v1.x | 质检自动化（quality_check.py / validation_gate.py）+ source_verifier + 增量刷新 update_skill.py | 🔲 |
| v2.x | 官网（点开就能试学）+ 女娲蒸「名师教学风格」sub-skill + cli/ 练习套件 + PyPI | 🔲 |

详见 [ROADMAP.md](ROADMAP.md)。

---

## 📜 许可证

MIT — 随便用，随便改，随便造。

<div align="center">

<br>

**🧬 同事.skill** 蒸一个**具体的人**做什么。<br>
**🌟 女娲.skill** 蒸**任何人**怎么想。<br>
**🎓 大师.skill** 蒸**一整行**的认知 —— 授人以鱼。<br>
**📖 学习.skill** 蒸**一条让你自己学会的路** —— 授人以渔。<br>

<br>

MIT License © [swaylq](https://github.com/swaylq) · 中文 README · [English](README_en.md)

</div>
