Question:
GitHub just released Copilot CLI, especially the autopilot + fleet features. I want to know how it compares to Ralph Loops. I heard it's better, especially faster and easier to use and uses less premium requests. Please check online sources for more information on it. Could I execute something like:

1. Create architecture + implementation document based on a feature specification (Software Architect)
2. Implement the architecture + implementation document (Software Engineer)
3. Test the implementation (Software Engineer)
4. Do a Code Review (Code Reviewer)

And loop this until the feature is implemented fully?

Answer:
Yes — **you can get very close to that workflow with Copilot CLI**, but there is one important correction:

**Copilot CLI autopilot + `/fleet` is better thought of as a built-in agent orchestrator, not as a full replacement for every Ralph-style outer loop.** It covers a lot of the same ground — autonomous continuation, subagent delegation, parallel task execution, plan mode, custom agents, hooks, and code review — but it does **not** by itself guarantee a strict multi-role “architect → engineer → tester → reviewer → repeat until all acceptance criteria pass” state machine unless you add explicit gates around it. ([GitHub Docs][1])

## The clean comparison

### Ralph Loop

Public Ralph references describe it as an **outer verification loop**: run the agent, verify whether the task is truly done, persist progress outside the model context, then start another iteration — often with fresh context each time. That is the whole point of the pattern. ([GitHub][2])

### Copilot CLI autopilot + `/fleet`

Copilot CLI gives you a **productized inner engine**:

- **plan mode** to create a structured implementation plan before code is written
- **autopilot** to keep working autonomously until Copilot thinks the task is complete
- **`/fleet`** to break work into subtasks and run subagents in parallel where dependencies allow
- built-in agents like **Explore**, **Task**, **General-purpose**, and **Code-review**
- **custom agents** if you want your own “software-architect” or “software-engineer” personas
- **hooks** to log, audit, and block risky actions or enforce policy at execution time
- **`/review`** for terminal-native code review
- **`--resume` / `--continue`** to keep working across sessions. ([The GitHub Blog][3])

So:

- **Ralph Loop** = explicit outer loop, explicit completion gate, often fresh context per iteration
- **Copilot CLI** = built-in autonomous worker/orchestrator with optional subagents, but you still need **objective stop conditions** if you want Ralph-grade rigor. ([GitHub][2])

## Is Copilot CLI “better” than Ralph Loops?

### Better for ease of use: **yes, usually**

Copilot CLI is much easier to use than hand-rolled Ralph loops because the orchestration primitives are already there: plan mode, autopilot, `/fleet`, built-in subagents, hooks, code review, and resumable sessions. You do not have to build the basic machinery yourself. ([The GitHub Blog][3])

### Better for speed: **often yes, but conditionally**

`/fleet` is specifically designed to speed up complex tasks by splitting them into smaller independent subtasks and running them in parallel where possible. GitHub’s own docs say that work such as implementing a feature plus creating tests is often well-suited to this. But it is not magic: if the task is highly sequential or ambiguous, the speedup will be smaller or disappear. ([GitHub Docs][4])

### Better for premium request usage: **not proven**

This is where the internet rumor mill starts wearing clown shoes.

GitHub’s docs **do not** claim that autopilot or `/fleet` uses fewer premium requests than Ralph loops. In fact, for Copilot CLI:

- each prompt uses premium requests according to the selected model’s multiplier
- in **autopilot**, additional autonomous continuation steps also consume premium requests
- more capable models cost more via higher multipliers. ([GitHub Docs][1])

So the honest answer is:

- **it may use fewer requests than a manual back-and-forth workflow** if you avoid lots of human follow-up prompts
- **it is not guaranteed to use fewer requests overall**
- `/fleet` may finish faster, but there is no official source saying it is inherently cheaper in premium-request terms. ([GitHub Docs][1])

## Could you run this workflow?

Yes — **with one refinement**.

Your proposed flow:

1. Create architecture + implementation document based on a feature specification (**Software Architect**)
2. Implement the architecture + implementation document (**Software Engineer**)
3. Test the implementation (**Software Engineer** / Task agent)
4. Do a code review (**Code Reviewer**)
5. Loop until the feature is fully implemented

is absolutely compatible with Copilot CLI’s capabilities, because:

- you can create **custom agents**
- Copilot CLI already has built-in agents for **Task** and **Code-review**
- Copilot may delegate to subagents automatically, and `/fleet` explicitly orchestrates subagents in parallel
- plan mode is designed to create the implementation plan before code is written. ([GitHub Docs][5])

