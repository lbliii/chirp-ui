"""Template filters required by chirp-ui components.

These match Chirp's filter API so chirp-ui works with any Chirp version.
Register via :func:`register_filters` when using Chirp.
"""


def bem(block: str, variant: str = "", modifier: str = "", cls: str = "") -> str:
    """Build chirpui BEM class string: chirpui-{block} chirpui-{block}--{variant} etc.

    Example:
        class="{{ "alert" | bem(variant=variant, cls=cls) }}"
        → "chirpui-alert chirpui-alert--success my-class"
    """
    parts = [f"chirpui-{block}"]
    if variant:
        parts.append(f"chirpui-{block}--{variant}")
    if modifier:
        parts.append(f"chirpui-{block}--{modifier}")
    if cls:
        parts.append(cls)
    return " ".join(parts)


def field_errors(errors: object, field_name: str) -> list[str]:
    """Extract error messages for a field from a ValidationError-style dict.

    Returns empty list if errors is None or field has no errors.
    """
    if errors is None:
        return []
    if not isinstance(errors, dict):
        return []
    return list(errors.get(field_name, []))


def register_filters(app: object) -> None:
    """Register chirp-ui filters (bem, field_errors) on a Chirp app.

    Call after App creation. Ensures chirp-ui components render correctly
    regardless of Chirp version::

        from chirp import App
        import chirp_ui
        app = App(...)
        chirp_ui.register_filters(app)
    """
    app.template_filter("bem")(bem)
    app.template_filter("field_errors")(field_errors)
