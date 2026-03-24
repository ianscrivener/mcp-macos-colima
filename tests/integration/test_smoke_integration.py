import subprocess

import pytest


@pytest.mark.integration
def test_colima_is_available_for_integration(has_colima):
    if not has_colima:
        pytest.skip("colima not found on PATH — skipping integration test")
    proc = subprocess.run(["colima", "version"], capture_output=True, text=True, check=False)
    assert proc.returncode == 0


@pytest.mark.integration
def test_colima_version_via_cli(has_colima):
    if not has_colima:
        pytest.skip("colima not found on PATH — skipping integration test")
    from mcp_colima.cli_wrapper import ColimaCLI

    cli = ColimaCLI()
    result = cli.run(["version"])
    assert result["error"] is False
    assert result["exit_code"] == 0
    assert result["stdout"]  # version string should be non-empty


@pytest.mark.integration
def test_colima_list_via_cli(has_colima):
    if not has_colima:
        pytest.skip("colima not found on PATH — skipping integration test")
    from mcp_colima.cli_wrapper import ColimaCLI

    cli = ColimaCLI()
    result = cli.run(["list", "--json"], parse_json=True)
    assert result["error"] is False
    # data should be a list (possibly empty if no profiles exist)
    assert isinstance(result["data"], list)
