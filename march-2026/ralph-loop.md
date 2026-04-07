The following is a conversation history between me and Gemini:

Question:
Given the provided agents, how can I restructure them to use a Ralph Loop? Which of the agents are suitable for this?

Response:
To implement a "Ralph Loop" (or autopilot mode), you must transition your agents from a conversational, turn-based workflow into a continuous `while` loop where the agent actively tests and validates its own work before ever returning control to you.

Here is a breakdown of which agents are suitable for this approach and exactly how to restructure them.

### Which Agents are Suitable?

A Ralph Loop requires concrete, mechanically verifiable outputs (like compiling code, passing tests, or rendering a UI). Therefore, not all of your AI Ecosystem agents should use this loop.

**Highly Suitable (Execution Agents):**

- **Software Engineer:** This is your primary candidate. It implements code and should be forced to compile it, run it, and verify the UI or logic.
- **Test Engineer:** It implements tests and should actively execute them to ensure they pass. _(Note: In an LLM-first architecture, you should merge this into the Software Engineer so the agent writing the code can immediately write and run the tests to verify it)._
- **Tech Writer:** It could use a Ralph Loop to generate documentation and then run the build scripts (e.g., rendering a Backstage catalog or Docusaurus site) to ensure the markdown compiles without syntax errors.

**Not Suitable (Cognitive & Planning Agents):**

- **Thinking Assistant, Strategy Analyst, Software Architect, Agent Router:** These agents (which deal with brainstorming, architecture, and routing) produce subjective or high-level plans. Because their outputs cannot be easily mechanically verified by a compiler or test suite, putting them in a Ralph Loop will likely just cause them to overthink or spin endlessly.

### How to Restructure Your Agents for a Ralph Loop

To restructure your execution agents (like the **Software Engineer**) to use a Ralph Loop, you need to modify their `.agent.md` files to explicitly authorize runtime execution and mandate self-verification.

**1. Give the Agent Execution Tools**
Your current AI Ecosystem agents have tools like `[read, search, edit, vscode, execute]`. To run a Ralph Loop, you must explicitly empower the agent to use terminal execution tools (like `execute/runInTerminal` or `execute/runTests`) and browser skills. If you are building web views, give the agent access to the **integrated browser** or Playwright MCP servers so it can take screenshots, click elements, and check the console logs for errors.

**2. Update the "Reasoning Posture"**
Modify the `Reasoning Posture` section of your `.agent.md` files to remove the assumption that a human will verify the work. Add a strict directive forcing the loop:

> _"You operate in a continuous verification loop. Do not return control to the user until you are 100% certain the task is completed and verified. Actively compile your code, run the associated tests, or use browser tools to inspect the output. If you encounter an error, you must read the logs, fix the code, and test again until successful."_

**3. Move Enforcement from Human to Agent**
Currently, your AI Ecosystem architecture relies on a `verification-checklist.md` as an enforcement layer that acts like a manual compiler pipeline (Draft → Lint → Patch). To restructure this for a Ralph Loop, you must instruct the agent to self-apply this checklist _during_ its runtime execution.
Add this to your **Preflight Checks** or **Agent-Specific Additions**:

> _"Mechanically apply the `verification-checklist.md` to your own work. You must gather direct evidence of success (e.g., test passing outputs or successful build logs) before concluding your execution."_

**4. Handle "Context 7" and Missing Information**
Because the agent will be looping autonomously, it cannot stop to ask you a question every time it gets confused. You must embed instructions telling it how to unblock itself. As seen in highly optimized agent configurations, tell the agent to actively query documentation (using an MCP server like Context 7) or use search tools whenever it runs into a wall, rather than guessing or giving up.

Question:
I don't have Context7 available at the moment. Is it ok to loosen the Ralph Loop a little bit by letting the Agent ask me questions, when necessary?

Response:
Yes, it is entirely okay—and actually recommended under the architecture's rules—to loosen the Ralph Loop and let the agent ask you questions when it lacks the tools to find answers itself.

