# INSTALL_MCP (mcp-macos-colima)

This guide explains how to install and configure the Colima MCP server (`mcp-colima`) for Claude, GitHub Copilot, Codex, and other MCP-capable clients.

## 1. Prerequisites

- macOS
- Python 3.11+
- Homebrew
- UV package manager
- Colima CLI (`colima`)

Install missing tools:

    brew install uv
    brew install colima

Verify:

    uv --version
    colima version

## 2. Clone And Set Up

    git clone git@github.com:ianscrivener/mcp-macos-colima.git
    cd mcp-macos-colima
    uv venv
    source .venv/bin/activate
    uv sync --extra dev

Important: `uv sync --extra dev` is required so runtime and test dependencies are installed.

## 3. MCP Server Definition

Use these values in your MCP client:

- server name: `mcp-macos-colima`
- command: `uv`
- args: `run mcp-colima`
- working directory (`cwd`): absolute path to your `mcp-macos-colima` repository

JSON-style example:

    {
      "mcpServers": {
        "mcp-macos-colima": {
          "command": "uv",
          "args": ["run", "mcp-colima"],
          "cwd": "/absolute/path/to/mcp-macos-colima"
        }
      }
    }

## 4. Client Notes

### Claude (Claude Code / Claude Desktop)

- Open MCP settings.
- Add the server using command/args/cwd above.
- Restart the client.
- Confirm tool discovery.

### GitHub Copilot (VS Code)

- Open MCP server management.
- Add one server (`mcp-macos-colima`) with the same command/args/cwd.
- Reload VS Code if required.

### Codex

- Open MCP/server configuration.
- Register the server with the same command/args/cwd.
- Restart/reload and verify tools appear.

## 5. Quick Verification

After registration, run:

- `colima_healthcheck`

Expected response includes:

- `status: ok`
- `server: mcp-colima`

## 6. Troubleshooting

### `uv` not found

- Install UV: `brew install uv`
- Verify from terminal: `uv --version`

### Python modules missing

- Re-run:

    source .venv/bin/activate
    uv sync --extra dev

### `colima` not found

- Install Colima via Homebrew.
- Verify `colima version`.

### Server starts but no tools appear

- Recheck `cwd` path.
- Recheck command/args values.
- Restart the client after config changes.
