import pytest
from tools import learner_state as ls


# --- init / save / load / validate ---

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


# --- update_module / record_exercise ---

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


# --- spaced repetition ---

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


# --- streak ---

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
