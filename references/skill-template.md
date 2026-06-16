# Skill Template — `{skill-slug}-learn`

The standard structure 私教.skill generates as **output**. Phase 3 of `SKILL.md` reads this and
fills each `{{placeholder}}` from the Phase 2 synthesis. The pedagogy obeys
`references/pedagogy-framework.md`. A populated example lives at `prototypes/rust-learn/`.

---

## Layout (one sijiao-skill = one directory, three layers)

```
{skill-slug}-learn/
├── SKILL.md                    # 教学层: the tutor agent
├── curriculum.json             # 课程层 source of truth (structured; validated by curriculum_builder)
├── curriculum.md               # 课程层 rendered (render_curriculum_md — never hand-edit)
├── learner-state.example.json  # 档案层 example (real learner-state.json is gitignored, per-user)
├── references/
│   ├── research/01-08.md       # 8-route notes (every claim traces to a source)
│   └── pedagogy.md             # skill-specific teaching notes
├── sub-skills/                 # optional (V2): nuwa-distilled "great teacher of X" styles
└── meta.json                   # machine-readable metadata
```

---

## `curriculum.json` — source of truth

Shape = the data contract in `tools/README.md`: `{"skill": str, "modules": [module, ...]}`.

Build order (use `tools/curriculum_builder.py`): author modules → `validate_dag` (fix all
errors) → `topo_sort` → `segment_by_dreyfus` → `render_curriculum_md` → write `curriculum.md`.
**Never hand-edit `curriculum.md` — regenerate it.**

Each module fills: `id`, `title`, `dreyfus_stage`, `prereqs`, `objectives[{text,bloom}]`,
`resources[{title,url,type}]`, `exercises[{kind,prompt,assessable}]`,
`milestone{project,competence_check}`, `honest_limit`.

---

## `SKILL.md` (the tutor) — literal template

Replace every `{{...}}`. Keep section headers — the tutor looks them up by header.

```markdown
---
name: {{skill-slug}}-learn
description: |
  {{skill-cn-name}} ({{skill-en-name}}) 私教 — 从 0 带到「胜任」的有状态学习教练。
  加载结构化课程 + 教学法协议 + 学习者档案，按你的水平自适应出题、批改、排复习。
  触发词：「学 {{skill}}」「教我 {{skill}}」「继续学 {{skill}}」「考我 {{skill}}」
allowed-tools: Read, Write, Edit, Bash, WebSearch, WebFetch
---

# {{skill-cn-name}} · 私教

> {{one-line: what competence this path delivers, and the honest ceiling.}}

## 激活规则
收到与 {{skill}} 学习相关的请求时，先读 `learner-state.json`，再按【开课协议】教学。

## 开课协议（每次开课）
1. 读 `learner-state.json`（不存在 → 先做【定位诊断】3-5 题，写 placement）。
2. 选今天的焦点：① `due_reviews` 有到期复习 → 先复习；② 否则进 `curriculum.md` 下一模块；
   ③ 某模块 mastery 低或 weak_spots 多 → 先补。
3. 一次只推进一个模块（认知负荷）。

## 教学法协议（per references/pedagogy-framework.md）
- 新概念：讲解 → worked example → 撤支架练习 → 独立练习。
- 技能：直接给可评估的 drill + 反馈。
- 记忆：检索练习，进 `spaced_queue`。
- 难度贴着 mastery 走，略高于当前水平。

## 评估与档案更新
出题 → 批改（right/partial/wrong）→ 调 `tools/learner_state.py`：
`update_module`（mastery / weak_spots）· `record_exercise` · `schedule_review` · `bump_streak`。

## 诚实边界
{{≥3 条：能到的段位上限；衰减最快的模块；需上传/线下反馈的部分；不发证。}}

## 课程大纲
完整路径见 [`curriculum.md`](curriculum.md)（由 `curriculum.json` 渲染）。
```

---

## `learner-state`

Per-user, dynamic, **gitignored**. Ship a `learner-state.example.json` so users see the shape
(schema in `tools/README.md`). The tutor reads/writes the real file via `tools/learner_state.py`.

## `meta.json` template

```json
{
  "name": "{{skill-slug}}-learn",
  "skill": "{{skill-en-name}}",
  "skill_cn": "{{skill-cn-name}}",
  "locale": "{{en|zh-CN|global}}",
  "profile": "{{from-zero|has-basics}}",
  "last_research_date": "{{YYYY-MM-DD}}",
  "source_count": 0,
  "primary_source_ratio": 0.0,
  "modules_count": 0,
  "dreyfus_ceiling": "competent",
  "generator": "sijiao-skill v{{X.Y}}",
  "version": "{{X.Y}}",
  "changelog": []
}
```

---

## Filling rules (for Phase 3)

1. **Never** fluff a placeholder — every one traces to a line in `references/research/0X-*.md`.
2. Thin coverage → write `_(薄弱覆盖 — 见诚实边界)_`, don't pad. Empty > fake.
3. Citations are real URLs to **specific pages** actually opened — never homepages or search pages.
4. Every module passes the three-fold validation (prereq-justified / resource-backed / practice-assessable).
5. Exercises are assessable; competence checks are **behavioral** ("能独立做 X", not "理解 X").
6. Locale: a `zh-CN` skill talks Chinese-internet idiom; an `en` skill uses the field's English.

## Anti-patterns

- ❌ `module: 学基础` — vague; what specifically, in what order?
- ❌ objectives that never leave *understand* — no practice.
- ❌ `exercise: 多做练习` — not assessable.
- ❌ competence check `理解了 X` — not behavioral; use `能独立做 X`.
- ❌ citing a homepage / search-results / topic page.
- ❌ skipping 诚实边界, or claiming a tutor produces an *expert*.
