import importlib.util
import os
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_SITE_SCRIPT = REPO_ROOT / "scripts" / "docs_site.py"


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
