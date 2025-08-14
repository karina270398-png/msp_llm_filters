mcp-llm-courts (local MVP)

Кратко: локальный MCP-сервер, который будет вызывать ваше публичное API арбитражных дел через адаптер. Сейчас содержит заглушки инструментов и базовую конфигурацию.

Структура
- src/mcp_llm_courts/server.py — MCP-сервер (STDIO), инструменты: ping, search_cases (заглушка), get_case_by_id (заглушка)
- pyproject.toml — зависимости и точка входа
- .env.example — переменные окружения

Быстрый старт
1) Python 3.10+
2) Установите зависимости:
   pip install -e .[dev]
3) Скопируйте .env.example в .env и отредактируйте при необходимости
4) Запуск как процесс MCP (STDIO):
   python -m mcp_llm_courts.server
   или скриптом:
   mcp-llm-courts

Инструменты (MVP)
- ping() → проверка доступности
- search_cases(filters: object, page: int=1, page_size: int=20) → пока возвращает мок
- get_case_by_id(case_id: string) → пока возвращает мок

Дальше
- Подключить ваше реальное API в adapter внутри server.py
- Добавить валидацию схем фильтров (Pydantic/JSON Schema)
- Логи/метрики, обработку ошибок, кэш

Инструкции для LLM
- prompts/system_instructions.md — правила маппинга естественных запросов в filters/page_size/sort.
- MCP-сервер — это «инструмент»; саму LLM подключает ваш клиент (IDE/чат/бэкенд), используя эти инструкции.

Тесты
- pytest: тестируем нормализацию дат и базовую пост-обработку без реальных внешних вызовов.
  Запуск: pytest -q

Локальный веб-UI
- Запуск: uvicorn mcp_llm_courts.webapp:app --reload --port 8000
- Откройте http://127.0.0.1:8000, введите запрос на русском, получите подробные результаты.
