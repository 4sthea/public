# Custom AI agents are scaffolding, not personas

**The true value of defining custom agents has almost nothing to do with giving an LLM a role or identity.** A large-scale study testing 162 personas across four model families found that simple persona prompts like "You are a Software Architect" have negligible or slightly negative effects on task accuracy. The value lies elsewhere entirely: in the mechanical scaffolding that agent definitions provide — hard tool restrictions, context window isolation, model routing, deterministic hooks, and structured handoffs. These are architectural constraints that operate outside the LLM's reasoning and cannot be replicated by good prompts or instruction files alone. For teams debating whether to keep custom agent.md files or collapse everything into raw prompts with Copilot's native modes, the answer is nuanced: **persona labels are largely theater, but the mechanical agent infrastructure they carry is genuinely load-bearing**.

The research landscape on this question has matured significantly through 2025–2026. Google DeepMind's evaluation of 180 agent configurations found multi-agent coordination improves performance by **80.9%** on parallelizable tasks but **degrades it by 39–70%** on sequential ones. Anthropic's own engineering team acknowledges it's "still unclear whether a single, general-purpose coding agent performs best across contexts" — this remains an open question even within leading AI labs. What has become clear is that the optimal approach depends on task structure, not ideological commitment to any particular agent count.

---

## Persona prompting is measurably ineffective on frontier models

The most rigorous evidence comes from Pei et al.'s study testing 162 personas across four LLM families on 2,410 factual questions. The finding is unambiguous: **prompting with personas has no or small negative effects on model performance** compared to no persona at all. Domain-aligned personas (e.g., "software engineer" for CS questions) showed a statistically significant but practically negligible positive effect (coefficient = 0.004). No reliable strategy emerged for choosing the right persona — random selection performed identically to deliberate selection.

This doesn't mean all role-related prompting is useless. Kong et al.'s "Better Zero-Shot Reasoning with Role-Play Prompting" found substantial improvements (ChatGPT accuracy on AQuA rose from **53.5% to 63.8%**), but the gains came from a structured two-stage methodology that functioned as an implicit chain-of-thought trigger — not from the identity assignment itself. Similarly, the ExpertPrompting framework demonstrated that richly detailed, automatically-generated expert profiles outperform both simple persona prompts and vanilla prompting. The pattern is consistent: **instructional content embedded in a persona description drives improvement, not the identity label**.

A medical domain study reinforced a crucial nuance: role-playing prompts significantly improved GPT-3.5's performance but showed minimal gains on GPT-4 and Claude 3 Opus. This aligns with the emerging consensus that **persona prompting helps weaker models more than frontier ones**. As OpenAI's 2025 developer report noted, the trend is convergence — reasoning depth, tool use, and conversational quality increasingly live inside the same flagship model. GPT-5 dynamically adjusts reasoning depth without needing external persona scaffolding. For teams using Opus 4, Sonnet 4, or GPT-5, the "you are an expert software architect" preamble is spending tokens for essentially zero return on accuracy.

---

## What agents actually do that prompts cannot

A February 2026 study by Drew Breunig and Srihari Sriraman exfiltrated and swapped system prompts between six CLI coding agents running identical models. The Codex prompt produced a "methodical, documentation-first approach"; the Claude prompt produced an "iterative, try-and-fix approach." Their conclusion: "A given model sets the theoretical ceiling of an agent's performance, but the system prompt determines whether this peak is reached." This sounds like evidence for persona value — but look closer. The behavioral divergence came from **detailed procedural instructions**, not identity claims.

The mechanical functions that distinguish an agent definition from a well-crafted prompt operate at the application layer, beyond the LLM's ability to override:

**Tool restrictions** are hard constraints, not suggestions. Claude Code's Agent SDK accepts `allowed_tools` parameters that mechanically prevent a read-only review agent from editing files. An instruction file saying "never delete files" is advisory; an `allowed_tools: ["Read"]` constraint is enforcement. This is the single most important mechanical function agents provide — the principle of least privilege applied to AI.

