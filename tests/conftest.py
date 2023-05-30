from pathlib import Path

import pytest


@pytest.fixture()
def test_dir(request):
    return Path(request.module.__file__).parent
