from pathlib import Path
from unittest.mock import Mock, call, patch

import pytest
from jinja2.exceptions import UndefinedError
from template import templating


def test_generate_success(test_dir):
    output_path = test_dir.joinpath("output_path")

    with patch("template.templating.write") as mock_write:
        templating.generate(
            static_search_path=test_dir.joinpath("templating/static"),
            templates_search_path=test_dir.joinpath("templating/templates"),
            templates_variables={"artifact_id": "a", "refs": "r"},
            output_path=output_path,
        )

        mock_write.assert_called_once_with(
            [
                (".migration/refs.json", "r"),
                ("pom.xml", "<project>\n    <artifactId>a</artifactId>\n</project>"),
                (Path("example.txt"), "Hello"),
            ],
            output_path,
            False,
        )


def test_generate_missing_variable(test_dir):
    output_path = test_dir.joinpath("output_path")

    with patch("template.templating.write") as mock_write:
        with pytest.raises(UndefinedError) as e:
            templating.generate(
                static_search_path=test_dir.joinpath("templating/static"),
                templates_search_path=test_dir.joinpath("templating/templates"),
                templates_variables={"artifact_id": "a"},
                output_path=output_path,
            )
        assert e.value.message == "'refs' is undefined"
        mock_write.assert_not_called()


def test_write_success():
    path = Mock(spec=Path)
    data = "data"

    joined_path = Mock(spec=Path, exists=Mock(return_value=False))
    output_path = Mock(spec=Path, joinpath=Mock(return_value=joined_path))

    templating.write(content=[(path, data)], output_path=output_path, exists_ok=False)

    assert output_path.joinpath.mock_calls == [call(path), call(path)]
    joined_path.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    joined_path.write_text.assert_called_once_with(data)


def test_write_path_exists():
    path = Mock(spec=Path)
    data = "data"

    joined_path = Mock(spec=Path, exists=Mock(return_value=True))
    output_path = Mock(spec=Path, joinpath=Mock(return_value=joined_path))

    with pytest.raises(RuntimeError) as e:
        templating.write(content=[(path, data)], output_path=output_path, exists_ok=False)

    assert str(e.value) == f"Output path exists: {joined_path}"
    assert output_path.joinpath.mock_calls == [call(path)]
    joined_path.parent.mkdir.assert_not_called()
    joined_path.write_text.assert_not_called()