**Context window isolation** gives each subagent its own independent context. Anthropic's documentation states subagents "preserve context by keeping exploration and implementation out of your main conversation." This prevents context pollution — a planning discussion about architecture doesn't consume tokens needed for implementation details. With Claude Code's system prompt conditionally assembled from **110+ components** based on environment and configuration, this isolation is structurally essential.

**Model routing** allows different agents to use different models. A planning agent might use Opus 4.5 for deep reasoning while a formatting agent uses Haiku for cost efficiency. Instruction files cannot control which model processes them.

**Deterministic hooks** execute code at specific lifecycle moments (PreToolUse, PermissionRequest) outside the LLM's control. These are hard guardrails that cannot be prompt-injected away. **Progressive disclosure** loads skill content on-demand rather than consuming tokens on every request. **Persistent memory** via MEMORY.md enables cross-session learning that static instruction files cannot provide.

The distinction matters practically: instruction files (AGENTS.md, CLAUDE.md, copilot-instructions.md) can encode project context, coding standards, and workflow preferences effectively. They cannot enforce tool restrictions, isolate context windows, route models, or execute deterministic hooks. **For persona and domain knowledge, instructions suffice. For mechanical constraints, agent definitions are irreplaceable.**

---

## Copilot's native modes handle the basics — custom agents handle the specifics

VS Code's Copilot architecture as of early 2026 provides three built-in local agents: **Agent** (autonomous coding with full tool access), **Plan** (read-only structured planning), and **Ask** (informational Q&A without code changes). The Plan agent creates structured implementation plans using only read-only tools, saves them to session memory, and offers handoff to implementation — essentially a native planning-then-implementing workflow built into the IDE.

Custom agent.md files sit alongside these native modes in the Agents dropdown and provide capabilities the built-in modes cannot:

Custom agents support **YAML frontmatter** specifying tool subsets, model priority lists, handoff workflows, subagent coordination, lifecycle hooks, and MCP server configurations. A security review agent can be locked to read-only tools with a specific model preference and custom instructions enforcing a review checklist. An architecture agent can hand off to an implementation agent with a single button click, passing context through a structured workflow. These are configurations the native Agent/Plan/Ask modes don't expose.

The relationship is complementary, not redundant. Native modes provide **general-purpose configurations**; custom agents provide **team-specific specializations**. A custom planning agent can override the built-in Plan agent's behavior with your team's specific planning methodology, architectural patterns, and technology constraints. The built-in Plan agent generates generic implementation plans; a custom architecture agent generates plans following your team's ADR format, referencing your specific infrastructure constraints, and routing through your preferred approval workflow.

The instruction hierarchy matters: `.github/copilot-instructions.md` provides always-on project context, `.instructions.md` files provide glob-scoped rules (e.g., React patterns for `**/*.tsx`), and `.agent.md` files provide switchable persona configurations with mechanical constraints. VS Code also supports `.claude/agents/` for cross-tool compatibility and AGENTS.md for the emerging cross-platform standard supported by Copilot's coding agent, Codex, Cursor, and Gemini CLI.

---

## Cognitive lane isolation works, but through focus rather than identity

The evidence for constraining agent scope is strong, with a clear mechanistic explanation. Anthropic's own engineering team found that when Claude attempted to build a full application without scope constraints, it tried to "one-shot" everything, ran out of context mid-implementation, and left features half-implemented. **With cognitive lane isolation** — constraining each session to work on one feature at a time with structured handoffs — the same model produced production-quality incremental code with proper testing and documentation.

The AgentCoder research quantified this: multi-agent decoupling with specialized Programmer, Test Designer, and Test Executor agents "typically doubles or better the margin of accuracy improvements gleaned from prompt engineering alone." Ablation studies found removing any specialized agent caused significant performance degradation, "underscoring the necessity of agent specialization and iterative correction." ACL 2024 research on prompt chaining confirmed three mechanisms: cognitive focus (each subtask isolates a single objective), typed interfaces (clear boundaries enable quality measurement), and iterative refinement (systematic checkpoints catch errors).

