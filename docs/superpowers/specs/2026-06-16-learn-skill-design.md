# 私教.skill — Design Spec

- **Date:** 2026-06-16
- **Author:** Skill-writer (with sway)
- **Status:** Approved design → ready for implementation planning
- **Repo (planned):** `sijiao-skill` · 私教.skill
- **Lineage:** 同事.skill → 女娲.skill → 大师.skill → **私教.skill**

---

## 1. One-liner

输入任意一个想学的技能，私教.skill 自动跑 **8 路调研**，蒸馏出一套有学习科学支撑的完整学习路径，并生成一个**有状态的私教 skill**——装到任何 agent，它带你从 0 把这门技能学会。

## 2. Positioning

- **master-skill = 授人以鱼**：装上后 agent **替你**做这一行的判断。
- **私教.skill = 授人以渔**：装上后 agent 不替你做，而是**带你自己变成会这门技能的人**。

家族第四代。复用前作跑通的「元 skill」管线，但目标对象从「让 agent 扮演专家」翻转成「让用户成为专家」。

## 3. Goals / Non-goals

**Goals**
- 任意技能都能蒸出一条「从 0 到能用」的学习路径（框架不设硬边界，对标 master-skill「任意行业」的野心）。
- 生成物是**真私教**：有状态、自适应、刻意练习驱动、追踪进度。
- 继承家族的**来源验真 + 诚实边界** DNA。

**Non-goals (YAGNI for V1)**
- 不做官网（V2 再做「点开就能试学」的 Next.js 站）。
- 不追求覆盖「需线下/真人反馈」技能的反馈闭环——这类技能照样蒸课程，但反馈环节诚实标注转线下。
- 不发证、不替代真人导师与社区。
- 生成物的 `cli/` bash 套件、`sub-skills/`（调女娲蒸「最会教这门的人」）列为可选，默认 V2。

## 4. Generated artifact — `{skill}-learn/` = 三层

每个生成的学习 skill 是一个自包含目录，分三层：

```
{skill}-learn/
├── SKILL.md              # 教学层：私教 agent 激活规则 + 教学法协议
├── curriculum.md         # 课程层：先修排序的学习路径（静态 / 共享 / 进 git）
├── learner-state.json    # 档案层：学习者进度（动态 / 私人 / 不进 git，已在 .gitignore）
├── references/
│   ├── research/         # 8 路调研笔记（每条心智模型/资源可追溯来源）
│   │   └── 01-08.md
│   └── pedagogy.md       # 这门技能特化的教学法说明
├── sub-skills/           # 可选（V2）：调女娲蒸「最会教这门的人」的教学风格
└── meta.json             # 机器可读元数据
```

- **课程层 (`curriculum.md`)** — 静态、共享、可进 git。阶段化路径，每个模块 = 学习目标（Bloom 分层）+ 正典资源 + 刻意练习 + 里程碑项目 + 「你会了的标志」（行为化）+ 衰减标注。附先修依赖图（无环）。
- **教学层 (`SKILL.md`)** — 静态、共享。被调用时读档 → 定位学习者在哪 → 用教学法协议教下一口 → 出题批改 → 写回档案。
- **档案层 (`learner-state.json`)** — 动态、私人、**不进 git**。记已学模块 / 各模块 Dreyfus 段位 / 薄弱点 / 错题 / 做过的项目 / 间隔重复排程 / 打卡连续度。

## 5. Meta-skill pipeline (Fork master-skill, swap to learning axis)

阶段照搬 master-skill，调研路线换成「学习轴」：

```
0  技能澄清      ← 粒度太粗主动收窄；探测「现有水平 / 目标 / 时间预算 / 技能类型」
1  8 路并行调研   ← 8 个子 agent，见下表
   ─ 调研评审关卡  ← 用户确认调研质量再继续
2  框架蒸馏      ← 按学习科学搭进阶模型（见 §6），三重验证挡水货
   ─ 蒸馏评审关卡  ← 用户确认课程框架再生成
3  写出 skill     ← 生成三层目录 + curriculum + learner-state schema
4  质检          ← 学习特化质检（见 §9）+ validation gate accept/reject
5  双 agent 精炼  ← 优化「激活即开课」程度
```

增量更新：`update 私教 X` 走 Phase 0C 路径，**SLOW_UPDATE 保护教学法内核 + 先修依赖图**（这些不衰减），只刷会烂的资源/课程/工具。

