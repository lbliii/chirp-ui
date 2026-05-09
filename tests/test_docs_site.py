import importlib.util
import os
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_SITE_SCRIPT = REPO_ROOT / "scripts" / "docs_site.py"
PATTERN_DOCS = {
    "navigation.md": "docs/NAVIGATION.md",
    "product-pages.md": "docs/PRODUCT-PAGE-PATTERNS.md",
    "media-sites.md": "docs/MEDIA-SITE-PATTERNS.md",
    "forums.md": "docs/FORUM-SITE-PATTERNS.md",
}


def _load_docs_site_module():
    spec = importlib.util.spec_from_file_location("chirp_ui_docs_site", DOCS_SITE_SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_bengal_env_prepends_workspace_repo(monkeypatch, tmp_path: Path) -> None:
    module = _load_docs_site_module()
    workspace_bengal = tmp_path / "b-stack" / "bengal"
    workspace_bengal.mkdir(parents=True)

    monkeypatch.setattr(module, "_WORKSPACE_BENGAL", workspace_bengal)
    monkeypatch.setenv("PYTHONPATH", "existing-path")

    env = module._build_bengal_env()

    assert env["PYTHONPATH"] == str(workspace_bengal) + os.pathsep + "existing-path"


def test_ensure_workspace_bengal_accepts_workspace_checkout(monkeypatch, tmp_path: Path) -> None:
    module = _load_docs_site_module()
    workspace_bengal = tmp_path / "b-stack" / "bengal"
    workspace_bengal.mkdir(parents=True)

    monkeypatch.setattr(module, "_WORKSPACE_BENGAL", workspace_bengal)
    monkeypatch.setattr(
        module,
        "_resolve_bengal_origin",
        lambda _env: workspace_bengal / "bengal" / "__init__.py",
    )

    module._ensure_workspace_bengal({})


def test_ensure_workspace_bengal_rejects_site_packages(monkeypatch, tmp_path: Path, capsys) -> None:
    module = _load_docs_site_module()
    workspace_bengal = tmp_path / "b-stack" / "bengal"
    workspace_bengal.mkdir(parents=True)

    monkeypatch.setattr(module, "_WORKSPACE_BENGAL", workspace_bengal)
    monkeypatch.setattr(
        module,
        "_resolve_bengal_origin",
        lambda _env: (
            tmp_path / ".venv" / "lib" / "python3.14" / "site-packages" / "bengal" / "__init__.py"
        ),
    )

    with pytest.raises(SystemExit, match="1"):
        module._ensure_workspace_bengal({})

    stderr = capsys.readouterr().err
    assert "installed Bengal package" in stderr
    assert "uv run poe docs-serve" in stderr


def test_pattern_docs_are_published_site_sources() -> None:
    """The Bengal-published docs should expose the shipped 0.7 pattern families."""
    pattern_dir = REPO_ROOT / "site" / "content" / "docs" / "patterns"

    assert (pattern_dir / "_index.md").is_file()
    for filename, canonical_doc in PATTERN_DOCS.items():
        text = (pattern_dir / filename).read_text(encoding="utf-8")

        assert "type: doc" in text
        assert canonical_doc in text
