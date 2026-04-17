"""Tests for `chirp_ui.inspect.list_provides` and `list_consumes`.

Verifies the introspection API correctly walks the template tree, parses both
plain and compound annotations, and exposes a stable record shape that apps
can use to audit dead provides / orphaned consumes.

See ``.context/composite-contracts-plan.md`` § Sprint 2.
"""

from chirp_ui.inspect import (
    ConsumeRecord,
    ProvideRecord,
    _parse_consumes_annotation,
    _parse_provide_annotation,
    list_consumes,
    list_provides,
)


class TestListProvides:
    def test_returns_provide_records(self):
        records = list_provides()
        assert records, "expected at least one provide statement"
        assert all(isinstance(r, ProvideRecord) for r in records)

    def test_known_provider_present(self):
        records = list_provides()
        accordion = next(
            (r for r in records if r.template == "accordion.html" and r.key == "_accordion_name"),
            None,
        )
        assert accordion is not None
        assert accordion.consumed_by == ("accordion_item",)
        assert accordion.line > 0
        assert "@provides" in accordion.raw_annotation

    def test_provider_with_multiple_consumers(self):
        records = list_provides()
        card = next(
            (r for r in records if r.template == "card.html" and r.key == "_card_variant"),
            None,
        )
        assert card is not None
        assert card.consumed_by == ("alert", "badge", "divider", "settings_row")

    def test_provider_with_no_documented_consumers(self):
        records = list_provides()
        bar_surface = next(
            (r for r in records if r.template == "command_bar.html" and r.key == "_bar_surface"),
            None,
        )
        assert bar_surface is not None
        assert bar_surface.consumed_by == ()
        assert "no consumers yet" in bar_surface.raw_annotation

    def test_results_are_sorted(self):
        records = list_provides()
        keys = [(r.template, r.line) for r in records]
        assert keys == sorted(keys)


class TestListConsumes:
    def test_returns_consume_records(self):
        records = list_consumes()
        assert records, "expected at least one consume call"
        assert all(isinstance(r, ConsumeRecord) for r in records)

    def test_known_consumer_present(self):
        records = list_consumes()
        accordion_item = next(
            (r for r in records if r.template == "accordion.html" and r.key == "_accordion_name"),
            None,
        )
        assert accordion_item is not None
        assert accordion_item.providers == ("accordion",)
        assert "@consumes" in accordion_item.raw_annotation

    def test_compound_annotation_splits_correctly(self):
        """badge.html declares two consumes in one annotation: must yield two records."""
        records = list_consumes()
        badge = [r for r in records if r.template == "badge.html"]
        assert len(badge) == 2
        by_key = {r.key: r for r in badge}
        assert by_key["_card_variant"].providers == ("card",)
        assert by_key["_surface_variant"].providers == ("panel", "surface")
        # both records share the same source line + raw annotation
        assert by_key["_card_variant"].line == by_key["_surface_variant"].line
        assert by_key["_card_variant"].raw_annotation == by_key["_surface_variant"].raw_annotation

    def test_compound_annotation_in_divider(self):
        """divider.html has the same compound pattern as badge."""
        records = list_consumes()
        divider = [r for r in records if r.template == "divider.html"]
        assert len(divider) == 2
        assert {r.key for r in divider} == {"_card_variant", "_surface_variant"}

    def test_multiple_consumes_on_one_line(self):
        """divider.html has two consume() calls chained with `or` on one line."""
        records = list_consumes()
        divider = [r for r in records if r.template == "divider.html"]
        # both records have the same line number (chained on one set statement)
        assert divider[0].line == divider[1].line

    def test_results_are_sorted(self):
        records = list_consumes()
        keys = [(r.template, r.line) for r in records]
        assert keys == sorted(keys)


class TestParseProvideAnnotation:
    def test_consumed_by_list(self):
        assert _parse_provide_annotation("consumed by: btn, icon_btn") == ("btn", "icon_btn")

    def test_no_consumers_returns_empty(self):
        assert _parse_provide_annotation("no consumers yet (reserved for future use)") == ()

    def test_single_consumer(self):
        assert _parse_provide_annotation("consumed by: accordion_item") == ("accordion_item",)


class TestParseConsumesAnnotation:
    def test_simple_clause(self):
        result = _parse_consumes_annotation("_card_variant from: card")
        assert result == [("_card_variant", ("card",))]

    def test_multi_provider_clause(self):
        result = _parse_consumes_annotation("_surface_variant from: panel, surface")
        assert result == [("_surface_variant", ("panel", "surface"))]

    def test_compound_two_keys(self):
        """Two keys in one annotation, second with a multi-provider list."""
        result = _parse_consumes_annotation(
            "_card_variant from: card, _surface_variant from: panel, surface"
        )
        assert result == [
            ("_card_variant", ("card",)),
            ("_surface_variant", ("panel", "surface")),
        ]

    def test_external_provider(self):
        result = _parse_consumes_annotation("_sse_state from: (external provider)")
        assert result == [("_sse_state", ("(external provider)",))]


class TestRecordsAreImmutable:
    def test_provide_record_is_frozen(self):
        records = list_provides()
        import dataclasses

        with __import__("pytest").raises(dataclasses.FrozenInstanceError):
            records[0].key = "mutated"

    def test_consume_record_is_frozen(self):
        records = list_consumes()
        import dataclasses

        with __import__("pytest").raises(dataclasses.FrozenInstanceError):
            records[0].key = "mutated"
