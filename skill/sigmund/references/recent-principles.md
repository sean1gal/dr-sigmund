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

## Anthropic — the three core principles, named explicitly

*Source:* Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) (Schluntz & Zhang, Dec 2024). Verbatim:

1. **Simplicity** — *"Maintain simplicity in your agent's design."*
2. **Transparency** — *"Prioritize transparency by explicitly showing the agent's planning steps."*
3. **ACI quality (agent-computer interface)** — *"Carefully craft your agent-computer interface (ACI) through thorough tool documentation and testing."*

**Apply (Dr. Sigmund's diagnostic axes):** Every session should grade the patient on these three. *"Is this the lowest-complexity solution that works?"* *"Are the agent's planning steps visible and inspectable?"* *"Could a human reading the tool descriptions predict how the agent will use them?"* These are the three criteria Phase 3 (Evaluator-Optimizer loop) scores against.

## Anthropic — the augmented LLM is the atomic building block

*Source:* same.

*What they say:* *"The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. Our current models can actively use these capabilities — generating their own search queries, selecting appropriate tools, and determining what information to retain."*

*Apply:* Every agent diagnosis starts here. *Does this patient have appropriate retrieval, tools, and memory?* Missing one is a named deficit. The patient may be running on a sophisticated framework but still missing one of the three atoms — diagnose the atom, not the framework.

## Anthropic — the five workflow patterns (clarified)

*Source:* same.

The five named patterns Dr. Sigmund prescribes:

| Pattern | When to use | Distinction |
|---|---|---|
| **Prompt Chaining** | "Task can be easily and cleanly decomposed into fixed subtasks. Trade off latency for higher accuracy." | Sequential; each step's output is next step's input. |
| **Routing** | "Distinct categories better handled separately, and where classification can be handled accurately." | Classify → dispatch to specialized followup. Includes model routing (small for easy, large for hard). |
| **Parallelization — Sectioning** | "Divided subtasks can be parallelized for speed." | Independent subtasks run simultaneously; results aggregated. |
| **Parallelization — Voting** | "Multiple perspectives or attempts are needed for higher confidence results." | Same task multiple times for diverse outputs. *Distinct from sectioning.* |
| **Orchestrator-Workers** | "Can't predict the subtasks needed." | *Critical contrast vs parallelization:* "subtasks aren't pre-defined, but determined by the orchestrator." |
| **Evaluator-Optimizer** | "Clear evaluation criteria, and when iterative refinement provides measurable value." | Generate → evaluate → refine in a loop. **Dr. Sigmund's Phase 3 uses this pattern on himself.** |

*Apply:* When a patient describes a multi-step workflow as "agent" and the steps are predictable, prescribe one of the first five patterns instead. Save the agent label (and the agent costs) for genuinely open-ended problems.

## Anthropic — Poka-yoke for tool design

*Source:* same, Appendix 2 — verbatim: *"Apply Poka-yoke design — change the arguments so that it is harder to make mistakes."*

*Apply:* When a patient's tool design enables silent misuse (no error on wrong-but-plausible arguments), prescribe Poka-yoke redesign. Concrete: change `delete(target_id)` to `delete(target_id, confirmation_token=required_string)` so the model has to opt into destructiveness. Tool design that makes mistakes hard to make is itself a clinical intervention.

## Anthropic — ground truth from the environment at each step

*Source:* same — verbatim: *"During execution, it's crucial for the agents to gain 'ground truth' from the environment at each step."*

*Apply:* Open-loop agents — those that commit to a multi-step plan without re-checking environmental state — are a named pathology (see `wild-pathologies.md`). The diagnostic question: *after each tool call, does the agent re-evaluate whether the next planned step still makes sense?* If no, prescribe an explicit "what changed?" step in the loop.

## The "Three Powers" plain-language layer (for patient-facing language)

*Source:* AI Agents Simplified, [Simplified Guide to Build Effective AI Agents](https://aiagentssimplified.substack.com/p/simplified-guide-to-build-effective) (April 2025). Verbatim: *"An effective AI agent has three key powers: Autonomy, Memory, Tool Use."*

*Apply:* When the patient's owner is non-technical, use *Autonomy / Memory / Tool Use* instead of *augmented LLM*. Same concept, layperson-accessible. The Substack's tighter framing is worth stealing for patient-facing copy.

## The Substack — outcome-based eval framing

*Source:* same, verbatim: *"Don't just measure 'Did it answer?' Measure 'Did it accomplish the goal?'"*

*Apply:* Sharpens Hamel's eval-tier hierarchy. When the patient has a passing eval suite but real failures, the eval is measuring *did it answer* rather than *did it accomplish the goal* — that's Eval Theater dressed up. Force the eval criterion to be outcome-shaped.

## Spring AI — type-safe structured output for evaluators

*Source:* Spring AI, [Effective Agents](https://docs.spring.io/spring-ai/reference/api/effective-agents.html). Verbatim: *"Type-safe structured output: `EvaluationResponse response = chatClient.prompt(prompt).call().entity(EvaluationResponse.class);`"*

*Apply:* When prescribing the Evaluator-Optimizer pattern (Phase 3 self-critique), the evaluator's output should be *structured*, not free-form text. A typed `Critique{passed: bool, criterion_failed: str, refinement_hint: str}` produces actionable feedback in a way `"This response could be better in some ways..."` does not.

## HN practitioners — three things the Anthropic post under-emphasizes

*Source:* HN [44301809](https://news.ycombinator.com/item?id=44301809) thread.

1. **Vendor-swap is rarely the bottleneck.** *"Having built several systems serving massive user bases with LLMs. I think the ability to swap out APIs just isn't the bottleneck.. like ever."* (XenophileJKO). Prescribing a heavy framework purely for vendor portability is over-engineering.
2. **Cost reality check.** A real-time conversation can burn $60 in tokens (koakuma-chan); a basic n8n workflow runs $3/3min (laurentiurad). When prescribing autonomous loops, *always* prescribe a cost-budget gate alongside.
3. **Operational complexity doesn't disappear.** *"Nothing works automagically. You still have to build in all the operational characteristics that you would for any traditional system."* (daxfohl). Add a *"what's the on-call story?"* question to any production-prescription session.

## Honest gaps (these came up dry)

- **Aman Sanger** has published essentially nothing himself in 2025-2026 beyond Lex Fridman appearances; Cursor's design philosophy is better extracted from product behavior + the Latent Space episode than from Sanger's writing.
- **Andriy Burkov** released *The Hundred-Page Language Models Book* (Jan 2025) but no agent-specific writing — foundations, not agent design.
- **Dwarkesh Patel's** 2025 agent coverage is largely the Karpathy interview ("AGI is a decade away," "RL is terrible"); useful as macro context, doesn't extend the principle base.

---

## When to load this file

Always, alongside `clinical-manual.md`. The principles here update the manual's themes; treating them as "optional" risks Dr. Sigmund prescribing yesterday's stance on multi-agent or missing the cache-hit-rate insight.
