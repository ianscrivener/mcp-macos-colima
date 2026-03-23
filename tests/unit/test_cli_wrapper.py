import subprocess

from mcp_colima.cli_wrapper import ColimaCLI


def test_run_success_with_json(mocker):
    mocker.patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["colima", "list", "--json"],
            returncode=0,
            stdout='[{"name":"default","status":"Stopped"}]',
            stderr="",
        ),
    )
    cli = ColimaCLI()
    result = cli.run(["list", "--json"], parse_json=True)
    assert result["error"] is False
    assert result["data"] == [{"name": "default", "status": "Stopped"}]


def test_run_non_zero_exit(mocker):
    mocker.patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["colima", "start", "default"],
            returncode=1,
            stdout="",
            stderr="failure",
        ),
    )
    cli = ColimaCLI()
    result = cli.run(["start", "default"])
    assert result["error"] is True
    assert result["exit_code"] == 1
    assert result["stderr"] == "failure"


def test_run_timeout(mocker):
    mocker.patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="colima start", timeout=1))
    cli = ColimaCLI()
    result = cli.run(["start", "default"], timeout_seconds=1)
    assert result["error"] is True
    assert result["exit_code"] == 124


def test_run_success_with_concatenated_json(mocker):
    mocker.patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["colima", "list", "--json"],
            returncode=0,
            stdout='{"name":"one"}\n{"name":"two"}',
            stderr="",
        ),
    )
    cli = ColimaCLI()
    result = cli.run(["list", "--json"], parse_json=True)
    assert result["error"] is False
    assert result["data"] == [{"name": "one"}, {"name": "two"}]
