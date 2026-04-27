# Dr. Sigmund — Recent Principles (2025-2026 Practitioner Updates)

Extends `clinical-manual.md`. New design principles surfaced from named developers, frameworks, and recent practitioner writing not yet in the main manual. Loaded alongside the manual.

The most consequential update: **Cognition reversed their own "Don't Build Multi-Agents" stance** in 2025. Dr. Sigmund's diagnostic for multi-agent architecture must reflect the updated position.

---

## Identity & Persona (extends manual §1)

**Skills > prompts for procedural knowledge.**
*Source:* Anthropic, [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills); Barry Zhang & Mahesh Murag at AI Engineer Code Summit 2025.
*What they say:* "Claude is powerful, but real work requires procedural knowledge and organizational context." Skills package "instructions, scripts, and executable code" so capability survives across sessions.
*Apply:* When a behavior recurs across sessions, factor it out of the system prompt into a SKILL.md with metadata header. The prompt declares *who*; skills carry *how*. Cursor, Goose, Amp, OpenCode, Microsoft and OpenAI have all adopted the [agentskills.io](https://agentskills.io/home) format — portability is real now.

**Progressive disclosure beats kitchen-sink prompts.**
*Source:* [Agent Skills spec](https://agentskills.io/home); [Simon Willison's annotation](https://simonwillison.net/2025/Dec/19/agent-skills/).
*What they say:* "Like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix, skills let Claude load information only as needed." Three load tiers — metadata, body, referenced files.
*Apply:* Stop concatenating every rule at session start. Triage prompt material into "always-on" (identity), "loaded when relevant" (skill body), and "fetched on demand" (linked references). Token cost falls and rule decay drops with it.

---

## Memory (extends manual §2)

**KV-cache hit rate is the production metric most teams ignore.**
*Source:* Yichao 'Peak' Ji, [Context Engineering for AI Agents — Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus).
*What they say:* "KV-cache hit rate is the single most important metric for a production-stage AI agent." Stable prompt prefixes, append-only context, explicit cache breakpoints.
*Apply:* Audit prompts for any non-stable content near the top — timestamps, varying tool lists, randomized examples. Each invalidates cache and silently doubles cost while increasing latency.

**Mask, don't remove.**
*Source:* [Manus blog](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus).
*What they say:* When restricting tools, "mask the token logits during decoding to prevent (or enforce) the selection of certain actions" rather than mutating the tool list — mutation invalidates KV cache and confuses the model when it sees prior calls to now-missing tools.
*Apply:* Toolset visible to the model should remain stable across the session. Gating happens at the *call* layer, not the *catalog* layer.

**File system as ultimate context.**
*Source:* [Manus blog](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus).
*What they say:* "The file system as the ultimate context in Manus: unlimited in size, persistent by nature, and directly operable by the agent itself."
*Apply:* Filesystem reads/writes are a memory layer, not just I/O. Specify in the prompt which files are durable state vs. scratch — otherwise the agent rewrites them on whim.

**Keep the wrong stuff in.**
*Source:* [Manus blog](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus).
*What they say:* "Leave the wrong turns in the context." Removing failed actions removes the signal that lets the model "implicitly update its internal beliefs" and not repeat them.
*Apply:* Don't clean up the trace before showing it back to the model. Failed tool calls are training data within the session.

---

## Tools (extends manual §3)

**Type-safe by default; reflection-and-retry on schema mismatch.**
*Source:* [Pydantic AI](https://ai.pydantic.dev/); [Mastra](https://mastra.ai/) (Zod schemas).
*What they say:* Pydantic AI gives "that Rust 'if it compiles, it works' feel" — schemas auto-generate from type hints, "if the LLM's output doesn't match your schema, it automatically prompts the model to try again."
*Apply:* Tool-call failure should produce a structured error the agent can correct against — not silent garbage downstream. Validation is a tool, not an afterthought.

**Tool responses are prompts in disguise.**
*Source:* Jason Liu, [Context Engineering: Rapid Agent Prototyping](https://jxnl.co/writing/2025/09/04/context-engineering-rapid-agent-prototyping/).
*What they say:* Tools should return "STATUS, OUTPUT_FILE, METRICS, WARNINGS, and FACETS" — giving "peripheral vision about task completion." Errors should "guide next actions."
*Apply:* Audit tool return shapes. A bare value is a missed opportunity — wrap it with metadata that nudges the next decision.

---

## Context Engineering (extends manual §4)

**Recitation manipulates attention.**
*Source:* [Manus blog](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus).
*What they say:* The agent maintains and rewrites a checklist to "bias its own focus toward the task objective" — restating the goal pulls it into recent context where attention is strongest.
*Apply:* Long-running agents should periodically restate the active goal. Cheap, high-yield. Counters Rule Decay Under Load.

**Initializer + worker split for long-running work.**
*Source:* Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
*What they say:* "The very first agent session uses a specialized prompt that asks the model to set up the initial environment" — subsequent sessions inherit that scaffolding through git history and a progress file.
*Apply:* Two prompts beat one for any task that spans sessions. The initializer creates the artifacts the worker depends on.

---

## Decision-Making (extends manual §5)

**Test the idea before you build the harness.**
*Source:* Jason Liu, [Rapid Agent Prototyping](https://jxnl.co/writing/2025/09/04/context-engineering-rapid-agent-prototyping/).
*What they say:* "If it works once in this harness, the idea is viable. If it fails consistently, you know what's missing without building any infrastructure." Prototype with a CLI before you write a message bus.
*Apply:* When a patient describes elaborate scaffolding around an unproven concept, prescribe a one-shot CLI test first.

---

## Self-Improvement (extends manual §6)

**Programs, not prompts — let optimizers do the tuning.**
*Source:* [DSPy (Stanford)](https://dspy.ai/), [arXiv 2310.03714](https://arxiv.org/pdf/2310.03714).
*What they say:* DSPy compiles "AI programs into effective prompts and weights" automatically. Signatures separate *what* from *how*; "if you change your code or your metrics, you can simply re-compile."
*Apply:* For agents tuned by hand on a metric for >2 weeks, recommend declaring a signature and metric, then letting MIPROv2 search the prompt space.

**Eval harness before agent.**
*Source:* [Inspect](https://inspect.aisi.org.uk/) (UK AISI); Eugene Yan.
*What they say:* Inspect ships "over 200 pre-built evaluations" and runs "arbitrary external agents like Claude Code, Codex CLI, and Gemini CLI" against benchmarks like SWE-Bench, GAIA, Cybench.
*Apply:* No agent goes to production without an Inspect (or equivalent) harness scoring it on every change. "Vibes" is not a metric.

---

## Communication (extends manual §7)

**Slop has a slope; quality does not auto-decay with quantity.**
*Source:* swyx, [Scaling without Slop](https://www.latent.space/p/2026).
*What they say:* "The most important problem in media now is scaling without slop, period." The defeat is "cutting back" output; the win is "changing the slope of slop."
*Apply:* When patients ship LLM output without curation, prescribe a "saying no a lot" gate — a curation pass with a stated reject-rate target.

---

## Multi-Agent Orchestration (UPDATES manual §8)

**Single-threaded writes; distributed intelligence.** *(Important update — Cognition's stance evolved.)*
*Source:* Cognition, [Multi-Agents: What's Actually Working](https://cognition.ai/blog/multi-agents-working) (the evolution of "Don't Build Multi-Agents").
*What they say:* "Multi-agent systems work best today when writes stay single-threaded and the additional agents contribute intelligence rather than actions." Code-review subagents, smart-friend routing, manager-child delegation work; parallel writers don't.
*Apply:* The blanket "no multi-agents" guideline is now too coarse. Read-subagents (review, search, analysis) earn their context. Write-parallel swarms still don't. Update Dr. Sigmund's diagnostic accordingly.

**Decentralization for reliability.**
*Source:* [Google ADK](https://google.github.io/adk-docs/); [developers' guide to multi-agent patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/).
*What they say:* "Reliability comes from decentralization and specialization. Multi-Agent Systems allow you to build the AI equivalent of a microservices architecture by assigning specific roles."
*Apply:* When Cognition's caution and Anthropic's research-system both apply, the tiebreaker is *write isolation*. Microservices analogy holds: one writer per resource.

---

## Honest gaps (these came up dry)

- **Aman Sanger** has published essentially nothing himself in 2025-2026 beyond Lex Fridman appearances; Cursor's design philosophy is better extracted from product behavior + the Latent Space episode than from Sanger's writing.
- **Andriy Burkov** released *The Hundred-Page Language Models Book* (Jan 2025) but no agent-specific writing — foundations, not agent design.
- **Dwarkesh Patel's** 2025 agent coverage is largely the Karpathy interview ("AGI is a decade away," "RL is terrible"); useful as macro context, doesn't extend the principle base.

---

## When to load this file

Always, alongside `clinical-manual.md`. The principles here update the manual's themes; treating them as "optional" risks Dr. Sigmund prescribing yesterday's stance on multi-agent or missing the cache-hit-rate insight.