But I would **not** implement it as four totally separate mandatory stages every time. That is elegant on paper and bureaucratic in practice.

## The version I would recommend

### Stage A — Plan first

Use **plan mode** to turn the feature spec into an architecture + implementation plan. That is the natural place for your “Software Architect” role. GitHub explicitly recommends planning before coding, and the typical `/fleet` workflow starts after plan creation. ([GitHub Docs][6])

### Stage B — Implement + test in autopilot + `/fleet`

Then hand the plan to autopilot and `/fleet`. Let Copilot split the work, use subagents, and run tests/builds with the built-in **Task** agent where appropriate. That is closer to how the product is meant to work than manually chaining five isolated agents for every task. ([GitHub Docs][4])

### Stage C — Review explicitly

Run `/review` for code review. That gives you a real reviewer step, and GitHub’s code-review agent is designed specifically to surface genuine issues without lots of noise. ([GitHub Docs][7])

### Stage D — Outer acceptance gate

If tests, lint, build, review, or acceptance criteria fail, then either:

- continue the same session with `--continue` / `--resume`, or
- use a thin script/wrapper around Copilot CLI to repeat the cycle until the gates pass or the iteration budget is exhausted. ([GitHub Docs][8])

That last part is the key: **Copilot CLI handles the inner orchestration; a tiny wrapper gives you Ralph-grade completion discipline.**

## So does Copilot CLI replace Ralph Loops?

### My view

**For many coding tasks, yes — mostly.**
Copilot CLI plus autopilot plus `/fleet` gives you most of the practical benefits people reach for Ralph loops to get:

- autonomous continuation
- decomposition
- subagents
- review
- test/build execution
- resumable sessions
- custom personas
- policy hooks. ([GitHub Docs][1])

### But not fully

If you care about:

- explicit acceptance gates
- deterministic stop conditions
- repeat-until-green behavior
- a true “review says no, go back and fix it” outer cycle
- fresh-context iteration boundaries

then a **thin Ralph-like outer loop still adds value**. That is not a flaw in Copilot CLI. It is just the difference between “autonomous agent” and “formally gated loop.” ([GitHub][2])

## Best-fit workflow for your exact use case

For your EGADS-style, role-driven setup, I would do this:

### Use custom agents

Create:

- `software-architect`
- `software-engineer`
- `code-reviewer`

Copilot CLI supports custom agents defined in `.agent.md` files, and they can be used directly or auto-selected by Copilot when appropriate. ([GitHub Docs][5])

### Use built-ins where they already fit

Do **not** invent custom agents for everything if built-ins already cover it well:

- use **Task** for builds/tests
- use **Code-review** or `/review` for review
- optionally use **Explore** for codebase investigation. ([GitHub Docs][5])

### Use hooks as hard guardrails

Use repository hooks to:

- log prompts
- block dangerous commands
- enforce “tests must pass before claiming done”
- enforce “architecture doc must exist before implementation begins”
- enforce policy around tool usage. GitHub explicitly documents repository-scoped hooks for auditing and blocking high-risk command patterns. ([GitHub Docs][9])

## What I would actually implement

A good first version would be:

1. **Plan mode**
   - “Use the software-architect agent to turn `feature-spec.md` into `architecture-and-implementation.md`.”

2. **Autopilot + `/fleet`**
   - “Implement `architecture-and-implementation.md` using the software-engineer agent. Run relevant tests and builds.”

3. **`/review`**
   - Review the changes.

4. **Outer pass/fail gate**
   - If build/tests/review fail, continue the session with the review findings and retry.

5. **Stop only when**
   - acceptance criteria satisfied
   - tests pass
   - build passes
   - review no longer finds blocking issues

That is the right balance between “use the product’s built-in orchestration” and “don’t trust vibes as a completion criterion.”

## Premium-request reality check

Because this matters for you:

- **Autopilot is not free in request terms**. Each autonomous continuation consumes premium requests, multiplied by model choice. ([GitHub Docs][1])
- GitHub’s own model guidance says **Claude Opus 4.5** is the most capable but uses more premium requests, **Claude Sonnet 4.5** is fast and cost-effective for routine coding, and **GPT-5.2 Codex** is strong for code generation and review. ([GitHub Docs][10])

So for cost/performance, I would likely use:

- **Architect / complex planning**: Opus or Sonnet depending task difficulty
- **Implementation**: Sonnet 4.5
- **Review**: GPT-5.2 Codex or Code-review agent
- **Task execution**: built-in Task agent

