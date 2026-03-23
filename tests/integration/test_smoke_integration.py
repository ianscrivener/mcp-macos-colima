import subprocess

import pytest


@pytest.mark.integration
def test_colima_is_available_for_integration():
    proc = subprocess.run(["colima", "version"], capture_output=True, text=True, check=False)
    assert proc.returncode == 0
