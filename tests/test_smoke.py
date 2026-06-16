def test_imports_resolve():
    import tools  # noqa: F401


def test_pedagogy_constants_shape():
    from tools import pedagogy_constants as pc
    assert pc.DREYFUS_STAGES[0] == "novice"
    assert pc.DREYFUS_STAGES[-1] == "expert"
    assert len(pc.DREYFUS_STAGES) == 5
    assert pc.BLOOM_LEVELS[0] == "remember"
    assert "create" in pc.BLOOM_LEVELS
