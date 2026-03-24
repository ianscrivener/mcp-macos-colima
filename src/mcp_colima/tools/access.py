from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from ..cli_wrapper import ColimaCLI
from .lifecycle import normalize_profile


def register_access_tools(mcp: FastMCP, cli: ColimaCLI) -> None:
    @mcp.tool
    def colima_ssh(
        command: str,
        profile: str = "default",
        timeout_seconds: int = 120,
    ) -> dict[str, Any]:
        """Run a one-shot shell command inside a Colima VM over SSH.

        Uses `colima ssh <profile> -- sh -lc <command>` for single-command
        execution. Interactive sessions are not supported.

        Args:
            command: Shell command to execute inside the VM.
            profile: Colima profile name (default: "default").
            timeout_seconds: Maximum seconds to wait for the command to complete.
        """
        name = normalize_profile(profile)
        return cli.run(
            ["ssh", "--profile", name, "--", "sh", "-lc", command],
            timeout_seconds=timeout_seconds,
        )
