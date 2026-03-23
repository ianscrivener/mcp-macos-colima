# Product Requirements Document (PRD)

# PRD: Lima & Colima MCP Servers

**Author:** Scriv
**Date:** 2026-03-23
**Status:** Draft 1

---

## Problem

Managing Lima VMs and Colima container runtimes on macOS requires manual CLI interaction. There is no structured way for AI assistants to discover, invoke, or orchestrate these tools — creating friction in AI-assisted development workflows that depend on local virtualisation and container infrastructure.

## Solution

Two separate FastMCP (Python) servers exposing Lima and Colima CLI operations as MCP tools. Each server wraps the respective CLI, returning structured JSON responses suitable for AI agent consumption.

## Why Two Servers

-   Lima and Colima operate at different abstraction levels — generic VMs vs container runtimes
-   Users may have one without the other
-   Clean tool namespaces (`lima_list` vs `colima_list`)
-   Independent versioning and maintenance

## Delivery

|  | Server 1 | Server 2 |
| --- | --- | --- |
| **Name** | `mcp-lima` | `mcp-colima` |
| **Runtime** | Python 3.11+ / FastMCP | Python 3.11+ / FastMCP |
| **Host dependency** | `limactl` (v2.x) | `colima` (latest) |
| **Transport** | stdio | stdio |
| **Config** | Claude Desktop / Claude Code | Claude Desktop / Claude Code |

## Phasing

| Phase | Scope |
| --- | --- |
| **Phase 1 — MVP** | Core tools only (see tables below) |
| **Phase 2** | Snapshots, disks, network, kubernetes |
| **Phase 3** | Templates, AI/MCP, utility commands |

---

## Lima (limactl v2.x) — Tool Surface

| Category | Command | Core | Description |
| --- | --- | --- | --- |
| **Lifecycle** | `create` | Y | Create instance from template/YAML/URL |
|  | `start` | Y | Start instance (creates if needed) |
|  | `stop` | Y | Stop a running instance |
|  | `restart` | Y | Restart a running instance |
|  | `delete` | Y | Delete an instance |
|  | `factory-reset` | N | Factory reset an instance |
|  | `start-at-login` | N | Register/unregister autostart |
| **Instance Mgmt** | `list` | Y | List instances with status/resources |
|  | `clone` | N | Clone an instance |
|  | `rename` | N | Rename an instance |
|  | `edit` | Y | Edit instance config or template |
|  | `protect` | N | Protect from accidental deletion |
|  | `unprotect` | N | Remove deletion protection |
|  | `info` | Y | Show diagnostic/system info |
|  | `watch` | N | Watch events from instances |
| **Shell & Access** | `shell` | Y | Execute shell/command in VM |
|  | `copy` | Y | Copy files between host and guest |
|  | `show-ssh` | N | Show SSH command *(deprecated)* |
|  | `tunnel` | N | Create a tunnel |
| **Disk** | `disk create` | N | Create a shared disk |
|  | `disk delete` | N | Delete a shared disk |
|  | `disk import` | N | Import a disk image |
|  | `disk list` | N | List shared disks |
|  | `disk resize` | N | Resize a shared disk |
|  | `disk unlock` | N | Unlock a stuck disk |
| **Snapshot** | `snapshot create` | N | Create a VM snapshot |
|  | `snapshot delete` | N | Delete a snapshot |
|  | `snapshot apply` | N | Restore from snapshot |
|  | `snapshot list` | N | List snapshots |
| **Network** | `network create` | N | Create a network |
|  | `network delete` | N | Delete a network |
|  | `network list` | N | List networks |
| **Template** | `template copy` | N | Copy a template locally |
|  | `template url` | N | Show template URL |
|  | `template validate` | N | Validate template YAML |
|  | `template yq` | N | Query template with yq |
| **AI/MCP** | `mcp serve` | N | Serve MCP sandbox tools for AI agents *(experimental)* |
| **Utility** | `validate` | N | Validate YAML files |
|  | `sudoers` | N | Generate sudoers content |
|  | `prune` | N | Prune garbage objects |
|  | `completion` | N | Generate shell completions |

**Phase 1 (Core): 10 tools** — create, start, stop, restart, delete, list, edit, info, shell, copy

Each tool references `METHODS_SUPPORTED.md` in the repo for detailed parameter mapping.

---

## Colima — Tool Surface

| Category | Command | Core | Description |
| --- | --- | --- | --- |
| **Lifecycle** | `start [profile]` | Y | Start VM (creates if needed) |
|  | `stop [profile]` | Y | Stop VM |
|  | `restart [profile]` | Y | Restart VM |
|  | `delete [profile]` | N | Delete VM (preserves data since v0.9) |
|  | `status [profile]` | Y | Show VM status and resources |
|  | `list` | Y | List all profiles with status |
| **Access** | `ssh [profile]` | Y | SSH into VM |
|  | `ssh-config [profile]` | N | Show SSH config |
| **Kubernetes** | `kubernetes start` | N | Start k8s on running instance |
|  | `kubernetes stop` | N | Stop k8s |
|  | `kubernetes reset` | N | Reset k8s cluster |
| **AI/Models** | `model run <model>` | N | Run AI model interactively (krunkit) |
|  | `model serve <model>` | N | Serve model with web chat UI |
| **Containerd** | `nerdctl -- <cmd>` | N | Run nerdctl commands |
|  | `nerdctl install` | N | Install nerdctl to $PATH |
| **Config/Util** | `template` | N | Generate config template YAML |
|  | `update` | N | Update Colima |
|  | `prune [profile]` | N | Prune unused data |
|  | `version` | Y | Show version |
|  | `completion` | N | Generate shell completions |

**Phase 1 (Core): 7 tools** — start, stop, restart, status, list, ssh, version

Each tool references `METHODS_SUPPORTED.md` in the repo for detailed parameter mapping.

---

## Common Design Patterns

Both servers follow the same conventions:

**CLI wrapping:** All tools call the underlying CLI via `subprocess.run()`, parse output (preferring `--json` where available), and return structured JSON.

**Error handling:** Non-zero exit codes return `{ "error": true, "exit_code": N, "stderr": "..." }`. Tools never raise — they always return a parseable response.

**Instance/profile targeting:** All lifecycle tools accept an optional instance name (Lima) or profile name (Colima), defaulting to `default`.

**Destructive operations:** Tools that delete or reset require an explicit confirmation parameter (e.g. `confirm=True`). Without it, they return a preview of what would be affected.

**Timeouts:** Long-running operations (start, restart) include a configurable timeout with sensible defaults matching the CLI (Lima: 10min, Colima: 5min).

## Constraints

-   macOS host only (Lima supports Linux/NetBSD but this targets macOS dev workflows)
-   Requires CLI tools pre-installed via Homebrew
-   stdio transport — no remote/networked access
-   No secrets or credentials handled by the MCP servers

## Success Criteria

-   Phase 1 tools pass basic smoke tests (start/stop/list cycle)
-   Structured JSON output for all tools
-   Works in both Claude Desktop and Claude Code
-   `METHODS_SUPPORTED.md` in each repo is accurate and current

## Open Questions

1.  Should `colima start` expose the full flag surface (30+ flags) or use a simplified parameter set with an `--edit` escape hatch?
2.  Should Lima's `shell` tool support streaming/interactive output or only one-shot commands?
3.  Is there value in a shared Python package for common patterns (subprocess wrapper, JSON parsing, error handling)?