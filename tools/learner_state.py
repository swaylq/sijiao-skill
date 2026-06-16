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
