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
        name = normalize_profile(profile)
        args = ["status", name, "--json"]
        if extended:
            args.append("--extended")
        return cli.run(args, timeout_seconds=timeout_seconds, parse_json=True)

    @mcp.tool
    def colima_list(timeout_seconds: int = 60) -> dict[str, Any]:
        return cli.run(["list", "--json"], timeout_seconds=timeout_seconds, parse_json=True)

    @mcp.tool
    def colima_version(timeout_seconds: int = 30) -> dict[str, Any]:
        return cli.run(["version"], timeout_seconds=timeout_seconds)
