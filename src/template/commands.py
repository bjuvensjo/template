from pathlib import Path

import click
from rich import print

from template.python_project import template as tpp


@click.command()
@click.option(
    "-o",
    "--output_dir",
    default=".",
    help="The directory in which to create the python project. Default '.'",
)
@click.argument("name")
def python_project(output_dir: str, name: str) -> None:
    tpp.create(output_dir=Path(output_dir), name=name)
    print(f"Created {name} in {output_dir}")
