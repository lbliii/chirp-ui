import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPO_ROOT / "pyproject.toml"
SHOWCASE_DOCKERFILE = REPO_ROOT / "examples" / "component-showcase" / "Dockerfile"


def test_showcase_extra_includes_chirp_startup_dependencies() -> None:
    project = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]
    showcase_dependencies = project["optional-dependencies"]["showcase"]

    assert "bengal-chirp>=0.10.0" in showcase_dependencies
    assert "itsdangerous>=2.2.0" in showcase_dependencies


def test_showcase_image_installs_showcase_extra() -> None:
    dockerfile = SHOWCASE_DOCKERFILE.read_text(encoding="utf-8")

    assert 'RUN pip install ".[showcase]"' in dockerfile