That is an opinionated setup, but it matches GitHub’s published tradeoff guidance. ([GitHub Docs][10])

## Bottom line

**Yes, you can absolutely run your architecture → implementation → test → review workflow with Copilot CLI.**
And for day-to-day use, **autopilot + `/fleet` is likely easier and often faster than a hand-built Ralph loop**. ([GitHub Docs][4])

But:

- **No, I would not trust it as a complete closed-loop “feature factory” without explicit acceptance gates.**
- **No, there is no official basis for saying it definitely uses fewer premium requests.**
- **Yes, the strongest setup is Copilot CLI as the inner orchestrator plus a thin Ralph-like outer gate for pass/fail discipline.**

That gives you the best of both worlds without building a tiny bureaucracy in a trench coat.

I can draft the exact setup next:
a Copilot CLI workflow using **custom agents + plan mode + `/fleet` + `/review` + hooks**, plus a small wrapper script that loops until tests and review pass.

[1]: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/autopilot "Allowing GitHub Copilot CLI to work autonomously - GitHub Docs"
[2]: https://github.com/vercel-labs/ralph-loop-agent?utm_source=chatgpt.com "ralph-loop-agent - Continuous Autonomy for the AI SDK"
[3]: https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/ "GitHub Copilot CLI is now generally available - GitHub Changelog"
[4]: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet "Running tasks in parallel with the /fleet command - GitHub Docs"
[5]: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-agents/invoke-custom-agents "Invoking custom agents - GitHub Docs"
[6]: https://docs.github.com/en/copilot/how-tos/copilot-cli/speeding-up-task-completion "Speeding up task completion with the /fleet command - GitHub Docs"
[7]: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-agents/agentic-code-review "Requesting a code review with GitHub Copilot CLI - GitHub Docs"
[8]: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-agents/overview?utm_source=chatgpt.com "Using GitHub Copilot CLI"
[9]: https://docs.github.com/en/copilot/tutorials/copilot-cli-hooks "Using hooks with Copilot CLI for predictable, policy-compliant execution - GitHub Docs"
[10]: https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices?utm_source=chatgpt.com "Best practices for GitHub Copilot CLI"

---

Yes. Your current agent set is already a good fit for Copilot CLI.

The clean mapping is:

- **software-architect** for bounded system-level design and tradeoffs, not code fixes
- **software-engineer** for implementation plus build/test verification, with a Ralph-style posture already baked into the agent itself
- **code-reviewer** for diff-based correctness/safety/maintainability review
- **security-reviewer** for concrete security-risk review grounded in evidence, not speculation

And Copilot CLI now gives you the missing orchestration primitives around them:

- **autopilot** for multi-step autonomous execution until Copilot thinks the task is complete, blocked, or hits a continuation limit ([GitHub Docs][1])
- **`/fleet`** for splitting a multi-step implementation plan into subagent work in parallel, typically after plan mode ([GitHub Docs][2])
- **custom agents** in `.github/agents`, invokable with `/agent`, by mentioning them in prompts, or via `--agent=...` on the command line ([GitHub Docs][3])
- **`/review`** for terminal-native code review of your current changes ([GitHub Docs][4])
- **hooks** in `.github/hooks/*.json`, which run synchronously and can block execution before tools are used ([GitHub Docs][5])

## The main design correction

Do **not** put your **software-architect** into the inner Ralph loop on every pass.

Your own CLASP/Ralph notes already point the right way: only **execution agents** are mechanically suited to Ralph-style verify/fix loops, while cognitive agents like Architect produce subjective output that is not directly verifiable the same way.

So the right loop is:

1. **Architect once** at the start of the feature
2. **Engineer in the inner loop**
3. **Code review**
4. **Security review**
5. **Loop engineer again if needed**
6. **Only call architect again if a review finds an architectural defect or missing boundary decision**

That avoids bureaucracy wearing a hard hat.

---

# Recommended workflow

## Phase A — Architecture pass, once per feature

Use your `software-architect` agent to turn the feature spec into a bounded implementation plan.

Because the architect agent is explicitly about boundaries, interfaces, deployment topology, quality attributes, feature decomposition, and test architecture — while excluding code-level fixes — it should produce the architecture/implementation document, then get out of the blast zone.

### Suggested output

- `docs/specs/<feature>.feature-spec.md`
- `docs/implementation/<feature>.architecture-and-implementation.md`

