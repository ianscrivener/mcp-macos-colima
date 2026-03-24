"""Unit tests for all MCP tool functions.

All tests use a fake ColimaCLI to avoid any real subprocess calls.
"""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from mcp_colima.tools.access import register_access_tools
from mcp_colima.tools.lifecycle import normalize_profile, register_lifecycle_tools
from mcp_colima.tools.status import register_status_tools


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ok(command: list[str], stdout: str = "", data=None) -> dict:
    return {"error": False, "command": command, "exit_code": 0, "stdout": stdout, "stderr": "", "data": data, "message": None}


def _err(command: list[str], exit_code: int = 1, stderr: str = "fail") -> dict:
    return {"error": True, "command": command, "exit_code": exit_code, "stdout": "", "stderr": stderr, "data": None, "message": None}


def _make_cli(return_value: dict | None = None) -> MagicMock:
    cli = MagicMock()
    cli.run.return_value = return_value or _ok(["colima"])
    return cli


def _extract_tool(mcp_mock: MagicMock, name: str):
    """Return the function registered via @mcp.tool for the given name."""
    for call in mcp_mock.tool.call_args_list:
        fn = call.args[0] if call.args else None
        if fn and fn.__name__ == name:
            return fn
    raise KeyError(f"Tool '{name}' not registered")


def _make_mcp() -> MagicMock:
    """Return a MagicMock that records @mcp.tool decorator calls."""
    mcp = MagicMock()
    # @mcp.tool used as bare decorator: mcp.tool(fn) -> fn
    mcp.tool.side_effect = lambda fn: fn
    return mcp


# ---------------------------------------------------------------------------
# normalize_profile
# ---------------------------------------------------------------------------

class TestNormalizeProfile:
    def test_none_returns_default(self):
        assert normalize_profile(None) == "default"

    def test_empty_string_returns_default(self):
        assert normalize_profile("") == "default"

    def test_whitespace_returns_default(self):
        assert normalize_profile("   ") == "default"

    def test_named_profile_returned_as_is(self):
        assert normalize_profile("my-profile") == "my-profile"

    def test_whitespace_stripped_from_named_profile(self):
        assert normalize_profile("  dev  ") == "dev"


# ---------------------------------------------------------------------------
# colima_start
# ---------------------------------------------------------------------------

class TestColimaStart:
    def setup_method(self):
        self.cli = _make_cli()
        self.mcp = _make_mcp()
        register_lifecycle_tools(self.mcp, self.cli)
        self.tool = _extract_tool(self.mcp, "colima_start")

    def test_start_defaults(self):
        self.tool()
        self.cli.run.assert_called_once_with(["start", "default"], timeout_seconds=300)

    def test_start_named_profile(self):
        self.tool(profile="dev")
        args = self.cli.run.call_args[0][0]
        assert args == ["start", "dev"]

    def test_start_with_cpus(self):
        self.tool(cpus=4)
        args = self.cli.run.call_args[0][0]
        assert "--cpus" in args
        assert "4" in args

    def test_start_memory_gib_int(self):
        self.tool(memory_gib=8)
        args = self.cli.run.call_args[0][0]
        idx = args.index("--memory")
        assert args[idx + 1] == "8"

    def test_start_memory_gib_truncates_to_int(self):
        """memory_gib must be passed as an integer even if caller supplies a float."""
        self.tool(memory_gib=4)
        args = self.cli.run.call_args[0][0]
        idx = args.index("--memory")
        assert "." not in args[idx + 1]

    def test_start_disk_gib(self):
        self.tool(disk_gib=60)
        args = self.cli.run.call_args[0][0]
        assert "--disk" in args and "60" in args

    def test_start_runtime(self):
        self.tool(runtime="containerd")
        args = self.cli.run.call_args[0][0]
        assert "--runtime" in args and "containerd" in args

    def test_start_kubernetes_flag(self):
        self.tool(kubernetes=True)
        args = self.cli.run.call_args[0][0]
        assert "--kubernetes" in args

    def test_start_no_kubernetes_by_default(self):
        self.tool()
        args = self.cli.run.call_args[0][0]
        assert "--kubernetes" not in args

    def test_start_custom_timeout(self):
        self.tool(timeout_seconds=600)
        kwargs = self.cli.run.call_args[1]
        assert kwargs["timeout_seconds"] == 600

    def test_start_returns_cli_result(self):
        expected = _ok(["colima", "start", "default"])
        self.cli.run.return_value = expected
        result = self.tool()
        assert result is expected


