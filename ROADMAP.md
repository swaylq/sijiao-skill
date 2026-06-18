# Roadmap — 私教.skill

家族第四代（同事 → 女娲 → 大师 → 私教）。把元 skill 框架从「蒸专家」翻转成「教你成为专家」——授人以渔。

## v0.1 — 地基 ✅

- **工具引擎**（纯标准库，35 测试全绿）
  - `curriculum_builder.py` — 先修 DAG 拓扑排序 + 环/未知先修/重复 id 校验 → Dreyfus 分段 → 渲染 `curriculum.md`
  - `learner_state.py` — 进度 / 错题 / SM-2-lite 间隔重复 / 打卡，原子写、注入式日期
  - `install.py` — 四宿主安装器 · `self_test.py` — 全样本回归
- **元 skill 内容**
  - `SKILL.md` — phases 0-5 工作流
  - `prompts/` — intake + 8 路调研 + 来源规范 + synthesis + quality_check
  - `references/pedagogy-framework.md` — 学习科学核心（Dreyfus / Bloom / 刻意练习 / 间隔重复 / 合意难度）
  - `references/skill-template.md` — `{skill}-learn` 产物模板
- **五个端到端样本** `prototypes/` — `rust-learn`(15) / `linear-algebra-learn`(13) / `english-reading-learn`(12) / `weight-loss-learn`(13) / `skincare-learn`(13)，均 novice→competent、三层齐全、DAG 经引擎校验；`weight-loss-learn` / `skincare-learn` 是非认知（生理+行为）技能，演示框架的「诚实降级」（医学/自报转线下）
- **开源打包** — README（中/英）+ ROADMAP + LICENSE + MIT

## v1.x — 拓宽 + 质检自动化 🔲

- `quality_check.py` + `validation_gate.py` — 把 `prompts/quality_check.md` 的 10 项 rubric 落成可跑代码（加权 accept/reject）
- `source_verifier.py` — URL 自动判类 + 黑名单强拦截（fork master-skill）
- `update_skill.py` — Phase 0C 增量刷新（SLOW_UPDATE 保护教学法 + 先修图）

## v2.x — 产品化 🔲

- **官网**（Next.js「点开就能试学」）— 在线和各技能的私教对话
- 调**女娲.skill** 蒸「最会教这门的名师」教学风格，嵌进 `sub-skills/`
- `cli/` — 把课程物化成可跑的练习套件（drill runner）
- PyPI 打包 + GitHub Action 定时刷新

## 设计取舍（来自 brainstorm）

- **框架不设硬边界，但样本从甜区起步** —— 对标 master-skill 从 LLM-agent-infra 起步往外扩。
- **天花板 = 胜任** —— 私教不吹「成为专家」；精通靠多年真实实践。
- **静态课程 / 动态档案分离** —— 课程进 git、可共享；`learner-state.json` 私人、不进 git。这是「真私教」跟「ChatGPT 列计划」的分水岭。
