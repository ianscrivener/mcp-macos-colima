import shutil

import pytest


@pytest.fixture
def has_colima() -> bool:
    return shutil.which("colima") is not None


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: marks tests that require a real Colima installation (deselect with -m 'not integration')",
    )
