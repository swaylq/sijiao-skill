# `tools/` — learn-skill tooling engine

Pure-Python, stdlib-only helpers reused by every generated `{skill}-learn` tutor.
Run tests from the project root: `python -m pytest tests/ -v`.

## Modules

| Module | Public functions | Responsibility |
|--------|------------------|----------------|
| `pedagogy_constants.py` | `DREYFUS_STAGES`, `BLOOM_LEVELS` | One source of truth for stage / cognitive-level ordering. |
| `curriculum_builder.py` | `topo_sort`, `validate_dag`, `segment_by_dreyfus`, `render_curriculum_md` | Turn a prereq DAG of modules into a topologically-ordered, Dreyfus-staged, rendered `curriculum.md`. Stateless, no I/O. |
| `learner_state.py` | `init_state`, `save_state`, `load_state`, `validate_state`, `update_module`, `record_exercise`, `schedule_review`, `due_reviews`, `bump_streak` | The dynamic, per-user `learner-state.json` store that makes the tutor stateful. All date logic takes an injected `today` (ISO `YYYY-MM-DD`) for deterministic behavior. |

## `curriculum` data contract

A curriculum is `{"skill": str, "modules": [module, ...]}` where each `module`:

```python
{
  "id": "ownership-borrowing",          # unique slug
  "title": "所有权与借用",
  "dreyfus_stage": "advanced_beginner", # one of DREYFUS_STAGES
  "prereqs": ["syntax-basics"],         # ids of other modules
  "objectives": [{"text": "能解释 move 语义", "bloom": "understand"}],
  "resources": [{"title": "TRPL ch.4", "url": "https://…", "type": "primary"}],
  "exercises": [{"kind": "drill", "prompt": "…", "assessable": True}],
  "milestone": {"project": "写个不用 clone 的链表", "competence_check": "能独立过 borrow checker"},
  "honest_limit": None,                  # or a string when AI can't grade this module
}
```

Pipeline: `validate_dag(modules)` → fix any errors → `topo_sort(modules)` →
`segment_by_dreyfus(...)` → `render_curriculum_md(skill, stages)`.

## `learner-state.json` shape

Dynamic, private, **never committed** (see root `.gitignore`). `modules` is a dict
keyed by `module_id` for O(1) update (refines the design-spec §7 list sketch).

```jsonc
{
  "schema_version": 1,
  "skill": "rust",
  "learner": { "goal": "", "weekly_hours": 6, "prior_level": "", "start_date": "2026-06-16" },
  "placement": { "dreyfus_stage": "novice", "calibrated_on": null },
  "modules": {
    "ownership-borrowing": { "status": "in_progress", "mastery": 0.6,
      "weak_spots": ["lifetime 标注"], "last_seen": "2026-06-17" }
  },
  "exercises": [ { "module": "...", "kind": "drill", "result": "partial", "ts": "..." } ],
  "misconceptions": [],
  "spaced_queue": [ { "item": "borrow checker 三原则", "reps": 2, "interval": 6, "due": "2026-06-23" } ],
  "streak": { "current": 5, "longest": 12, "last_session": "2026-06-16" },
  "honest_limits_hit": []
}
```

**Spaced repetition (`schedule_review`)** — SM-2-lite: `quality` 0–5, `<3` is a lapse.
Intervals: pass #1 → 1d, pass #2 → 6d, pass #3+ → previous × 2 (rounded); a lapse
resets to reps 0 / interval 1d.
