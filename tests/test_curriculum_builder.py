import pytest
from tools import curriculum_builder as cb


def _mods(*pairs):
    """pairs of (id, [prereqs]) -> minimal module dicts."""
    return [{"id": i, "title": i, "dreyfus_stage": "novice", "prereqs": list(p)}
            for i, p in pairs]


# --- topo_sort ---

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


# --- validate_dag ---

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


# --- segment_by_dreyfus ---

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


# --- render_curriculum_md ---

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
