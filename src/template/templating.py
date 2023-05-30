"""
A generic module for templating with Jinja 2, combined with static content.
"""
import logging
from pathlib import Path
from typing import Sequence

from jinja2 import Environment, FileSystemLoader, StrictUndefined


def get_templates(search_path: Path, variables: dict) -> Sequence[tuple[Path, str]]:
    env = Environment(
        loader=FileSystemLoader(search_path),
        undefined=StrictUndefined,
    )

    # templates
    templates = [
        (template, env.get_template(template)) for template in env.list_templates()
    ]

    # rendered templates
    rendered_templates = [
        (
            env.from_string(path).render(**variables),
            template.render(**variables),
        )
        for path, template in templates
    ]

    return rendered_templates


def get_static(search_path: Path) -> Sequence[tuple[Path, str]]:
    return [
        (f.relative_to(search_path), f.read_text())
        for f in search_path.glob("**/*")
        if f.is_file()
    ]


def get_content(
    static_search_path: Path,
    templates_search_path: Path,
    templates_variables: dict[str, str],
) -> Sequence[tuple[Path, str]]:
    return get_templates(templates_search_path, templates_variables) + get_static(
        static_search_path
    )


def write(
    content: Sequence[tuple[Path, str]], output_path: Path, exists_ok=False
) -> None:
    if not exists_ok:
        for rel_path, _ in content:
            path = output_path.joinpath(rel_path)
            if path.exists():
                msg = f"Output path exists: {path}"
                logging.error(msg)
                raise RuntimeError(msg)

    for rel_path, data in content:
        path = output_path.joinpath(rel_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data)
        logging.info("Wrote %s: %s", path, data)


def generate(
    static_search_path: Path,
    templates_search_path: Path,
    templates_variables: dict[str, str],
    output_path: Path,
    exists_ok=False,
) -> None:
    content = get_content(
        static_search_path,
        templates_search_path,
        templates_variables,
    )
    write(content, output_path, exists_ok)
