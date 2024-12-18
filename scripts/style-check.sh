#!/bin/bash

uv run ruff check airtrafficsim
uv run ruff format --check airtrafficsim
uv run mypy airtrafficsim tests