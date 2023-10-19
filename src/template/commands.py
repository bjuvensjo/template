from pathlib import Path

import click
from rich import print

from template.groovy_maven_project import template as gp
from template.python_poetry_project import template as pp


@click.command()
@click.option(
    "-o",
    "--output_dir",
    default=".",
    help="The directory in which to create the python project. Default '.'",
)
@click.option(
    "-g",
    "--group_id",
    default="mygroup",
    help="The Maven group id. Default 'mygroup'",
)
@click.option(
    "-v",
    "--version",
    default="1.0.0-SNAPSHOT",
    help="The Maven version. Default '1.0.0-SNAPSHOT'",
)
@click.option(
    "-p",
    "--packaging",
    default="jar",
    help="The Maven packaging. Default 'jar'",
)
@click.option(
    "-j",
    "--java-version",
    default="17",
    help="The Java version. Default '17'",
)
@click.argument("artifact_id")
def groovy_maven_project(
    output_dir: str,
    group_id: str,
    artifact_id: str,
    version: str,
    packaging: str,
    java_version: str,
) -> None:
    print(
        gp.create(
            output_dir=Path(output_dir),
            group_id=group_id,
            artifact_id=artifact_id,
            version=version,
            packaging=packaging,
            java_version=java_version,
        )
    )


@click.command()
@click.option(
    "-o",
    "--output_dir",
    default=".",
    help="The directory in which to create the python project. Default '.'",
)
@click.argument("name")
def python_poetry_project(output_dir: str, name: str) -> None:
    print(pp.create(output_dir=Path(output_dir), name=name))
