#!/bin/bash

uv run ruff check airtrafficsim tests
uv run ruff format --check airtrafficsim tests
uv run mypy airtrafficsim tests