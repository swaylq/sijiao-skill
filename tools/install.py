"""Install a generated {skill}-learn into a host's skills directory. Stdlib only.

Usage:
    python3 -m tools.install install --host claude --source ./prototypes/rust-learn
    python3 -m tools.install list-hosts
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# host -> skills dir relative to the user's home
HOSTS = {
    "claude": ".claude/skills",
    "openclaw": ".openclaw/skills",
    "codex": ".codex/skills",
    "hermit": ".hermit/skills",
}

# never copied into an install — per-user / generated / vcs cruft
_IGNORE = shutil.ignore_patterns("learner-state.json", "__pycache__", ".git", "*.pyc")


def host_target(host: str, skill_name: str, home=None) -> Path:
    """Resolve the install path for a skill on a host. Pure (home injectable)."""
    if host not in HOSTS:
        raise ValueError(f"unknown host {host!r}; known: {sorted(HOSTS)}")
    base = Path(home) if home is not None else Path.home()
    return base / HOSTS[host] / skill_name


def install(source, host: str, home=None) -> Path:
    """Copy a skill directory into the host's skills dir; returns the target path.

    The per-user `learner-state.json` is never copied (the `.example.json` is).
    """
    source = Path(source)
    if not source.is_dir():
        raise ValueError(f"source is not a directory: {source}")
    target = host_target(host, source.name, home=home)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target, ignore=_IGNORE)
    return target


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tools.install", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("install", help="install a skill into a host")
    pi.add_argument("--host", required=True, choices=sorted(HOSTS))
    pi.add_argument("--source", required=True, help="path to the {skill}-learn directory")
    sub.add_parser("list-hosts", help="list known hosts and their paths")
    args = p.parse_args(argv)

    if args.cmd == "list-hosts":
        for h, path in HOSTS.items():
            print(f"{h}\t~/{path}/")
        return 0
    if args.cmd == "install":
        target = install(args.source, args.host)
        print(f"installed → {target}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
