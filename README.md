# mcp-colima

FastMCP server for core Colima operations on macOS.

## Scope

Phase 1 tools:

- `colima_start`
- `colima_stop`
- `colima_restart`
- `colima_status`
- `colima_list`
- `colima_ssh`
- `colima_version`

## Prerequisites

- macOS host
- `colima` installed and available on `PATH`
- Python 3.11+
- UV package manager

## Setup

```bash
cd mcp/colima-macos-mcp
uv venv
source .venv/bin/activate
uv sync --extra dev
```

## Run

```bash
source .venv/bin/activate
uv run mcp-colima
```

FastMCP defaults to stdio transport for MCP clients like Claude Desktop and Claude Code.

## Tests

```bash
source .venv/bin/activate
uv run pytest -m "not integration" --cov=. --cov-report=term-missing
uv run pytest --cov=. --cov-report=term-missing
```

## Notes

- Tool responses are always parseable JSON objects.
- Non-zero CLI exits are normalized into `{ "error": true, ... }` responses.
- `colima_ssh` is one-shot and requires a command string.
# mcp-macos-colima
