# 学习.skill Tooling Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the pure-Python tooling engine that every generated `{skill}-learn` tutor reuses — the prereq-DAG curriculum builder and the stateful learner-progress store.

**Architecture:** Two independent, side-effect-light modules under `tools/`, sharing one tiny constants module. `curriculum_builder.py` turns a structured module list (a prereq DAG) into a topologically-ordered, Dreyfus-staged curriculum and renders it to markdown. `learner_state.py` is the dynamic, per-user `learner-state.json` companion that makes the tutor stateful (progress, weak spots, SM-2-lite spaced repetition, streaks). Both are forkable from / parallel to master-skill's `tools/` but are net-new IP for the learning axis.

**Tech Stack:** Python 3.11+, standard library only (`json`, `datetime`, `pathlib`, `dataclasses` not required), pytest for tests. Zero third-party runtime deps (mirrors master-skill's "zero external deps" value).

**Scope of THIS plan:** `tools/pedagogy_constants.py`, `tools/curriculum_builder.py`, `tools/learner_state.py` + their tests. Out of scope (later plans): SKILL.md, 8 research prompts, `pedagogy-framework.md`, `skill_writer.py`, `source_verifier.py` fork, `quality_check.py`/`validation_gate.py`, the rust prototype run, README/packaging.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `conftest.py` (project root) | Empty — makes pytest add the project root to `sys.path` so `from tools import …` resolves. |
| `tools/__init__.py` | Empty — marks `tools/` an importable package. |
| `tools/pedagogy_constants.py` | Shared enums: `DREYFUS_STAGES`, `BLOOM_LEVELS`. One source of truth, imported by both modules. |
| `tools/curriculum_builder.py` | `topo_sort`, `validate_dag`, `segment_by_dreyfus`, `render_curriculum_md`. Stateless functions over a structured module list. |
| `tools/learner_state.py` | `init_state`, `load_state`, `save_state`, `validate_state`, `update_module`, `record_exercise`, `schedule_review`, `due_reviews`, `bump_streak`. Operates on a `learner-state` dict; all date logic takes an injected `today` (ISO string) for deterministic tests. |
| `tests/test_curriculum_builder.py` | Tests for the four curriculum functions. |
| `tests/test_learner_state.py` | Tests for the nine state functions. |

**Data contract — a `curriculum` is** `{"skill": str, "modules": [module, ...]}` where each `module` is:

```python
{
  "id": "ownership-borrowing",          # unique slug
  "title": "所有权与借用",
  "dreyfus_stage": "advanced_beginner", # one of DREYFUS_STAGES
  "prereqs": ["syntax-basics"],         # list of other module ids
  "objectives": [{"text": "能解释 move 语义", "bloom": "understand"}],
  "resources": [{"title": "TRPL ch.4", "url": "https://…", "type": "primary"}],
  "exercises": [{"kind": "drill", "prompt": "…", "assessable": True}],
  "milestone": {"project": "写个不用 clone 的链表", "competence_check": "能独立过 borrow checker"},
  "honest_limit": None,                  # or a string when AI can't grade this module
}
```

**Note:** `learner-state.modules` refines the spec §7 sketch from a *list* to a *dict keyed by `module_id`* for O(1) update. Everything else matches spec §7.

---

## Task 1: Project tooling setup

**Files:**
- Create: `conftest.py`
- Create: `tools/__init__.py`
- Create: `tests/__init__.py` (absent on purpose — skip; pytest discovers `tests/` without it)

- [ ] **Step 1: Create the package + pytest path files**

```bash
cd /Users/mac/claudeclaw/skill-writer/projects/learn-skill
mkdir -p tools tests
: > tools/__init__.py
: > conftest.py
```

- [ ] **Step 2: Add a smoke test**

Create `tests/test_smoke.py`:

```python
def test_imports_resolve():
    import tools  # noqa: F401
```

- [ ] **Step 3: Run it to verify pytest + import path work**

Run: `python -m pytest tests/test_smoke.py -v`
Expected: PASS (1 passed). If `ModuleNotFoundError: tools`, the root `conftest.py` is missing.

- [ ] **Step 4: Commit**

```bash
git add conftest.py tools/__init__.py tests/test_smoke.py
git commit -m "chore: pytest scaffold for learn-skill tools"
```

---

## Task 2: Pedagogy constants

**Files:**
- Create: `tools/pedagogy_constants.py`
- Test: `tests/test_smoke.py` (extend)

- [ ] **Step 1: Write the failing test** — append to `tests/test_smoke.py`:

```python
def test_pedagogy_constants_shape():
    from tools import pedagogy_constants as pc
    assert pc.DREYFUS_STAGES[0] == "novice"
    assert pc.DREYFUS_STAGES[-1] == "expert"
    assert len(pc.DREYFUS_STAGES) == 5
    assert pc.BLOOM_LEVELS[0] == "remember"
    assert "create" in pc.BLOOM_LEVELS
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_smoke.py::test_pedagogy_constants_shape -v`
Expected: FAIL with `ModuleNotFoundError` / `AttributeError`.

- [ ] **Step 3: Implement** — create `tools/pedagogy_constants.py`:

```python
"""Shared pedagogy enums — one source of truth for stage/level ordering."""

# Dreyfus model of skill acquisition — drives curriculum stage segmentation.
DREYFUS_STAGES = ["novice", "advanced_beginner", "competent", "proficient", "expert"]

# Bloom's revised taxonomy — drives per-objective cognitive level.
BLOOM_LEVELS = ["remember", "understand", "apply", "analyze", "evaluate", "create"]
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_smoke.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/pedagogy_constants.py tests/test_smoke.py
git commit -m "feat(tools): pedagogy constants (Dreyfus stages, Bloom levels)"
```

---

## Task 3: `curriculum_builder.topo_sort`

**Files:**
- Create: `tools/curriculum_builder.py`
- Test: `tests/test_curriculum_builder.py`

- [ ] **Step 1: Write the failing test** — create `tests/test_curriculum_builder.py`:

```python
import pytest
from tools import curriculum_builder as cb


def _mods(*pairs):
    """pairs of (id, [prereqs]) -> minimal module dicts."""
    return [{"id": i, "title": i, "dreyfus_stage": "novice", "prereqs": list(p)}
            for i, p in pairs]


def test_topo_sort_orders_prereqs_first():
    mods = _mods(("b", ["a"]), ("a", []), ("c", ["b"]))
    order = [m["id"] for m in cb.topo_sort(mods)]
    assert order.index("a") < order.index("b") < order.index("c")


def test_topo_sort_stable_for_independent_nodes():
    mods = _mods(("a", []), ("b", []), ("c", []))
    assert [m["id"] for m in cb.topo_sort(mods)] == ["a", "b", "c"]


def test_topo_sort_raises_on_cycle():
    mods = _mods(("a", ["b"]), ("b", ["a"]))
    with pytest.raises(ValueError, match="cycle"):
        cb.topo_sort(mods)


def test_topo_sort_raises_on_unknown_prereq():
    mods = _mods(("a", ["ghost"]))
    with pytest.raises(ValueError, match="unknown prereq"):
        cb.topo_sort(mods)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_curriculum_builder.py -v`
Expected: FAIL with `ModuleNotFoundError: tools.curriculum_builder`.

- [ ] **Step 3: Implement** — create `tools/curriculum_builder.py`:

```python
"""Turn a structured module list (a prereq DAG) into a staged, rendered curriculum."""
from __future__ import annotations

from tools.pedagogy_constants import DREYFUS_STAGES


def topo_sort(modules: list[dict]) -> list[dict]:
    """Kahn's algorithm. Stable in input order among zero-indegree nodes.

    Raises ValueError on an unknown prereq or a cycle.
    """
    by_id = {m["id"]: m for m in modules}
    indeg = {m["id"]: 0 for m in modules}
    adj: dict[str, list[str]] = {m["id"]: [] for m in modules}
    for m in modules:
        for p in m.get("prereqs", []):
            if p not in by_id:
                raise ValueError(f"unknown prereq {p!r} for module {m['id']!r}")
            adj[p].append(m["id"])
            indeg[m["id"]] += 1
    queue = [m["id"] for m in modules if indeg[m["id"]] == 0]
    order: list[str] = []
    while queue:
        n = queue.pop(0)
        order.append(n)
        for nb in adj[n]:
            indeg[nb] -= 1
            if indeg[nb] == 0:
                queue.append(nb)
    if len(order) != len(modules):
        raise ValueError("cycle detected in prereq graph")
    return [by_id[i] for i in order]
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_curriculum_builder.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/curriculum_builder.py tests/test_curriculum_builder.py
git commit -m "feat(tools): topo_sort for prereq DAG"
```

---

## Task 4: `curriculum_builder.validate_dag`

**Files:**
- Modify: `tools/curriculum_builder.py`
- Test: `tests/test_curriculum_builder.py` (extend)

- [ ] **Step 1: Write the failing test** — append:

```python
def test_validate_dag_clean_graph_no_errors():
    mods = _mods(("a", []), ("b", ["a"]))
    assert cb.validate_dag(mods) == []


def test_validate_dag_reports_unknown_prereq():
    mods = _mods(("a", ["ghost"]))
    errs = cb.validate_dag(mods)
    assert any("ghost" in e for e in errs)


def test_validate_dag_reports_cycle():
    mods = _mods(("a", ["b"]), ("b", ["a"]))
    assert any("cycle" in e for e in cb.validate_dag(mods))


def test_validate_dag_reports_duplicate_ids():
    mods = _mods(("a", []), ("a", []))
    assert any("duplicate" in e for e in cb.validate_dag(mods))
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_curriculum_builder.py -k validate_dag -v`
Expected: FAIL with `AttributeError: module 'tools.curriculum_builder' has no attribute 'validate_dag'`.

- [ ] **Step 3: Implement** — append to `tools/curriculum_builder.py`:

```python
def validate_dag(modules: list[dict]) -> list[str]:
    """Return a list of human-readable problems; empty list means valid."""
    errors: list[str] = []
    ids = [m["id"] for m in modules]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        errors.append(f"duplicate module ids: {dup}")
    idset = set(ids)
    unknown = False
    for m in modules:
        for p in m.get("prereqs", []):
            if p not in idset:
                errors.append(f"module {m['id']!r} has unknown prereq {p!r}")
                unknown = True
    if not dup and not unknown:
        try:
            topo_sort(modules)
        except ValueError:
            errors.append("prereq graph has a cycle")
    return errors
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_curriculum_builder.py -v`
Expected: PASS (8 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/curriculum_builder.py tests/test_curriculum_builder.py
git commit -m "feat(tools): validate_dag (dupes, unknown prereqs, cycles)"
```

---

## Task 5: `curriculum_builder.segment_by_dreyfus`

**Files:**
- Modify: `tools/curriculum_builder.py`
- Test: `tests/test_curriculum_builder.py` (extend)

- [ ] **Step 1: Write the failing test** — append:

```python
def test_segment_groups_by_stage_in_dreyfus_order():
    mods = [
        {"id": "x", "title": "x", "dreyfus_stage": "competent", "prereqs": []},
        {"id": "y", "title": "y", "dreyfus_stage": "novice", "prereqs": []},
    ]
    segs = cb.segment_by_dreyfus(mods)
    assert [s["stage"] for s in segs] == ["novice", "competent"]
    assert [m["id"] for m in segs[0]["modules"]] == ["y"]


def test_segment_omits_empty_stages():
    mods = [{"id": "y", "title": "y", "dreyfus_stage": "novice", "prereqs": []}]
    segs = cb.segment_by_dreyfus(mods)
    assert len(segs) == 1 and segs[0]["stage"] == "novice"
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_curriculum_builder.py -k segment -v`
Expected: FAIL with `AttributeError: … has no attribute 'segment_by_dreyfus'`.

- [ ] **Step 3: Implement** — append:

```python
def segment_by_dreyfus(sorted_modules: list[dict]) -> list[dict]:
    """Group modules into stages in DREYFUS order, preserving within-stage order.

    Empty stages are omitted. Pass topo_sort()'d modules to keep prereq order.
    """
    segments: list[dict] = []
    for stage in DREYFUS_STAGES:
        mods = [m for m in sorted_modules if m.get("dreyfus_stage") == stage]
        if mods:
            segments.append({"stage": stage, "modules": mods})
    return segments
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_curriculum_builder.py -v`
Expected: PASS (10 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/curriculum_builder.py tests/test_curriculum_builder.py
git commit -m "feat(tools): segment_by_dreyfus"
```

---

## Task 6: `curriculum_builder.render_curriculum_md`

**Files:**
- Modify: `tools/curriculum_builder.py`
- Test: `tests/test_curriculum_builder.py` (extend)

- [ ] **Step 1: Write the failing test** — append:

```python
def test_render_curriculum_md_has_headers_and_content():
    mods = [{
        "id": "ownership", "title": "所有权", "dreyfus_stage": "novice",
        "prereqs": ["syntax"],
        "objectives": [{"text": "解释 move", "bloom": "understand"}],
        "exercises": [{"kind": "drill", "prompt": "改一个编译错误", "assessable": True}],
        "milestone": {"project": "无 clone 链表", "competence_check": "独立过 borrow checker"},
        "honest_limit": None,
    }]
    md = cb.render_curriculum_md("rust", cb.segment_by_dreyfus(mods))
    assert md.startswith("# rust")
    assert "## 阶段：novice" in md
    assert "所有权" in md and "`(ownership)`" in md
    assert "先修：syntax" in md
    assert "understand" in md
    assert "独立过 borrow checker" in md
    assert md.endswith("\n")


def test_render_curriculum_md_shows_honest_limit():
    mods = [{
        "id": "stroke", "title": "运笔", "dreyfus_stage": "novice", "prereqs": [],
        "objectives": [], "exercises": [], "milestone": None,
        "honest_limit": "需上传作品由真人 critique",
    }]
    md = cb.render_curriculum_md("watercolor", cb.segment_by_dreyfus(mods))
    assert "⚠️ 诚实边界：需上传作品由真人 critique" in md
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_curriculum_builder.py -k render -v`
Expected: FAIL with `AttributeError: … has no attribute 'render_curriculum_md'`.

- [ ] **Step 3: Implement** — append:

```python
def render_curriculum_md(skill: str, stages: list[dict]) -> str:
    """Render staged modules to curriculum.md text. Deterministic, no I/O."""
    lines = [f"# {skill} — 学习路径", ""]
    for seg in stages:
        lines.append(f"## 阶段：{seg['stage']}")
        lines.append("")
        for m in seg["modules"]:
            lines.append(f"### {m['title']}  `({m['id']})`")
            if m.get("prereqs"):
                lines.append(f"- 先修：{', '.join(m['prereqs'])}")
            for obj in m.get("objectives", []):
                lines.append(f"- 目标（{obj['bloom']}）：{obj['text']}")
            for ex in m.get("exercises", []):
                lines.append(f"- 练习（{ex['kind']}）：{ex['prompt']}")
            mile = m.get("milestone")
            if mile:
                lines.append(
                    f"- 里程碑：{mile['project']} — 会了的标志：{mile['competence_check']}"
                )
            if m.get("honest_limit"):
                lines.append(f"- ⚠️ 诚实边界：{m['honest_limit']}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_curriculum_builder.py -v`
Expected: PASS (12 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/curriculum_builder.py tests/test_curriculum_builder.py
git commit -m "feat(tools): render_curriculum_md"
```

---

## Task 7: `learner_state` — init / save / load / validate

**Files:**
- Create: `tools/learner_state.py`
- Test: `tests/test_learner_state.py`

- [ ] **Step 1: Write the failing test** — create `tests/test_learner_state.py`:

```python
import pytest
from tools import learner_state as ls


def test_init_state_has_schema_defaults():
    s = ls.init_state("rust", goal="转行后端", weekly_hours=6,
                      prior_level="编程有基础", start_date="2026-06-16")
    assert s["schema_version"] == ls.SCHEMA_VERSION
    assert s["skill"] == "rust"
    assert s["learner"]["weekly_hours"] == 6
    assert s["placement"]["dreyfus_stage"] == "novice"
    assert s["modules"] == {}
    assert s["streak"]["current"] == 0


def test_validate_state_accepts_fresh_state():
    s = ls.init_state("rust", start_date="2026-06-16")
    assert ls.validate_state(s) == []


def test_validate_state_flags_bad_stage():
    s = ls.init_state("rust", start_date="2026-06-16")
    s["placement"]["dreyfus_stage"] = "wizard"
    assert any("dreyfus_stage" in e for e in ls.validate_state(s))


def test_save_then_load_roundtrips(tmp_path):
    s = ls.init_state("rust", start_date="2026-06-16")
    p = tmp_path / "learner-state.json"
    ls.save_state(p, s)
    assert ls.load_state(p) == s


def test_load_rejects_invalid_state(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text('{"schema_version": 999}', encoding="utf-8")
    with pytest.raises(ValueError):
        ls.load_state(p)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_learner_state.py -v`
Expected: FAIL with `ModuleNotFoundError: tools.learner_state`.

- [ ] **Step 3: Implement** — create `tools/learner_state.py`:

```python
"""learner-state.json — per-user, dynamic, private progress for a {skill}-learn tutor.

The static curriculum is shared/committed; this file is the dynamic, private
companion that makes the tutor stateful. Never committed (see .gitignore).
All date logic takes an injected `today` (ISO 'YYYY-MM-DD') for deterministic tests.
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from tools.pedagogy_constants import DREYFUS_STAGES

SCHEMA_VERSION = 1


def init_state(skill: str, *, goal: str = "", weekly_hours: int = 0,
               prior_level: str = "", start_date: str) -> dict:
    """Create a fresh learner-state dict with schema defaults."""
    return {
        "schema_version": SCHEMA_VERSION,
        "skill": skill,
        "learner": {
            "goal": goal,
            "weekly_hours": weekly_hours,
            "prior_level": prior_level,
            "start_date": start_date,
        },
        "placement": {"dreyfus_stage": "novice", "calibrated_on": None},
        "modules": {},          # module_id -> progress dict
        "exercises": [],
        "misconceptions": [],
        "spaced_queue": [],     # list of {"item","reps","interval","due"}
        "streak": {"current": 0, "longest": 0, "last_session": None},
        "honest_limits_hit": [],
    }


def validate_state(state: dict) -> list[str]:
    """Return a list of structural problems; empty means valid."""
    errors: list[str] = []
    if state.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    for key in ("skill", "learner", "placement", "modules", "exercises",
                "spaced_queue", "streak"):
        if key not in state:
            errors.append(f"missing key: {key}")
    stage = state.get("placement", {}).get("dreyfus_stage")
    if stage is not None and stage not in DREYFUS_STAGES:
        errors.append(f"invalid dreyfus_stage: {stage}")
    return errors


def save_state(path, state: dict) -> None:
    """Atomic write (tmp + replace) so a crash never truncates the file."""
    p = Path(path)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


def load_state(path) -> dict:
    """Read + validate. Raises ValueError on an invalid file."""
    state = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate_state(state)
    if errors:
        raise ValueError(f"invalid learner-state: {errors}")
    return state
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_learner_state.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/learner_state.py tests/test_learner_state.py
git commit -m "feat(tools): learner_state init/save/load/validate"
```

---

## Task 8: `learner_state` — update_module / record_exercise

**Files:**
- Modify: `tools/learner_state.py`
- Test: `tests/test_learner_state.py` (extend)

- [ ] **Step 1: Write the failing test** — append:

```python
def test_update_module_upserts_and_stamps_last_seen():
    s = ls.init_state("rust", start_date="2026-06-16")
    ls.update_module(s, "ownership", today="2026-06-17",
                     status="in_progress", mastery=0.4)
    m = s["modules"]["ownership"]
    assert m["status"] == "in_progress"
    assert m["mastery"] == 0.4
    assert m["last_seen"] == "2026-06-17"


def test_update_module_dedupes_weak_spots():
    s = ls.init_state("rust", start_date="2026-06-16")
    ls.update_module(s, "ownership", today="2026-06-17",
                     add_weak_spots=["lifetime"])
    ls.update_module(s, "ownership", today="2026-06-18",
                     add_weak_spots=["lifetime", "trait 对象"])
    assert s["modules"]["ownership"]["weak_spots"] == ["lifetime", "trait 对象"]


def test_record_exercise_appends():
    s = ls.init_state("rust", start_date="2026-06-16")
    ls.record_exercise(s, "ownership", kind="drill", result="partial",
                       today="2026-06-17")
    assert s["exercises"][-1] == {
        "module": "ownership", "kind": "drill",
        "result": "partial", "ts": "2026-06-17",
    }
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_learner_state.py -k "update_module or record_exercise" -v`
Expected: FAIL with `AttributeError: … has no attribute 'update_module'`.

- [ ] **Step 3: Implement** — append to `tools/learner_state.py`:

```python
def update_module(state: dict, module_id: str, *, today: str,
                  status: str | None = None, mastery: float | None = None,
                  add_weak_spots: list[str] | None = None) -> dict:
    """Upsert a module's progress and stamp last_seen=today."""
    m = state["modules"].get(module_id)
    if m is None:
        m = {"status": "not_started", "mastery": 0.0,
             "weak_spots": [], "last_seen": None}
        state["modules"][module_id] = m
    if status is not None:
        m["status"] = status
    if mastery is not None:
        m["mastery"] = mastery
    for w in add_weak_spots or []:
        if w not in m["weak_spots"]:
            m["weak_spots"].append(w)
    m["last_seen"] = today
    return m


def record_exercise(state: dict, module_id: str, *, kind: str,
                    result: str, today: str) -> dict:
    """Append an attempted-exercise record."""
    rec = {"module": module_id, "kind": kind, "result": result, "ts": today}
    state["exercises"].append(rec)
    return rec
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_learner_state.py -v`
Expected: PASS (8 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/learner_state.py tests/test_learner_state.py
git commit -m "feat(tools): update_module + record_exercise"
```

---

## Task 9: `learner_state` — spaced repetition (schedule_review / due_reviews)

**Files:**
- Modify: `tools/learner_state.py`
- Test: `tests/test_learner_state.py` (extend)

- [ ] **Step 1: Write the failing test** — append:

```python
def test_schedule_review_first_pass_due_next_day():
    s = ls.init_state("rust", start_date="2026-06-16")
    e = ls.schedule_review(s, "borrow rules", quality=5, today="2026-06-16")
    assert e["reps"] == 1 and e["interval"] == 1
    assert e["due"] == "2026-06-17"


def test_schedule_review_intervals_grow():
    s = ls.init_state("rust", start_date="2026-06-16")
    ls.schedule_review(s, "borrow rules", quality=5, today="2026-06-16")  # due +1
    e2 = ls.schedule_review(s, "borrow rules", quality=5, today="2026-06-17")
    assert e2["reps"] == 2 and e2["interval"] == 6 and e2["due"] == "2026-06-23"
    e3 = ls.schedule_review(s, "borrow rules", quality=4, today="2026-06-23")
    assert e3["reps"] == 3 and e3["interval"] == 12 and e3["due"] == "2026-07-05"


def test_schedule_review_failure_resets():
    s = ls.init_state("rust", start_date="2026-06-16")
    ls.schedule_review(s, "borrow rules", quality=5, today="2026-06-16")
    e = ls.schedule_review(s, "borrow rules", quality=1, today="2026-06-17")
    assert e["reps"] == 0 and e["interval"] == 1 and e["due"] == "2026-06-18"


def test_due_reviews_returns_items_due_on_or_before_today():
    s = ls.init_state("rust", start_date="2026-06-16")
    ls.schedule_review(s, "a", quality=5, today="2026-06-16")  # due 06-17
    ls.schedule_review(s, "b", quality=5, today="2026-06-10")  # due 06-11
    assert set(ls.due_reviews(s, today="2026-06-17")) == {"a", "b"}
    assert ls.due_reviews(s, today="2026-06-16") == ["b"]
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_learner_state.py -k "schedule_review or due_reviews" -v`
Expected: FAIL with `AttributeError: … has no attribute 'schedule_review'`.

- [ ] **Step 3: Implement** — append to `tools/learner_state.py`:

```python
def schedule_review(state: dict, item: str, *, quality: int, today: str) -> dict:
    """SM-2-lite. quality 0-5; <3 is a lapse. Updates/creates the queue entry.

    Intervals: pass#1 -> 1d, pass#2 -> 6d, pass#3+ -> previous*2 (rounded).
    A lapse resets reps to 0 and interval to 1d.
    """
    today_d = date.fromisoformat(today)
    entry = next((e for e in state["spaced_queue"] if e["item"] == item), None)
    if entry is None:
        entry = {"item": item, "reps": 0, "interval": 0, "due": today}
        state["spaced_queue"].append(entry)
    if quality < 3:
        entry["reps"] = 0
        entry["interval"] = 1
    else:
        entry["reps"] += 1
        if entry["reps"] == 1:
            entry["interval"] = 1
        elif entry["reps"] == 2:
            entry["interval"] = 6
        else:
            entry["interval"] = round(entry["interval"] * 2)
    entry["due"] = (today_d + timedelta(days=entry["interval"])).isoformat()
    return entry


def due_reviews(state: dict, *, today: str) -> list[str]:
    """Items whose due date is on or before today, in queue order."""
    today_d = date.fromisoformat(today)
    return [e["item"] for e in state["spaced_queue"]
            if date.fromisoformat(e["due"]) <= today_d]
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/test_learner_state.py -v`
Expected: PASS (12 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/learner_state.py tests/test_learner_state.py
git commit -m "feat(tools): SM-2-lite spaced repetition (schedule_review/due_reviews)"
```

---

## Task 10: `learner_state` — bump_streak

**Files:**
- Modify: `tools/learner_state.py`
- Test: `tests/test_learner_state.py` (extend)

- [ ] **Step 1: Write the failing test** — append:

```python
def test_bump_streak_first_session():
    s = ls.init_state("rust", start_date="2026-06-16")
    ls.bump_streak(s, today="2026-06-16")
    assert s["streak"] == {"current": 1, "longest": 1, "last_session": "2026-06-16"}


def test_bump_streak_consecutive_day_increments():
    s = ls.init_state("rust", start_date="2026-06-16")
    ls.bump_streak(s, today="2026-06-16")
    ls.bump_streak(s, today="2026-06-17")
    assert s["streak"]["current"] == 2 and s["streak"]["longest"] == 2


def test_bump_streak_same_day_is_noop():
    s = ls.init_state("rust", start_date="2026-06-16")
    ls.bump_streak(s, today="2026-06-16")
    ls.bump_streak(s, today="2026-06-16")
    assert s["streak"]["current"] == 1


def test_bump_streak_gap_resets_but_keeps_longest():
    s = ls.init_state("rust", start_date="2026-06-16")
    ls.bump_streak(s, today="2026-06-16")
    ls.bump_streak(s, today="2026-06-17")   # current 2, longest 2
    ls.bump_streak(s, today="2026-06-20")   # gap -> reset
    assert s["streak"]["current"] == 1 and s["streak"]["longest"] == 2
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest tests/test_learner_state.py -k bump_streak -v`
Expected: FAIL with `AttributeError: … has no attribute 'bump_streak'`.

- [ ] **Step 3: Implement** — append to `tools/learner_state.py`:

```python
def bump_streak(state: dict, *, today: str) -> dict:
    """Update the daily streak. Consecutive day -> +1, same day -> noop, gap -> reset."""
    s = state["streak"]
    today_d = date.fromisoformat(today)
    last = s["last_session"]
    if last is None:
        s["current"] = 1
    else:
        last_d = date.fromisoformat(last)
        if last_d == today_d:
            pass
        elif last_d == today_d - timedelta(days=1):
            s["current"] += 1
        else:
            s["current"] = 1
    s["longest"] = max(s["longest"], s["current"])
    s["last_session"] = today
    return s
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest tests/ -v`
Expected: PASS (all green — 16 in `test_learner_state.py`, 12 in `test_curriculum_builder.py`, 2 smoke).

- [ ] **Step 5: Commit**

```bash
git add tools/learner_state.py tests/test_learner_state.py
git commit -m "feat(tools): daily streak tracking"
```

---

## Task 11: Full suite green + tooling README

**Files:**
- Create: `tools/README.md`
- Test: all

- [ ] **Step 1: Run the whole suite**

Run: `python -m pytest tests/ -v`
Expected: PASS, ~30 tests, 0 failures.

- [ ] **Step 2: Write `tools/README.md`** documenting the two modules' public functions and the `curriculum` / `learner-state` data contracts (copy the shapes from this plan's File Structure section). No code logic — just the interface table + the data-shape blocks.

- [ ] **Step 3: Commit**

```bash
git add tools/README.md
git commit -m "docs(tools): document curriculum_builder + learner_state interfaces"
```

---

## Self-Review

**1. Spec coverage (this plan only covers the tooling slice of the spec):**
- spec §4 `learner-state.json` layer → Tasks 7-10 ✅
- spec §7 schema (refined list→dict for modules, noted) → Tasks 7-10 ✅
- spec §6 Dreyfus staging → Task 5 (`segment_by_dreyfus`) ✅; Bloom levels surfaced in objectives render → Task 6 ✅
- spec §6 "每模块必须有可评估练习" + behavioral competence check → represented in the data contract + rendered (Task 6); *enforced* by `quality_check.py` which is a LATER plan (noted gap, intentional).
- spec §9 "先修图无环且有据" → `validate_dag` Task 4 ✅
- spec §4 honest_limit surfaced → Task 6 ✅
- NOT in this plan (by scope): SKILL.md, prompts, pedagogy-framework.md, source_verifier, quality_check/validation_gate, skill_writer, prototype run, packaging. Tracked for Plans 2-3.

**2. Placeholder scan:** No "TBD/TODO/handle edge cases" — every step has runnable code/commands. ✅

**3. Type consistency:** `DREYFUS_STAGES` (shared constant) used identically in both modules; `modules` is a dict keyed by id in every `learner_state` function; `curriculum` module dicts use the same keys (`id/title/dreyfus_stage/prereqs/objectives/exercises/milestone/honest_limit`) across Tasks 3-6; spaced-queue entry shape (`item/reps/interval/due`) consistent across Task 9. ✅

---

## Execution Handoff

See the chat message for the two execution options.
