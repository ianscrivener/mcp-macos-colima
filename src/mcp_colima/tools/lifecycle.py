from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from ..cli_wrapper import ColimaCLI


def normalize_profile(profile: str | None) -> str:
    return (profile or "default").strip() or "default"


def register_lifecycle_tools(mcp: FastMCP, cli: ColimaCLI) -> None:
    @mcp.tool
    def colima_start(
        profile: str = "default",
        cpus: int | None = None,
        memory_gib: float | None = None,
        disk_gib: int | None = None,
        runtime: str | None = None,
        kubernetes: bool = False,
        timeout_seconds: int = 300,
    ) -> dict[str, Any]:
        name = normalize_profile(profile)
        args: list[str] = ["start", name]
        if cpus is not None:
            args.extend(["--cpus", str(cpus)])
        if memory_gib is not None:
            args.extend(["--memory", str(memory_gib)])
        if disk_gib is not None:
            args.extend(["--disk", str(disk_gib)])
        if runtime is not None:
            args.extend(["--runtime", runtime])
        if kubernetes:
            args.append("--kubernetes")
        return cli.run(args, timeout_seconds=timeout_seconds)

    @mcp.tool
    def colima_stop(profile: str = "default", force: bool = False, timeout_seconds: int = 180) -> dict[str, Any]:
        name = normalize_profile(profile)
        args = ["stop", name]
        if force:
            args.append("--force")
        return cli.run(args, timeout_seconds=timeout_seconds)

    @mcp.tool
    def colima_restart(
        profile: str = "default",
        force: bool = False,
        timeout_seconds: int = 300,
    ) -> dict[str, Any]:
        name = normalize_profile(profile)
        args = ["restart", name]
        if force:
            args.append("--force")
        return cli.run(args, timeout_seconds=timeout_seconds)