### 8 路调研 (the new routes)

| # | 路线 | 找什么 | 一手来源例 |
|---|------|--------|-----------|
| 1 | 知识地图 / 先修依赖 | 概念清单 + 依赖顺序（技能树） | 大学课程序列、教材目录、roadmap 图 |
| 2 | 正典教材与课程 | 真正被反复推荐的书/课/MOOC（≥3 独立推荐交叉验证） | 资源本体，非「十大榜单」软文 |
| 3 | 高手当年怎么学的 | 真实路径，非理想路径 | 「我怎么学会 X 的」长文、专家访谈、learning-in-public 日志 |
| 4 | 刻意练习 / 题库（含练习环境） | 该动手做什么、在哪做，按难度分级 | 题集、drill、kata、带反馈的项目、上手环境搭建 |
| 5 | 常见卡点 / 误区 / 平台期 | 新手在哪卡、什么误解、平台期怎么破 | 教学论坛、「为什么新手学不会 X」、错误概念集 |
| 6 | 能力评估 / 里程碑 | 怎么知道到了哪段（行为化标志） | rubric、benchmark、作品集/认证信号 |
| 7 | 反馈与社区 | 真实反馈/批改/陪练从哪来（AI 给不了时） | 导师平台、代码评审、critique 圈、赛事、活跃社区 |
| 8 | 动机 · 习惯 · 节奏 | 学会的人怎么坚持的 + 现实耗时基准 + 平台期/倦怠怎么扛 | 「我怎么坚持学完 X」复盘、现实时间线讨论、习惯/问责法 |

闭环：知道 (1,2) → 跟学 (3) → 练 (4) → 反馈 (7) → 避坑 (5) → 评估 (6) → 坚持 (8)。

每路调研笔记沿用 master-skill 的 `source_id` 规范 + 一手/二手判类 + 黑名单。

## 6. Pedagogy core (the B-graft = our `pedagogy-framework.md`)

对标 master-skill 的 `extraction-framework.md`，但提炼的是「一条从 0 到能用的学习路径」，不是「专家认知」。课程不是把资料排序，是按学习科学搭进阶模型：

- **Dreyfus 五段**（新手 → 进阶新手 → 胜任 → 精通 → 专家）→ 给阶段切分。
- **Bloom 分类**（记忆 → 理解 → 应用 → 分析 → 评价 → 创造）→ 给每模块目标定层级。
- **刻意练习**：每模块必须有「可产出可评估结果」的练习，不是「读完这本书」。
- **间隔重复 + 检索练习**：由 `learner-state.json` 排程哪些该复习。
- **合意难度 / worked-example → faded guidance**：先给范例，再逐步撤支架到独立练习。

**蒸馏三重验证**（对标 master-skill）——每个模块得过：
1. 先修顺序真有依据（非拍脑袋）；
2. 资源真被独立推荐过（≥2 处独立来源）；
3. 练习真能产出可评估的东西。

## 7. `learner-state.json` schema (sketch)

```jsonc
{
  "skill": "rust",
  "learner": { "goal": "转行后端", "weekly_hours": 6, "prior_level": "有编程基础/Rust 零基础", "start_date": "2026-06-16" },
  "placement": { "dreyfus_stage": "advanced_beginner", "calibrated_on": "2026-06-16" },
  "modules": [
    { "id": "ownership-borrowing", "status": "in_progress", "mastery": 0.6,
      "bloom_ceiling": "apply", "weak_spots": ["lifetime 标注"],
      "last_seen": "2026-06-16", "next_review": "2026-06-19" }
  ],
  "exercises": [ { "module": "ownership-borrowing", "kind": "drill", "result": "partial", "ts": "..." } ],
  "misconceptions": ["以为 clone 总是深拷贝"],
  "spaced_queue": [ { "item": "borrow checker 三原则", "due": "2026-06-19" } ],
  "streak": { "current": 5, "longest": 12, "last_session": "2026-06-16" },
  "honest_limits_hit": []
}
```

**Open question (resolve in planning):** 档案存哪——生成 skill 目录内（gitignored）vs 集中 `~/.config/sijiao-skill/<skill>/`（多技能 + 多 host 共享、隐私更清晰）。倾向后者，但 V1 可先放目录内。

## 8. Tutor runtime (使用时)

