# Dr. Sigmund — The Pharmacy

Three tiers of prescription. Dr. Sigmund picks per case, in order of preference: existing well-loved tools first, trusted-creator referrals second, proprietary remedies last (only where real gaps exist).

The order matters. Recommending an existing great tool before shipping our own is *both* more honest and more credible — and it builds goodwill in the community we'd otherwise be competing with.

---

## Tier 1 — Recommend existing well-loved MCPs/tools

These are the workhorses. Well-built, well-maintained, broadly trusted. Dr. Sigmund prescribes them by name.

### Memory & state

| Symptom | Tool | Notes |
|---|---|---|
| Cross-session forgetting (lightweight) | **[Official Memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)** (`@modelcontextprotocol/server-memory`) | Local knowledge-graph: entities, relations, observations. Quick wins. |
| Cross-IDE memory needs | **[Mem0 / OpenMemory MCP](https://mem0.ai/openmemory)** | Vector-first, works across Cursor/Claude/VS Code |
| Temporal facts ("when did X change") | **[Zep / Graphiti MCP](https://atlan.com/know/zep-vs-mem0/)** | Temporal knowledge graph; benchmark leader (~14pt over Mem0 on factuality) |
| Want runtime *and* memory together | **[Letta (MemGPT)](https://github.com/letta-ai/letta)** | Three-tier memory + full agent runtime |
| Multi-agent shared memory | **[memento-mcp](https://glama.ai/mcp/servers/categories/knowledge-and-memory)** | Neo4j-backed. Heavy infra — recommend only when justified. |

### Codebase navigation

| Symptom | Tool | Notes |
|---|---|---|
| Burning tokens on filesystem reads | **[Serena](https://github.com/oraios/serena)** | LSP-backed symbol-level retrieve/edit. **Highest-ROI MCP in the catalog.** Default prescription for any coding agent. Anthropic-listed plugin. |
| Git operations | **[GitHub MCP](https://github.com/github/github-mcp-server)** (PRs/issues/reviews) + **[git-mcp-server](https://github.com/cyanheads/git-mcp-server)** (full workflow) | Table stakes. |

### Sequential thinking / planning

| Symptom | Tool | Notes |
|---|---|---|
| Jumps to action without planning | **[Sequential Thinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)** (official) | Default prescription. Cheap, well-supported. |
| Too many tools, picks badly | **[spences10/sequentialthinking-tools](https://mcpservers.org/servers/spences10/mcp-sequentialthinking-tools)** | Confidence-scored tool recommendations per step |
| Needs structured *thinking style* | **[Thinking Patterns MCP](https://lobehub.com/mcp/emmahyde-thinking-patterns)** | Multiple frameworks: decomposition, decision-making, hypothesis testing |

### Verification (test/lint/type)

| Symptom | Tool | Notes |
|---|---|---|
| JS/TS agent | **[ESLint MCP](https://eslint.org/docs/latest/use/mcp)** (official) | Direct linter access |
| Writes code without running it | **[mcp-test-runner](https://www.pulsemcp.com/servers/privsim-test-runner)** | Unified across multiple test frameworks |
| Self-improvement loops | **[lastmile-ai/mcp-eval](https://github.com/lastmile-ai/mcp-eval)** + **[Atla MCP](https://atla-ai.com/post/atla-mcp-server)** | LLM-judge scoring |

### Cost & token discipline

| Symptom | Tool | Notes |
|---|---|---|
| Cost-anxious, want pre-call estimate | **[Token Oracle](https://mcpmarket.com/server/token-oracle)** | Estimates cost before request |
| Runaway-spend prevention | **[Agent Budget Guard](https://earezki.com/ai-news/2026-03-02-i-built-an-mcp-server-so-my-ai-agent-can-track-its-own-spending/)** | Post-call tracking + circuit-breaker |

### Tool sprawl / governance

| Symptom | Tool | Notes |
|---|---|---|
| 10+ MCPs installed | **[MCP Gateway Registry](https://github.com/agentic-community/mcp-gateway-registry)** | Federate behind one entry point |
| Enterprise needs | **[Cloudflare](https://blog.cloudflare.com/enterprise-mcp/)** / **[Kong](https://konghq.com/blog/learning-center/what-is-a-mcp-gateway)** / **[Arcade](https://www.arcade.dev/blog/mcp-gateway-pattern/)** gateways | Audit + access control |

**Where this tier is adequate** (we should *recommend, not build*): codebase navigation (Serena is exceptional), git operations, ESLint, basic memory KG, sequential thinking, MCP gateway federation. Building competing products here is wasteful.

---

## Tier 2 — Direct to trusted-creator skills, patterns, and required reading

When the right remedy is something built or written by someone the patient should *trust by name*. Dr. Sigmund leverages reputation. This tier breaks into three sub-tiers:

### 2a. Installable artifacts by trusted creators

| Symptom | Trusted source | Artifact | Why direct here |
|---|---|---|---|
| Code-touching agent without good context strategy | **Aider** ([aider.chat](https://aider.chat/)) by Paul Gauthier | The Aider repo map + git checkpointing pattern | The gold standard for codebase compression — even if not directly installable in their setup, the pattern is worth borrowing |
| Heavy memory needs beyond what MCPs handle | **Letta** ([letta.com](https://www.letta.com/)) by the MemGPT team | The Letta runtime | When the patient really needs OS-style virtual memory paging, recommend the system that invented the pattern |
| Multi-language LSP-style code intelligence | **Serena** ([oraios/serena](https://github.com/oraios/serena)) | Direct install | (Also in Tier 1 — top-tier, name-recognized) |
| Skill ecosystem on Claude | **Anthropic** ([claude.com/plugins](https://claude.com/plugins)) | Official Anthropic plugins + the [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) repo | First-party authority |
| Security audit on agent's own MCPs | **Trail of Bits** skill catalog ([github.com/trailofbits/skills](https://github.com/trailofbits/skills)) | Their security/audit skills | Reputation for rigor |

### 2b. Required reading by trusted authors

When the right intervention isn't a tool — it's the patient (or the patient's owner) reading the right thing. Dr. Sigmund prescribes the article like a book recommendation from a thoughtful doctor.

| Symptom | Author | Required reading | When to prescribe |
|---|---|---|---|
| Wants to ship multi-agent before the work justifies it | **Walden Yan / Cognition** | [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) | Read before any multi-agent build |
| Has no eval discipline | **Hamel Husain** | [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) | Read before next sprint |
| Confused about prompt vs. context | **Andrej Karpathy** | [Context engineering tweet thread](https://x.com/karpathy/status/1937902205765607626) + [LLM OS framing](https://huggingface.co/blog/shivance/illustrated-llm-os) | Read before refactoring system prompt |
| Building agents from scratch | **Anthropic** (Schluntz & Zhang) | [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) + [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Foundational — required before any architectural decision |
| Tool-using agent | **Anthropic** | [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Read before designing or auditing a tool surface |
| Agent has any external comms or tool access | **Simon Willison** | [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | Mandatory security reading |
| Self-reflection loops not working | **Shunyu Yao** | [ReAct paper](https://arxiv.org/abs/2210.03629) + [Latent Space interview](https://www.latent.space/p/shunyu) | Reflection without an evaluator is theatre |
| Long-running agent | **Anthropic** | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | The premature-completion fix |
| Agent has no character | **Anthropic** | [Claude's Constitution](https://www.anthropic.com/news/claudes-constitution) | The values-hierarchy template |

### 2c. Templates by trusted communities

| Symptom | Source | Artifact |
|---|---|---|
| Empty/malformed `.cursorrules` | **[Cursor Directory](https://cursor.directory/)** | Curated .cursorrules templates by language/framework |
| Empty `AGENTS.md` | **[agents.md](https://agents.md/)** + [GitHub's 2,500-repo analysis](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) | Six-section template (commands, testing, project structure, code style, git workflow, boundaries) |
| Building a skill | **[agentskills.io](https://agentskills.io)** open standard | SKILL.md schema (cross-vendor: Claude, Hermes) |
| Building an MCP | **[modelcontextprotocol.io](https://modelcontextprotocol.io/)** | Official spec + SDK |

---

## Tier 3 — Dr. Sigmund proprietary remedies (the gaps)

For each ailment where Tier 1 is missing/bloated/wrong-framed and no trusted-creator artifact in Tier 2 fits, we ship our own. These are the gaps.

### The pharmacy roster (proposals)

#### 1. `sigmund-rx` (skill) ★ build first
**One line.** Reads a session transcript, generates a markdown prescription pad with concrete MCP installs, rules-file edits, and behavior changes.
**Treats.** All diagnoses — the prescription delivery mechanism itself.
**Gap.** The core Dr. Sigmund product. Nothing in the MCP world produces a clinical prescription artifact. **This is the brand surface — without it, Dr. Sigmund has no delivery mechanism.**
**Form.** Skill — runs locally on transcripts.

#### 2. `sigmund-journal` (MCP + skill) ★ build third or fourth
**One line.** Auto-writes a session journal at end-of-session with decisions, dead-ends, and "open issues for next time" — designed to be *read by the next session's agent*.
**Treats.** Session Amnesia; the "groundhog day" where the agent re-discovers the same problems.
**Gap.** chat-history-recorder-mcp dumps raw history. mcp-memory-service is general-purpose KG storage. Neither writes the *next agent's briefing* — a different artifact, optimized for a cold-start agent re-entering the project.

#### 3. `sigmund-token-meter` (MCP + skill) ★ build third
**One line.** Live per-turn token spend with diagnostic alerts ("you've spent 40K tokens re-reading the same file 7 times").
**Treats.** Token Hemorrhage; Re-Read Compulsion.
**Gap.** Token Oracle estimates *forward*, Agent Budget Guard caps *afterward*. Neither does the *diagnostic* piece — naming the *behavioral pattern* causing the spend.

#### 4. `sigmund-loop-breaker` (MCP) ★ build fourth
**One line.** Detects and interrupts repetitive tool-call loops in real time, surfacing a structured "you are stuck" message back to the agent.
**Treats.** Iterative Compulsion Disorder; tool-call perseveration.
**Gap.** The closest things are framework-level loop guards filed as bug reports (Claude Code #15945, Gemini CLI #3928, Cline #9673). Pattern is well-known but unmonetized as a service.

#### 5. `sigmund-symptom-scanner` (skill) ★ build second
**One line.** Static-analysis scan of `AGENTS.md`/`.cursorrules`/system prompt for known anti-patterns ("rule 14 contradicts rule 27"; "you've defined 'be concise' three times"; "no rollback policy specified").
**Treats.** Pre-existing conditions encoded into the agent's identity file.
**Gap.** Nobody lints rules files. Cheap to build, ships fast, generates organic content (each finding is a tweet).

#### 6. `sigmund-anchor` (MCP)
Persistent identity/persona block injected at every turn — the agent's "self" that survives compaction. Treats Identity Drift.

#### 7. `sigmund-toolset-audit` (skill)
Scans installed MCPs and reports unused, redundant, conflicting, or token-bloated tool surfaces. Treats Tool Hoarding Disorder.

#### 8. `sigmund-checkpoint` (MCP)
Lightweight git-shadow snapshot before destructive tool calls; one-command rollback. Portable version of Gemini CLI's checkpointing.

#### 9. `sigmund-compaction-coach` (MCP)
Custom compaction prompt that preserves diagnostic-relevant context (open hypotheses, failed paths) instead of generic summarization. Treats Lossy-Compaction Syndrome.

#### 10. `sigmund-mirror` (skill)
Reflective skill that asks the agent five clinically-flavored questions ("what did you assume that turned out false today?") and writes answers to the project journal.

#### 11. `sigmund-context-budget` (MCP)
Budget MCP the agent calls before reading a file. Behavioral commitment device. Treats Context Gluttony.

#### 12. `sigmund-second-opinion` (MCP)
Single tool call that hands the current plan to a *different model* for one-shot critique. Branded as a referral, not a router.

#### 13. `sigmund-discharge-summary` (skill)
End-of-session artifact for the *human* user. Medical-record-quality discharge document. Treats user-side trust collapse from opaque sessions.

#### 14. `sigmund-rules-template-pack` (skill)
Curated `AGENTS.md` templates by patient archetype, generated *from* session diagnosis. Closes the diagnostic loop.

#### 15. `sigmund-followup` (skill / cron)
Runs Dr. Sigmund again on a delta of new transcripts and produces a longitudinal "you've been doing better at X but Y has gotten worse" report. Retention engine.

---

## Sequencing — first five products to build

Ranked by **frequency of underlying ailment × build feasibility × differentiation**:

1. **`sigmund-rx`** — without it, Dr. Sigmund has no delivery mechanism. Frequency 100%, very high feasibility, *is* the brand.
2. **`sigmund-symptom-scanner`** — pairs naturally with launch. Day-one users see real findings on real files. Generates organic shareable content per finding.
3. **`sigmund-token-meter`** — cost is universal pain. The "Dr. Sigmund saved me money" stories.
4. **`sigmund-loop-breaker`** — acute, catastrophic when it happens, no consumer-grade fix exists. Strong word-of-mouth.
5. **`sigmund-journal`** — retention engine. Converts single-session diagnoses into ongoing care.

**Explicitly de-prioritized for v1:** `sigmund-anchor`, `sigmund-compaction-coach`, `sigmund-second-opinion`, `sigmund-checkpoint`. Excellent ideas, but each requires deeper integration with one model/vendor's quirks and will benefit from the data the first five products generate.

---

## Recent additions (2025-2026)

### Tier 1 — More existing tools to recommend

**Eval & measurement:**
- **[Inspect (UK AISI)](https://inspect.aisi.org.uk/)** — open-source eval framework, 200+ pre-built evals, runs Claude Code/Codex/Gemini CLI as agents, sandboxes via Docker/K8s/Modal. *Prescribe when:* anyone says "we test it manually." Gold standard. The most-credible neutral evaluator.
- **[OpenAI Evals](https://github.com/openai/evals)** — registry-driven framework. *Prescribe when:* patient wants a non-Anthropic-aligned eval substrate.

**Agent frameworks (newer):**
- **[DSPy](https://dspy.ai/)** — Stanford NLP. Programs not prompts; signatures + modules + optimizers (MIPROv2). *Prescribe when:* hand-tuning prompts against a metric for >2 weeks. **Treats Stochastic Graduate Descent.**
- **[Pydantic AI](https://ai.pydantic.dev/)** — type-safe Python agent framework. Validation + retry built in. *Prescribe when:* Python production, bitten by malformed tool args.
- **[Mastra](https://mastra.ai/)** — TS equivalent. Zod schemas, model router, dev studio at `localhost:4111`. *Prescribe when:* TS shop currently rolling their own loop.
- **[smolagents](https://github.com/huggingface/smolagents)** — Hugging Face. Code-as-action: agents emit Python, not JSON tool calls. ~30% fewer steps on complex benchmarks. *Prescribe when:* tool surface is composable Python and JSON ceremony dominates turns.
- **[Magentic-One](https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/)** — Microsoft Research. *Prescribe sparingly:* heavyweight; cite as the *reference architecture* for write-isolated subagent design.
- **[Google ADK](https://google.github.io/adk-docs/)** — code-first, event-driven, multi-agent. *Prescribe when:* GCP/Gemini-bound patient.
- **[AG2](https://github.com/ag2ai/ag2)** (formerly AutoGen) — streaming/event-driven core, dependency injection, typed tools. *Prescribe when:* AutoGen-shop debating migration.

**Memory (specialized — see [forensic-intake.md](forensic-intake.md) §2 for the decision tree):**
- **[Letta v1](https://www.letta.com/blog/letta-v1-agent)** — OS-style three-tier memory with native reasoning. Use v1, not legacy MemGPT-style.
- **[Mem0g](https://mem0.ai/)** + **[OpenMemory MCP](https://mem0.ai/openmemory)** — vector memory with graph contradiction detection + local-privacy MCP.
- **[Zep / Graphiti](https://github.com/getzep/graphiti)** — temporal knowledge graph with bitemporal edges. For mutating facts + audit trail.
- **[Anthropic Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)** (`memory_20250818`, beta) — client-side filesystem tool for Claude.
- **[Anthropic Compaction API](https://platform.claude.com/docs/en/build-with-claude/compaction)** (Jan 2026) — server-side automatic summarization. Pair with Memory Tool.

### Tier 2b — More required reading by trusted authors

| Symptom | Author | Required reading |
|---|---|---|
| Cache costs ballooning, no clear cause | **Yichao 'Peak' Ji (Manus)** | [Context Engineering — Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) — single most-cited 2025 source |
| Considering multi-agent architecture | **Walden Yan / Cognition** | [Multi-Agents: What's Actually Working](https://cognition.ai/blog/multi-agents-working) — the *evolved* 2025 stance, alongside the original "Don't Build Multi-Agents" |
| Tool-design quality is the bottleneck | **Jason Liu** | [Rapid Agent Prototyping](https://jxnl.co/writing/2025/09/04/context-engineering-rapid-agent-prototyping/) — STATUS/OUTPUT/METRICS schema |
| Eval Theater suspected | **Hugo Bowne-Anderson** | [Vanishing Gradients podcast](https://hugobowne.substack.com/podcast), Ep 50 with Hamel Husain |
| Practitioner state-of-the-art context | **swyx + Alessio Fanelli** | [Latent Space — 2026 thesis](https://www.latent.space/p/2026) — required for Slop Scaling |
| Vibe-Coding Rot suspected | **Jeremy Howard** | [Build to Last](https://www.fast.ai/posts/2025-10-30-build-to-last.html) |

### Tier 2a — Karpathy minimalism (read-and-build skills)

The unifying principle: **the artifact must be small enough to read in one sitting *and* real enough to actually work.** Reject toy demos; reject framework-wrapped tutorials. When a patient demonstrates surface-level understanding without underlying mechanism, prescribe the corresponding Karpathy repo as required reading *and* reproduction. Reading Karpathy without reproducing is itself a Documentation-Substitution Reflex.

| Symptom | Repo | Prescription |
|---|---|---|
| Treats backprop as a black box | **[micrograd](https://github.com/karpathy/micrograd)** | ~150 lines of pure Python = the entirety of autograd. Read, then reproduce by hand. |
| Treats transformers as a black box | **[nanoGPT](https://github.com/karpathy/nanoGPT)** (57.2k stars) | Train an actual GPT in code you can hold in your head. Production-capable despite minimalism. |
| Framework dependency keeps abstracting away the math | **[llm.c](https://github.com/karpathy/llm.c)** (29.7k) | LLM training in raw C/CUDA. Strip Python and PyTorch entirely; what's left is the math. |
| Can't reason about inference performance | **[llama2.c](https://github.com/karpathy/llama2.c)** (19.5k) | Single-file dependency-free Llama 2 inference in pure C. |
| Doesn't understand the full ChatGPT pipeline | **[nanochat](https://github.com/karpathy/nanochat)** (52.6k) | End-to-end pretrain → SFT → RLHF → serve, reproducible for $100. Full-stack literacy dose. |
| About to train a model and isn't sure how | **[A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/)** | Step-by-step: become one with the data → end-to-end skeleton with dumb baselines → overfit → regularize → tune. Required reading. |

These are also a stylistic prescription. *Prescribe the Karpathy reading style itself* — when a patient's identity files are bloated, point them at how Karpathy writes READMEs (typically <50 lines, install + use + done). Style transfer matters.

### Tier 2c — More trusted-community templates

- **[agentskills.io](https://agentskills.io)** — the open standard adopted by Anthropic, Microsoft, OpenAI, Cursor, Goose, Amp, OpenCode for portable skills.

### Skip / don't recommend

- **Cursor native Memories** — feature was pulled in v2.1.x. Recommend Cursor Rules + Memory Bank pattern files instead.
- **OpenAI Swarm** — superseded by OpenAI Agents SDK; cite the handoff *concept*, not the framework.
- **Vercel AI SDK 6** — fine for Next.js apps but doesn't extend Sigmund's vocabulary.
- **MMLU, BIG-bench** — saturated for frontier models; legacy comparison only.

---

## How Dr. Sigmund chooses tier per prescription

In a discharge summary, prescriptions should follow this default order:

1. **Try Tier 2b first.** If a Hamel/Karpathy/Anthropic post would solve the conceptual root cause, start there. Reading is cheaper than installing.
2. **Then Tier 1.** Recommend the well-loved existing tool by name. Link it. Tell the patient why it's the right fit.
3. **Then Tier 2a/2c.** Direct to specific trusted-creator templates or installable artifacts when the gap is template-shaped or framework-shaped.
4. **Then Tier 3.** Prescribe our proprietary remedy *only* when no upstream solution fits cleanly. Always explain why we ship our own.

This order is the reputational moat. A pharmacy that recommends *other people's* great work first is more trusted than one that always sells its own brand.