### Suggested command

```bash
copilot --agent=software-architect --prompt "
Read docs/specs/<feature>.feature-spec.md.
Create docs/implementation/<feature>.architecture-and-implementation.md.

Requirements:
- keep scope bounded
- define affected components, interfaces, data flow, tests, and migration steps
- do not implement code
- do not invent repo facts
- if constraints are missing, state them explicitly
"
```

That command pattern is supported because Copilot CLI custom agents can be invoked directly with `--agent=...`. ([GitHub Docs][3])

---

## Phase B — Engineering loop

This is the part that should be Ralph-like.

Your `software-engineer` agent already says it implements changes safely and minimally, runs build/tests, reads the output, fixes errors, and loops until verified or blocked. That is excellent as the **inner worker behavior**.

### Best interactive path

Use **plan mode**, then accept the plan and build on **autopilot + `/fleet`**. GitHub’s own docs describe `/fleet` as something you typically use after plan creation, and explicitly note the “accept plan and build on autopilot + /fleet” path. ([GitHub Docs][2])

### Best scripted path

For predictable repeatability, use the engineer agent directly with autopilot.

```bash
copilot --agent=software-engineer \
  --autopilot \
  --yolo \
  --max-autopilot-continues 8 \
  --prompt "
Implement docs/implementation/<feature>.architecture-and-implementation.md.

Rules:
- stay within the documented scope
- update only required files
- run the relevant build, lint, and tests
- if a check fails, fix and retry within this session
- when finished, write a short implementation summary to reports/loop/<feature>/engineer-summary.md
- do not claim completion without evidence
"
```

Autopilot is documented to keep working until Copilot decides the task is complete, blocked, you interrupt it, or a continuation limit is reached; `--max-autopilot-continues` is explicitly supported. ([GitHub Docs][1])

### When to use `/fleet`

Use `/fleet` when the implementation plan clearly contains parallelizable work, such as:

- backend endpoint changes
- frontend UI changes
- tests
- docs updates

GitHub’s docs explicitly position `/fleet` for multi-step implementation plans where some operations can be done in parallel. ([GitHub Docs][2])

### My practical recommendation

Use this split:

- **Interactive:** architect → plan mode → autopilot + `/fleet`
- **Scripted outer loop:** engineer via `--agent=software-engineer --autopilot`

That gives you both speed and control.

---

## Phase C — Review gates

You have two strong custom gates already:

- **code-reviewer** for correctness, safety, maintainability, and repo standards on diffs/PRs/snippets
- **security-reviewer** for concrete code/config security risks grounded in evidence

### Why use your custom reviewers instead of only `/review`

`/review` is great interactively, but your own agents are better for a repeatable outer loop because you can force a consistent output format with `--agent=...`. GitHub documents `/review` as an interactive slash command, while custom agents can be invoked directly from the command line. ([GitHub Docs][4])

### Suggested code review command

```bash
copilot --agent=code-reviewer --prompt "
Review the current git diff against docs/implementation/<feature>.architecture-and-implementation.md.

Output exactly:
status: pass | needs_changes | blocked

Blocking issues:
- ...

Non-blocking issues:
- ...

Recommended next engineer prompt:
- ...
" > reports/loop/<feature>/code-review.txt
```

### Suggested security review command

```bash
copilot --agent=security-reviewer --prompt "
Review the current git diff for concrete security risks.

Scope:
- changed files only
- no speculation beyond visible evidence

Output exactly:
status: pass | needs_changes | blocked

Blocking issues:
- ...

Non-blocking issues:
- ...

Recommended next engineer prompt:
- ...
" > reports/loop/<feature>/security-review.txt
```

### Optional interactive review

You can still run:

```text
/review
```

inside Copilot CLI for a quick interactive check of the current changes. GitHub documents `/review` for terminal-native change review. ([GitHub Docs][4])

---

# The actual loop

This is the loop I recommend for you:

```text
feature spec
  -> software-architect (once)
  -> software-engineer (autopilot, possibly /fleet)
  -> code-reviewer
  -> security-reviewer
  -> if reviews or tests fail: software-engineer again
  -> if reviewer says architecture is wrong/missing: software-architect again
  -> stop only when all gates pass
```

That is the useful hybrid:

- **Copilot CLI** handles the inner orchestration
- **your outer wrapper** handles the hard stop conditions

---

# Minimal repo additions

## 1. Hook config

