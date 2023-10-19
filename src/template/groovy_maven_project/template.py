from pathlib import Path

from template.templating import generate

template_path = Path(__file__).parent


def create(
    output_dir: Path,
    group_id: str,
    artifact_id: str,
    version: str,
    packaging: str,
    java_version: str,
) -> str:
    output_path = output_dir.joinpath(artifact_id)
    if output_path.exists():
        return f"Error: {output_path} already exists"

    generate(
        static_search_path=template_path.joinpath("static"),
        templates_search_path=template_path.joinpath("templates"),
        templates_variables={
            "group_id": group_id,
            "artifact_id": artifact_id,
            "version": version,
            "packaging": packaging,
            "java_version": java_version,
        },
        output_path=output_path,
    )

    # Create directories
    package_path = f"{group_id}/{artifact_id}".replace(".", "/")
    for s in [
        "src/main/java",
        "src/main/resources",
        "src/test/java",
        "src/test/resources",
    ]:
        output_path.joinpath(s).joinpath(package_path).mkdir(parents=True)

    return f"Created {artifact_id} in {output_path}"
