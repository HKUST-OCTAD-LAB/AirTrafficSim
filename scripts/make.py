#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "typer",
# ]
# ///

import os
from pathlib import Path
from typing import Iterable

import typer

PATH_ROOT = Path(__file__).parent.parent
app = typer.Typer(no_args_is_help=True)


@app.command()
def check() -> None:
    os.system("uv run ruff check src tests")
    os.system("uv run ruff format --check src tests")
    os.system("uv run mypy src tests")


@app.command()
def fix() -> None:
    os.system("uv run ruff check --fix src tests")
    os.system("uv run ruff format src tests")


#
# for vis
#


copy = typer.Typer(no_args_is_help=True)
app.add_typer(copy, name="copy")


def _g(files: Iterable[str]) -> str:
    return " ".join(f'-g "!{file}"' for file in files)


def xclip(cmd: Iterable[str]) -> str:
    return f"{cmd} | xclip -sel clipboard"


PATH_DUMP = PATH_ROOT / "scripts" / "dump.sh"
EXCLUDE = ["docs/assets", "src/airtrafficsim-client", "uv.lock", "mkdocs.yml"]


@copy.command()
def all(exclude: list[str] = EXCLUDE) -> None:
    g = _g(exclude)
    os.system(xclip(f"cd {PATH_ROOT} && bash {PATH_DUMP} {g}"))


if __name__ == "__main__":
    app()
