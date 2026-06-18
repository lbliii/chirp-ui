"""Unit tests for chirp_ui.config_schema (AI chat saga, Phase 1).

No browser, no Chirp — the helper is stdlib + dataclasses only, mirroring
tests/test_grid_state.py. Locks the typed-projection contract config_form
renders from.
"""

from chirp_ui.config_schema import Field, ProjectedField, Widget, project_fields


def test_explicit_widget_wins() -> None:
    pf = project_fields([Field("bio", type="str", widget=Widget.TEXTAREA)])[0]
    assert pf.widget == "textarea"


def test_infers_toggle_for_bool() -> None:
    assert project_fields([Field("stream", type="bool", default=True)])[0].widget == "toggle"


def test_infers_select_when_choices_present() -> None:
    f = Field("model", choices=(("a", "A"), ("b", "B")))
    pf = project_fields([f])[0]
    assert pf.widget == "select"
    assert pf.choices == ({"value": "a", "label": "A"}, {"value": "b", "label": "B"})


def test_bounded_numeric_is_range_unbounded_is_number() -> None:
    bounded = project_fields([Field("temp", type="float", min=0, max=2, step=0.1)])[0]
    unbounded = project_fields([Field("max_tokens", type="int")])[0]
    assert bounded.widget == "range"
    assert unbounded.widget == "number"


def test_value_pulled_from_values_then_default() -> None:
    fields = [Field("model", default="gpt-4o")]
    assert project_fields(fields, {"model": "claude"})[0].value == "claude"
    assert project_fields(fields, {})[0].value == "gpt-4o"


def test_secret_is_masked_and_forces_password() -> None:
    pf = project_fields([Field("api_key", secret=True)], {"api_key": "sk-real"})[0]
    assert pf.widget == "password"
    assert pf.value == ""


def test_options_callable_overrides_static_choices() -> None:
    pf = project_fields([Field("model", options_callable=lambda: [("x", "X")])])[0]
    assert pf.choices == ({"value": "x", "label": "X"},)


def test_accepts_plain_dict_like_coerce_column() -> None:
    pf = project_fields([{"name": "n", "type": "bool", "default": False}])[0]
    assert isinstance(pf, ProjectedField)
    assert pf.widget == "toggle"


def test_required_when_no_default_and_not_secret() -> None:
    assert project_fields([Field("q")])[0].required is True
    assert project_fields([Field("q", default="")])[0].required is False
    assert project_fields([Field("k", secret=True)])[0].required is False
