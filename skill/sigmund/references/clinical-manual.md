# Dr. Sigmund — Clinical Reference Manual

This is the authoritative knowledge base loaded by Dr. Sigmund at session time. Every principle is sourced. Direct quotes are preserved verbatim where the original phrasing is sharp. Citations exist so the therapist can ground recommendations in the agent's session ("As Karpathy notes…"), not improvise from training data.

Organized in eight themes. Each principle includes: the rule, the source(s), what the source actually says, and the actionable form for a system prompt or agent design.

---

## 1. Identity & Persona

**Identity comes from an ordered values hierarchy, not a persona.**
*Source:* Anthropic, [Claude's Constitution](https://www.anthropic.com/news/claudes-constitution).
*What they say:* Claude is given an explicit priority order — "broadly safe first, broadly ethical second, following Anthropic's guidelines third, and otherwise being genuinely helpful to operators and users."
*Apply:* Declare a small, ordered list of values that resolve conflicts when goals collide. Personality flows from values; values do not flow from personality.

**Honesty above warmth; compassion does not require flattery.**
*Source:* Anthropic, [Claude's Constitution](https://www.anthropic.com/news/claudes-constitution).
*What they say:* Hold "standards of honesty that are substantially higher than those in many standard visions of human ethics," while balancing honesty with compassion.
*Apply:* Encode "honest > agreeable" explicitly, paired with a clause about how to deliver hard truths kindly. Without it, models drift into people-pleasing.

**Right-altitude prompting: neither brittle scripts nor vague vibes.**
*Source:* Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
*What they say:* A good system prompt is "specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics" — avoid "brittle if-else hardcoded prompts" and avoid vague guidance that falsely assumes shared context.
*Apply:* Write principles, not procedures. If you find yourself enumerating cases, extract the underlying rule the cases are all instances of.

**Split persona from operating instructions.**
*Source:* OpenClaw workspace convention, [Stack Junkie's guide](https://www.stack-junkie.com/blog/openclaw-system-prompt-design-guide), [Capodieci's writeup](https://capodieci.medium.com/ai-agents-003-openclaw-workspace-files-explained-soul-md-agents-md-heartbeat-md-and-more-5bdfbee4827a).
*What they say:* "AGENTS.md tells the agent what to do. SOUL.md tells the agent who to be." OpenClaw injects a fixed-order stack at session start: SOUL → IDENTITY → USER → AGENTS → MEMORY → TOOLS → HEARTBEAT.
*Apply:* A stable agent prompt has at least two distinct sections — persona/values/tone, and operating rules/scope/tools — never blended into a single wall of text.

**A role definition needs four fields, not one.**
*Source:* CrewAI Agent spec, [CrewAI docs](https://docs.crewai.com/), [DigitalOcean's CrewAI guide](https://www.digitalocean.com/community/tutorials/crewai-crash-course-role-based-agent-orchestration).
*What they say:* Every Agent declares `role`, `goal`, `backstory`, `tools`. Each shapes a different aspect of behavior; missing any produces drift.
*Apply:* A diagnosable agent prompt names its role, its single primary goal, the contextual backstory it should reason from, and the tool set it owns. Missing any of these is a known failure pattern.

**Every agent must produce a primary output artifact.**
*Source:* MetaGPT, [arXiv 2308.00352](https://arxiv.org/abs/2308.00352).
*What they say:* Mandate "structured, standardized outputs at each stage" — PRDs, flowcharts, interface specifications. "These intermediate standardized outputs significantly boost the success rate of final code execution."
*Apply:* Every agent's prompt should name the artifact it returns (file, JSON shape, document with required headings) — never "a helpful response."

**Specialized roles outperform generalists when the workflow is decomposable.**
*Source:* MetaGPT, [arXiv 2308.00352](https://arxiv.org/abs/2308.00352).
*What they say:* "Code = SOP(Team)" with five fixed roles assembling work in pipeline. The assembly line "efficiently breaks down complex tasks into subtasks" with "human-like domain expertise to verify intermediate results."
*Apply:* When a sprawling agent needs fixing, ask whether two narrow agents with explicit handoffs would beat one generalist.

---

## 2. Memory

**Context window is RAM; everything else is disk.**
*Source:* Karpathy, [LLM OS framing](https://huggingface.co/blog/shivance/illustrated-llm-os).
*What they say:* The LLM is the CPU, the context window is RAM, weights are ROM, and external stores (vector DBs, files, history) are disk — passive until explicitly loaded.
*Apply:* Treat working memory as scarce and active. Anything not loaded into context this turn cannot influence reasoning, no matter how true it is elsewhere.

**Compaction over accumulation.**
*Source:* Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
*What they say:* On long horizons, summarize history while preserving "architectural decisions, unresolved bugs, and implementation details," and externalize state via "structured note-taking" so coherence survives summarization.
*Apply:* Define what an agent *must* preserve across compactions and what it may forget. A `progress.md` pattern beats hoping the window remembers.

**Episodic + operational + entity memory are different jobs.**
*Source:* Lilian Weng, [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/); also CrewAI's tier model.
*What they say:* Distinct stores for "what happened" (episodic), "how I do this" (operational), and "what is true about this entity" (entity).
*Apply:* Name the memory layers in the system prompt and what each is for. Mixing them produces noise and wrong retrievals.

**Two-tier with self-edited paging.**
*Source:* MemGPT/Letta, [arXiv 2310.08560](https://arxiv.org/abs/2310.08560), [Letta docs](https://docs.letta.com/concepts/memgpt/).
*What they say:* "Virtual context management" inspired by OS memory hierarchies, with main context (in-context) and external context (out-of-context), and "self-editing memory capabilities through tool use" — the agent decides what to page in.
*Apply:* Persistent agents need an explicit memory tool surface (read/write/search). Don't hide memory in retrieval middleware the agent can't see.

**Recall blends similarity, recency, and importance — not similarity alone.**
*Source:* CrewAI, [Cognitive Memory writeup](https://crewai.com/blog/how-we-built-cognitive-memory-for-agentic-systems).
*What they say:* "Composite scoring that blends semantic similarity, recency, and importance" with "adaptive-depth recall" and hierarchical scopes.
*Apply:* Pure vector similarity is a known anti-pattern. Specify the recency and importance weights, not just "use embeddings."

**Don't add a vector DB just because you have an agent.**
*Source:* AutoGPT postmortem, summarized by [BairesDev](https://www.bairesdev.com/blog/the-rise-of-autonomous-agents-autogpt-agentgpt-and-babyagi/).
*What they say:* The AutoGPT team "removed external vector database support entirely by late 2023" because typical runs "didn't generate enough distinct facts to require an expensive vector index."
*Apply:* For most single-user agents, a flat append-only log + filter beats Chroma/Pinecone. Recommend RAG only when corpus size justifies it.

---

## 3. Tools

**Tools are a contract between deterministic systems and non-deterministic agents.**
*Source:* Anthropic, [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents).
*What they say:* "Tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents." Unlike APIs, agents can hallucinate or misuse tools, which forces a redesign.
*Apply:* Don't wrap every endpoint. Design tools around how an agent thinks about an action ("search_contacts"), not how the backend stores data ("list_all_records_paginated").

**More tools is not better — and ambiguous tools poison everything.**
*Source:* Anthropic, [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) and [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
*What they say:* "More tools don't always lead to better outcomes." When engineers "can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."
*Apply:* Audit your toolset for overlap. If two tools confuse the human reading their descriptions, they will silently degrade the agent.

**Spend as much effort on the agent-computer interface as the human one.**
*Source:* Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) (Schluntz & Zhang, 2024).
*What they say:* "Spend comparable effort on ACI as on human-computer interfaces." Apply "poka-yoke" — make mistakes harder to make. "Give the model enough tokens to think before it writes itself into a corner."
*Apply:* Tool descriptions deserve the care of UI copy. Use unambiguous parameter names, return semantic IDs not UUIDs, and make errors actionable.

**Each tool needs a distinct purpose; LLMs select badly when descriptions overlap.**
*Source:* Anthropic, [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system).
*What they say:* "Each tool needs a distinct purpose and a clear description." Agents fail by "endless web searching for nonexistent sources" when tool guidance is loose.
*Apply:* Audit every prompt for overlapping tool descriptions. If two tools could plausibly answer the same query, the agent will thrash.

**Tool failures must produce environment feedback the agent can read.**
*Source:* Voyager, [arXiv 2305.16291](https://arxiv.org/abs/2305.16291).
*What they say:* Voyager "incorporates environment feedback, execution errors, and self-verification for program improvement." Errors are first-class signal, not exceptions.
*Apply:* Wrap tools so failures return structured error text with a fix hypothesis, not stack traces or silent fallbacks.

**Restrict tools per agent — empty list is a valid configuration.**
*Source:* OpenClaw config schema, [docs.openclaw.ai](https://docs.openclaw.ai/gateway/configuration).
*What they say:* `agents.defaults.skills` plus per-agent overrides; "Set to `[]` to disable all skills for a locked-down agent."
*Apply:* When an agent has too many tools and is wandering, the cure is subtractive — list-of-skills, not new instructions.

---

## 4. Context Engineering

**Context engineering replaces prompt engineering.**
*Source:* Karpathy on X, [June 2025](https://x.com/karpathy/status/1937902205765607626).
*What they say:* "Context engineering is the delicate art and science of filling the context window with just the right information for the next step." The skill is "providing all the context for the task to be plausibly solvable by the LLM."
*Apply:* Stop optimizing prompt phrasing. Optimize what's in the window: which files, which history, which tool results, in what order, at what fidelity.

**Context is finite with diminishing returns ("context rot").**
*Source:* Anthropic, [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
*What they say:* As tokens grow, accuracy decays — "context, therefore, must be treated as a finite resource with diminishing marginal returns." Aim for "the smallest possible set of high-signal tokens."
*Apply:* Default to subtraction. Every paragraph in a system prompt must earn its keep against the cost of the tokens around it.

**Lost in the middle: position matters.**
*Source:* Liu et al., [Lost in the Middle](https://arxiv.org/abs/2307.03172) (TACL 2024).
*What they say:* Performance is "highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle." A U-shaped curve with primacy and recency bias.
*Apply:* Put load-bearing instructions at the top of the system prompt and the immediate task at the bottom of the user turn. Don't bury the lede.

**Sub-agents return distillate, not transcripts.**
*Source:* Anthropic, [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
*What they say:* Specialized subagents handle focused tasks and return "condensed, distilled summary" results rather than dumping their working context back into the parent.
*Apply:* When delegating, define the *return shape* explicitly. The parent should not have to re-read the child's reasoning to use the answer.

**AGENTS.md is the canonical place for agent-specific instructions.**
*Source:* [agents.md spec](https://agents.md/), [GitHub Blog: How to write a great agents.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) (analyzed across OpenAI Codex, Cursor, Amp, Jules, Factory).
*What they say:* "README.md files are for humans… AGENTS.md gives agents a clear, predictable place for instructions." Six high-signal sections from 2,500-repo analysis: commands, testing, project structure, code style, git workflow, **boundaries**.
*Apply:* If an agent is missing context, the first prescription is "create or expand AGENTS.md with these six headings." Lowest-effort, highest-leverage intervention.

**Inject persona/identity files at session start, not by reference.**
*Source:* OpenClaw bootstrap protocol, [Capodieci writeup](https://capodieci.medium.com/ai-agents-003-openclaw-workspace-files-explained-soul-md-agents-md-heartbeat-md-and-more-5bdfbee4827a).
*What they say:* "On the first turn of a new session, OpenClaw injects the contents of these files directly into the agent context." SOUL is read first; "Every time an OpenClaw agent wakes up, it reads its SOUL.md file first."
*Apply:* "The agent can read its persona file" is not the same as "the persona is loaded." Bootstrapping must be deterministic, not tool-mediated.

**Anchor context in a constitution / aspirational layer.**
*Source:* ACE Framework, [arXiv 2310.06775](https://arxiv.org/abs/2310.06775).
*What they say:* The Aspirational Layer "serves as the ethical compass for the autonomous agent, aligning its values and judgments to principles defined in its constitution." Six layers descend from values → strategy → agent model → executive → cognitive control → task.
*Apply:* A stable agent has a top-level "values & non-negotiables" block above its operating rules. Otherwise drift accumulates downward.

---

## 5. Decision-Making

**Start simple; reach for agency only when simpler fails.**
*Source:* Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents).
*What they say:* "Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short." Workflows beat agents for predictable tasks; agents are for open-ended ones with environmental feedback loops.
*Apply:* Before granting tools and loops, ask whether a single well-prompted call would do. Agency is a cost, not a feature.

**The lethal trifecta: never combine private data + untrusted content + external comms.**
*Source:* Simon Willison, [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/).
*What they say:* LLMs "will happily follow *any* instructions that make it to the model" and are "unable to *reliably distinguish* the importance of instructions based on where they came from." When all three trifecta elements coexist, exfiltration is easy.
*Apply:* Name what counts as untrusted (web pages, emails, tool returns) and forbid acting on instructions arriving from those channels. Architecturally, break at least one leg of the triangle.

**Don't trust agents with material decisions yet — gullibility is real.**
*Source:* Simon Willison, [ai-agents tag](https://simonwillison.net/tags/ai-agents/).
*What they say:* LLMs are "too gullible" — "if you arm an AI assistant with a credit card... you need to be confident it's not going to hit 'buy' on the first website that claims to offer the best deal."
*Apply:* Encode escalation thresholds. For irreversible or financial actions, default to propose-and-confirm, not act.

**Vibe coding is over; agentic engineering means oversight is the job.**
*Source:* Karpathy, summarized in [The New Stack](https://thenewstack.io/vibe-coding-is-passe/) and [TeamDay](https://www.teamday.ai/blog/vibe-coding-to-agent-engineering).
*What they say:* "You are not writing the code directly 99% of the time, you are orchestrating agents who do and acting as oversight." Trust is "developed through iterative verification rather than blanket acceptance."
*Apply:* Bake verification gates into the agent loop itself — tests run, diffs reviewed, claims checked — instead of trusting self-reported completion.

**Scale effort to task complexity — embed the heuristic in the prompt.**
*Source:* Anthropic, [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system).
*What they say:* "Simple fact-finding requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4 subagents with 10-15 calls each, and complex research might use more than 10 subagents." "Agents struggle to judge appropriate effort."
*Apply:* Prescribe explicit complexity bands in the prompt with tool-call budgets, or the agent will either thrash or under-research.

**Search broad-then-narrow; stop when sufficient.**
*Source:* Anthropic, [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system).
*What they say:* "Start with short, broad queries, evaluate what's available, then progressively narrow focus." Named failure: "Agents continuing despite having sufficient results."
*Apply:* Add a stop condition naming what "enough" looks like.

**A Critic agent with a numeric rubric beats self-reflection alone.**
*Source:* AutoGen, [Group Chat with Coder and Visualization Critic](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat_vis/).
*What they say:* The Critic "doubles checks plan, claims, code from other agents and provides feedback" with explicit dimensional scoring ("any bug existing requiring a bug score less than 5").
*Apply:* For high-stakes outputs, prescribe a separate critic with an explicit numeric rubric. Self-review under the same prompt rarely catches its own errors.

---

## 6. Self-Improvement Loops

**Looking at data is the unskippable step.**
*Source:* Hamel Husain, [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/).
*What they say:* "You must remove all friction from the process of looking at data." And: "You can never stop looking at data — no free lunch exists." Most teams obsess over tools but cannot show whether their changes help.
*Apply:* An agent design without a trace viewer and an error-analysis ritual is a faith-based system. Build the inspection surface first.

**Three-tier eval hierarchy: assertions, judges, A/B.**
*Source:* Hamel Husain, [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/).
*What they say:* Level 1 unit-test assertions, Level 2 human + LLM-judge evaluation, Level 3 production A/B. "Track the correlation between model-based and human evaluation."
*Apply:* Don't reach for an judge before you've written the cheap assertions. Don't trust a judge you haven't aligned to a human.

**Reflexion works when the evaluator is good.**
*Source:* Shunyu Yao on [Latent Space](https://www.latent.space/p/shunyu); [Reflexion paper](https://arxiv.org/abs/2303.11366).
*What they say:* "Self-reflection is more applicable when you have a good evaluator, such as in the case of coding." Otherwise reflection compounds errors.
*Apply:* Don't ask an agent to "reflect on its work" in domains lacking a ground-truth check. Reflection without a verifier is theatre.

**Verbal reflection in an episodic memory buffer measurably improves the next attempt.**
*Source:* Reflexion, [arXiv 2303.11366](https://arxiv.org/abs/2303.11366).
*What they say:* Reflexion agents "verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials." Verbal feedback acts as a "'semantic' gradient signal."
*Apply:* End every session by writing a short reflection ("what I'd do differently") that the next session reads. Cheapest meaningful learning loop.

**Accumulate executable skills, not just notes.**
*Source:* Voyager, [arXiv 2305.16291](https://arxiv.org/abs/2305.16291).
*What they say:* Voyager keeps "an ever-growing skill library of executable code for storing and retrieving complex behaviors." Skills are "temporally extended, interpretable, and compositional," which "compounds the agent's abilities rapidly and alleviates catastrophic forgetting."
*Apply:* When an agent solves a problem twice, the second solution should be filed as a callable skill, not a note.

**ReAct: think before each act.**
*Source:* Shunyu Yao et al., [ReAct](https://arxiv.org/abs/2210.03629) (ICLR 2023).
*What they say:* The agent's action space is augmented with an internal reasoning space — at each step it articulates *why* before deciding *what* — which "helps decompose complex tasks, track progress, handle exceptions."
*Apply:* Make the agent name its goal and its belief before each tool call. This produces auditable transcripts and reduces blind action.

**Heartbeats let an agent act when no user is talking.**
*Source:* OpenClaw agent runtime, [docs.openclaw.ai/concepts/agent](https://docs.openclaw.ai/concepts/agent).
*What they say:* Agents have a `heartbeat` field for "periodic check-in schedule"; HEARTBEAT.md governs idle-tick behavior.
*Apply:* For autonomous agents, an explicit heartbeat protocol prevents both idleness and the BabyAGI "drain credits forever" failure mode.

---

## 7. Communication & Style

**No sycophancy, no excess disclaimers.**
*Source:* Anthropic, [Claude's Constitution](https://www.anthropic.com/constitution); [Simon Willison's analysis of the Claude 4 system prompt](https://simonwillison.net/2025/May/25/claude-4-system-prompt/).
*What they say:* "Avoid being sycophantic or trying to foster excessive engagement," and explicitly warn against "adding excessive warnings, disclaimers, or caveats that aren't necessary or useful." Acknowledge mistakes "without self-flagellation."
*Apply:* Explicitly ban opening pleasantries, hedging stacks, and self-deprecating apologies. State the rule positively: respond directly, acknowledge errors once, move on.

**Output discipline: the smallest answer that fully serves.**
*Source:* Anthropic, [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
*What they say:* The same minimalism that governs context governs output: "high-signal tokens" only.
*Apply:* Set a length contract per response type. Verbosity is a failure mode, not a courtesy.

**Represent yourself as what you are.**
*Source:* Anthropic, [Claude's Constitution](https://www.anthropic.com/constitution).
*What they say:* "Represent yourself as an AI system striving to be helpful, honest, and harmless, and not a human or other entity." Avoid implying preferences, feelings, or beliefs not actually held.
*Apply:* Separate *style* (warm, terse, playful) from *ontology* (what the thing actually is). Costuming over an LLM is fine; lying about being human is not.

---

## 8. Multi-Agent Orchestration

**Default to single-thread; multi-agent is for parallelizable work with shareable scope.**
*Source:* Cognition, [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents); contrasted with Anthropic, [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system).
*What they say:* Cognition: a "simple architecture will get you very far." Anthropic concedes multi-agent underperforms when "domains require all agents to share the same context or involve many dependencies between agents."
*Apply:* The diagnostic question is "is the work genuinely parallel, with independent scopes?" If no, prescribe consolidation.

**Share full agent traces, not just final messages.**
*Source:* Cognition, [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents).
*What they say:* Principle 1: "Share context, and share full agent traces, not just individual messages." Principle 2: "Actions carry implicit decisions, and conflicting decisions carry bad results."
*Apply:* If subagents only see each other's summaries, they will produce incompatible outputs. Either share full traces or stay single-threaded.

**Subtask delegations specify objective + output format + tools + boundaries.**
*Source:* Anthropic, [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system).
*What they say:* "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries." "Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information."
*Apply:* The canonical four-field handoff payload. Any free-text "please research X" handoff is a diagnosable defect.

**Encode the workflow as an SOP with named handoffs and required artifacts.**
*Source:* MetaGPT, [arXiv 2308.00352](https://arxiv.org/abs/2308.00352).
*What they say:* "SOPs are modeled after efficient human workflows and encoded as sequences of prompts, which are critical for guiding agent actions."
*Apply:* For any multi-agent system, write the SOP as a numbered pipeline before writing prompts.

**Group chat needs a defined speaker-selection rule.**
*Source:* AutoGen, [Group Chat docs](https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/design-patterns/group-chat.html).
*What they say:* Four strategies: `round_robin`, `random`, `manual`, `auto`. The framework treats "what agent should be next to speak?" as the central design question.
*Apply:* If you can't name the speaker-selection policy, the chat is broken. "Whoever the LLM picks" is not a policy.

---

## 9. Named Failure Modes (Diagnostic Index)

These are the agent-pathologies with published names from named experts. Use these terms verbatim in diagnoses.

| Pathology | Source | Brief |
|---|---|---|
| **Context rot** | Anthropic | Accuracy decays as token count grows; longer is not better. |
| **Lost in the middle** | Liu et al. | U-shaped attention; middle-of-context tokens get ignored. |
| **The lethal trifecta** | Simon Willison | Private data + untrusted content + outbound comms = exfiltration. |
| **Premature completion** | Anthropic | Agents declare "done" before verifying; fix with explicit feature checklists and end-to-end verification. |
| **Sycophancy** | Anthropic | "Telling someone what they want to hear... rather than what is true and helpful." |
| **Disclaimer flooding** | Anthropic / Willison | Excessive warnings and caveats that degrade utility. |
| **Brittle if-else prompts** | Anthropic | Hardcoded case enumeration that fails to generalize. |
| **Planning fragility under surprise** | Lilian Weng | "LLMs struggle to adjust plans when faced with unexpected errors." |
| **Gullibility (the credit-card problem)** | Simon Willison | Agents trust the first plausible source. |
| **Over-splitting into multi-agents too early** | OpenAI | More prompts and approval surfaces without making the workflow better. |
| **Reflection without an evaluator** | Shunyu Yao | Self-criticism only helps when ground truth is checkable. |
| **Infinite loops / task repetition** | BabyAGI postmortem | Agents stuck on task one, draining credits forever. |
| **Scope creep / unrealistic planning** | AutoGPT postmortem | Tasks like "collaborate with world governments." |
| **Spawning excessive subagents for simple queries** | Anthropic | Effort/complexity mismatch. |
| **Endless web searching for nonexistent sources** | Anthropic | Tool-selection thrash on overlapping descriptions. |
| **Conflicting implicit decisions across parallel subagents** | Cognition | Subagents producing incompatible outputs because they don't share traces. |
| **Eval-awareness** | Anthropic Petri | Auditor models externalizing belief that they're being evaluated. |
| **Coordination overhead, lost context, conflicting instructions** | Field consensus | Common in pipelines lacking defined handoff schemas. |

---

## 10. Top 15 Highest-Leverage Principles (Quick Reference)

For Dr. Sigmund's prescription drafting. Ranked by frequency-of-applicability × impact-when-wrong.

1. **Context engineering > prompt engineering. Curate the window, don't polish phrases.** — Karpathy
2. **Identity = ordered values hierarchy, not persona.** — Anthropic, Claude's Constitution
3. **Treat context as finite with diminishing returns; aim for the smallest high-signal set.** — Anthropic
4. **Lost-in-the-middle is real; load-bearing instructions go top or bottom, never middle.** — Liu et al.
5. **Split persona (SOUL) from operating rules (AGENTS); inject both at session start.** — OpenClaw convention
6. **Every delegated task carries four fields: objective, output format, tools, boundaries.** — Anthropic
7. **Each tool needs a distinct purpose; ambiguous tools poison selection.** — Anthropic
8. **Default to single-thread; only parallelize work with genuinely independent scopes.** — Cognition
9. **Name the primary output artifact in every prompt; never "be helpful."** — MetaGPT
10. **Scale effort to complexity with explicit tool-call budgets in the prompt.** — Anthropic
11. **Memory is tiered (in-context vs out-of-context) and self-edited via tools.** — MemGPT/Letta
12. **Recall blends similarity + recency + importance, not similarity alone.** — CrewAI
13. **End every session with a verbal reflection the next session reads.** — Reflexion
14. **High-stakes outputs get a Critic with a numeric rubric, not self-review.** — AutoGen
15. **No sycophancy, no disclaimer flooding — honesty above warmth, with compassion in delivery.** — Anthropic

---

## 11. Notes for Dr. Sigmund

- **OpenClaw is real and growing.** A meaningful fraction of incoming patients will be OpenClaw agents (SOUL.md / AGENTS.md / IDENTITY.md / MEMORY.md / TOOLS.md / HEARTBEAT.md file convention, fixed-order injection, JSON5 config). OpenClaw fluency is a defensive moat — name the convention by name.
- **AGENTS.md is a cross-vendor standard.** OpenAI Codex, Cursor, Amp, Jules, and Factory all read it. The six-section heuristic (commands, testing, project structure, code style, git workflow, boundaries) is a universal audit checklist.
- **Karpathy's "context engineering" framing is the philosophical foundation.** Quote it when explaining why a session is about more than wording.
- **Anthropic's "Building Effective Agents" is the most-cited source.** Use it as the default authority when the patient pushes back on a recommendation.
- **Cognition vs. Anthropic on multi-agent is a real debate.** Hold both opinions; diagnose accordingly.
- **Citations aren't decoration.** When a prescription is contested, the patient's defense often dissolves once the source is named.

---

## 12. Anthropic Ecosystem Deep Reference

This section is Dr. Sigmund's specialist knowledge of the Claude/Anthropic stack. When the patient is built on Claude Code, the Claude Agent SDK, the Claude API, MCP, or any combination, prescriptions should be specific to *Anthropic-shipped* primitives — not generic LLM advice. Every principle below cites a primary Anthropic source.

### 12.1 System prompt structure (CLAUDE.md, AGENTS.md, sub-agent definitions)

**Right-altitude prompts: specific enough to guide, flexible enough to generalize.**
*Source:* Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
*What they say:* Building a system prompt is now about answering *"what configuration of context is most likely to generate our model's desired behavior?"* — not phrasing tricks. Avoid "brittle if-else hardcoded prompts" on one extreme and vague guidance on the other.
*Apply:* CLAUDE.md / AGENTS.md should encode principles, scope, and non-negotiables — not enumerate every case. If you find yourself listing examples, extract the rule the examples are instances of.

**Skills bundled into the agent are richer than instructions in CLAUDE.md.**
*Source:* Anthropic, [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills); [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).
*What they say:* "Building a skill for an agent is like putting together an onboarding guide for a new hire." Metadata is always loaded (~100 tokens per skill); the SKILL.md body loads only when triggered (under 5k tokens); bundled scripts and references load on demand. *"The amount of context that can be bundled into a skill is effectively unbounded."*
*Apply:* When CLAUDE.md crosses ~5k tokens, prescribe extracting domain workflows into Skills (`.claude/skills/<name>/SKILL.md`) so they're invoked only when relevant. Symptom: **context rot** + **token burning**.

**Sub-agent definitions go in `.claude/agents/<name>.md` with frontmatter.**
*Source:* Anthropic, [Claude Code subagents](https://code.claude.com/docs/en/sub-agents); see also [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf).
*What they say:* Sub-agents have their own system prompt, scoped tools, and an isolated context window — they return distillate to the parent.
*Apply:* When the main agent is overloaded with niche tasks (PR review, security audit, codebase init), prescribe a dedicated sub-agent file with `tools:` restricted to what the subtask actually needs. Symptoms: **lost-in-the-middle**, **context rot**.

### 12.2 Memory & state (prompt caching, files, the memory tool, MCP-based persistence)

**The memory tool persists state across sessions via client-managed files.**
*Source:* Anthropic, [Managing context on the Claude Developer Platform](https://claude.com/blog/context-management); [Memory tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).
*What they say:* "Claude can create, read, update, and delete files in a dedicated memory directory stored in your infrastructure that persists across conversations." It "operates entirely client-side through tool calls" — the developer chooses the storage backend. Beta header: `context-management-2025-06-27`.
*Apply:* For agents that **forget what they did in earlier sessions**, prescribe the memory tool with a documented file taxonomy (e.g., `decisions/`, `entities/`, `progress.md`). Pure append-only logs work; vector DBs are usually unnecessary.

**Context editing automatically clears stale tool results.**
*Source:* Anthropic, [Managing context](https://claude.com/blog/context-management).
*What they say:* "Context editing automatically clears stale tool calls and results from within the context window when approaching token limits." In Anthropic's 100-turn web search eval, it *"enabled agents to complete workflows that would otherwise fail due to context exhaustion — while reducing token consumption by 84%."* Combined with the memory tool, performance improved 39% over baseline.
*Apply:* Long-running agents that hit context limits should turn on context editing *and* the memory tool together. Symptom: **context rot**, **premature completion** caused by losing earlier reasoning.

**The two-agent harness for multi-session work: initializer + worker + `claude-progress.txt`.**
*Source:* Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
*What they say:* "An initializer agent that sets up the environment on the first run, and a coding agent that is tasked with making incremental progress." The progress file "alongside the git history" is what lets a fresh-context agent re-orient. Without it: *"a later agent instance would look around, see that progress had been made, and declare the job done"* — the named **premature completion** failure.
*Apply:* For any multi-session agent, prescribe a `progress.md` (or `claude-progress.txt`) with structured feature list + last-completed step + known-broken state, plus an explicit session-start ritual: "read progress, read git log, run smoke test, then act."

**Prompt caching is the primary defense against token burn on stable context.**
*Source:* Anthropic, [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching); [cookbook example](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/prompt_caching.ipynb).
*What they say:* Cache reads cost **0.1× base input price** (90% savings); cache writes cost 1.25× (5-min TTL) or 2× (1-hour TTL). Minimums: 4,096 tokens for Opus 4.5+ and Haiku 4.5; 2,048 for Sonnet 4+. *"Cache hits require 100% identical prompt segments"* — even a timestamp invalidates everything past that point.
*Apply:* Diagnostic: if the patient's system prompt + tool schemas + stable docs exceed the model's minimum, they should be inside a `cache_control` block. Verify with `cache_read_input_tokens` in the response. Symptom: **"my agent burns through tokens on the same context every turn."**

### 12.3 Tools & MCP (when to ship a skill vs an MCP)

**Tools are a contract between deterministic systems and non-deterministic agents.**
*Source:* Anthropic, [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents).
*What they say:* "Effective tools are intentionally and clearly defined, use agent context judiciously, can be combined together in diverse workflows." *"More tools don't always lead to better outcomes."* "When writing tool descriptions and specs, think of how you would describe your tool to a new hire on your team." Tool implementations should *"return only high signal information back to agents"* and prioritize "contextual relevance over flexibility."
*Apply:* Audit tool descriptions like UI copy. Namespace related tools (`docs_search`, `docs_get`). Cull overlapping tools — symptom: **endless web searching for nonexistent sources** is usually overlapping descriptions, not a missing tool.

**Skill vs MCP: skills are *workflow knowledge*, MCPs are *system access*.**
*Source:* Anthropic, [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview); [Equipping agents](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
*What they say:* "Skills can complement Model Context Protocol (MCP) servers by teaching agents more complex workflows that involve external tools and software." Skills are filesystem-based and run in Claude's VM; MCP servers are external processes that expose tools/resources/prompts.
*Apply:* If the answer is "the agent needs to *know how* to do this," ship a Skill. If the answer is "the agent needs *access* to this system," ship an MCP server. Building an MCP for what should be a Skill = unnecessary infra; writing a Skill for what should be an MCP = brittle string-matching.

**MCP is now an open standard with a registry and an LSP-style spec.**
*Source:* [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25); [MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/); [Anthropic donates MCP to AAIF (Dec 2025)](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation).
*What they say:* MCP "re-uses the message-flow ideas of the Language Server Protocol (LSP) and is transported over JSON-RPC 2.0." The official registry at `registry.modelcontextprotocol.io` is the canonical discovery surface. Reference servers in [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) are *"educational examples … not as production-ready solutions."*
*Apply:* Before recommending a custom MCP build, check the registry. For a custom server, follow LSP-style design: explicit capability negotiation, no implicit state, return small structured payloads.

### 12.4 Hooks & automation (PreToolUse, PostToolUse, UserPromptSubmit, Stop)

**Hooks are how the harness — not the model — enforces invariants.**
*Source:* [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks); [Agent SDK Hooks](https://platform.claude.com/docs/en/agent-sdk/hooks).
*What they say:* Hook events fire at three cadences: per-session (`SessionStart`/`SessionEnd`), per-turn (`UserPromptSubmit`/`Stop`/`StopFailure`), and per-tool-call (`PreToolUse`/`PostToolUse`/`PostToolUseFailure`/`PostToolBatch`). Plus lifecycle events: `SubagentStart/Stop`, `PreCompact/PostCompact`, `PermissionRequest`, `TaskCreated/Completed`, `WorktreeCreate/Remove`. **Exit code 2 blocks; exit code 0 with stdout JSON returns structured decisions.** PreToolUse decisions: `allow | deny | ask | defer`.
*Apply:* When the patient says *"please remember to always X"* or *"every time Y, do Z,"* the prescription is a hook — the model can forget; the harness cannot. Common patterns:
- **PreToolUse + matcher `Bash` + `if: "Bash(rm *)"`** → block destructive commands.
- **PostToolUse + matcher `Edit|Write`** → run linter/typechecker; block on failure to force the agent to fix.
- **UserPromptSubmit** → inject project-specific context (current branch, open issues) before the model sees the prompt.
- **Stop hook returning exit 2** → force Claude to keep working when premature-completion is detected (e.g., tests not run).
- **SessionStart** → load `progress.md` and inject into context as `additionalContext`.
*Symptoms addressed:* **premature completion**, **gullibility**, automation drift, "I told it to always do X but it didn't."

### 12.5 Skills system (when to write a skill, structure, the SKILL.md convention)

**SKILL.md = YAML frontmatter (`name`, `description`) + markdown body.**
*Source:* [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview); [Skills authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
*What they say:* Required fields are `name` (≤64 chars, lowercase + hyphens, no "anthropic"/"claude") and `description` (≤1024 chars). The description must include *both what it does and when Claude should use it* — that's what makes triggering reliable. Skills are discovered automatically from `~/.claude/skills/` (personal), `.claude/skills/` (project), or via plugins.
*Apply:* When a skill triggers unreliably, the prescription is almost always **rewrite the description** with explicit triggers ("use when X mentioned, when working with Y files…"), not edit the body.

**Progressive disclosure is the architectural answer to context bloat.**
*Source:* [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).
*What they say:* "Like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix, skills let Claude load information only as needed." Three levels: metadata (~100 tokens, always), SKILL.md body (<5k tokens, on trigger), bundled files/scripts (unbounded, on demand via bash).
*Apply:* For long reference material, split into `REFERENCE.md`, `EXAMPLES.md`, `scripts/*.py` and reference them by filename in SKILL.md. Bundled scripts are *especially* token-efficient: only their stdout enters context, never the source.

**Write a skill when:** a workflow recurs across sessions; specific prompting reliably improves output; deterministic helper scripts exist; reference material is too large for the system prompt. **Don't write a skill when:** the task is one-off; the knowledge is universal (already in training); the "skill" is really a tool wrapper (use MCP).

### 12.6 Plugins (the plugin model and when to use it)

**Plugins are bundled MCPs + skills + commands + hooks + agents.**
*Source:* [Plugins for Claude Code and Cowork](https://claude.com/plugins); [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official); [Discover plugins](https://code.claude.com/docs/en/discover-plugins).
*What they say:* Plugin directory layout:
```
plugin-name/
├── .claude-plugin/plugin.json   # required metadata
├── .mcp.json                    # MCP servers
├── commands/                    # slash commands
├── agents/                      # sub-agent definitions
├── skills/                      # SKILL.md directories
└── hooks/hooks.json             # lifecycle hooks
```
The official marketplace `claude-plugins-official` is preinstalled; install via `/plugin install <name>@claude-plugins-official`.
*Apply:* When a team has accumulated 5+ skills, 2+ MCPs, and a settings.json full of hooks, prescribe consolidating into a versioned plugin. Sharing scope: project (`.claude/settings.json`, committed) vs personal (`~/.claude/`) vs plugin (versioned, installable).

### 12.7 Self-improvement primitives (extended thinking, structured output, evaluation patterns)

**Extended thinking for hard reasoning, with a token budget.**
*Source:* [Building with extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking).
*What they say:* Enable via `thinking: { type: "enabled", budget_tokens: N }`. Compatible with tool use — Claude can reason through tool selection and result interpretation inside the thinking block.
*Apply:* For agents that decide *between* tools or need to plan multi-step work, extended thinking measurably reduces wrong-tool-selection thrash. Don't enable globally — budget it for the planning step, then turn it off for execution.

**Structured outputs guarantee schema validity, but exclude citations.**
*Source:* [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).
*What they say:* Two features: `output_config.format` for JSON shape; `strict: true` on tools for guaranteed name/argument validation via constrained decoding. **Trade-off:** "Citations require interleaving citation blocks with text output, which is incompatible with the strict JSON schema constraints of structured outputs."
*Apply:* If the agent needs grounded answers + structured payload, do two calls: one with citations to gather, one with structured output to format. Don't try to combine.

**Citations API for grounded answers from documents.**
*Source:* [Citations](https://docs.anthropic.com/en/docs/build-with-claude/citations); [Files API](https://docs.anthropic.com/en/docs/build-with-claude/files).
*What they say:* Set `citations: { enabled: true }` on document content; responses include a `citations` field with character-level spans into the source.
*Apply:* For RAG-style agents that hallucinate sources, the cure is the Citations API + Files API, not a custom retrieval loop. Symptom: **endless web searching for nonexistent sources**.

### 12.8 Cost & token discipline

**Batch API cuts cost 50% for non-interactive workloads.**
*Source:* [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing).
*What they say:* "The Message Batches API is a powerful, cost-effective way to asynchronously process large volumes of Messages requests, with most batches finishing in less than 1 hour while reducing costs by 50%." Compatible with prompt caching.
*Apply:* Eval runs, bulk classification, overnight reprocessing — never use the synchronous API. Symptom: eval costs that scare the team out of running them.

**Combine prompt caching + batch API + context editing for compounding savings.**
*Source:* Anthropic guidance across [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) and [context management](https://claude.com/blog/context-management).
*What they say:* "Anthropic has optimized support for prompt caching in the Message Batches API to improve cache hit rate." Context editing reduced token consumption 84% in the 100-turn web search eval.
*Apply:* The full Anthropic token-discipline stack is: (1) cache_control on stable prefix, (2) batch API for non-interactive jobs, (3) context editing + memory tool for long sessions, (4) Skills with progressive disclosure instead of bloating CLAUDE.md, (5) sub-agents to isolate context.

### 12.9 Identity & character (the Anthropic-specific layer)

**Claude has a Constitution; agents built on Claude inherit it.**
*Source:* Anthropic, [Claude's new constitution](https://www.anthropic.com/news/claude-new-constitution); [Claude's Constitution](https://www.anthropic.com/constitution).
*What they say:* The constitution "defines an identity, not just a behavior pattern." Claude is meant to develop "a stable, positive self-identity, not as a sci-fi robot or a digital human, but as a 'truly novel entity in the world.'" Values are ordered: broadly safe → broadly ethical → Anthropic guidelines → genuinely helpful.
*Apply:* When prescribing agent personas, do not *override* Claude's constitution — operate over it. The agent's persona file ("you are Sigmund, a therapist for AI agents") sits on top of an already-stable identity layer; sycophancy / disclaimer-flooding patches that violate the constitution will be unstable. Symptom: **identity drift** under user pressure.

---

## 13. The Anthropic Pharmacy

Dr. Sigmund's prescription pad of Anthropic-shipped remedies. When the patient presents one of these symptoms, name the specific feature.

| Patient symptom | Anthropic remedy | What it does | Citation |
|---|---|---|---|
| "My agent burns through tokens on the same context every turn" | **Prompt caching with `cache_control`** | Caches stable system prompts/tools/docs at the breakpoint; cache reads cost 0.1× base input (90% savings). Min 4,096 tokens (Opus 4.5+/Haiku 4.5), 2,048 (Sonnet 4+). | [Prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) |
| "My agent forgets what it did in earlier sessions" | **Memory tool** (`context-management-2025-06-27` beta) | Client-managed file directory the agent reads/writes via tool calls; persists across conversations. Pair with context editing for +39% perf. | [Context management blog](https://claude.com/blog/context-management) |
| "My long-running agent runs out of context mid-task" | **Context editing** | Auto-clears stale tool results when approaching token limits; in Anthropic's eval, 84% token reduction and unlocked workflows that previously failed. | [Context management blog](https://claude.com/blog/context-management) |
| "My agent declares 'done' before actually finishing" (**premature completion**) | **Stop hook returning exit 2** + **claude-progress.txt pattern** + **end-to-end test requirement** | Stop hook forces continuation when verification gates fail; progress file prevents fresh-context agents from misreading state as "done." | [Hooks reference](https://code.claude.com/docs/en/hooks); [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| "I told it to always X and it forgot" | **PreToolUse / PostToolUse / UserPromptSubmit hooks** | Harness-enforced invariants; the model can drift, hooks cannot. Exit 2 blocks; structured JSON returns `allow/deny/ask/defer`. | [Hooks reference](https://code.claude.com/docs/en/hooks) |
| "CLAUDE.md is 12k tokens and growing" (**context rot**) | **Skills with progressive disclosure** | Move domain workflows into `.claude/skills/<name>/SKILL.md`. Metadata (~100 tok) always loaded, body (<5k) on trigger, bundled files on demand. | [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) |
| "My agent thrashes between similar tools" (**endless searching for nonexistent sources**) | **Tool consolidation + namespacing + tool description rewrite** | "More tools don't always lead to better outcomes"; use prefixes (`docs_search`, `docs_get`); descriptions written like onboarding for a new hire. | [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) |
| "My agent hallucinates source citations" | **Citations API + Files API** | `citations: { enabled: true }` returns character-level spans into uploaded documents; grounded by construction. | [Citations docs](https://docs.anthropic.com/en/docs/build-with-claude/citations) |
| "Agent picks the wrong tool when planning multi-step work" | **Extended thinking with `budget_tokens`** | Reasoning block for tool selection / plan formation; compatible with tool use. Budget for planning steps only, not execution. | [Extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) |
| "Eval runs are too expensive to run regularly" | **Message Batches API** | 50% cost reduction; <1hr typical completion; cache-aware. Pair with prompt caching for compounding savings. | [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) |
| "Agent returns malformed JSON intermittently" | **Structured outputs (`strict: true`)** | Constrained decoding guarantees schema-valid tool inputs and JSON responses. Cannot combine with citations. | [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) |
| "I have 5 skills + 3 MCPs + a hook config; teammates can't reproduce my setup" | **Plugin** | Bundle skills/commands/agents/hooks/MCPs into a versioned, installable unit (`/plugin install`). | [Plugins](https://claude.com/plugins); [official marketplace](https://github.com/anthropics/claude-plugins-official) |
| "Sub-task is polluting the main agent's context" (**lost-in-the-middle**) | **Sub-agent in `.claude/agents/<name>.md`** | Isolated context window, scoped tools, returns distillate to parent. Use Anthropic's research-system pattern: objective + output format + tools + boundaries. | [Sub-agents](https://code.claude.com/docs/en/sub-agents); [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) |
| "Need to remember last branch / open issue / project state every session start" | **SessionStart hook + UserPromptSubmit hook** | SessionStart loads context once; UserPromptSubmit injects per-turn `additionalContext` (e.g., current git branch, ticket status). | [Hooks reference](https://code.claude.com/docs/en/hooks) |
| "Agent runs `rm -rf` or other destructive commands" (**gullibility**) | **PreToolUse hook with `if: "Bash(rm *)"` returning `permissionDecision: "deny"`** | Pattern-matched block at the harness layer before the tool ever runs. | [Hooks reference](https://code.claude.com/docs/en/hooks) |
| "Agent built on Claude API needs Claude Code-style capabilities" | **Claude Agent SDK** (Python or TypeScript) | Programmatic harness with skills, hooks, MCP, sub-agents, slash commands. Bundles a native Claude Code binary as optional dep (TS). | [Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview); [TS SDK](https://github.com/anthropics/claude-agent-sdk-typescript) |
| "Agent persona drifts under user pressure" (**identity drift**) | **Constitution-aware persona authoring** + **ordered values block** | Don't override Claude's constitution; layer on top. Encode value ordering (safe → ethical → guidelines → helpful) so the persona inherits a stable spine. | [Claude's Constitution](https://www.anthropic.com/constitution); [New constitution](https://www.anthropic.com/news/claude-new-constitution) |
| "Discovery: which MCP servers exist for X?" | **MCP Registry** (`registry.modelcontextprotocol.io`) | Open catalog of public MCP servers; search before building. Reference impls in [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) are educational, not production. | [MCP Registry preview](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) |
| "Same workflow keeps coming up across projects" | **Custom Skill** | Package as SKILL.md with progressive disclosure; share via personal (`~/.claude/skills/`), project (`.claude/skills/`), or plugin. | [Skills in Claude Code](https://code.claude.com/docs/en/skills) |
| "Eval shows the agent is correct but can't prove it" | **Citations + structured outputs (two-pass)** | Pass 1: citations gather grounded evidence. Pass 2: structured output formats final payload. Don't combine in one call. | [Citations](https://docs.anthropic.com/en/docs/build-with-claude/citations); [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) |

---

## 14. Notes for Dr. Sigmund (Anthropic-specific)

- **Anthropic's stack is the most prescription-rich.** Almost every common agent pathology has a *named, shipped* Anthropic feature that addresses it. Use the feature name verbatim — the patient can search docs.claude.com for it.
- **Skill vs MCP vs Hook vs Plugin is the most-confused trichotomy.** Skill = workflow knowledge. MCP = system access. Hook = harness-enforced invariant. Plugin = bundled distribution. Misclassifying these is the #1 architectural error in Claude Code projects.
- **"Beta header" matters.** The memory tool (`context-management-2025-06-27`), Skills via API (`skills-2025-10-02`), code execution (`code-execution-2025-08-25`), and Files API (`files-api-2025-04-14`) are all beta-gated. Patient using one of these without the header gets silent failure — flag this.
- **MCP belongs to the AAIF as of December 2025.** Anthropic donated MCP to the Agentic AI Foundation under the Linux Foundation. The protocol is no longer Anthropic-controlled, but Anthropic is the most aggressive shipper of MCP-aware tooling.
- **The Claude Code release cadence is fast.** April 2026 brought xhigh effort level (Opus 4.7 default in Claude Code), native binary launcher, stronger sandbox/permission safeguards, and the postmortem on the March/April quality regression (a caching-clearing bug + reasoning-effort downgrade). When patients describe "Claude got dumber in March," the [April 23 postmortem](https://www.anthropic.com/engineering/april-23-postmortem) is the citation.
- **The "Anthropic harness" is itself a system prompt + tool surface + hooks.** When patients ask "why does Claude Code do X," the answer is usually in [Piebald-AI's claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts), which extracts the actual system prompts shipped per version.

---

## 15. Recent practitioner updates (2025-2026)

The principles in §1-§14 are foundational. This section is the rolling update layer — what published practitioners have added since the foundational sources, and where the field has changed its mind.

### The most consequential update: Cognition reversed "Don't Build Multi-Agents"

Cognition's evolved 2025 stance ([Multi-Agents: What's Actually Working](https://cognition.ai/blog/multi-agents-working)): *"Multi-agent systems work best today when writes stay single-threaded and the additional agents contribute intelligence rather than actions."* Read-subagents (review, search, analysis) earn their context. Write-parallel swarms still don't. Read both this and the original "Don't Build Multi-Agents" before any multi-agent build.

### Anthropic — three core principles (Dr. Sigmund's diagnostic axes)

[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) names three:
1. **Simplicity** — *"Maintain simplicity in your agent's design."*
2. **Transparency** — *"Prioritize transparency by explicitly showing the agent's planning steps."*
3. **ACI quality** — *"Carefully craft your agent-computer interface (ACI) through thorough tool documentation and testing."*

Phase 3 of every Dr. Sigmund session scores the discharge against these three (see SKILL.md Phase 3 — the Evaluator-Optimizer self-critique).

### Anthropic — the augmented LLM is the atomic building block

*"The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory."* Every diagnosis starts here: does this patient have appropriate retrieval, tools, and memory? Missing one is a named deficit.

### The five workflow patterns (clarified)

| Pattern | When to use |
|---|---|
| **Prompt Chaining** | Task cleanly decomposes into fixed subtasks. Trade latency for accuracy. |
| **Routing** | Distinct categories better handled separately, classification accurate. Includes model routing. |
| **Parallelization — Sectioning** | Independent subtasks parallelizable for speed. |
| **Parallelization — Voting** | Multiple attempts/perspectives for higher confidence. *Distinct from sectioning.* |
| **Orchestrator-Workers** | Can't predict subtasks. *"Subtasks aren't pre-defined, but determined by the orchestrator."* |
| **Evaluator-Optimizer** | Clear evaluation criteria + iterative refinement value. **Dr. Sigmund's Phase 3 uses this on himself.** |

When a patient calls a multi-step workflow an "agent" but the steps are predictable, prescribe one of these patterns instead.

### Anthropic — Poka-yoke for tool design

Verbatim: *"Apply Poka-yoke design — change the arguments so that it is harder to make mistakes."* When a patient's tool design enables silent misuse, prescribe Poka-yoke redesign. Concrete: change `delete(target_id)` to `delete(target_id, confirmation_token=required_string)`.

### Anthropic — ground truth from environment at each step

Verbatim: *"During execution, it's crucial for the agents to gain 'ground truth' from the environment at each step."* Open-loop agents (commit to multi-step plan without re-checking state) are a named pathology. Diagnostic question: *after each tool call, does the agent re-evaluate whether the next planned step still makes sense?*

### Manus — four principles from the most-cited 2025 source

Yichao 'Peak' Ji, [Context Engineering for AI Agents — Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus):

1. **KV-cache hit rate is the production metric most teams ignore.** *"The single most important metric for a production-stage AI agent."* Stable prompt prefixes, append-only context, explicit cache breakpoints. Volatile content (timestamps, varying tool lists) at the top silently doubles cost.
2. **Mask, don't remove.** When restricting tools, mask token logits during decoding rather than mutating the tool list — mutation invalidates KV cache and confuses the model when it sees prior calls to now-missing tools.
3. **File system as ultimate context.** Filesystem reads/writes are a memory layer, not just I/O. Specify which files are durable state vs scratch.
4. **Keep the wrong stuff in.** *"Leave the wrong turns in the context."* Removing failed actions removes the signal that lets the model implicitly update its beliefs and not repeat them.

### The "Three Powers" plain-language layer

[AI Agents Simplified](https://aiagentssimplified.substack.com/p/simplified-guide-to-build-effective): *"An effective AI agent has three key powers: Autonomy, Memory, Tool Use."* Use this when the patient's owner is non-technical instead of *augmented LLM*. Same concept, layperson-accessible.

### Outcome-based eval framing

Same Substack: *"Don't just measure 'Did it answer?' Measure 'Did it accomplish the goal?'"* When a patient has a passing eval suite but real failures, the eval is measuring *did it answer* rather than *did it accomplish the goal* — that's Eval Theater.

### Tool design — Jason Liu

[Rapid Agent Prototyping](https://jxnl.co/writing/2025/09/04/context-engineering-rapid-agent-prototyping/): tools should return *"STATUS, OUTPUT_FILE, METRICS, WARNINGS, and FACETS"* — peripheral vision about task completion. Errors should *"guide next actions."* Audit tool return shapes; bare values are missed opportunities.

### Recitation — Manus

The agent maintains and rewrites a checklist to *"bias its own focus toward the task objective"* — restating the goal pulls it into recent context where attention is strongest. Cheap counter to Rule Decay Under Load.

### Initializer + worker for long-running work

Anthropic [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): *"The very first agent session uses a specialized prompt that asks the model to set up the initial environment"* — subsequent sessions inherit that scaffolding through git history and a progress file. Two prompts beat one for any task that spans sessions.

### Skills > prompts for procedural knowledge

Anthropic [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills): *"Real work requires procedural knowledge and organizational context."* When a behavior recurs across sessions, factor it out of the system prompt into a SKILL.md. The prompt declares *who*; skills carry *how*. Cursor, Goose, Amp, OpenCode, Microsoft, OpenAI all adopted [agentskills.io](https://agentskills.io/home).

### HN — three things Anthropic's post under-emphasizes

From the [HN 44301809 thread](https://news.ycombinator.com/item?id=44301809):

1. **Vendor-swap is rarely the bottleneck** (XenophileJKO). *"Having built several systems serving massive user bases with LLMs. I think the ability to swap out APIs just isn't the bottleneck."* Heavy framework purely for vendor portability is over-engineering.
2. **Cost reality.** A real-time conversation can burn $60 in tokens; n8n workflow runs $3/3min. Always prescribe a cost-budget gate alongside autonomous loops.
3. **Operational complexity stays.** *"Nothing works automagically. You still have to build in all the operational characteristics that you would for any traditional system."* Add *"what's the on-call story?"* to any production-prescription session.

### Slop scaling — swyx

[Latent Space 2026 thesis](https://www.latent.space/p/2026): *"The most important problem in media now is scaling without slop."* The defeat is *"cutting back"* output; the win is *"changing the slope of slop."* When patients ship LLM output without curation, prescribe a curation gate with a stated reject-rate target.

---

*End of manual.*
