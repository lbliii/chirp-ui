"""Contract proofs for Chirp ``app.check()`` with ``use_chirp_ui`` (#389, #390)."""

from __future__ import annotations

import contextlib
import io
import tempfile
from pathlib import Path

import pytest

pytest.importorskip("chirp")

from chirp import App, AppConfig
from chirp.ext.chirp_ui import use_chirp_ui


def _minimal_chirpui_app(
    *,
    template_dir: Path,
    extra_templates: dict[str, str] | None = None,
) -> App:
    for name, source in (extra_templates or {}).items():
        (template_dir / name).write_text(source, encoding="utf-8")

    app = App(AppConfig(template_dir=str(template_dir), skip_contract_checks=True))
    use_chirp_ui(app)

    @app.route("/")
    async def home(request):
        from chirp.templating.returns import Template

        return Template("home.html")

    return app


@pytest.mark.contract
def test_app_check_reports_design_system_and_passes() -> None:
    """Positive proof: use_chirp_ui wires checks that report INFO and exit 0."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "home.html").write_text("<h1>Home</h1>", encoding="utf-8")
        app = _minimal_chirpui_app(template_dir=root)

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            app.check()

        output = buf.getvalue()
        assert "design system" in output.lower()
        assert "chirp-ui" in output.lower()
        assert "all clear" in output.lower()


@pytest.mark.contract
def test_app_check_errors_on_bad_chirpui_import() -> None:
    """Negative proof: typo'd {% from "chirpui/..." %} surfaces ERROR (#390)."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        app = _minimal_chirpui_app(
            template_dir=root,
            extra_templates={
                "home.html": (
                    "{% from \"chirpui/cardd.html\" import card %}\n{{ card(title='Oops') }}"
                ),
            },
        )

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), pytest.raises(SystemExit) as exc:
            app.check()

        assert exc.value.code == 1
        output = buf.getvalue().lower()
        assert "error" in output
        assert "chirpui/cardd.html" in output or "cardd" in output
