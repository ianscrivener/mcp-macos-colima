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
        name = normalize_profile(profile)
        return cli.run(["ssh", "--profile", name, "--", "sh", "-lc", command], timeout_seconds=timeout_seconds)
