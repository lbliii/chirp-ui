"""Shared kida + Alpine bootstrap for framework integration examples.

Not published on PyPI — copy into your app or import from this tree when
running the reference apps under ``examples/integrations/``.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from kida import ChoiceLoader, Environment, FileSystemLoader
from kida.template import Markup

from chirp_ui import get_loader, register_filters, static_path

ALPINE_VERSION = "3.15.8"
CDN = "https://cdn.jsdelivr.net/npm"

# Same inline bootstrap Chirp injects (src/chirp/server/alpine.py).
SAFE_DATA_SHIM = """
(function(){
  var q=[];
  window._chirpAlpineData=function(n,f){
    if(window.Alpine&&Alpine.version){Alpine.data(n,f);}else{q.push([n,f]);}
  };
  document.addEventListener("alpine:init",function(){
    Alpine.store("modals",{});
    Alpine.store("trays",{});
    Alpine.safeData=function(n,f){Alpine.data(n,f);};
    q.forEach(function(r){Alpine.data(r[0],r[1]);});q=[];
  });
})();
"""


class KidaFilterApp:
    """Adapter so ``register_filters()`` works on a kida ``Environment``."""

    def __init__(self, env: Environment) -> None:
        self._env = env

    def template_filter(self, name: str | None = None):
        def decorator(fn):
            self._env.filters[name] = fn
            return fn

        return decorator

    def template_global(self, name: str | None = None):
        def decorator(fn):
            self._env.globals[name] = fn
            return fn

        return decorator


def static_root() -> Path:
    return static_path()


def make_env(
    *,
    template_dir: Path | str,
    csrf_field: Callable[[], Markup | str],
) -> Environment:
    """Kida environment with chirp-ui loader, filters, and CSRF global."""
    env = Environment(
        loader=ChoiceLoader([
            FileSystemLoader(str(template_dir)),
            get_loader(),
        ]),
        autoescape=True,
    )
    register_filters(KidaFilterApp(env))
    env.globals["csrf_field"] = csrf_field
    return env


def render_template(env: Environment, name: str, **context: object) -> str:
    return env.get_template(name).render(**context)


def page_shell(
    *,
    title: str,
    body: str,
    static_prefix: str = "/static",
    include_htmx: bool = False,
) -> str:
    """Wrap rendered kida body in a full HTML document with assets + Alpine."""
    alpine_core = f"{CDN}/alpinejs@{ALPINE_VERSION}/dist/cdn.min.js"
    htmx_script = (
        f'<script src="{CDN}/htmx.org@2.0.4/dist/htmx.min.js"></script>\n'
        if include_htmx
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="{static_prefix}/chirpui.css">
  <link rel="stylesheet" href="{static_prefix}/chirpui-transitions.css">
  <script src="{static_prefix}/chirpui.js"></script>
  {htmx_script}
</head>
<body class="chirpui-body">
  <main class="chirpui-container" style="padding-block: var(--chirpui-spacing-lg);">
    {body}
  </main>
  <script>{SAFE_DATA_SHIM}</script>
  <script src="{static_prefix}/chirpui-alpine.js"></script>
  <script defer src="{alpine_core}"></script>
</body>
</html>"""
