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
        memory_gib: int | None = None,
        disk_gib: int | None = None,
        runtime: str | None = None,
        kubernetes: bool = False,
        timeout_seconds: int = 300,
    ) -> dict[str, Any]:
        """Start a Colima VM. Creates the instance if it does not already exist.

        Args:
            profile: Colima profile name (default: "default").
            cpus: Number of CPUs to allocate.
            memory_gib: Memory in whole GiB to allocate (Colima requires an integer).
            disk_gib: Disk size in GiB to allocate.
            runtime: Container runtime to use (e.g. "docker", "containerd").
            kubernetes: Enable Kubernetes when starting.
            timeout_seconds: Maximum seconds to wait for the VM to start.
        """
        name = normalize_profile(profile)
        args: list[str] = ["start", name]
        if cpus is not None:
            args.extend(["--cpus", str(cpus)])
        if memory_gib is not None:
            args.extend(["--memory", str(int(memory_gib))])
        if disk_gib is not None:
            args.extend(["--disk", str(disk_gib)])
        if runtime is not None:
            args.extend(["--runtime", runtime])
        if kubernetes:
            args.append("--kubernetes")
        return cli.run(args, timeout_seconds=timeout_seconds)

    @mcp.tool
    def colima_stop(profile: str = "default", force: bool = False, timeout_seconds: int = 180) -> dict[str, Any]:
        """Stop a running Colima VM.

        Args:
            profile: Colima profile name (default: "default").
            force: Force-stop the VM without a graceful shutdown.
            timeout_seconds: Maximum seconds to wait for the VM to stop.
        """
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
        """Restart a Colima VM (stop then start).

        Args:
            profile: Colima profile name (default: "default").
            force: Force-stop before restarting.
            timeout_seconds: Maximum seconds to wait for the full restart cycle.
        """
        name = normalize_profile(profile)
        args = ["restart", name]
        if force:
            args.append("--force")
        return cli.run(args, timeout_seconds=timeout_seconds)

    @mcp.tool
    def colima_update(
        profile: str = "default",
        kubernetes: bool = False,
        timeout_seconds: int = 300,
    ) -> dict[str, Any]:
        """Update the Colima VM configuration (runtime components and optional Kubernetes).

        Runs `colima update` which applies pending configuration changes to a
        running or stopped instance without a full teardown.

        Args:
            profile: Colima profile name (default: "default").
            kubernetes: Pass --kubernetes to update Kubernetes components as well.
            timeout_seconds: Maximum seconds to wait for the update to complete.
        """
        name = normalize_profile(profile)
        args = ["update", name]
        if kubernetes:
            args.append("--kubernetes")
        return cli.run(args, timeout_seconds=timeout_seconds)
