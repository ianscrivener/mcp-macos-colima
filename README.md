# mcp-macos-colima

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
- UV package manager installed

Install UV (if needed):

```bash
brew install uv
uv --version
```

## Clone And Setup

```bash
git clone git@github.com:ianscrivener/mcp-macos-colima.git
cd mcp-macos-colima
uv venv
source .venv/bin/activate
uv sync --extra dev
```

`uv sync --extra dev` is required to install runtime and test dependencies from `pyproject.toml`.

## Run MCP Server

```bash
source .venv/bin/activate
uv run mcp-colima
```

FastMCP defaults to stdio transport, suitable for MCP clients such as Claude Code.

For MCP clients, configure the server command as:

```bash
uv run mcp-colima
```

## Test

```bash
source .venv/bin/activate
uv run pytest -m "not integration" --cov=. --cov-report=term-missing
uv run pytest --cov=. --cov-report=term-missing
```

Client reports should be stored under:

- `test_reports/mcp_colima/claude_code/`
- `test_reports/mcp_colima/copilot/`
- `test_reports/mcp_colima/codex/`
- `test_reports/mcp_colima/gemini/`

## GitHub Workflow

Pull latest:

```bash
git checkout main
git pull origin main
```

Push changes:

```bash
git add -A
git commit -m "<summary>"
git push origin main
```

## Notes

- Tool responses are parseable JSON objects.
- Non-zero CLI exits are normalized into `{ "error": true, ... }` responses.
- `colima_ssh` is one-shot and requires a command string.