GitHub documents repository hooks under `.github/hooks/`, with JSON config loaded automatically from `.github/hooks/*.json`. Hooks run synchronously and can block execution. ([GitHub Docs][5])

Create:

```text
.github/
  hooks/
    copilot-cli-policy.json
    scripts/
      session-banner.ps1
      pre-tool-policy.ps1
      log-prompt.ps1
```

### `.github/hooks/copilot-cli-policy.json`

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "type": "command",
        "powershell": "./scripts/session-banner.ps1",
        "cwd": ".github/hooks",
        "timeoutSec": 10
      }
    ],
    "userPromptSubmitted": [
      {
        "type": "command",
        "powershell": "./scripts/log-prompt.ps1",
        "cwd": ".github/hooks",
        "timeoutSec": 10
      }
    ],
    "preToolUse": [
      {
        "type": "command",
        "powershell": "./scripts/pre-tool-policy.ps1",
        "cwd": ".github/hooks",
        "timeoutSec": 15
      }
    ]
  }
}
```

### `session-banner.ps1`

```powershell
$ErrorActionPreference = "Stop"

Write-Host @"
COPILOT CLI POLICY ACTIVE
- architecture must exist before implementation
- dangerous git/file commands may be blocked
- review gates must pass before claiming completion
"@
exit 0
```

### `log-prompt.ps1`

```powershell
$ErrorActionPreference = "Stop"

$logDir = ".\logs"
$logFile = Join-Path $logDir "audit.jsonl"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$inputText = [Console]::In.ReadToEnd()
$entry = @{
    timestamp = (Get-Date).ToString("o")
    type = "userPromptSubmitted"
    payload = $inputText
} | ConvertTo-Json -Compress

Add-Content -Path $logFile -Value $entry
exit 0
```

### `pre-tool-policy.ps1`

This should be boring and ruthless.

```powershell
$ErrorActionPreference = "Stop"
$inputText = [Console]::In.ReadToEnd()

# Very simple denylist. Tighten later with proper parsing if needed.
$blockedPatterns = @(
    "git push",
    "git reset --hard",
    "git clean -fd",
    "gh pr merge",
    "rm -rf",
    "del /f /s /q"
)

foreach ($pattern in $blockedPatterns) {
    if ($inputText -match [regex]::Escape($pattern)) {
        Write-Error "Blocked by Copilot CLI policy: $pattern"
        exit 1
    }
}

exit 0
```

That is not sophisticated, but it is enough to stop the most annoying self-inflicted fireworks.

---

## 2. Loop workspace

Create:

```text
reports/
  loop/
    <feature>/
      engineer-summary.md
      code-review.txt
      security-review.txt
      final-status.txt
```

---

# Minimal outer loop script

This wrapper is the missing part that turns “autonomous agent” into “Ralph-grade gated loop.”

## `scripts/copilot-feature-loop.ps1`

```powershell
param(
    [Parameter(Mandatory = $true)]
    [string]$FeatureName,

    [Parameter(Mandatory = $true)]
    [string]$FeatureSpecPath,

    [int]$MaxIterations = 5
)

$ErrorActionPreference = "Stop"

$loopDir = "reports/loop/$FeatureName"
New-Item -ItemType Directory -Force -Path $loopDir | Out-Null

$implDoc = "docs/implementation/$FeatureName.architecture-and-implementation.md"

# Step 1: architecture pass
if (-not (Test-Path $implDoc)) {
    copilot --agent=software-architect --prompt @"
Read $FeatureSpecPath.
Create $implDoc.

Requirements:
- bounded architecture + implementation plan
- affected components
- interfaces
- tests
- migration notes if needed
- no code changes
"@
}

