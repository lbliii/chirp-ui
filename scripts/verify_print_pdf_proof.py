#!/usr/bin/env python3
"""Verify Bengal print PDFs semantically and through Poppler rasterization."""

from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_TEXT = (
    "LEGACY_PYTHON_SENTINEL",
    "LEGACY_TEMPLATE_SENTINEL",
    "DISCLOSURE_SENTINEL",
    "LONG_CALLOUT_SENTINEL",
    "LONG_CODE_START_SENTINEL",
    "LONG_CODE_END_SENTINEL",
    "TABLE_ROW_01",
    "TABLE_ROW_30",
    "FIGURE_SENTINEL",
    "https://example.com/reference?mode=full",
    "https://docs.example.com/print-contract/",
)
REQUIRED_STRUCTURE = ("H1", "H2", "Link", "Table", "TR", "TH", "TD", "Figure")


def run(*args: str) -> str:
    process = subprocess.run(args, check=True, capture_output=True, text=True)
    if process.stderr.strip():
        msg = f"{args[0]} emitted warnings:\n{process.stderr.strip()}"
        raise RuntimeError(msg)
    return process.stdout


def ppm_tokens(payload: bytes, count: int) -> tuple[list[bytes], int]:
    tokens: list[bytes] = []
    index = 0
    while len(tokens) < count:
        while index < len(payload) and payload[index] in b" \t\r\n":
            index += 1
        if payload[index : index + 1] == b"#":
            index = payload.index(b"\n", index) + 1
            continue
        end = index
        while end < len(payload) and payload[end] not in b" \t\r\n":
            end += 1
        tokens.append(payload[index:end])
        index = end
    while index < len(payload) and payload[index] in b" \t\r\n":
        index += 1
    return tokens, index


