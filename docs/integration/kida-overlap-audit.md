# Kida 0.11 vs chirp-ui integration guide overlap

Audit of Kida 0.11 framework tutorials against chirp-ui's standalone adoption
guides. Part of [#377](https://github.com/lbliii/chirp-ui/issues/377) /
[#393](https://github.com/lbliii/chirp-ui/issues/393).

**Scope split:** Kida documents how to run **Kida as the template engine** in
Flask, Django, and Starlette/FastAPI. chirp-ui documents how to render **chirp-ui
macros** (design system, Alpine, static assets) on top of kida — with or without
Chirp. The two doc sets are complementary, not competing.

| Doc set | Audience | Owns |
|---|---|---|
| [Kida framework tutorials](https://lbliii.github.io/kida/docs/tutorials/flask-integration/) | Any Kida user | `init_kida`, `KidaTemplates`, `KidaStarlette`, `render_block`, typed `{% def %}`, `kida check` |
| [chirp-ui integration guides](standalone-core.md) | chirp-ui adopters without Chirp | `get_loader()`, `register_filters()`, Alpine shim, static mount, CSRF bridge, capability matrix |

---

## Overlap matrix

Legend: **Shared** = same concept, both docs mention it · **Kida-only** ·
**chirp-ui-only** · **Tension** = different recommended wiring, both valid

### Flask

| Topic | Kida 0.11 | chirp-ui | Verdict |
|---|---|---|---|
| Python 3.14+ requirement | Yes | Yes (via `pyproject.toml`) | **Shared** |
| Template engine choice | `init_kida()` → `app.extensions["kida"]` | Bare `Environment` + `ChoiceLoader` + `get_loader()` | **Tension** — see resolution below |
| View render path | `kida.contrib.flask.render_template()` | `render_template(env, …)` → `Response(page_shell(...))` | **Shared** goal, different helper |
| HTMX / fragment routes | `template.render_block("preview", …)` | Same API in reference app (`POST /htmx/greet`) | **Shared** |
| Filters / globals | `kida_env.add_global`, `@kida_env.filter()` | `register_filters()` via kida adapter | **Shared** goal; chirp-ui ships the filter set |
| Static assets | Not covered | Mount `static_path()` | **chirp-ui-only** |
| Alpine + safeData shim | Not covered | [standalone-core.md](standalone-core.md) | **chirp-ui-only** |
| CSRF bridge | Not covered | Flask-WTF → `csrf_field` global | **chirp-ui-only** |
| Upgrade pitch (Chirp) | Not covered | [capability-matrix.md](capability-matrix.md) | **chirp-ui-only** |

**Tension resolution:** chirp-ui's reference apps use a standalone `make_env()` so
copy-paste works without monkey-patching Flask. Production apps may prefer
`init_kida()` and register chirp-ui on the returned environment — both paths
render the same kida templates.

### Django

| Topic | Kida 0.11 | chirp-ui | Verdict |
|---|---|---|---|
| Backend wiring | `KidaTemplates` in `TEMPLATES` + `using="kida"` | Render kida in view; thin Django shell template | **Tension** — see resolution below |
| Fragment views | `engines["kida"].env.get_template(…).render_block()` | Same pattern in reference app | **Shared** |
| CSRF | `get_token(request)` in context | Bridge to `csrf_field` global (`csrfmiddlewaretoken`) | **Shared** token; chirp-ui adds macro global |
| Static files | Not covered | `STATICFILES_DIRS` + `collectstatic` | **chirp-ui-only** |
| Form errors → macros | Not covered | `django_errors(form)` adapter | **chirp-ui-only** |
| Alpine / assets | Not covered | [standalone-core.md](standalone-core.md) | **chirp-ui-only** |

**Tension resolution:** Kida's backend path is the native Django integration.
chirp-ui recommends **render-in-view (option b)** because mixed Django-template +
kida files are the highest-friction seam — a thin `{{ content|safe }}` wrapper
avoids two engines in one file. Teams that fully commit to Kida as their only
template backend can follow Kida's tutorial and add chirp-ui loader/filters to
that environment.

### FastAPI / Starlette

| Topic | Kida 0.11 | chirp-ui | Verdict |
|---|---|---|---|
| Adapter | `KidaTemplates(directory=…)` + `TemplateResponse` | `make_env()` + `Depends()` renderer | **Tension** — see resolution below |
| Async routes | Native async handlers | Sync kida render inside async route | **Shared** (both fine for typical pages) |
| Fragment endpoints | `render_block` on POST | Reference `POST /htmx/greet` | **Shared** |
| CSRF | Not covered | Session token / `starlette-csrf` bridge | **chirp-ui-only** |
| htmx script | Not covered | `page_shell(..., include_htmx=True)` | **chirp-ui-only** |
| Alpine / assets | Not covered | [standalone-core.md](standalone-core.md) | **chirp-ui-only** |

**Tension resolution:** Same as Flask — use `KidaStarlette` and layer chirp-ui
registration on its environment, or copy the reference app's explicit renderer.

### Cross-cutting (all frameworks)

| Topic | Kida 0.11 | chirp-ui | Verdict |
|---|---|---|---|
| `render_block` / HTMX partials | [Framework Integration API](https://lbliii.github.io/kida/docs/usage/framework-integration/) | Mentioned in per-framework guides | **Shared** — Kida owns API depth |
| Typed `{% def %}` / `{% template %}` | Tutorials + `kida check --typed` | Component macros (future `--typed` gate #367) | **Shared** engine feature |
| Template verification | `kida check` CLI | `uv run poe template-check` (stubbed env) | **Shared** — chirp-ui wraps Kida for filter globals |
| Jinja migration notes | Kida tutorials link to coming-from-jinja2 | "Do not mix engines" in each guide | **Shared** — no contradiction |
| Chirp / `use_chirp_ui` | Not covered (Chirp skill exists separately) | [capability-matrix.md](capability-matrix.md) upgrade pitch | **chirp-ui-only** |

---

## Contradictions

**None found.** The apparent "tensions" above are intentional scope choices:

- Kida tutorials minimize framework-specific glue to teach Kida APIs.
- chirp-ui guides minimize framework magic to teach chirp-ui wiring and funnel
  heavy glue toward Chirp.

Bootstrap instructions (Environment creation, `render_block`, CSRF token source)
are compatible when chirp-ui registration is added to a Kida-initiated environment.

---

## Cross-link recommendations

Implemented in [#394](https://github.com/lbliii/chirp-ui/issues/394):

| chirp-ui guide | Link to Kida |
|---|---|
| [flask.md](flask.md) | [Flask Integration tutorial](https://lbliii.github.io/kida/docs/tutorials/flask-integration/) |
| [django.md](django.md) | [Django Integration tutorial](https://lbliii.github.io/kida/docs/tutorials/django-integration/) |
| [fastapi.md](fastapi.md) | [Starlette & FastAPI Integration tutorial](https://lbliii.github.io/kida/docs/tutorials/starlette-integration/) |
| [standalone-core.md](standalone-core.md) | [Framework Integration API](https://lbliii.github.io/kida/docs/usage/framework-integration/) |

Kida-side follow-up (outside this repo): add a "Using chirp-ui macros" note to
each framework tutorial pointing at [standalone-core.md](standalone-core.md) and
the [capability matrix upgrade pitch](capability-matrix.md#upgrade-pitch-why-chirp).

---

## Related

- Epic [#377](https://github.com/lbliii/chirp-ui/issues/377) — Adoption guide dedupe
- Saga [#284](https://github.com/lbliii/chirp-ui/issues/284) — Framework-Agnostic Adoption On-Ramp