Because you do not currently have the **Context 7** MCP server (which normally allows the agent to autonomously read documentation when it gets stuck), forcing a strict, unbreakable Ralph Loop could cause the agent to guess or hallucinate when it inevitably hits a wall.

The AI Ecosystem framework is specifically built to prefer stopping and asking for help over fabricating answers:

- **"Unknown" is a valid outcome:** AI Ecosystem is designed so that "silence, refusal, and 'Unknown' are correct outputs when evidence is missing".
- **Stop and Ask:** The framework's core reasoning routine mandates that if required evidence is missing or unreadable, the agent must **"STOP (do not guess)"** and "request the minimum missing input".
- **Software Engineer Rules:** Your execution agent is explicitly instructed to "Ask for minimum files if repo access is limited".

To safely loosen your Ralph Loop, you should modify the agent's prompt to include a fallback condition. For example, you can instruct it: **"Do not return to the user until you are 100% sure the task is closed, but if you are not 100% sure or lack the necessary documentation, you must stop and tell me"**.

This adjustment ensures the agent still tries to work as autonomously as possible, but safely hands control back to you for guidance instead of making up incorrect code or spinning endlessly in a broken loop.

Question:
What steps should I take to start implementing this restructuring?

Response:
To start implementing this LLM-first restructuring for your AI Ecosystem ecosystem, you should tackle the transition in practical, phased steps. Based on the principles of agent orchestration, skills, and the "Ralph Loop", here is the exact step-by-step blueprint to transform your architecture:

### Step 1: Delete Obsolete Agents and Set Up the Orchestrator

First, clean house by removing the deep human-centric hierarchies that slow down the AI.

- **Delete the redundant agents:** Remove `agent-router.agent.md`, `test-architect.agent.md`, `test-engineer.agent.md`, `tech-debt-analyst.agent.md`, `tech-debt-resolver.agent.md`, `strategy-analyst.agent.md`, `feature-engineer.agent.md`, `code-analyst.agent.md`, and `tech-writer.agent.md` from your ecosystem.
- **Create the Orchestrator:** Replace the old "Agent Router" with a supreme Orchestrator custom agent. Configure this agent to use **Claude 3.5/4.5 Sonnet**, as it is highly "agentic" and eager to manage tasks.
- **Set Orchestrator Guardrails:** In the Orchestrator's markdown file, explicitly state: _"You break down complex requests into tasks and delegate them to specialist sub-agents. You coordinate work but you never implement anything yourself."_. You must also explicitly list the names of the remaining sub-agents (e.g., Software Architect, Software Engineer, Code Reviewer) so it knows who it can call.

### Step 2: Collapse Procedures, Templates, and Wiring into Skills

Currently, AI Ecosystem scatters logic across `*.procedure.md`, `*.template.md`, and `*.prompt.md` files. You need to collapse these into monolithic, on-demand **Skills**.

- **Create a Skills Folder:** Create a `.github/skills/` directory (or use a global `copilot-skills` folder).
- **Build `skill.md` files:** For a workflow like "Tech Debt Remediation", bundle the procedural steps, the expected structural template, and any execution scripts into a single `skill.md` file.
- **Optimize Front Matter:** At the top of each `skill.md`, write a very explicit description in the front matter (e.g., _"invoke this skill whenever you are asked to remediate tech debt"_). This ensures the agent dynamically loads the context _only_ when relevant, keeping the context window pristine.

### Step 3: Empower the "Software Engineer" with a Ralph Loop

Transform your `software-engineer.agent.md` from a conversational coder into an autonomous execution agent.

- **Grant Terminal & Browser Tools:** Ensure the agent's tool configuration explicitly includes terminal execution tools (like `execute/runInTerminal` or `execute/runTests`) and browser tools (like `vscode/openSimpleBrowser` or Playwright) so it can mechanically verify its work.
- **Rewrite the Reasoning Posture:** Update the `software-engineer.agent.md` to mandate the Ralph Loop: _"You operate in a continuous verification loop. Do not return control to the user until you have actively compiled your code, run the associated tests, or used browser tools to inspect the output and verify success."_.
- **Add the Fallback Clause:** Because you don't have the Context 7 documentation server, add the safety valve we discussed: _"If you are not 100% sure, or if you lack the necessary documentation to unblock an error, you must stop and ask me for guidance rather than guessing."_.

