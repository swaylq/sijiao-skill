# Intake — 技能澄清 + 学习者画像 (Phase 0)

Before any research, pin down six things. Ask conversationally. **Reject over-broad skills.**

## Clarify the skill (narrow aggressively)

Too broad → narrow with the user:

- "AI" → "用 PyTorch 训一个图像分类模型" / "LLM 应用开发"
- "编程" → "Rust 后端" / "前端 React"
- "画画" → "数字板厚涂插画" / "水彩风景"

**Granularity test:** can you name the canonical first resource AND a week-1 exercise? If not, narrower.

## Capture the learner (sets pacing + scaffolding)

1. **现有水平**: 零基础 / 有相关基础（哪些）/ 学过但生疏
2. **目标**: 兴趣 / 转行 / 过考试或认证 / 做出某个具体作品
3. **时间预算**: 每周几小时 + 有没有 deadline
4. **locale**: 中文 / 英文工作语言（决定资源语言 + 表达 DNA）

## Detect skill type (sets honest-limits + route emphasis)

| 类型 | 例 | AI 私教能做到 |
|------|-----|--------------|
| cognitive / knowledge | 编程 / 数学 / 语言阅读 | 全程可教可批改（**甜区**） |
| craft | 画画 / 乐器 / 写作 | 课程可蒸，反馈需上传作品 → route 7 |
| physical | 游泳 / 健身动作 | 课程可蒸，练习反馈必须线下 → route 7 |
| social | 谈判 / 演讲 | 课程 + 角色扮演，真实反馈需真人 |

Record the type → it sets each module's `honest_limit` defaults.

## New vs update

新建 → full pipeline. `update 学习 X` → Phase 0C 增量（只刷 route 2/4/7 这些衰减快的，保护 DAG + 教学法）。

## Output → `intake.json`

```json
{ "skill": "", "skill_cn": "", "granularity_ok": true, "prior_level": "",
  "goal": "", "weekly_hours": 0, "deadline": null, "locale": "",
  "skill_type": "cognitive|craft|physical|social", "mode": "new|update" }
```
