import asyncio
from typing import Any, Dict

from mcp_llm_courts.server import search_cases


async def main() -> None:
    payload: Dict[str, Any] = {
        "filters": {
            "need_document": True,
            "participant": "1027739020760",
            "start_date_from": "2024-12-01",
            "start_date_to": "2025-01-31",
            "updated_at_from": "2024-12-01",
            "updated_at_to": "2025-12-31",
        },
        "page": 1,
        "page_size": 3,
    }
    res = await search_cases(payload)
    items = res.get("items", [])
    preview = [{"id": it.get("id"), "title": it.get("title"), "date": it.get("date")} for it in items]
    print({
        "total": res.get("total"),
        "count": len(items),
        "preview": preview,
    })


if __name__ == "__main__":
    asyncio.run(main())
