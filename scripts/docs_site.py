#!/usr/bin/env python3
"""Run Bengal docs commands against this repo's site root.

Relative ``site`` arguments can resolve to the Bengal checkout's own docs when
``bengal`` is installed from a sibling editable workspace. This helper pins the
source path to ``chirp-ui/site`` and gives local preview commands a clean asset
baseline before the dev server starts watching for changes.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "site"
_WORKSPACE_BENGAL = REPO_ROOT.parent / "b-stack" / "bengal"


def _build_bengal_env() -> dict[str, str]:
    """Prefer a sibling Bengal checkout when this repo lives in the b-stack workspace."""
    env = dict(os.environ)
    if not _WORKSPACE_BENGAL.exists():
        return env

    bengal_repo = str(_WORKSPACE_BENGAL)
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        bengal_repo
        if not existing_pythonpath
        else bengal_repo + os.pathsep + existing_pythonpath
    )
    return env


def _resolve_bengal_origin(env: dict[str, str]) -> Path | None:
    """Resolve the Bengal module path that the child docs command would import."""
    probe = subprocess.run(
        [
            sys.executable,
            "-c",
            "import bengal; from pathlib import Path; print(Path(bengal.__file__).resolve())",
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    output = probe.stdout.strip().splitlines()
    if not output:
        return None
    return Path(output[-1])


def _ensure_workspace_bengal(env: dict[str, str]) -> None:
    """Fail fast when preview commands would use the installed Bengal package."""
    if not _WORKSPACE_BENGAL.exists():
        return

    try:
        bengal_origin = _resolve_bengal_origin(env)
    except (subprocess.CalledProcessError, OSError) as exc:
        print(
            "Could not verify which Bengal checkout the docs preview would use.",
            file=sys.stderr,
        )
        print(
            "Try `uv sync --group dev --group docs`, then rerun `uv run poe docs-serve`.",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    if bengal_origin is not None and bengal_origin.is_relative_to(_WORKSPACE_BENGAL):
        return

    resolved = str(bengal_origin) if bengal_origin is not None else "<unresolved>"
    print(
        "Refusing to run docs preview with the installed Bengal package.",
        file=sys.stderr,
    )
    print(f"Resolved Bengal import: {resolved}", file=sys.stderr)
    print(f"Expected workspace checkout under: {_WORKSPACE_BENGAL}", file=sys.stderr)
    print(
        "Run `uv sync --group dev --group docs`, then rerun `uv run poe docs-serve`.",
        file=sys.stderr,
    )
    raise SystemExit(1)


def _run_bengal(*args: str) -> None:
    env = _build_bengal_env()
    _ensure_workspace_bengal(env)
    subprocess.run(
        [sys.executable, "-m", "bengal", *args],
        cwd=REPO_ROOT,
        env=env,
        check=True,
    )


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in {"build", "serve"}:
        print("Usage: python scripts/docs_site.py [build|serve]", file=sys.stderr)
        return 2

    command = argv[1]
    if command == "build":
        _run_bengal("site", "build", "--clean-output", str(SITE_ROOT))
        return 0

    _run_bengal("site", "serve", str(SITE_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
