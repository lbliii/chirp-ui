"""Market trading-floor fixture data and context builder."""

from __future__ import annotations

from urllib.parse import urlencode

from chirp import Request

MARKET_SECTORS: tuple[dict[str, str], ...] = (
    {"id": "tech", "label": "Technology", "icon": "TC"},
    {"id": "energy", "label": "Energy", "icon": "EN"},
    {"id": "finance", "label": "Finance", "icon": "FN"},
    {"id": "consumer", "label": "Consumer", "icon": "CS"},
)

MARKET_SYMBOLS: tuple[dict[str, object], ...] = (
    {
        "symbol": "MEOW",
        "name": "Lucky Cat Holdings",
        "sector": "tech",
        "price": 142.38,
        "change": 4.82,
        "change_pct": 3.51,
        "volume": "18.2M",
        "status": "success",
        "summary": "Meme-adjacent consumer platform with strong retail flow.",
        "tags": ("momentum", "retail", "high-beta"),
    },
    {
        "symbol": "NVAQ",
        "name": "NovaQuant Systems",
        "sector": "tech",
        "price": 88.04,
        "change": -1.27,
        "change_pct": -1.42,
        "volume": "6.4M",
        "status": "warning",
        "summary": "Quant infra name with elevated latency on the options tape.",
        "tags": ("infra", "options", "watch"),
    },
    {
        "symbol": "BRNT",
        "name": "Blue Ridge Energy",
        "sector": "energy",
        "price": 61.17,
        "change": 2.11,
        "change_pct": 3.57,
        "volume": "9.8M",
        "status": "success",
        "summary": "Midstream and storage operator with clean spread capture.",
        "tags": ("energy", "yield", "midstream"),
    },
    {
        "symbol": "GLDR",
        "name": "Guilder Trust",
        "sector": "finance",
        "price": 54.92,
        "change": -0.64,
        "change_pct": -1.15,
        "volume": "3.1M",
        "status": "muted",
        "summary": "Regional bank trust with stable dividend profile.",
        "tags": ("finance", "dividend", "defensive"),
    },
    {
        "symbol": "SPRX",
        "name": "Sprout Retail",
        "sector": "consumer",
        "price": 27.66,
        "change": 0.93,
        "change_pct": 3.48,
        "volume": "12.7M",
        "status": "success",
        "summary": "Same-day commerce operator with improving gross margin.",
        "tags": ("consumer", "same-day", "margin"),
    },
    {
        "symbol": "ORBT",
        "name": "Orbit Labs",
        "sector": "tech",
        "price": 19.44,
        "change": -2.08,
        "change_pct": -9.67,
        "volume": "22.5M",
        "status": "error",
        "summary": "Satellite analytics startup with a guidance reset in pre-market.",
        "tags": ("space", "guidance", "volatile"),
    },
)

MARKET_ACTIVITY: tuple[dict[str, str], ...] = (
    {"time": "09:41:08", "symbol": "MEOW", "side": "buy", "size": "4,200", "price": "142.36"},
    {"time": "09:41:02", "symbol": "ORBT", "side": "sell", "size": "18,900", "price": "19.41"},
    {"time": "09:40:54", "symbol": "SPRX", "side": "buy", "size": "2,100", "price": "27.62"},
    {"time": "09:40:47", "symbol": "NVAQ", "side": "sell", "size": "900", "price": "88.02"},
    {"time": "09:40:39", "symbol": "BRNT", "side": "buy", "size": "6,400", "price": "61.14"},
)


def market_url(
    *,
    base_path: str = "/screen-lucky-cat-market",
    query: str = "",
    sector: str = "",
    status: str = "",
) -> str:
    params: dict[str, str] = {}
    if query:
        params["q"] = query
    if sector:
        params["sector"] = sector
    if status:
        params["status"] = status
    if not params:
        return base_path
    return f"{base_path}?{urlencode(params)}"


def _format_change(value: float) -> str:
    prefix = "+" if value >= 0 else ""
    return f"{prefix}{value:.2f}"


def _format_pct(value: float) -> str:
    prefix = "+" if value >= 0 else ""
    return f"{prefix}{value:.2f}%"


