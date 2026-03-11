Specification: LLM-First CLASP Restructuring for VS Code Agents

1. Architectural Transition: From 7-Layer Sprawl to Monolithic Skills

Architectural Mandate: We are standardizing the transition from the legacy 7-layer taxonomy of CLASP (Constitution, Enforcement, Cognition, Procedure, Wiring, Structure, and Context) into a streamlined, LLM-first architecture of Monolithic Skills. This restructuring optimizes agent performance by reducing context sprawl while maintaining the epistemic rigor required to prevent "laundry uncertainty"—where an agent hides gaps in knowledge behind confident phrasing.

While most layers collapse into skill-specific directories, the Structure (*.template.md) layer must remain a rigid, immutable skeleton. This ensures that the agent cannot deviate from the defined interface or invent content where evidence is missing; an empty section under a heading is the only acceptable output for missing context.

Transformation Mapping Table

Legacy CLASP Layer	New Monolithic Location	Functional Responsibility
Constitution	/.github/copilot-instructions.md	Supreme epistemic laws: truth > helpfulness > speed.
Enforcement	/.github/verification-checklist.md	Canonical pass/fail gates and evidence-gathering rules.
Cognition	/.github/skills/{skill-name}/*.agent.md	Specialist reasoning posture and authorized domain limits.
Procedures	/.github/skills/{skill-name}/*.procedure.md	Explicit execution playbooks and change-propagation steps.
Wiring	/.github/skills/{skill-name}/*.prompt.md	Task-level tool selection and output shape definitions.
Structure	/.github/templates/*.template.md	Rigid interfaces; enforces "Unknown" over fabrication.
Context	/.github/skills/{skill-name}/resources/	Read-only domain grounding and component catalogs.


--------------------------------------------------------------------------------


2. The Monolithic Skill Folder Specification

Skill Folder Directory Structure

Each specialist capability must be encapsulated in a discrete directory located at /.github/skills/{skill-name}/. These folders must be discoverable via @ or / commands in the VS Code Copilot Chat and contain:

1. Unified Instructions: Markdown files integrating cognition contracts and task wiring.
2. Scripts & MCP Servers: Executable logic and Model Context Protocol (MCP) server configurations (e.g., context7 for documentation reading) that the skill may invoke.
3. Resources: Grounding data, system maps, and read-only references.

Skill Integration Logic: The "Referenced ≠ Read" Safeguard

To eliminate the primary vector for hallucination—where an agent claims to follow a playbook it never actually loaded—all skill integrations must enforce the following logic:

* Explicit Invocation: The agent must attempt to read the procedure file at the start of any task.
* Hard Stop Condition: If a procedure or context file is unreadable or missing, the agent MUST STOP and request the input verbatim from the user. It is strictly prohibited from guessing or approximating steps.
* Discovery: Skills must be configured for the @ (agent mention) and / (slash command) registries, ensuring specialists like @designer or /refactor load only the required context.


--------------------------------------------------------------------------------


3. Orchestrator/Sub-Agent Hierarchy Configuration

The Orchestrator Role (Logistics/PM Only)

The Orchestrator functions as a technical PM. It manages the mission but never touches the code.

* Constraint: The Orchestrator must operate under a strict Anti-Helpfulness Rule. It is authorized only to decompose requests, delegate to specialists, and coordinate results.
* Rationalization: Models "want" to be helpful and often attempt to implement code themselves. The Orchestrator must be prohibited from providing implementation lines to sub-agents to prevent authority leakage.

Model Selection Rationale

* Orchestrator: Claude 3.5 Sonnet. Chosen for its high agency and "eager Labrador" energy. It is excellent at following complex logistics but is outclassed in implementation precision.
* Planner & Coder: GPT-4o / Codex. Prescribed for logic-heavy task breakdown and superior "coding chops." These models handle the implementation work delegated by Sonnet.
* Designer: Gemini 1.5 Pro. Utilized specifically for UI/UX aesthetics and styling, where it consistently outperforms other frontier models.

Context Isolation: The "Magic of Sub-agents"

To support massive code generation (e.g., 2,700+ lines) without bloating the primary conversation, the Orchestrator must use the Agent Tool to spawn sub-agents in isolated windows.

* Isolation Protocol: Sub-agents consume their own context windows. Only final artifacts and success/fail statuses are returned to the Orchestrator.
* Metric: This protocol allows the project to scale infinitely; a sub-agent can process 100k tokens of research while the Orchestrator’s context window remains lean (e.g., under 11K tokens).


--------------------------------------------------------------------------------


4. Implementation of the Ralph Loop (Verification)

The Verification Persona

The "Ralph Loop" is the architectural closing of the loop. An agent cannot assert completion simply because a script ran; it must adopt a Verification Persona that critically audits the result.

Agent Browser Skill Integration

Utilizing the Agent Browser Skill (Playwright + Chrome DevTools Protocol), the agent must:

1. Launch & Render: Boot a local instance of the application.
2. Visual Audit: Take screenshots of the UI to compare the rendered DOM against the requirements in the Structure/Template layer.
3. Log Analysis: Scrape console logs and network traffic via CDP to identify runtime errors invisible to static analysis.

Automated Verification Hooks

Configure VS Code Hooks to trigger the Ralph Loop at key lifecycle points:

* Hook Trigger: post-tool-use or session-stop.
* Action: Automatically run a validation script that forces the agent to document its findings in an Evidence Ledger.
* Epistemic Rule: If the browser cannot render the page or a log is missing, the agent must report "Unknown" rather than "Success."


--------------------------------------------------------------------------------


5. Multi-Agent Session Management & Infrastructure

Mission Control (Agent Sessions View)

All agents must report real-time status to the VS Code Agent Sessions view. This interface acts as the single pane of glass for monitoring local, background, and cloud tasks simultaneously.

Operational Isolation via Git Worktrees

For Background Mode tasks, agents must utilize Git Worktrees.

* Why: Unlike simple branching, Worktrees allow agents to work in isolated workspaces on different branches without taking over the developer's active working directory or requiring manual repo clones. This prevents file-system collisions during parallel execution.

The Sentence Species Model (Five-Second Classifier)

To maintain monolithic instruction integrity, apply the Sentence Species Model. Every sentence in a skill's instruction block must be categorized and separated:

* Style (Voice): Tone and readability (e.g., "Use a professional, architect's tone").
* Teaching (Understanding): Analogies and explanations to help the agent reason.
* Enforcement (Compliance): Pass/fail gates (e.g., "Stop if required context is unreadable").
* Procedure (Steps): Ordered playbooks and propagation passes.
* Wiring (Mechanical): Paths to templates, tools, and output formats.


--------------------------------------------------------------------------------


6. Integrity and Deployment Checklist

Upon completion of the CLASP-to-Monolithic transition, the agent must generate a Model Report Card verifying the following:

Task Component	Architectural Success Criteria
Orchestrator Delegation	Orchestrator successfully delegates to parallel sub-agents without writing code.
Skill Loading	The Monolithic Skill folder is loaded on-demand via slash command/mention.
Referenced ≠ Read	Agent triggers a "Hard Stop" when a required procedure file is removed.
Ralph Loop Execution	Agent Browser Skill captures visual evidence and logs of the implementation.
Worktree Isolation	Background agents operate in distinct worktrees with zero HEAD collisions.
Epistemic Honesty	The agent returns "Unknown" when context is withheld (Silence as Success).
Evidence Ledger	Every claim in the final artifact is mapped to a quote from the source code.

Mandatory Final Verification:

1. Parallel Stress Test: Trigger a "Software Architect" task and verify the sub-agents (Coder and Designer) return results to a Sonnet-led Orchestrator without context pollution.
2. Hook Integrity: Manually stop an agent session and confirm the session-stop hook triggers the automated Ralph Loop browser audit.
3. Epistemic Audit: Confirm that the agent refuses to fill a "Security" section if the .agent.md file excludes security reasoning from its domain. #
