#!/bin/bash

uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy src tests