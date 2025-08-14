import asyncio
import os
from typing import Any, Dict

from mcp_llm_courts.llm_client import nl_to_filters_via_ollama
from mcp_llm_courts.server import api_search, Settings, SearchRequest, SearchFilters
from mcp_llm_courts.nl_converter import convert_nl_to_filters


async def run_case(label: str, parsed: Dict[str, Any]) -> None:
    settings = Settings()
    # Всегда включаем документы для длинного ответа
    parsed.setdefault("filters", {})
    parsed["filters"]["need_document"] = True
    # Пейджинг
    page = int(parsed.get("page", 1))
    page_size = int(parsed.get("page_size", settings.default_page_size))
    page_size = min(page_size, settings.max_page_size)

    req = SearchRequest(
        filters=SearchFilters(**parsed["filters"]),
        page=page,
        page_size=page_size,
    )
    res = await api_search(settings, req)
    items = res.items

    print(f"\n[{label}] parsed=", parsed)
    print(f"[{label}] total={res.total}, page={res.page}, page_size={res.page_size}, items={len(items)}")
    for i, it in enumerate(items[:min(5, len(items))], 1):
        print(f"  {i}. {it.title} | {it.date} | sum={it.sum} {it.currency} | status={it.status}")


async def main() -> None:
    queries = [
        "покажи три дела",
        "покажи 5 дел по цене иска",
        "покажи цены иска пяти дел от 20 марта 2024 года зарегистрированных в Арбитражном суде Челябинской области",
    ]

    for q in queries:
        # Rule-based
        rb = convert_nl_to_filters(q)
        rb.setdefault("page_size", 3)
        await run_case(f"rule-based: {q}", rb)

        # LLM (если настроена)
        if os.getenv("OLLAMA_BASE_URL"):
            try:
                llm = nl_to_filters_via_ollama(q)
                await run_case(f"llm: {q}", llm)
            except Exception as e:
                print(f"[llm: {q}] ERROR: {e}")


if __name__ == "__main__":
    asyncio.run(main())