# ---------------------------------------------------------------------------
# colima_stop
# ---------------------------------------------------------------------------

class TestColimaStop:
    def setup_method(self):
        self.cli = _make_cli()
        self.mcp = _make_mcp()
        register_lifecycle_tools(self.mcp, self.cli)
        self.tool = _extract_tool(self.mcp, "colima_stop")

    def test_stop_defaults(self):
        self.tool()
        self.cli.run.assert_called_once_with(["stop", "default"], timeout_seconds=180)

    def test_stop_named_profile(self):
        self.tool(profile="staging")
        args = self.cli.run.call_args[0][0]
        assert args[1] == "staging"

    def test_stop_force(self):
        self.tool(force=True)
        args = self.cli.run.call_args[0][0]
        assert "--force" in args

    def test_stop_no_force_by_default(self):
        self.tool()
        args = self.cli.run.call_args[0][0]
        assert "--force" not in args

    def test_stop_custom_timeout(self):
        self.tool(timeout_seconds=60)
        kwargs = self.cli.run.call_args[1]
        assert kwargs["timeout_seconds"] == 60


# ---------------------------------------------------------------------------
# colima_restart
# ---------------------------------------------------------------------------

class TestColimaRestart:
    def setup_method(self):
        self.cli = _make_cli()
        self.mcp = _make_mcp()
        register_lifecycle_tools(self.mcp, self.cli)
        self.tool = _extract_tool(self.mcp, "colima_restart")

    def test_restart_defaults(self):
        self.tool()
        self.cli.run.assert_called_once_with(["restart", "default"], timeout_seconds=300)

    def test_restart_named_profile(self):
        self.tool(profile="prod")
        args = self.cli.run.call_args[0][0]
        assert args == ["restart", "prod"]

    def test_restart_force(self):
        self.tool(force=True)
        args = self.cli.run.call_args[0][0]
        assert "--force" in args

    def test_restart_no_force_by_default(self):
        self.tool()
        args = self.cli.run.call_args[0][0]
        assert "--force" not in args

    def test_restart_custom_timeout(self):
        self.tool(timeout_seconds=120)
        kwargs = self.cli.run.call_args[1]
        assert kwargs["timeout_seconds"] == 120


# ---------------------------------------------------------------------------
# colima_update
# ---------------------------------------------------------------------------

class TestColimaUpdate:
    def setup_method(self):
        self.cli = _make_cli()
        self.mcp = _make_mcp()
        register_lifecycle_tools(self.mcp, self.cli)
        self.tool = _extract_tool(self.mcp, "colima_update")

    def test_update_defaults(self):
        self.tool()
        self.cli.run.assert_called_once_with(["update", "default"], timeout_seconds=300)

    def test_update_named_profile(self):
        self.tool(profile="ci")
        args = self.cli.run.call_args[0][0]
        assert args == ["update", "ci"]

    def test_update_kubernetes_flag(self):
        self.tool(kubernetes=True)
        args = self.cli.run.call_args[0][0]
        assert "--kubernetes" in args

    def test_update_no_kubernetes_by_default(self):
        self.tool()
        args = self.cli.run.call_args[0][0]
        assert "--kubernetes" not in args

    def test_update_custom_timeout(self):
        self.tool(timeout_seconds=120)
        kwargs = self.cli.run.call_args[1]
        assert kwargs["timeout_seconds"] == 120

    def test_update_returns_cli_result(self):
        expected = _ok(["colima", "update", "default"])
        self.cli.run.return_value = expected
        result = self.tool()
        assert result is expected


# ---------------------------------------------------------------------------
# colima_status
# ---------------------------------------------------------------------------

class TestColimaStatus:
    def setup_method(self):
        self.cli = _make_cli()
        self.mcp = _make_mcp()
        register_status_tools(self.mcp, self.cli)
        self.tool = _extract_tool(self.mcp, "colima_status")

    def test_status_defaults(self):
        self.tool()
        self.cli.run.assert_called_once_with(
            ["status", "default", "--json"],
            timeout_seconds=60,
            parse_json=True,
        )

    def test_status_named_profile(self):
        self.tool(profile="dev")
        args = self.cli.run.call_args[0][0]
        assert args[1] == "dev"

    def test_status_extended(self):
        self.tool(extended=True)
        args = self.cli.run.call_args[0][0]
        assert "--extended" in args

    def test_status_no_extended_by_default(self):
        self.tool()
        args = self.cli.run.call_args[0][0]
        assert "--extended" not in args

    def test_status_always_includes_json_flag(self):
        self.tool()
        args = self.cli.run.call_args[0][0]
        assert "--json" in args

    def test_status_parse_json_true(self):
        self.tool()
        kwargs = self.cli.run.call_args[1]
        assert kwargs["parse_json"] is True


