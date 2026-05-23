import json
import re

from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
COMPONENT_OPTIONS = ROOT / "docs" / "COMPONENT-OPTIONS.md"
MANIFEST = ROOT / "src" / "chirp_ui" / "manifest.json"


def _component_sections() -> dict[str, str]:
    text = COMPONENT_OPTIONS.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^### `?([^`\n]+)`?\n", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1).strip()] = text[start:end]
    return sections


def test_public_templated_components_document_maturity_and_authoring() -> None:
    sections = _component_sections()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["components"]

    for name, component in manifest.items():
        if not component.get("template") or component.get("maturity") == "internal":
            continue

        section = sections[name]
        assert f"- **Maturity:** `{component['maturity']}`" in section
        assert f"- **Authoring:** `{component['authoring']}`" in section