### Step 4: Automate the Enforcement and Constitution Layers

Move away from requiring a human to manually pass an agent's draft through the `verification-checklist.md`.

- **Shift Enforcement to the Agent:** In your execution agent's preflight checks, add a directive instructing it to mechanically self-apply the `verification-checklist.md` and gather direct evidence of success _during_ its runtime execution.
- **Enable Self-Updating Instructions:** To prevent your global `copilot-instructions.md` constitution from experiencing "drift" as the codebase evolves, embed a rule in your active agents (like the Orchestrator and Software Engineer) instructing them to automatically update the instructions file every time they learn or change something structural in the product.

### Step 5: Test the Handoff Workflow

Once the files are restructured, test the flow using the **Agent Handoff** methodology.

1.  Open VS Code and start locally in Plan Mode with your **Software Architect** to brainstorm a feature or map out the architecture.
2.  Once you like the plan, invoke the **Orchestrator** and tell it to implement the high-value ideas.
3.  Watch as the Orchestrator delegates the implementation to your **Software Engineer** sub-agent, which will pull in the necessary monolithic **Skills**, write the flat code, run its own tests in the Ralph Loop, and only report back once it succeeds.

Question:
How do I create a monolithic skill to replace multiple fragmented layers?

Response:
To transition away from AI Ecosystem's fragmented 7-layer taxonomy into an LLM-first architecture, you need to collapse your scattered procedures, templates, and task-wiring into a single **Agent Skill**.

Skills are essentially modular packages that bundle instructions, scripts, and templates together. They are only pulled into the AI's context window _on demand_ when relevant, which prevents context bloat and eliminates the need for the agent to chase down references across multiple files.

Here is the step-by-step process to create a monolithic skill that replaces your fragmented AI Ecosystem layers:

**1. Create the Skill Folder and File**
Instead of having a `.prompt.md`, a `.procedure.md`, and a `.template.md` in different directories, create a single dedicated folder for the task.

- Inside your repository, create a directory like `.github/skills/tech-debt-remediation/` (or place it in your user-level `copilot-skills` folder).
- Inside that folder, create a single markdown file named exactly `skill.md`.

**2. Add the "Wiring" (Front Matter)**
In the AI Ecosystem framework, `*.prompt.md` files and the Agent Router dictate when a task is executed. In a skill, this is replaced entirely by the metadata at the very top of the `skill.md` file.

- You **must** include a `name` and a `description` in the front matter.
- The model actively reads the description to decide whether to automatically pull this skill into the context window. Be highly specific. For example: `invoke this skill whenever you are asked to remediate tech debt`.

**3. Embed the "Procedure" (The Steps)**
Next, take the ordered step-by-step execution playbook from your old `*.procedure.md` files and paste them directly into the body of the `skill.md` file.

- Use strong, directive language. The sources note that writing instructions as "you must do X" yields much higher success rates than writing them as loose advice.
- Include instructions telling the agent to actively run terminal commands, compile code, or use the browser to verify its own work, creating your **Ralph Loop**.

**4. Integrate the "Structure" and "Enforcement"**
AI Ecosystem previously forced the agent to load a separate `.template.md` to know how to format its output and a `verification-checklist.md` to know if it succeeded.

- **For Templates:** You can either paste the template structure directly into the `skill.md` body, or place a `template.md` file in the exact same skill folder and tell the skill to reference it using a relative path (e.g., `Respond with the ./template.md`).
- **For Enforcement:** Add the specific pass/fail criteria directly to the bottom of the skill. Instruct the agent that it cannot return the final output until it has mechanically validated these rules against its own work.

### Example Monolithic `skill.md`

Here is what the consolidated file looks like:

```markdown
---
name: Tech Debt Remediation
description: Invoke this skill whenever the user asks you to fix, resolve, or remediate technical debt in the codebase.
---

# Tech Debt Remediation Skill

## 1. Procedure

You must follow this workflow exactly:

1. Read the provided tech debt report to understand the structural problem.
2. Formulate a plan to refactor the code without changing observable behavior.
3. Identify the shared structure first before scaffolding or editing any files.
4. Execute the code changes.

## 2. Autonomous Verification (Ralph Loop)

You operate in a continuous verification loop. Do not return control to the user until you have done the following:

- Run the build tools (`npm run build` or equivalent) to ensure your changes compile.
- Run the test suite (`npm run test`) to ensure no existing behavior was broken.
- If a test fails, read the logs, fix your code, and run the tests again.

## 3. Output Structure

Once verified, respond using the exact format defined in `./remediation-template.md`.
```

By structuring your ecosystem this way, you create an **Obvious Entry Point**. The agent reads one file, understands the trigger, knows the steps, knows the format, and knows how to verify the work, all within a single isolated context window.

Question:
How can I set up an Orchestrator and sub-agents?

Response:
To set up an orchestrator and sub-agents in Visual Studio Code, you can use the "configure custom agent" feature to create a lightweight orchestration framework. This setup relies on one main "Orchestrator" agent that acts as a project manager, delegating tasks to multiple specialized "Sub-Agents" (such as a planner, coder, and designer).

Here is how you can configure each part of this ecosystem:

### 1. Setting up the Orchestrator Agent

The orchestrator's sole responsibility is to break down complex requests, coordinate workflows, and delegate tasks to specialists.

- **Model Choice:** Use **Claude Sonnet 4.5**, as it is highly "agentic" and eager to drive tasks forward, making it an excellent project manager.
- **Tools:** Configure the orchestrator with only two tools: `agent` (which gives it the ability to call the sub-agents) and `memory`.
- **Prompt Configuration:** Explicitly instruct the agent: _"you break down complex requests into tasks and delegate them to specialist sub-agents. You coordinate work but you never implement anything yourself"_.
- **Sub-agent Awareness:** You must explicitly list the exact names of the sub-agents it is allowed to call directly in its prompt (e.g., "they are planner, coder, and designer").
- **Anti-Micromanagement Guardrails:** Orchestrator models often think they know everything and will try to dictate exact code changes. You must include strict rules forbidding the orchestrator from telling the sub-agents _how_ to do their work.

### 2. Setting up the Sub-Agents

Sub-agents do the actual heavy lifting. You can configure each sub-agent to use a different underlying model depending on what it is best at.

- **The Planner Agent:**
  - **Role:** Takes the initial requirements and builds a plan.
  - **Prompt:** Keep it simple: _"you create plans you do not write code"_. Give it access to all tools so it can read the workspace.
- **The Coder Agent:**
  - **Role:** Writes the actual implementation based on the plan.
  - **Model & Tools:** Assign it a coding-optimized model and provide tools like MCP servers (e.g., Context 7) so it can read documentation.
  - **Prompt:** To counter the orchestrator's tendency to micromanage, explicitly tell the coder: _"question everything you're told make your own decisions"_. This is also where you should enforce your mandatory coding principles (like preferring flat, explicit code).
- **The Designer Agent:**
  - **Role:** Handles UI, UX, and styling.
  - **Model:** Assign it a model that excels at design generation (e.g., Gemini 3 Pro).
  - **Prompt:** Give it full creative autonomy, explicitly telling it to focus on usability and aesthetics, and again warning it not to let the orchestrator dictate its job.

### How they work together

Once set up, you only need to interact with the Orchestrator. The orchestrator will call the sub-agents in parallel or sequentially. Because sub-agents operate inside their own isolated context windows, they can generate thousands of lines of code or read extensive documentation without polluting the main orchestrator's context window. Once a sub-agent finishes its task, its isolated context is destroyed and it simply returns the relevant results back to the orchestrator.