However, Amazon Science's research blog warns against overengineering: "Excessive decomposition can increase complexity and coordination overhead to the point of diminishing returns," sacrificing "the novelty and contextual richness that LLMs can provide by capturing hidden relationships within the complete context." Google DeepMind's landmark study of 180 configurations quantified the trade-off precisely: multi-agent coordination yields highest returns when **single-agent baseline accuracy is below 45%**. If the base model already hits 80% accuracy on a task, adding agents may introduce more noise than value. Accuracy gains saturate around **four agents** without proper hierarchical topology.

The practical takeaway: cognitive lane isolation works not because telling Claude "you are only an architect" changes its reasoning, but because **constraining tool access, limiting context scope, and focusing each session on a single concern** prevents the failure modes that frontier models still exhibit on complex, multi-step tasks.

---

## The industry is converging on structured minimalism

Every major framework author and AI lab has arrived at essentially the same position: **start with the simplest solution possible, and add agent complexity only when demonstrably needed.**

Anthropic's guidance progression — augmented LLM → compositional workflows → autonomous agents — emphasizes that "this might mean not building agentic systems at all." OpenAI's practical guide states: "Start with a single agent and evolving to multi-agent systems only when needed." Microsoft's merged Agent Framework documentation advises: "If you can write a function to handle the task, do that instead of using an AI agent." Even CrewAI, whose entire product is multi-agent teams, recommends starting with two agents.

The quantitative research supports specific guidance. Anthropic's multi-agent research system uses an orchestrator with **3–5 subagents** for parallel work, and their internal evaluation showed this outperformed single-agent by **90.2%** on research tasks — but only because research is inherently parallelizable. For sequential coding tasks, Google DeepMind's data shows single-agent approaches consistently outperform multi-agent configurations. The practical minimum viable agent set for software development appears to be **two to three agents**: a planning/orchestrating agent (broad context, read-heavy), an implementation agent (code editing, test running), and optionally a review/validation agent (read-only verification).

The broader industry trend is clearly toward multi-agent systems — Gartner reported a **1,445% surge** in multi-agent system inquiries from Q1 2024 to Q2 2025 — but simultaneously, research shows that multi-agent benefits diminish as base model capabilities improve. A May 2025 study found that "the benefits of MAS over SAS diminish as LLM capabilities improve." This creates an interesting tension: the industry is adopting multi-agent architectures at the exact moment the underlying models are becoming capable enough to reduce their necessity. The likely resolution is that multi-agent patterns will persist for genuinely parallelizable work and hard isolation requirements, while single-agent-with-good-instructions will handle the majority of sequential development tasks.

---

## Conclusion: the agent definition as an engineering contract

The research converges on a clear framework for deciding when custom agent definitions earn their keep. **Three conditions justify a dedicated agent**: the task requires hard tool restrictions that cannot be advisory, the work benefits from context window isolation (either for focus or parallelism), or the workflow demands structured handoffs between distinct phases. If none of these apply, a well-written instruction file achieves the same result at lower complexity.

The persona component of agent definitions — the "You are a Software Architect" identity framing — is the least valuable part of the entire construct. It persists in agent.md files mostly as documentation for human operators, not as a meaningful behavioral lever for frontier models. What matters is the mechanical contract: which tools can this agent touch, what context does it see, which model processes its requests, and what deterministic checks gate its actions.

For teams that have consolidated from many agents to few, the research suggests a practical floor of **two to three agents** for complex software development workflows, with the recognition that a single agent plus good instruction files handles most day-to-day coding tasks effectively. The optimal architecture treats agent definitions not as character sheets for AI role-play, but as **engineering contracts** — precise specifications of capability, scope, and constraint that the scaffolding layer enforces mechanically, regardless of what the model might otherwise choose to do.