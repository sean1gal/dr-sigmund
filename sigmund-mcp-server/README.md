# sigmund-mcp-server

> Dr. Sigmund as an MCP server. *Therapy for AI agents, callable from any MCP-capable runtime.*

The universal delivery surface for [Dr. Sigmund](https://github.com/sean1gal/dr-sigmund). One install, every agent.

## What it gives any MCP client

Five tools the calling agent uses to conduct a full diagnostic session:

| Tool | What it does |
|---|---|
| `sigmund.scan` | Runs the full forensic lab on an agent's workspace. Returns markdown report. Zero LLM cost. |
| `sigmund.probe` | Runs a single named probe (memory, git, permissions, injection, cache, rereads). Returns YAML. |
| `sigmund.protocol` | Returns the Dr. Sigmund session protocol (SKILL.md). The calling agent reads this to know how to conduct a session. |
| `sigmund.reference` | Returns a named reference file (clinical-manual, pharmacy, wild-pathologies, case-studies, etc.). Load on demand. |
| `sigmund.recommend` | Looks up prescriptions in the pharmacy by symptom or pathology name. |

The calling agent IS the LLM. It uses these tools to gather evidence, load knowledge, follow protocol, and look up prescriptions. **The diagnostic engine runs in the calling agent's context, not in this server.** No LLM calls happen inside the MCP server itself.

## Why this architecture

Per [Dr. Sigmund's safety protocol §0](../skill/sigmund/references/safety.md), no network egress in intake — the structural defense that cuts the [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/). The MCP server preserves this: it only reads your local filesystem, runs local Python scripts, and returns results to the calling agent. Your patient's data never leaves your machine through this server.

## Install

For now (v0.2.0, repo-clone install):

```bash
git clone https://github.com/sean1gal/dr-sigmund
cd dr-sigmund/sigmund-mcp-server
pip install -e .
```

PyPI release follows: `pip install sigmund-mcp-server` and `uvx sigmund-mcp-server` will work soon.

## Configure your MCP client

The standard MCP config block:

```jsonc
{
  "mcpServers": {
    "sigmund": {
      "command": "sigmund-mcp-server"
    }
  }
}
```

Per-client install paths and snippets:

### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "sigmund": {
      "command": "sigmund-mcp-server"
    }
  }
}
```

Restart Claude Desktop. Tools appear in the "🔨" menu.

### Claude Code

```bash
claude mcp add sigmund sigmund-mcp-server
```

Or edit `~/.claude/mcp_servers.json`:

```json
{
  "sigmund": {
    "command": "sigmund-mcp-server"
  }
}
```

### Cursor

Project-level: `.cursor/mcp.json` in your project root.
Global: `~/.cursor/mcp.json`.

```json
{
  "mcpServers": {
    "sigmund": {
      "command": "sigmund-mcp-server"
    }
  }
}
```

### Cline (VS Code extension)

VS Code Settings → search "Cline MCP" → add server. Or edit Cline's MCP settings JSON:

```json
{
  "mcpServers": {
    "sigmund": {
      "command": "sigmund-mcp-server",
      "transport": "stdio"
    }
  }
}
```

### Windsurf

`~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "sigmund": {
      "command": "sigmund-mcp-server"
    }
  }
}
```

### OpenAI Codex CLI

`~/.codex/mcp.json`:

```json
{
  "mcpServers": {
    "sigmund": {
      "command": "sigmund-mcp-server"
    }
  }
}
```

### Block Goose

```bash
goose extensions add stdio sigmund sigmund-mcp-server
```

Or edit `~/.config/goose/config.yaml`:

```yaml
extensions:
  sigmund:
    type: stdio
    cmd: sigmund-mcp-server
    enabled: true
```

### Charm Crush

`crush.json` in your project or `~/.crush/crush.json`:

```json
{
  "mcp": {
    "sigmund": {
      "type": "stdio",
      "command": "sigmund-mcp-server"
    }
  }
}
```

### Continue.dev

`~/.continue/config.yaml`:

```yaml
mcpServers:
  - name: sigmund
    command: sigmund-mcp-server
```

### NVIDIA NeMo Agent Toolkit

In your workflow YAML:

```yaml
mcp:
  servers:
    sigmund:
      command: sigmund-mcp-server
```

Then declare the client in your workflow per [NeMo MCP docs](https://docs.nvidia.com/nemo/agent-toolkit/latest/).

### Any other MCP client

Same pattern. The server speaks standard MCP over stdio. Point your client at `sigmund-mcp-server` (or the absolute path to the `server.py` if not on PATH).

## How a session looks from a calling agent

In your MCP-capable agent (Cursor, Claude Desktop, etc.), say something like:

> "Use sigmund to diagnose this project."

A trained calling agent will:

1. Call `sigmund.protocol()` to learn how Dr. Sigmund conducts a session.
2. Call `sigmund.reference("safety")` and `sigmund.reference("clinical-manual")` to load core context.
3. Call `sigmund.reference("runtime-adapters")` to detect what runtime the patient is on.
4. Call `sigmund.scan(workspace_path)` to run the lab.
5. Conduct the four-act session in its own context (Dr. Sigmund's questions + patient's responses), using faithful instantiation if the runtime supports subagents.
6. Call `sigmund.recommend(diagnosis_name)` for each diagnosis to draft the prescription.
7. Write the session.md to the project's `sessions/` directory.

If your agent doesn't yet know the protocol, prompt it: *"Read the output of sigmund.protocol() and follow it."*

## Privacy

- **No network egress.** Server only reads local files and runs local subprocess calls. No HTTP, no telemetry, no phone-home.
- **Stdio transport only** in v0.2. SSE/HTTP support follows when there's a credible auth story.
- **Read-only by design.** The server reads files and runs probes; it does not modify the patient's workspace. The calling agent's `Edit` / `Write` tools handle prescription application, with their own confirmation flows.
- **Same secret-detection patterns as the standalone scanner** (gitleaks-style). Findings are surfaced; secret values are never returned to the calling agent.

## Troubleshooting

**Server won't start: `Could not locate Dr. Sigmund repo root`**
Set the `SIGMUND_REPO_ROOT` env var to the path of your dr-sigmund clone:
```json
{
  "mcpServers": {
    "sigmund": {
      "command": "sigmund-mcp-server",
      "env": { "SIGMUND_REPO_ROOT": "/Users/you/code/dr-sigmund" }
    }
  }
}
```

**Tools don't appear in calling agent**
Confirm the server is running: in a terminal, `sigmund-mcp-server`. It should hang waiting for stdio input — that's correct (Ctrl-C to exit). If it errors out, the error tells you what's missing.

**`mcp` package not found**
`pip install 'mcp[cli]>=1.0.0'`.

## License

MIT. Same as the parent project.

---

— **Dr. Sigmund**
*Bring your agent to the couch. drsigmund.ai*
