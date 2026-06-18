"""Team roster table fixture data and filtering."""

from __future__ import annotations

TABLE_DATA: list[tuple[str, str, str, str, str, str]] = [
    ("Alice", "alice@example.com", "Admin", "success", "2h ago", "◇"),
    ("Bob", "bob@example.com", "User", "warning", "1d ago", "◆"),
    ("Carol", "carol@example.com", "User", "success", "5m ago", "○"),
    ("Dave", "dave@example.com", "Admin", "default", "3d ago", "△"),
    ("Eve", "eve@example.com", "User", "success", "1h ago", "□"),
    ("Frank", "frank@example.com", "Guest", "default", "1w ago", "▷"),
    ("Grace", "grace@example.com", "Admin", "success", "30m ago", "◇"),
    ("Henry", "henry@example.com", "User", "warning", "2d ago", "◆"),
    ("Ivy", "ivy@example.com", "User", "success", "4h ago", "○"),
    ("Jack", "jack@example.com", "Guest", "default", "5d ago", "△"),
    ("Kate", "kate@example.com", "Admin", "success", "15m ago", "□"),
    ("Leo", "leo@example.com", "User", "success", "1h ago", "▷"),
    ("Mia", "mia@example.com", "User", "warning", "6h ago", "◇"),
    ("Noah", "noah@example.com", "Guest", "default", "2w ago", "◆"),
    ("Oscar", "oscar@example.com", "Admin", "success", "45m ago", "○"),
]
PAGE_SIZE = 5


def filter_table_data(
    q: str,
    role: str,
    sort_col: str,
    sort_dir: str,
) -> list[tuple[str, str, str, str, str, str]]:
    """Filter and sort TABLE_DATA by query, role, and sort params."""
    col_map = {"name": 0, "email": 1, "role": 2, "status": 3, "last_active": 4}
    sort_idx = col_map.get(sort_col, 0)
    filtered = [
        r
        for r in TABLE_DATA
        if (not q or q in r[0].lower() or q in r[1].lower() or q in r[2].lower())
        and (not role or r[2] == role)
    ]
    return sorted(filtered, key=lambda r: str(r[sort_idx]).lower(), reverse=(sort_dir == "desc"))
