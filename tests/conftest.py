import shutil

import pytest


@pytest.fixture
def has_colima() -> bool:
    return shutil.which("colima") is not None