def inspect_ppm(path: Path, *, grayscale: bool) -> dict[str, float | int]:
    payload = path.read_bytes()
    tokens, offset = ppm_tokens(payload, 4)
    if tokens[0] != b"P6" or tokens[3] != b"255":
        raise RuntimeError(f"unsupported PPM header in {path}")
    width, height = int(tokens[1]), int(tokens[2])
    pixels = payload[offset:]
    expected = width * height * 3
    if len(pixels) != expected:
        raise RuntimeError(f"truncated raster {path}: {len(pixels)} != {expected}")

    stride = max(1, (width * height) // 150_000)
    dark = 0
    sampled = 0
    max_channel_delta = 0
    for pixel in range(0, width * height, stride):
        index = pixel * 3
        red, green, blue = pixels[index : index + 3]
        sampled += 1
        if min(red, green, blue) < 245:
            dark += 1
        max_channel_delta = max(
            max_channel_delta,
            abs(red - green),
            abs(green - blue),
            abs(red - blue),
        )

    dark_ratio = dark / sampled
    if dark_ratio < 0.001:
        raise RuntimeError(f"apparently blank raster page {path}: {dark_ratio:.5f}")
    if grayscale and max_channel_delta > 3:
        raise RuntimeError(f"grayscale raster contains channel delta {max_channel_delta} in {path}")

    corners = ((2, 2), (width - 3, 2), (2, height - 3), (width - 3, height - 3))
    for x, y in corners:
        index = (y * width + x) * 3
        if min(pixels[index : index + 3]) < 245:
            raise RuntimeError(f"non-paper corner pixel at {(x, y)} in {path}")

    return {
        "width": width,
        "height": height,
        "dark_ratio": round(dark_ratio, 5),
        "max_channel_delta": max_channel_delta,
    }


def verify_pdf(pdf: Path, raster_dir: Path, *, grayscale: bool) -> dict[str, object]:
    info = run("pdfinfo", str(pdf))
    if "Tagged:          yes" not in info:
        raise RuntimeError(f"{pdf.name} is not tagged")
    pages_line = next(line for line in info.splitlines() if line.startswith("Pages:"))
    pages = int(pages_line.split(":", 1)[1])
    if pages < 4:
        raise RuntimeError(f"{pdf.name} has implausibly few pages: {pages}")

    structure = run("pdfinfo", "-struct-text", str(pdf))
    missing_structure = [role for role in REQUIRED_STRUCTURE if role not in structure]
    if missing_structure:
        raise RuntimeError(f"{pdf.name} missing structure roles: {missing_structure}")

    text = run("pdftotext", "-layout", str(pdf), "-")
    missing_text = [sentinel for sentinel in REQUIRED_TEXT if sentinel not in text]
    if missing_text:
        raise RuntimeError(f"{pdf.name} missing printable content: {missing_text}")
    if "utm_source" in text:
        raise RuntimeError(f"{pdf.name} leaked a tracking parameter into printed text")

    scenario_dir = raster_dir / pdf.stem
    scenario_dir.mkdir(parents=True, exist_ok=True)
    prefix = scenario_dir / "page"
    run("pdftoppm", "-r", "96", "-png", str(pdf), str(prefix))
    run("pdftoppm", "-r", "96", str(pdf), str(prefix))

    rasters: list[dict[str, object]] = []
    ppm_paths = sorted(scenario_dir.glob("page-*.ppm"))
    png_paths = sorted(scenario_dir.glob("page-*.png"))
    if len(ppm_paths) != pages or len(png_paths) != pages:
        raise RuntimeError(f"{pdf.name} raster page count did not match PDF metadata")
    for ppm, png in zip(ppm_paths, png_paths, strict=True):
        raster = inspect_ppm(ppm, grayscale=grayscale)
        raster["png"] = png.relative_to(pdf.parent).as_posix()
        rasters.append(raster)
        ppm.unlink()

    return {"file": pdf.name, "pages": pages, "rasters": rasters}


def write_report(output_dir: Path, results: list[dict[str, object]]) -> None:
    cards: list[str] = []
    for result in results:
        figures = "".join(
            (
                "<figure>"
                f'<img loading="lazy" src="{html.escape(str(raster["png"]))}" '
                f'alt="Rendered page from {html.escape(str(result["file"]))}">'
                f"<figcaption>{raster['width']}x{raster['height']} · "
                f"dark ratio {raster['dark_ratio']}</figcaption>"
                "</figure>"
            )
            for raster in result["rasters"]
        )
        cards.append(
            f"<section><h2>{html.escape(str(result['file']))}</h2>"
            f"<p>{result['pages']} pages · tagged · outlined · semantic text verified</p>"
            f'<div class="pages">{figures}</div></section>'
        )
    report = f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><title>Bengal print PDF proof</title>
<style>
body {{ font: 16px/1.5 system-ui; margin: 2rem; color: #111; background: #eee; }}
section {{ background: white; padding: 1rem; margin-block: 1rem; border: 1px solid #aaa; }}
.pages {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
figure {{ margin: 0; }} img {{ display: block; width: 100%; border: 1px solid #777; }}
figcaption {{ font-size: .85rem; margin-block-start: .25rem; }}
</style>
<body><h1>Bengal print PDF proof</h1>
<p>All documents passed tagged-PDF, outline, structure, text-completeness, raster, and paper-edge checks.</p>
{"".join(cards)}
</body></html>
"""
    (output_dir / "index.html").write_text(report, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "output" / "pdf",
        help="Directory produced by build_print_pdf_proof.py",
    )
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    for executable in ("pdfinfo", "pdftotext", "pdftoppm"):
        if shutil.which(executable) is None:
            raise RuntimeError(f"missing required Poppler executable: {executable}")

    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    raster_dir = output_dir / "raster"
    results = [
        verify_pdf(
            output_dir / scenario["file"],
            raster_dir,
            grayscale=bool(scenario["grayscale"]),
        )
        for scenario in manifest["scenarios"]
    ]
    write_report(output_dir, results)
    for result in results:
        print(f"verified {result['file']} ({result['pages']} pages)")


if __name__ == "__main__":
    main()
