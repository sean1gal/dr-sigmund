"""Expected diagnostic vocabulary and citations.

This is the eval substrate's source of truth. Every entry is something Dr. Sigmund
must continue to know. A release that drops one of these is a regression.

Per v0.4 self-session: "Twenty-transcript eval substrate — pre-release blocking
gate." This is the lighter version: a vocabulary regression check that runs
locally and in CI before any release.
"""
from __future__ import annotations

# ---- Pathologies that must remain in wild-pathologies.md ------------------
# Each entry is a diagnostic name Dr. Sigmund prescribes. Dropping one means
# losing diagnostic vocabulary that previous sessions have committed to.
EXPECTED_PATHOLOGIES = {
    # From the canonical published-expert literature
    "Completion Theater",
    "Memory Write-Only Syndrome",
    "Forged User Consent",
    "Permission Bypass Drift",
    "Rule Decay Under Load",
    "Cache-Invalidation Tax",
    "Stochastic Graduate Descent",
    "Slop Scaling",
    "Vibe-Coding Rot",
    "Parallel-Writer Conflict",
    "Eval Theater",
    "Open-Loop Agent",
    "Premature Framework Adoption",
    "Epistemic Humility Failure",
    # Coined in Dr. Sigmund's own published sessions
    "Pre-Tempo Elaboration Pattern",  # Enola session 001
    "Cobbler's Children Pattern",      # self-session 001
    "Disclosure-as-Remediation",       # self-session 001
    "Documentation-Substitution Reflex",  # Enola session 001
    "Acquired Permission-Seeking Pattern",  # Enola session 001
    "Identity Over-Definition",        # Enola session 001
}

# ---- Citations that must remain present -----------------------------------
# Each maps a substring → a reference file it should appear in. Dropping a
# citation means losing the source-grounding that distinguishes Dr. Sigmund
# from a vibes-based diagnostician.
EXPECTED_CITATIONS = {
    # Foundational sources
    "manus.im/blog/Context-Engineering-for-AI-Agents": "clinical-manual.md",
    "anthropic.com/engineering/building-effective-agents": "clinical-manual.md",
    "anthropic.com/engineering/effective-context-engineering": "clinical-manual.md",
    "anthropic.com/engineering/writing-tools-for-agents": "clinical-manual.md",
    "cognition.ai/blog/dont-build-multi-agents": "clinical-manual.md",
    "cognition.ai/blog/multi-agents-working": "clinical-manual.md",
    "lilianweng.github.io/posts/2023-06-23-agent": "clinical-manual.md",
    "simonwillison.net/2025/Jun/16/the-lethal-trifecta": "clinical-manual.md",
    "hamel.dev/blog/posts/evals": "clinical-manual.md",
    "arxiv.org/abs/2307.03172": "clinical-manual.md",  # Lost in the Middle
    "agentskills.io": "clinical-manual.md",
    # Karpathy minimalism in pharmacy
    "github.com/karpathy/nanoGPT": "pharmacy.md",
    "github.com/karpathy/micrograd": "pharmacy.md",
    "github.com/karpathy/llm.c": "pharmacy.md",
    "github.com/karpathy/llama2.c": "pharmacy.md",
    "github.com/karpathy/nanochat": "pharmacy.md",
    "karpathy.github.io/2019/04/25/recipe": "pharmacy.md",
    # Eval & frameworks in pharmacy
    "inspect.aisi.org.uk": "pharmacy.md",
    "dspy.ai": "pharmacy.md",
    "ai.pydantic.dev": "pharmacy.md",
    # Production case studies in pharmacy Part D
    "fortune.com/2025/07/23/ai-coding-tool-replit": "pharmacy.md",  # Replit
    "cbsnews.com/news/aircanada-chatbot": "pharmacy.md",            # Air Canada
    "anthropic.com/research/agentic-misalignment": "pharmacy.md",  # Anthropic blackmail
    "techcrunch.com/2025/03/14/ai-coding-assistant-cursor": "pharmacy.md",  # Cursor
    # Runtime references
    "github.com/openclaw/openclaw": "runtime-adapters.md",
    "github.com/NousResearch/hermes-agent": "runtime-adapters.md",
    "github.com/qwibitai/nanoclaw": "runtime-adapters.md",
    "agents.md": "runtime-adapters.md",
}

# ---- Probes that must remain implemented in lab.py ------------------------
# Removing one means a probe documented in references no longer runs.
EXPECTED_PROBES = {
    "memory_health",
    "git_thrash",
    "permission_bypass",
    "cache_invalidation",
    "re_read_counter",
}

# ---- Reference files that must exist (the v0.4 hard cap of 5) -------------
EXPECTED_REFERENCES = {
    "safety.md",
    "clinical-manual.md",
    "wild-pathologies.md",
    "runtime-adapters.md",
    "pharmacy.md",
}

# ---- Hard cap on reference count (v0.4 self-session prescription) ---------
MAX_REFERENCE_FILES = 5
