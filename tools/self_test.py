"""Regression over all prototypes: every curriculum DAG validates and every
learner-state example is schema-valid. Run: `python3 -m tools.self_test`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# allow running as a plain script (`python tools/self_test.py`) too
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import curriculum_builder as cb  # noqa: E402
from tools import learner_state as ls  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PROTO_DIR = ROOT / "prototypes"


def check_prototype(d: Path) -> list[str]:
    problems: list[str] = []
    cur = d / "curriculum.json"
    if cur.exists():
        data = json.loads(cur.read_text(encoding="utf-8"))
        errs = cb.validate_dag(data["modules"])
        problems += [f"{d.name}: DAG {e}" for e in errs]
        if not errs:
            cb.topo_sort(data["modules"])  # raises if somehow inconsistent
    ex = d / "learner-state.example.json"
    if ex.exists():
        state = json.loads(ex.read_text(encoding="utf-8"))
        problems += [f"{d.name}: state {e}" for e in ls.validate_state(state)]
    return problems


def main() -> int:
    protos = sorted(p for p in PROTO_DIR.iterdir() if p.is_dir()) if PROTO_DIR.exists() else []
    problems: list[str] = []
    for d in protos:
        problems += check_prototype(d)
    if problems:
        print("SELF-TEST FAIL:")
        for p in problems:
            print(" -", p)
        return 1
    print(f"SELF-TEST OK — {len(protos)} prototype(s) valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
