from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from ..cli_wrapper import ColimaCLI
from .lifecycle import normalize_profile


def register_status_tools(mcp: FastMCP, cli: ColimaCLI) -> None:
    @mcp.tool
    def colima_status(
        profile: str = "default",
        extended: bool = False,
        timeout_seconds: int = 60,
    ) -> dict[str, Any]:
        """Get the current status of a Colima VM.

        Returns parsed JSON with VM state, runtime, CPU, memory, and disk info.

        Args:
            profile: Colima profile name (default: "default").
            extended: Pass --extended for additional detail (Colima >= 0.6).
            timeout_seconds: Maximum seconds to wait for the status response.
        """
        name = normalize_profile(profile)
        args = ["status", name, "--json"]
        if extended:
            args.append("--extended")
        return cli.run(args, timeout_seconds=timeout_seconds, parse_json=True)

    @mcp.tool
    def colima_list(timeout_seconds: int = 60) -> dict[str, Any]:
        """List all Colima VM instances and their current states.

        Returns parsed JSON array of all profiles with status, runtime, and
        resource allocation for each.

        Args:
            timeout_seconds: Maximum seconds to wait for the list response.
        """
        return cli.run(["list", "--json"], timeout_seconds=timeout_seconds, parse_json=True)

    @mcp.tool
    def colima_version(timeout_seconds: int = 30) -> dict[str, Any]:
        """Return Colima and bundled component version information.

        Output is plain text (stdout) from `colima version`.

        Args:
            timeout_seconds: Maximum seconds to wait for the version response.
        """
        return cli.run(["version"], timeout_seconds=timeout_seconds)
