fmt:
    uv run ruff check src scripts --fix-only
    uv run ruff format src scripts
    uv run mypy src tests

check:
    uv run ruff check src tests
    uv run ruff format --check src tests
    uv run mypy src tests