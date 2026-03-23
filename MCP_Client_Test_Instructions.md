# MCP Client Test Instructions (mcp-macos-colima)

## Objective
Validate `mcp-macos-colima` consistently across Claude Code, GitHub Copilot Chat, Codex, and Gemini.

## Repository Context

- Repository root: `mcp-macos-colima`
- MCP command: `uv run mcp-colima`
- Reports root: `test_reports/mcp_colima/`

## Setup

```bash
git clone git@github.com:ianscrivener/mcp-macos-colima.git
cd mcp-macos-colima
uv venv
source .venv/bin/activate
uv sync --extra dev
```

## Test Scope

Phase 1 tools:

- `colima_start`
- `colima_stop`
- `colima_restart`
- `colima_status`
- `colima_list`
- `colima_ssh`
- `colima_version`

## Standard Sequence (A-J)

1. Tool discovery
2. Health check
3. Start and list
4. Status JSON
5. SSH command
6. Version
7. Stop
8. Invalid profile error contract
9. Timeout handling
10. Restart

## Safety Rules

- Do not run destructive commands against profiles you do not own.
- Use `default` unless a disposable profile is required by your test plan.

## Response Contract

All tool responses must be parseable JSON and should include standard fields:

- `error`
- `command`
- `exit_code`
- `stdout`
- `stderr`
- `data` (when present)

## Per-Client Report Paths

- `test_reports/mcp_colima/claude_code/mcp-client-results-<date>.md`
- `test_reports/mcp_colima/copilot/mcp-client-results-<date>.md`
- `test_reports/mcp_colima/codex/mcp-client-results-<date>.md`
- `test_reports/mcp_colima/gemini/mcp-client-results-<date>.md`

## Required Report Sections

1. Client metadata
2. MCP connection metadata
3. A-J test matrix (pass/fail + evidence)
4. Failure details
5. Final verdict (`Ready`, `Ready with caveats`, `Not ready`)

## GitHub Workflow

```bash
git checkout main
git pull origin main
# run tests and update reports
git add -A
git commit -m "Update colima test reports"
git push origin main
```
