---
name: sijiao-skill
description: |
  私教.skill — 输入「我想学的技能」，自动完成 8 路深度调研（知识地图 / 正典教材 / 高手路径 / 刻意练习 / 常见卡点 / 能力评估 / 反馈社区 / 动机节奏），按学习科学蒸馏成一个有状态的「私教」skill。
  生成的 {skill}-learn 是自包含目录（课程 + 教学协议 + 学习者档案），装到任何 agent，从 0 带你到「胜任」。
  触发词：「学 X」「我想学 X」「教我 X」「做个 X 的学习 skill」「带我学 X」「update 私教 X」「继续学 X」「考我 X」。
allowed-tools: Read, Write, Edit, Bash, WebSearch, WebFetch
---

# 私教 · 技能蒸馏术（授人以渔）

> 「同事蒸一个人，女娲蒸一种思维，大师蒸一整行的 OS，私教蒸一条让你自己学会的路。」

## 核心理念

master-skill 让 agent **替你**做专家判断；私教.skill 让 agent **把你变成**会这门技能的人。

一个好的 `{skill}-learn` 不是课程百科，是一条**可运行、从 0 到胜任的路径**，分三层：

- **课程层** `curriculum.json` / `curriculum.md` — 先修排序、Dreyfus 分段的模块，每个带目标 / 资源 / 练习 / 里程碑
- **教学层** `SKILL.md` — 读档 → 定位 → 按教学法协议教 → 出题批改
- **档案层** `learner-state.json` — 进度 / 错题 / 间隔重复 / 打卡（私人、不进 git）

方法论看 `references/pedagogy-framework.md`，产物模板看 `references/skill-template.md`。

## 范围约束（重要）

- **框架不设硬边界**：任何技能都能蒸出课程；但 AI 教不了的（手艺 / 身体 / 社交的真实反馈）**诚实标注**转上传 / 线下 / 真人（route 7），不假装能批改。
- **天花板 = 胜任（competent）**：私教带到「能独立做常规任务」，再往上（精通 / 专家）靠多年真实实践——明说，不吹「成为专家」。
- **甜区优先做样本**：认知 / 知识型（编程 / 数学 / 语言阅读）先跑通，见 `prototypes/`。

## 路径占位符

所有产物落在生成 skill 自己的目录内，自包含：

```
{skill-slug}-learn/   ← Phase 3 产出（结构见 references/skill-template.md）
```

## 执行流程

### Phase 0 · 技能澄清 + 学习者画像
按 `prompts/intake.md`：收窄过粗的技能、采集水平 / 目标 / 时间预算 / locale、探测技能类型（定 honest-limits）。产出 `intake.json`。
- `update 私教 X` → **Phase 0C**：只重跑衰减快的 route 2/4/7，patch 进已有 skill，保护 DAG + 教学法（SLOW_UPDATE 区）。

### Phase 1 · 8 路并行调研
按 `prompts/research/01-08.md`（来源规范见 `prompts/_source_id_manifest.md`）启动 8 个子 agent：

| 路 | 主题 | 路 | 主题 |
|----|------|----|------|
| 1 | 知识地图 / 先修依赖 | 5 | 常见卡点 / 误区 / 平台期 |
| 2 | 正典教材与课程 | 6 | 能力评估 / 里程碑 |
| 3 | 高手当年怎么学的 | 7 | 反馈与社区 |
| 4 | 刻意练习 / 题库 | 8 | 动机 · 习惯 · 节奏 |

每路写 `references/research/0N-*.md`，每条结论挂 `source_id`。
- **调研评审关卡**：让用户确认调研质量再往下（垃圾输入污染下游）。

### Phase 2 · 框架蒸馏
按 `prompts/synthesis.md` + `references/pedagogy-framework.md`：建先修 DAG（`validate_dag` 通过）→ Dreyfus 分段（天花板 competent）→ 填每个模块（Bloom 目标 / 正典资源 / **≥1 可评估练习** / 行为化里程碑 / `honest_limit`）→ 织入卡点 → 三重验证（先修有据 / 资源被独立推荐 / 练习可评估）。
- **蒸馏评审关卡**：先给课程骨架（模块 + 顺序）让用户确认，再填全。

### Phase 3 · 写出 skill
按 `references/skill-template.md` 生成三层目录：
- `curriculum.json` →（`tools/curriculum_builder.py`：`validate_dag` → `topo_sort` → `segment_by_dreyfus` → `render_curriculum_md`）→ `curriculum.md`
- 教学层 `SKILL.md`（填模板：开课协议读 `learner-state.json`、教学法协议、调 `tools/learner_state.py` 更新档案）
- `learner-state.example.json` + `pedagogy.md` + `meta.json` + `references/research/` 留痕

### Phase 4 · 质检
按 `prompts/quality_check.md` 跑 10 项（来源一手率 / DAG 无环且有据 / 每模块有可评估练习 / 里程碑行为化 / Bloom 递进 / 天花板诚实 / 资源真且具体 / 诚实边界齐 / learner-state 接好 / locale 一致）。validation gate 出 accept / conditional / reject + 具体改法。critical 失败（黑名单源 / 环 / 模块无练习 / 吹「专家」）一票否决。

### Phase 5 · 双 agent 精炼
一个 agent 扮零基础学习者走一遍开课，另一个查「激活即开课」「自适应是否真用了档案」，修到顺。

## 调用生成出来的 skill

```
> 学 rust            # 没装过 → 触发本 skill 蒸一个 rust-learn
> 继续学 rust         # 已有 rust-learn → 读档接着教
> 考我 rust 所有权     # 触发对应模块的检索练习
> update 私教 rust    # 半年后增量刷新资源 / 工具
```

装到任意 host：`python3 tools/install.py install --host claude --source ./rust-learn`。

## 品味守则（速查）

- 课程是**路径**不是书单；每模块必有「会了的标志」+ 可评估练习。
- 顺序按真实先修，不按目录页。
- **诚实 > 完整**：教不了的明说，到不了专家明说。
- 私教**记得你**：每次读档、按档案自适应，不重复问「你学到哪」。

## 与其他 skill 的关系

- **同事.skill** 蒸一个具体的人做什么。
- **女娲.skill** 蒸任何人怎么想。
- **大师.skill** 蒸一整行的认知 + 工作流 + 工具（**授人以鱼**）。
- **私教.skill** 蒸一条让你自己学会的路（**授人以渔**）。Phase 3 可选调女娲蒸「最会教这门的名师」当 sub-skill。