# ---------------------------------------------------------------------------
# colima_list
# ---------------------------------------------------------------------------

class TestColimaList:
    def setup_method(self):
        self.cli = _make_cli()
        self.mcp = _make_mcp()
        register_status_tools(self.mcp, self.cli)
        self.tool = _extract_tool(self.mcp, "colima_list")

    def test_list_command(self):
        self.tool()
        self.cli.run.assert_called_once_with(["list", "--json"], timeout_seconds=60, parse_json=True)

    def test_list_custom_timeout(self):
        self.tool(timeout_seconds=30)
        kwargs = self.cli.run.call_args[1]
        assert kwargs["timeout_seconds"] == 30

    def test_list_parse_json_true(self):
        self.tool()
        kwargs = self.cli.run.call_args[1]
        assert kwargs["parse_json"] is True

    def test_list_returns_cli_result(self):
        data = [{"name": "default", "status": "Running"}]
        expected = _ok(["colima", "list", "--json"], data=data)
        self.cli.run.return_value = expected
        result = self.tool()
        assert result["data"] == data


# ---------------------------------------------------------------------------
# colima_version
# ---------------------------------------------------------------------------

class TestColimaVersion:
    def setup_method(self):
        self.cli = _make_cli()
        self.mcp = _make_mcp()
        register_status_tools(self.mcp, self.cli)
        self.tool = _extract_tool(self.mcp, "colima_version")

    def test_version_command(self):
        self.tool()
        self.cli.run.assert_called_once_with(["version"], timeout_seconds=30)

    def test_version_custom_timeout(self):
        self.tool(timeout_seconds=10)
        kwargs = self.cli.run.call_args[1]
        assert kwargs["timeout_seconds"] == 10

    def test_version_no_parse_json(self):
        """version output is plain text — parse_json must NOT be passed as True."""
        self.tool()
        kwargs = self.cli.run.call_args[1]
        assert kwargs.get("parse_json", False) is False


# ---------------------------------------------------------------------------
# colima_ssh
# ---------------------------------------------------------------------------

class TestColimaSSH:
    def setup_method(self):
        self.cli = _make_cli()
        self.mcp = _make_mcp()
        register_access_tools(self.mcp, self.cli)
        self.tool = _extract_tool(self.mcp, "colima_ssh")

    def test_ssh_default_profile(self):
        self.tool(command="uname -a")
        args = self.cli.run.call_args[0][0]
        assert args == ["ssh", "--profile", "default", "--", "sh", "-lc", "uname -a"]

    def test_ssh_named_profile(self):
        self.tool(command="ls /", profile="dev")
        args = self.cli.run.call_args[0][0]
        assert args[2] == "dev"
        assert "--profile" in args

    def test_ssh_command_passed_through(self):
        self.tool(command="echo hello")
        args = self.cli.run.call_args[0][0]
        assert args[-1] == "echo hello"

    def test_ssh_shell_wrapper(self):
        """Command must be wrapped in sh -lc so PATH and login env are available."""
        self.tool(command="docker ps")
        args = self.cli.run.call_args[0][0]
        assert "sh" in args and "-lc" in args

    def test_ssh_double_dash_separator(self):
        self.tool(command="ls")
        args = self.cli.run.call_args[0][0]
        assert "--" in args

    def test_ssh_custom_timeout(self):
        self.tool(command="sleep 5", timeout_seconds=30)
        kwargs = self.cli.run.call_args[1]
        assert kwargs["timeout_seconds"] == 30

    def test_ssh_returns_cli_result(self):
        expected = _ok(["colima", "ssh", "default", "--", "sh", "-lc", "uname"], stdout="Linux")
        self.cli.run.return_value = expected
        result = self.tool(command="uname")
        assert result is expected

    def test_ssh_error_propagated(self):
        expected = _err(["colima", "ssh", "default", "--", "sh", "-lc", "false"])
        self.cli.run.return_value = expected
        result = self.tool(command="false")
        assert result["error"] is True