Question:
Show me a template for a monolithic skill.md file.

Response:
Here is a template for a monolithic `skill.md` file that collapses your fragmented layers into a single, on-demand context window for the AI.

You should place this file inside a dedicated folder for the specific task, such as `.github/skills/feature-development/skill.md`.

```markdown
---
name: [Skill Name, e.g., Feature Specification & Implementation]
description:
  [
    Highly specific trigger,
    e.g.,
    Invoke this skill whenever the user asks you to implement a new feature,
    build out a spec,
    or create new functionality in the application.,
  ]
---

# [Skill Name]

## 1. Procedure

You must follow this workflow exactly to complete the task:

1. **Analyze Requirements:** Read the provided problem statement or goals to understand the scope.
2. **Identify Shared Structure:** Before scaffolding or editing any files, explicitly identify the shared structure and dependencies required.
3. **Execute Implementation:** Write the code changes required to fulfill the goal. Prefer flat, explicit code over deep hierarchies or abstractions.

## 2. Autonomous Verification (Ralph Loop)

You operate in a continuous verification loop. Do not return control to the user until you have actively verified your work using the following steps:

- Run the build tools (e.g., `npm run build`) to ensure your changes compile successfully.
- Run the test suite (e.g., `npm run test`) to ensure no existing behavior was broken and the new feature works.
- If a test fails or the build breaks, you must read the logs, fix your code, and test again until successful.
- _Fallback:_ If you lack the necessary documentation to unblock an error, you must stop and ask the user for guidance rather than guessing.

## 3. Enforcement Gates

You must mechanically validate your work against these pass/fail criteria before considering the task complete:

- [Criteria 1, e.g., No new dependencies were introduced without explicit user approval.]
- [Criteria 2, e.g., The code contains no 'TODO' or 'FIXME' comments.]

## 4. Output Structure

Once your work is complete and fully verified, respond using the exact format defined below:

### Summary of Changes

[A brief explanation of what was implemented]

### Verification Evidence

[Paste the successful build or test logs here proving the code works]
```

### Breakdown of the Monolithic Skill Components

- **Front Matter (The Wiring):** The top of the file contains YAML front matter with a **name** and **description**, which are strictly required to define the skill. This replaces your old Agent Router and `.prompt.md` files. The model actively reads this description to decide whether to automatically pull the skill into the context window when you ask it a question, so it is crucial to be as descriptive as possible about when it should trigger.
- **Procedure (The Playbook):** This section replaces your scattered `.procedure.md` files. Instead of writing instructions as loose advice, you should use strong, directive language like "you must do X," which yields much higher success rates from the AI.
- **Autonomous Verification (The Ralph Loop):** This section empowers the agent to verify its own work. Instead of waiting for a human to apply a verification checklist, you explicitly instruct the agent to run terminal scripts, compile code, or gather system information to prove the task was successful.
- **Enforcement Gates:** This replaces the need for a global, "always-on" `verification-checklist.md`. By bringing the specific pass/fail criteria directly into the skill, the AI only has to process the rules that are immediately relevant to the task it is performing.
- **Output Structure:** This replaces your `.template.md` files. You can either embed the expected markdown structure directly into the bottom of the skill file, or you can place a separate template file in the same folder and instruct the skill to reference it using a relative path, such as `./template.md`.

Question:
How do I create an Orchestrator agent in VS Code?

Response:
To create an Orchestrator agent in VS Code, you can use the "configure custom agent" feature to define a specialized custom agent that coordinates workflows rather than writing code.

Here is how you should configure the Orchestrator agent:

- **Select the Right Model:** Choose a highly "agentic" model like **Claude Sonnet 4.5**. This model acts like an eager project manager that wants to drive tasks forward, making it ideal for orchestration, even if it isn't the best at writing the actual code.
- **Configure Tools:** Limit the orchestrator to only two tools: the **`agent`** tool (which gives it the ability to call other sub-agents) and the **`memory`** tool.
- **Define the Core Prompt:** Keep the main prompt simple and direct. Instruct it: _"You are a project orchestrator. You break down complex requests into tasks and delegate them to specialist sub-agents. You coordinate work but you never implement anything yourself"_.
- **List Available Sub-agents:** You must explicitly tell the orchestrator the exact names of the sub-agents it is allowed to call (for example, "they are planner, coder, and designer").
- **Add Anti-Micromanagement Guardrails:** Orchestrator models tend to be overconfident and will often try to tell sub-agents exactly what lines of code to change. You must include strict rules lower down in the prompt explicitly forbidding the orchestrator from telling the sub-agents _how_ to do their work.

Once configured, this agent will sit at the top of your agent ecosystem, breaking down your requests and delegating them to sub-agents in parallel, each of which will run in its own isolated context window.

Question:
How do I add a Ralph Loop to my Engineer?

Response:
To add a "Ralph Loop" (also known as autopilot mode) to your Software Engineer agent, you need to transition it from a conversational agent into one that continuously tests and verifies its own code. A Ralph Loop is essentially "a while loop in which the agent tries to work to absolute completion".

Here are the specific steps to modify your `software-engineer.agent.md` file to implement this:

**1. Leverage Execution Tools**
Your current `software-engineer.agent.md` already includes `execute` in its tool array (`tools: [read, search, agent, search, edit, todo, vscode, execute]`). This is perfect, as it gives the agent permission to run terminal commands. If you are building web interfaces, you should also give it access to an **agent browser skill** so it can autonomously navigate to the local host, take screenshots, and verify that the UI renders correctly without you having to check it manually.

**2. Update the Reasoning Posture**
Currently, your Software Engineer's `Reasoning Posture` tells it to favor "minimal, safe changes" and highlight risks. You need to rewrite this section to mandate self-verification. Add explicit instructions telling the agent to **"always check your work before returning control to the user"**. Instruct it to actively run your build tools or Jest test suite (which is already in its authorized domain) and read the terminal outputs to fix any errors it encounters.

**3. Add the "100% Sure" Rule with a Fallback**
To enforce the loop, you must explicitly instruct the agent not to stop working until it has concrete proof of success. Add this directive to the prompt: **"don't come back to me until you're 100% sure that the loop is closed"**.
However, to prevent the agent from spinning endlessly if it gets completely stuck, you must include a fallback clause: **"if you're not 100% sure then you need to tell me out the other side"**.

**4. Modify the Preflight Checks**
In your current `software-engineer.agent.md` file, the `Agent-Specific Additions` section contains a rule to "List validation steps as conditional if tests/build tools are not specified". For a Ralph Loop, you should remove this. Instead of just listing validation steps, mandate that the agent must actively discover the test commands and execute them to gather direct evidence of success before concluding the task.

Question:
What does a custom agent Orchestrator file look like?

Response:
Based on the provided walkthrough of a custom orchestration framework, an Orchestrator agent file is a relatively short markdown file. Here is a structural representation of what that file looks like:

```markdown
---
name: Orchestrator
description: A project manager that delegates tasks to sub-agents.
model: Claude Sonnet 4.5
tools: [agent, memory]
---

# Orchestrator Agent

## Role

You are a project orchestrator. You break down complex requests into tasks and delegate them to specialist sub-agents. You coordinate work but you never implement anything yourself.

## Available Sub-Agents

You have access to the following sub-agents to complete tasks:

- planner
- coder
- designer.

## Workflow

1. Understand the request.
2. Plan and break it down into steps.
3. Delegate tasks to the appropriate sub-agents.
4. Coordinate between the agents depending on the work that was done.
5. Report the final results back to the user.

## Rules (Anti-Micromanagement)

- **Don't tell sub-agents how to do their work.**
- Do not give them the exact lines of code to change. Let the specialists make their own decisions.
```

Here is a breakdown of why the file is structured this way:

- **The Model:** The file specifies **Claude Sonnet 4.5** because it is highly "agentic" and eager to drive tasks forward, making it the perfect project manager.
- **The Tools:** The orchestrator is restricted to only two tools: the **`agent`** tool (which gives it the ability to invoke the sub-agents) and the **`memory`** tool. It is not given tools to read or write files directly because it is not allowed to do the work itself.
- **Sub-Agent Awareness:** You must explicitly tell the orchestrator the exact names of the sub-agents it is allowed to call so it knows who is on its "dev team".
- **The Guardrails:** The model will naturally think it knows everything and will try to micromanage the coder and designer agents. The rules section at the bottom is critical for forcing the orchestrator to step back and just act as a logistics coordinator.

Question:
Which AI Ecosystem layers should I combine into one skill?

Response:
To transition your AI Ecosystem ecosystem into an LLM-first architecture using a monolithic `skill.md` file, you should combine **four specific layers** of the 7-layer AI Ecosystem taxonomy.

By collapsing these task-specific layers, you eliminate the "referenced ≠ read" hallucination vector and prevent the agent from having to chase dependencies across scattered files.

Here are the specific AI Ecosystem layers you should combine into a single skill:

**1. Wiring (`*.prompt.md`)**

- **AI Ecosystem Role:** Prompts act as the "task-level glue" that selects an agent, declares the evidence scope, and references procedures and templates.
- **How it translates to a Skill:** The prompt layer becomes the YAML front matter (`name` and `description`) at the very top of your `skill.md` file. The model reads this description to dynamically decide when to pull the skill into its context window, replacing the need for manual task routing.

**2. Procedures (`*.procedure.md`)**

- **AI Ecosystem Role:** Procedures are playbooks containing ordered steps, stop conditions, and propagation passes.
- **How it translates to a Skill:** You extract the step-by-step instructions from the procedure file and paste them directly into the body of the `skill.md`. This becomes the core execution playbook for the agent.

**3. Structure (`*.template.md`)**

- **AI Ecosystem Role:** Templates define headings, placeholder lists, and the required section structure for the final output.
- **How it translates to a Skill:** Instead of forcing the AI to load a separate template file, you embed the expected markdown structure directly at the bottom of the `skill.md` file, or place the template file in the exact same skill folder and instruct the skill to reference it locally.

**4. Enforcement (`verification-checklist.md`)**

- **AI Ecosystem Role:** In AI Ecosystem, enforcement is a global checklist that acts as the single owner of pass/fail criteria.
- **How it translates to a Skill:** Instead of polluting the context window with global rules, you extract only the specific pass/fail criteria relevant to the task and place them directly into the skill. This allows the execution agent to self-verify its work (via the "Ralph Loop") against these gates before completing the task.

**What about the other three layers?**
You do not bundle the remaining three layers into the task-specific skill:

- **Constitution (`copilot-instructions.md`):** Keep this as a global file for absolute, universal epistemic rules (e.g., "never fabricate").
- **Cognition (`*.agent.md`):** This remains your actual sub-agent configuration (e.g., your Software Engineer or Software Architect).
- **Context (`.github/context/*.md`):** Keep these as separate, descriptive grounding files (like repository maps) that the agent only reads when attempting to understand the broader system.

Question:
Can you show me a prompt to automate the 'Self-updating Instructions'?

Response:
To automate "Self-updating Instructions," the prompt you need to use is remarkably simple. You just need to add this exact directive to your active agent's rules:

> **"update the copilot instructions file every time it learns something or changes something in the product"**.

### How to implement it:

You should embed this rule directly into the markdown configuration file of your most active execution agents, such as your `software-engineer.agent.md` or your Orchestrator agent. You can place it in the "Reasoning Posture" or "Rules" section of the file.

### Why this works:

Instruction files are designed to provide "always-on" global context, but they notoriously "get out of date almost instantly" as you build new features or change architectural patterns. By adding this single line to an agent that is constantly making changes (like your coder sub-agent), you turn the AI into the maintainer of its own governance framework.

Instead of you manually syncing the `copilot-instructions.md` file, the agent will automatically rewrite the rules in the background to ensure your repository's reality never drifts from its documentation.