def market_context(
    request: Request, *, base_path: str = "/screen-lucky-cat-market"
) -> dict[str, object]:
    query = (request.query.get("q") or "").strip()
    sector = (request.query.get("sector") or "").strip()
    status = (request.query.get("status") or "").strip()

    symbols = list(MARKET_SYMBOLS)
    if query:
        needle = query.lower()
        symbols = [
            item
            for item in symbols
            if needle in str(item["symbol"]).lower()
            or needle in str(item["name"]).lower()
            or any(needle in tag.lower() for tag in item["tags"])
        ]
    if sector:
        symbols = [item for item in symbols if item["sector"] == sector]
    if status:
        symbols = [item for item in symbols if item["status"] == status]

    selected = symbols[0] if symbols else None
    movers_up = sorted(
        [item for item in MARKET_SYMBOLS if float(item["change_pct"]) > 0],
        key=lambda item: float(item["change_pct"]),
        reverse=True,
    )[:3]
    movers_down = sorted(
        [item for item in MARKET_SYMBOLS if float(item["change_pct"]) < 0],
        key=lambda item: float(item["change_pct"]),
    )[:3]

    sector_items = [
        {
            **area,
            "active": area["id"] == sector,
            "href": market_url(base_path=base_path, query=query, sector=area["id"], status=status),
        }
        for area in MARKET_SECTORS
    ]
    status_items = [
        {
            "id": "",
            "label": "All states",
            "active": not status,
            "href": market_url(base_path=base_path, query=query, sector=sector),
        },
        {
            "id": "success",
            "label": "Gainers",
            "active": status == "success",
            "href": market_url(base_path=base_path, query=query, sector=sector, status="success"),
        },
        {
            "id": "warning",
            "label": "Watch",
            "active": status == "warning",
            "href": market_url(base_path=base_path, query=query, sector=sector, status="warning"),
        },
        {
            "id": "error",
            "label": "Losers",
            "active": status == "error",
            "href": market_url(base_path=base_path, query=query, sector=sector, status="error"),
        },
    ]

    return {
        "market_route": base_path,
        "market_query": query,
        "market_sector": sector,
        "market_status": status,
        "market_sector_label": next(
            (item["label"] for item in MARKET_SECTORS if item["id"] == sector),
            "All sectors",
        ),
        "market_sectors": sector_items,
        "market_status_items": status_items,
        "market_symbols": [
            {
                **item,
                "change_label": _format_change(float(item["change"])),
                "change_pct_label": _format_pct(float(item["change_pct"])),
                "price_label": f"${float(item['price']):,.2f}",
                "selected": selected is not None and item["symbol"] == selected["symbol"],
            }
            for item in symbols
        ],
        "market_selected": (
            {
                **selected,
                "change_label": _format_change(float(selected["change"])),
                "change_pct_label": _format_pct(float(selected["change_pct"])),
                "price_label": f"${float(selected['price']):,.2f}",
            }
            if selected
            else None
        ),
        "market_movers_up": [
            {
                **item,
                "change_label": _format_change(float(item["change"])),
                "change_pct_label": _format_pct(float(item["change_pct"])),
                "price_label": f"${float(item['price']):,.2f}",
            }
            for item in movers_up
        ],
        "market_movers_down": [
            {
                **item,
                "change_label": _format_change(float(item["change"])),
                "change_pct_label": _format_pct(float(item["change_pct"])),
                "price_label": f"${float(item['price']):,.2f}",
            }
            for item in movers_down
        ],
        "market_activity": MARKET_ACTIVITY,
        "market_hints": [
            {"label": "MEOW", "href": market_url(base_path=base_path, query="MEOW")},
            {"label": "momentum", "href": market_url(base_path=base_path, query="momentum")},
            {"label": "energy", "href": market_url(base_path=base_path, sector="energy")},
        ],
        "market_portfolio_value": "$1,284,920.44",
        "market_day_pnl": "+$18,402.18",
        "market_day_pnl_pct": "+1.45%",
        "market_open_positions": "14",
        "market_watch_count": "28",
    }
