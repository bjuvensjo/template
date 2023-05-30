from pathlib import Path

from template.templating import generate

template_path = Path(__file__).parent


def create(output_dir: Path, name: str) -> None:
    output_path = output_dir.joinpath(name)

    generate(
        static_search_path=template_path.joinpath("static"),
        templates_search_path=template_path.joinpath("templates"),
        templates_variables={
            "name": name,
            "workspace_folder": output_path.absolute().as_posix(),
            "package": name.replace("-", "_").lower(),
        },
        output_path=output_path,
    )
