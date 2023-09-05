from pathlib import Path

from template.templating import generate

template_path = Path(__file__).parent


def create(output_dir: Path, name: str) -> str:
    output_path = output_dir.joinpath(name)
    if output_path.exists():
        return f"Error: {output_path} already exists"

    generate(
        static_search_path=template_path.joinpath("static"),
        templates_search_path=template_path.joinpath("templates"),
        templates_variables={
            "name": name,
            "workspace_folder": output_path.absolute().as_posix(),
            "package": name.replace("-", "_").replace(".", "_").lower(),
        },
        output_path=output_path,
    )

    return f"Created {name} in {output_path}"
