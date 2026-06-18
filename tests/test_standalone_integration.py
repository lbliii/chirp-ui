"""CI smoke test for the no-Chirp standalone path (#285).

Proves the framework-agnostic integration seams stay green:

- ``get_loader()`` + ``register_filters()`` render chirp-ui macros
- ``static_path()`` serves ``chirpui.css``
- A minimal WSGI app boots and returns a page with an interactive component
- ``check_alpine_runtime()`` passes when the Alpine bootstrap is wired
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from http.client import HTTPConnection
from threading import Thread
from wsgiref.simple_server import WSGIServer, make_server

import pytest
from kida import ChoiceLoader, Environment
from kida.template import Markup

from chirp_ui import get_loader, register_filters, static_path
from chirp_ui.alpine import check_alpine_runtime

_ALPINE_VERSION = "3.15.8"
_CDN = "https://cdn.jsdelivr.net/npm"

# Same inline bootstrap Chirp injects (src/chirp/server/alpine.py).
_SAFE_DATA_SHIM = """
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


class _KidaFilterApp:
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


def make_standalone_env() -> Environment:
    """Bare kida environment with chirp-ui loader and filters — no Chirp."""
    env = Environment(
        loader=ChoiceLoader([get_loader()]),
        autoescape=True,
    )
    register_filters(_KidaFilterApp(env))
    env.globals["csrf_field"] = lambda: Markup(
        '<input type="hidden" name="_csrf_token" value="smoke-test">'
    )
    return env


def render_standalone_demo_page(*, static_prefix: str = "/static") -> str:
    """Full HTML document with CSS, Alpine bootstrap, and theme_toggle."""
    env = make_standalone_env()
    body = env.from_string(
        '{% from "chirpui/theme_toggle.html" import theme_toggle %}'
        "{% from 'chirpui/card.html' import card %}"
        "{% call card(title='Standalone smoke') %}"
        "<p>chirp-ui without Chirp.</p>"
        "{{ theme_toggle() }}"
        "{% endcall %}"
    ).render()
    alpine_core = f"{_CDN}/alpinejs@{_ALPINE_VERSION}/dist/cdn.min.js"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>chirp-ui standalone smoke</title>
  <link rel="stylesheet" href="{static_prefix}/chirpui.css">
  <link rel="stylesheet" href="{static_prefix}/chirpui-transitions.css">
  <script src="{static_prefix}/chirpui.js"></script>
</head>
<body>
  {body}
  <script>{_SAFE_DATA_SHIM}</script>
  <script src="{static_prefix}/chirpui-alpine.js"></script>
  <script defer src="{alpine_core}"></script>
</body>
</html>"""


def _standalone_wsgi_app(environ, start_response):
    path = environ.get("PATH_INFO", "/") or "/"
    method = environ.get("REQUEST_METHOD", "GET").upper()
    root = static_path()

    if method != "GET":
        start_response("405 Method Not Allowed", [("Content-Type", "text/plain")])
        return [b"Method Not Allowed"]

    if path == "/":
        html = render_standalone_demo_page()
        body = html.encode("utf-8")
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [body]

    if path.startswith("/static/"):
        rel = path.removeprefix("/static/").lstrip("/")
        if ".." in rel.split("/"):
            start_response("403 Forbidden", [("Content-Type", "text/plain")])
            return [b"Forbidden"]
        target = (root / rel).resolve()
        if not str(target).startswith(str(root.resolve())):
            start_response("403 Forbidden", [("Content-Type", "text/plain")])
            return [b"Forbidden"]
        if not target.is_file():
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Not Found"]
        if target.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif target.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"
        else:
            content_type = "application/octet-stream"
        data = target.read_bytes()
        start_response("200 OK", [("Content-Type", content_type)])
        return [data]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not Found"]


@pytest.fixture(scope="module")
def standalone_server_url() -> Iterator[str]:
    """Boot a threaded WSGI server for the no-Chirp smoke app."""
    server: WSGIServer = make_server("127.0.0.1", 0, _standalone_wsgi_app)
    host, port = server.server_address
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def _get(url: str, path: str) -> tuple[int, dict[str, str], bytes]:
    conn = HTTPConnection(url.replace("http://", ""))
    conn.request("GET", path)
    response = conn.getresponse()
    headers = {k.lower(): v for k, v in response.getheaders()}
    body = response.read()
    conn.close()
    return response.status, headers, body


class TestStandaloneCoreContracts:
    def test_static_path_serves_chirpui_css(self) -> None:
        css = static_path() / "chirpui.css"
        assert css.is_file()
        assert b"--chirpui-" in css.read_bytes()

    def test_get_loader_resolves_macros(self) -> None:
        env = make_standalone_env()
        html = env.from_string(
            '{% from "chirpui/badge.html" import badge %}{{ badge("ok", variant="success") }}'
        ).render()
        assert "chirpui-badge" in html
        assert "ok" in html

    def test_register_filters_wires_bem_and_field_errors(self) -> None:
        env = make_standalone_env()
        assert "bem" in env.filters
        assert "field_errors" in env.filters
        assert "build_hx_attrs" in env.globals

    def test_render_includes_interactive_factory(self) -> None:
        html = render_standalone_demo_page()
        assert 'x-data="chirpuiThemeToggle()"' in html
        assert check_alpine_runtime(html).ok is True


class TestStandaloneWsgiSmoke:
    def test_home_renders_interactive_page(self, standalone_server_url: str) -> None:
        status, _, body = _get(standalone_server_url, "/")
        assert status == 200
        html = body.decode("utf-8")
        assert "chirpui-card" in html
        assert 'x-data="chirpuiThemeToggle()"' in html
        assert check_alpine_runtime(html).ok is True

    def test_static_css_is_served(self, standalone_server_url: str) -> None:
        status, headers, body = _get(standalone_server_url, "/static/chirpui.css")
        assert status == 200
        assert "text/css" in headers.get("content-type", "")
        assert b"--chirpui-" in body

    def test_static_alpine_js_is_served(self, standalone_server_url: str) -> None:
        status, _, body = _get(standalone_server_url, "/static/chirpui-alpine.js")
        assert status == 200
        assert b"chirpuiThemeToggle" in body or b"register(" in body

    def test_alpine_cdn_url_uses_browser_build(self) -> None:
        html = render_standalone_demo_page()
        assert re.search(r"alpinejs@3\.\d+\.\d+/dist/cdn\.min\.js", html)

    def test_static_path_traversal_blocked(self, standalone_server_url: str) -> None:
        status, _, _ = _get(standalone_server_url, "/static/../py.typed")
        assert status in {403, 404}
