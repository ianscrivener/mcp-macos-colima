# METHODS_SUPPORTED

This document maps MCP methods to the current Phase 1 Colima command surface.

## Response Contract

All tools return structured JSON. Error responses follow:

```json
{
  "error": true,
  "exit_code": 1,
  "stderr": "...",
  "command": ["colima", "..."]
}
```

## Phase 1 Methods

| MCP method | CLI mapping | Key parameters | Notes |
| --- | --- | --- | --- |
| `colima_start` | `colima start [profile]` | `profile`, `cpus`, `memory_gib`, `disk_gib`, `runtime`, `kubernetes`, `timeout_seconds` | Simplified parameter set |
| `colima_stop` | `colima stop [profile]` | `profile`, `force`, `timeout_seconds` |  |
| `colima_restart` | `colima restart [profile]` | `profile`, `force`, `timeout_seconds` |  |
| `colima_status` | `colima status [profile] --json` | `profile`, `extended`, `timeout_seconds` | Parses JSON output |
| `colima_list` | `colima list --json` | `timeout_seconds` | Parses JSON output |
| `colima_ssh` | `colima ssh [--profile <name>] -- sh -lc <command>` | `profile`, `command`, `timeout_seconds` | One-shot execution only |
| `colima_version` | `colima version` | `timeout_seconds` | Plain text output |
