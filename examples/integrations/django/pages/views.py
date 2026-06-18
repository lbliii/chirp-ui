"""Render kida in views; wrap with a thin Django shell template."""

from __future__ import annotations

import sys
from pathlib import Path

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from kida.template import Markup

from pages.forms import ContactForm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "_shared"))

from chirpui_bootstrap import make_env, page_shell, render_template  # noqa: E402

KIDA_TEMPLATES = Path(__file__).resolve().parent / "kida_templates"


def _django_errors(form: ContactForm) -> dict[str, list[str]]:
    """Map Django ValidationError lists to chirp-ui ``field_errors`` shape."""
    return {name: [str(error) for error in errors] for name, errors in form.errors.items()}


def _render_kida(request: HttpRequest, template: str, **context: object) -> str:
    token = get_token(request)

    def csrf_field() -> Markup:
        return Markup(
            f'<input type="hidden" name="csrfmiddlewaretoken" value="{token}">'
        )

    env = make_env(template_dir=KIDA_TEMPLATES, csrf_field=csrf_field)
    body = render_template(env, template, **context)
    return page_shell(title="Django + chirp-ui", body=body)


@require_http_methods(["GET", "POST"])
def index(request: HttpRequest) -> HttpResponse:
    form = ContactForm(request.POST or None)
    saved = False
    if request.method == "POST" and form.is_valid():
        messages.success(request, f"Saved {form.cleaned_data['name']}.")
        saved = True
        form = ContactForm()

    html = _render_kida(
        request,
        "index.html",
        errors=_django_errors(form),
        name_value=form["name"].value() or "",
        saved=saved,
    )
    return render(request, "pages/shell.html", {"content": html})
