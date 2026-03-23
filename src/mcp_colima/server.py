from __future__ import annotations

from fastmcp import FastMCP

from .cli_wrapper import ColimaCLI
from .tools.access import register_access_tools
from .tools.lifecycle import register_lifecycle_tools
from .tools.status import register_status_tools


def create_server() -> FastMCP:
    mcp = FastMCP(name="mcp-colima")
    cli = ColimaCLI()

    register_lifecycle_tools(mcp, cli)
    register_status_tools(mcp, cli)
    register_access_tools(mcp, cli)

    @mcp.tool
    def colima_healthcheck() -> dict[str, str]:
        return {"status": "ok", "server": "mcp-colima"}

    return mcp


def main() -> None:
    create_server().run()


if __name__ == "__main__":
    main()
