import pytest
from tools import install


def test_host_target_maps_known_hosts(tmp_path):
    t = install.host_target("claude", "rust-learn", home=tmp_path)
    assert t == tmp_path / ".claude/skills/rust-learn"


def test_host_target_rejects_unknown_host(tmp_path):
    with pytest.raises(ValueError, match="unknown host"):
        install.host_target("ghost", "x", home=tmp_path)


def test_install_copies_tree_and_skips_learner_state(tmp_path):
    src = tmp_path / "demo-learn"
    (src / "references").mkdir(parents=True)
    (src / "SKILL.md").write_text("x", encoding="utf-8")
    (src / "learner-state.json").write_text("{}", encoding="utf-8")          # per-user
    (src / "learner-state.example.json").write_text("{}", encoding="utf-8")  # shipped
    home = tmp_path / "home"

    target = install.install(src, "claude", home=home)

    assert (target / "SKILL.md").exists()
    assert (target / "references").is_dir()
    assert (target / "learner-state.example.json").exists()
    assert not (target / "learner-state.json").exists()  # per-user state never copied


def test_install_overwrites_existing(tmp_path):
    src = tmp_path / "demo-learn"
    src.mkdir()
    (src / "SKILL.md").write_text("v2", encoding="utf-8")
    home = tmp_path / "home"
    install.install(src, "claude", home=home)
    target = install.install(src, "claude", home=home)  # second install, no error
    assert (target / "SKILL.md").read_text(encoding="utf-8") == "v2"


def test_self_test_passes_on_repo():
    from tools import self_test
    assert self_test.main() == 0