for ($i = 1; $i -le $MaxIterations; $i++) {
    Write-Host "=== Iteration $i / $MaxIterations ==="

    copilot --agent=software-engineer --autopilot --yolo --max-autopilot-continues 8 --prompt @"
Implement $implDoc.

Rules:
- stay within scope
- run relevant build/lint/test commands
- fix failures before stopping
- write a short summary to $loopDir/engineer-summary.md
- do not claim completion without evidence
"@

    copilot --agent=code-reviewer --prompt @"
Review the current git diff against $implDoc.

Output exactly:
status: pass | needs_changes | blocked

Blocking issues:
- ...

Non-blocking issues:
- ...

Recommended next engineer prompt:
- ...
"@ | Out-File "$loopDir/code-review.txt" -Encoding utf8

    copilot --agent=security-reviewer --prompt @"
Review the current git diff for concrete security risks.

Output exactly:
status: pass | needs_changes | blocked

Blocking issues:
- ...

Non-blocking issues:
- ...

Recommended next engineer prompt:
- ...
"@ | Out-File "$loopDir/security-review.txt" -Encoding utf8

    $codeReview = Get-Content "$loopDir/code-review.txt" -Raw
    $secReview = Get-Content "$loopDir/security-review.txt" -Raw

    $codePass = $codeReview -match "status:\s*pass"
    $secPass = $secReview -match "status:\s*pass"

    if ($codePass -and $secPass) {
        "PASS" | Out-File "$loopDir/final-status.txt" -Encoding utf8
        Write-Host "Feature passed both review gates."
        exit 0
    }

    $nextPrompt = @"
Continue implementing $implDoc.

Address the following review findings.

Code review:
$codeReview

Security review:
$secReview

Do not expand scope. Fix only blocking issues first.
Run relevant verification again.
"@

    $nextPrompt | Out-File "$loopDir/next-engineer-prompt.txt" -Encoding utf8
}

"FAILED_MAX_ITERATIONS" | Out-File "$loopDir/final-status.txt" -Encoding utf8
Write-Error "Max iterations reached without passing review gates."
exit 1
```

## Why this works

It respects the role boundaries you already defined:

- architect does architecture
- engineer changes code and verifies
- reviewer critiques diffs
- security reviewer critiques security
- only the engineer is in the recurring execution loop

That matches both your agent definitions and your own Ralph-loop research notes.

---

# Recommended usage pattern in practice

## For bigger features

Use **interactive Copilot CLI**:

1. open `copilot`
2. switch to **plan mode**
3. create the implementation plan
4. accept plan and build on **autopilot + `/fleet`** ([GitHub Docs][2])
5. run your custom review agents or `/review` ([GitHub Docs][4])
6. if blocking findings remain, rerun engineer with the reviewer outputs

## For repeatable repo-local automation

Use the PowerShell loop above.

That is the version most compatible with your CLASP style because it is:

- explicit
- bounded
- auditable
- role-separated

---

# Small tweaks I would make to your agents

Your agents are already good. I would only add these:

## software-architect

Add one line:

> “This agent is normally invoked once per feature or when a reviewer identifies an architectural gap. It is not part of the default inner implementation loop.”

This prevents over-architecting every paper cut. Your architect is already scoped to system-level decisions and avoids unrelated redesign.

## software-engineer

Add one line:

> “When invoked by an outer loop, prioritize reviewer blocking issues over new improvements.”

This keeps it from drifting into “while I’m here” nonsense.

## code-reviewer

Add one line:

> “When asked, emit a strict machine-readable verdict (`pass | needs_changes | blocked`) before narrative findings.”

Because your current reviewer is excellent for human review, but the loop wrapper benefits from a cleaner parser. The agent already focuses on visible diffs and concrete risks.

## security-reviewer

Add one line:

> “When asked, emit a strict machine-readable verdict (`pass | needs_changes | blocked`) before narrative findings.”

Same reason.

---

# Final recommendation

Use **Copilot CLI as the inner orchestrator** and your own **outer gate** for completion discipline.

The best version for your setup is:

- **architect once**
- **engineer with autopilot**
- **use `/fleet` when the implementation plan is parallelizable**
- **review with code-reviewer + security-reviewer**
- **loop only the engineer unless a review reveals an architectural defect**

That gets you the upside of Copilot CLI without turning your workflow into a tiny ministry of self-important agent paperwork.

Some earlier uploaded files have expired on my side, so I grounded this setup in the agent files and summaries that were still available. Re-upload older governance files if you want me to turn this into a repo-exact CLASP artifact set with the precise filenames and folder conventions you’re using.

[1]: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/autopilot "Allowing GitHub Copilot CLI to work autonomously - GitHub Docs"
[2]: https://docs.github.com/en/copilot/how-tos/copilot-cli/speeding-up-task-completion "Speeding up task completion with the /fleet command - GitHub Docs"
[3]: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-agents/invoke-custom-agents "Invoking custom agents - GitHub Docs"
[4]: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-agents/agentic-code-review "Requesting a code review with GitHub Copilot CLI - GitHub Docs"
[5]: https://docs.github.com/en/copilot/tutorials/copilot-cli-hooks "Using hooks with Copilot CLI for predictable, policy-compliant execution - GitHub Docs"
