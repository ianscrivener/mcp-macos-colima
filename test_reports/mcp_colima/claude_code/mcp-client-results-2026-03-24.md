# MCP Client Test Report — Claude Code

**Date:** 2026-03-24  
**Generated:** 2026-03-24T11:14:47+0000  
**Duration:** 19.5s  

## 1. Client Metadata

| Field | Value |
|-------|-------|
| Client | Claude Code (claude-sonnet-4-6) |
| Platform | macOS Darwin 25.3.0 (arm64) |
| Test date | 2026-03-24 |
| Script | run_claude_code_tests.py |
| FastMCP client version | 3.1.1 |

## 2. MCP Connection Metadata

| Field | Value |
|-------|-------|
| Transport | stdio |
| Command | `uv run mcp-colima` |
| Working directory | `/Users/ianscrivener/bin/mcp-servers/mcp-macos-colima` |
| MCP framework | FastMCP 3.1.1 |
| Server name | mcp-colima |
| Server version | 3.1.1 |

## 3. Test Matrix (A–J)

| ID | Test | Result | Notes |
|----|------|--------|-------|
| A | Tool discovery | PASS | 9 tools discovered |
| B | Health check | PASS | status=ok, server=mcp-colima |
| C | Start and list | PASS | start idempotent (already running); list confirmed Running |
| D | Status JSON | PASS | JSON data block present with VM details |
| E | SSH command | PASS | uname -a returned Linux kernel string |
| F | Version | PASS | colima version string returned |
| G | Stop | PASS | exit_code=0, graceful stop |
| H | Invalid profile error contract | PASS | error=true, exit_code=1 as expected for unknown profile |
| I | Timeout handling | PASS | error=true, exit_code=124 (SIGALRM timeout at 1s) |
| J | Restart | PASS | colima restarted successfully |

## 4. Failure Details

No failures.

## 5. Evidence Snapshots

### A — Tool Discovery

```json
{
  "name": "Tool discovery",
  "pass": true,
  "tool_count": 9,
  "tools": [
    "colima_healthcheck",
    "colima_list",
    "colima_restart",
    "colima_ssh",
    "colima_start",
    "colima_status",
    "colima_stop",
    "colima_update",
    "colima_version"
  ]
}
```

### B — Health Check

```json
{
  "name": "Health check",
  "pass": true,
  "response": {
    "status": "ok",
    "server": "mcp-colima"
  }
}
```

### D — Status JSON (data excerpt)

```json
{
  "display_name": "colima",
  "driver": "QEMU",
  "arch": "aarch64",
  "runtime": "docker",
  "mount_type": "sshfs",
  "docker_socket": "unix:///Users/ianscrivener/.colima/default/docker.sock",
  "containerd_socket": "unix:///Users/ianscrivener/.colima/default/containerd.sock",
  "kubernetes": false,
  "cpu": 2,
  "memory": 2147483648,
  "disk": 107374182400
}
```

### E — SSH Command Output

```
Linux colima 6.8.0-100-generic #100-Ubuntu SMP PREEMPT_DYNAMIC Tue Jan 13 16:39:21 UTC 2026 aarch64 aarch64 aarch64 GNU/Linux
```

### F — Version

```
colima version 0.10.1
git commit: ed905203afdbc6fd4eae6cc301918099ff31e86e

runtime: docker
arch: aarch64
client: v29.3.0
server: v29.2.1
```

### H — Invalid Profile (error contract)

```json
{
  "error": true,
  "command": [
    "colima",
    "status",
    "does-not-exist",
    "--json"
  ],
  "exit_code": 1,
  "stdout": "",
  "stderr": "time=\"2026-03-24T22:14:52+11:00\" level=fatal msg=\"colima [profile=does-not-exist] is not running\"",
  "data": null,
  "message": null
}
```

### I — Timeout Handling

```json
{
  "error": true,
  "command": [
    "colima",
    "start",
    "default"
  ],
  "exit_code": 124,
  "stdout": "",
  "stderr": "Command timed out after 1 seconds",
  "data": null,
  "message": null
}
```

## 6. Final Verdict

**Ready**

All 10 tests passed. The mcp-macos-colima server is fully functional when accessed via the Claude Code MCP client.