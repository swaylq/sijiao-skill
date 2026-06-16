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