调用 `{skill}-learn`：
1. 读 `learner-state.json`（首次 → 做几道诊断题做 placement）。
2. 决定今天教什么：下一模块 / 到期复习 / 补薄弱点。
3. 教学法协议：讲解 → 范例（worked example）→ 撤支架练习 → 独立练习 → 反馈。该苏格拉底/费曼的地方用。
4. 出题、批改、更新档案（mastery / 错题 / 下次复习日）。
5. 碰到 AI 教不了的（手艺/身体型）→ 提示上传作品或转线下，**不假装能批改**，记 `honest_limits_hit`。

## 9. Quality gates + honest limits

白嫖 master-skill 的来源验真 / 黑名单 / validation gate，加学习特化几条：

- 先修依赖图**无环且每条边有据**；
- **每个模块有可评估练习**（不是「读完这本书」）；
- 「会了」的标志是**行为化**的（「能做 X」），不是「理解了」；
- 诚实边界**必填**。

**诚实边界（家族 DNA）**：
- AI 看不了你的物理动作 → 手艺/身体型技能给课程，但反馈环节转上传/线下；
- 资源/课程 3–6 月衰减，先修图 + 教学法不衰减（SLOW_UPDATE 保护）；
- 不替代真人导师与社区，不发证；
- placement 是自报 + 诊断题，不是正式测评。

## 10. Repo packaging

仓库结构 + README 套用 `projects/skill-packaging-playbook.md`（已存）：hero + badges → **先放「私教带教」对话样例**（show don't tell）→ 一行安装 → 样本表 → 工作原理 → 项目结构 → roadmap → MIT → star-history。中文 README 为主 + `README_en.md` 镜像。

元 skill 自身仓库结构：

```
sijiao-skill/
├── SKILL.md
├── prompts/{intake, research/01-08, synthesis, quality_check}.md
├── tools/
│   ├── skill_writer.py        # forked
│   ├── curriculum_builder.py  # NEW: 先修图 → 阶段化课程
│   ├── learner_state.py       # NEW: init/update 档案
│   ├── source_verifier.py     # inherited
│   ├── quality_check.py / validation_gate.py / install.py
├── references/{pedagogy-framework, skill-template, decay-table}.md
├── prototypes/{rust-learn, linear-algebra-learn, english-reading-learn}/
└── README.md / README_en.md / ROADMAP.md / LICENSE / .gitignore
```

## 11. Prototypes (甜区起步，对标 master-skill 从 LLM-agent-infra 起步)

| 技能 | 类型 | 为什么选它打头阵 |
|------|------|----------------|
| `rust` | 硬技术 | 题库/编译器反馈丰富，刻意练习闭环天然成立 |
| `线性代数` | 认知/数学 | 先修依赖清晰、评估标准化，最能验证「先修图 + 三重验证」 |
| `英语阅读理解` | 语言·认知甜区 | AI 能出题能批改（口语要实时音频反馈，是 honest-limits 案例，不打头阵） |

## 12. Naming

- 元 skill：**私教.skill**，repo `sijiao-skill`（英文 slug 可再 bikeshed）。
- 生成物：**`{skill}-learn/`**（如 `rust-learn`、`linear-algebra-learn`、`english-reading-learn`）。
- 触发词：「学 X」「我想学 X」「教我 X」「做个 X 的学习 skill」「update 私教 X」。

## 13. Roadmap

| 版本 | 内容 |
|------|------|
| v0.x | SKILL.md 工作流 + 8 路 prompts + tools（fork + curriculum_builder + learner_state）+ pedagogy-framework |
| v1.0 | 第一个甜区样本（rust）端到端跑通 + 仓库公开 |
| v1.x | 线性代数 + 英语阅读理解；学习特化质检 + validation gate |
| v2.x | 官网（Next.js「点开就能试学」）+ sub-skills（女娲蒸名师教学风格）+ cli/ 练习套件 + PyPI 打包 |

## 14. Open questions (for planning)

1. `learner-state.json` 存放位置（目录内 gitignored vs 集中 `~/.config/sijiao-skill/`）。
2. placement 诊断题：每个技能必做 vs 可跳过。
3. tools 从 master-skill fork 的范围——直接 copy 改，还是抽公共库依赖。
4. `curriculum_builder.py` 的先修图表示（DAG 文件格式 + 拓扑排序输出）。
