"""``python -m chirp_ui`` dispatch — subcommand front door.

Currently a single subcommand (``find``) plus a pointer to the existing
``python -m chirp_ui.manifest`` entry point. New subcommands go here.

See ``docs/plans/PLAN-agent-grounding-depth.md § Sprint 6``.
"""

from __future__ import annotations

import sys


def _usage() -> str:
    return (
        "Usage: python -m chirp_ui <command> [args...]\n"
        "\n"
        "Commands:\n"
        "  find       Search components by name, category, or description\n"
        "  manifest   (alias) python -m chirp_ui.manifest — emit the full manifest as JSON\n"
    )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help"}:
        sys.stdout.write(_usage())
        return 0

    command, rest = args[0], args[1:]
    if command == "find":
        from chirp_ui.find import main as find_main

        return find_main(rest)
    if command == "manifest":
        from chirp_ui.manifest import main as manifest_main

        return manifest_main(rest)

    sys.stderr.write(f"unknown command: {command!r}\n\n{_usage()}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
