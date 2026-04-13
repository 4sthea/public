# Scripts and Hooks Reference

> **Audience:** Developers working on the Divical monorepo.
> **Scope:** All shell scripts, Python utility scripts, Git hooks, agent lifecycle hooks, and dev container lifecycle scripts present in this repository.

---

## Overview

The repository contains scripts and hooks in five distinct categories:

| Category                                                                                             | Location             | Purpose                                                                  |
| ---------------------------------------------------------------------------------------------------- | -------------------- | ------------------------------------------------------------------------ |
| [Agent lifecycle hooks](#1-agent-lifecycle-hooks-githubhooks)                                        | `.github/hooks/`     | Intercept Copilot agent events (session start, tool use, stop)           |
| [Developer & AI Ecosystem governance scripts](#2-developer--AI Ecosystem-governance-scripts-scripts) | `scripts/`           | Local quality gates, AI Ecosystem artifact auditing, repo-map generation |
| [Dev container lifecycle scripts](#3-dev-container-lifecycle-scripts-devcontainer)                   | `.devcontainer/`     | Container setup and service management                                   |
| [Root-level convenience scripts](#4-root-level-convenience-scripts)                                  | `/workspace/` (root) | Start/stop local development servers                                     |
| [GitHub Actions workflows](#5-github-actions-workflows-githubworkflows)                              | `.github/workflows/` | CI and scheduled automation                                              |

---

## 1. Agent Lifecycle Hooks (`.github/hooks/`)

These hooks integrate with GitHub Copilot's agent event system. They are wired in `.github/hooks/hooks.json` (canonical registry: see `AI Ecosystem-artifact-freshness.md` § Hooks). The hooks are **not** standard Git hooks; they are Copilot-specific lifecycle callbacks.

### `session-start.sh`

**Hook event:** `SessionStart`

Runs at the beginning of every agent session. Injects contextual metadata into the agent's working context so the agent is aware of:

- The current Git branch (`git branch --show-current`).
- The five most recent commits (`git log --oneline -5`).
- The active workflow state file, if one exists under `.github/runtime/` — specifically the most recently updated `*.state.json` not inside an `archive/` subdirectory. It also extracts and surfaces the `posture` field from that JSON (defaults to `"delivery"`).

All of this is returned as a JSON `additionalContext` payload. This means agents always start a session with awareness of what branch they are on, recent work, and any in-progress orchestrated workflow.

---

### `pre-tool-use.sh`

**Hook event:** `PreToolUse`

Runs before every tool call. Acts as a safety gate for terminal command execution.

**Behaviour:**

- All non-terminal tools (anything other than `run_in_terminal`, `execute_command`, `terminal`) are **always allowed** immediately — the hook short-circuits after the tool-name check.
- For terminal tools, it extracts the command string from the tool input and evaluates it against `.github/hooks/command-policy.json`.
- Returns one of three decisions: `allow`, `ask` (prompt user for confirmation), or `deny` (block outright with a reason).
- If the policy file is missing or the command string cannot be extracted, the default is `allow`.

See [`command-policy.json`](#command-policyjson) below for the rule definitions.

---

### `command-policy.json`

**Type:** Configuration (JSON) — consumed by `pre-tool-use.sh`.

Defines two rule sets:

**`deny` patterns** — commands that are always blocked:

| Pattern                                           | Reason                                               |
| ------------------------------------------------- | ---------------------------------------------------- |
| `git reset --hard`                                | Destroys uncommitted work and rewrites history       |
| `git push --force` (without `--force-with-lease`) | Can overwrite remote commits                         |
| `git clean -fd`                                   | Deletes untracked files and directories irreversibly |
| `rm -rf /` or `rm -rf ..`                         | Recursive force-delete of root or parent paths       |
| Writes to `/dev/sd*` block devices                | Overwriting raw block devices                        |

**`ask` patterns** — commands that require user confirmation before execution:

| Pattern                       | Reason                                              |
| ----------------------------- | --------------------------------------------------- |
| `git push --force-with-lease` | Safer force push, but still rewrites remote history |
| `git checkout -- .`           | Discards all unstaged changes                       |
| `git stash drop`              | Permanently discards a stash entry                  |
| `rm -r` (recursive delete)    | Confirm target is intentional                       |
| `DROP TABLE/DATABASE/SCHEMA`  | Destructive database DDL                            |
| `TRUNCATE TABLE`              | Irreversible data removal                           |
| `--no-verify` flag            | Bypasses safety hooks (pre-commit, pre-push)        |

> **Scope note:** This policy is enforced for Copilot agent terminal calls only. It has no effect on manual shell sessions.

---

### `post-format.sh`

**Hook event:** `PostToolUse`

Runs after every file-editing tool call (`create_file`, `replace_string_in_file`, `multi_replace_string_in_file`, `editFiles`). Auto-formats the file that was just written.

**Formatting behaviour by file type:**

| Extension                                            | Tool                           | Commands run                                        |
| ---------------------------------------------------- | ------------------------------ | --------------------------------------------------- |
| `.py`                                                | `ruff` (if available)          | `ruff format <file>` then `ruff check --fix <file>` |
| `.ts`, `.tsx`, `.js`, `.jsx`, `.json`, `.css`, `.md` | `prettier` (or `npx prettier`) | `prettier --write <file>`                           |

If neither formatter is available for a given file type, the hook exits silently (exit 0) — it never blocks an edit.

---

### `stop-context-check.sh`

**Hook event:** `Stop`

Runs when the agent attempts to finish a session. Its purpose is to prevent agents from stopping with stale context documentation — specifically files under `.github/context/`.

**Flow:**

1. **Guard — infinite loop prevention:** If the `stop_hook_active` flag is `true` (meaning a re-invocation triggered by this hook's own remediation), the hook exits immediately (`{}`), allowing stop unconditionally.
2. **Guard — read-only sessions:** Checks `git diff` and `git ls-files --others` for uncommitted or untracked changes outside `.github/`. If there are no such changes, the session was read-only and the hook exits immediately (no freshness check needed).
3. **Freshness detection:** Calls `scripts/verify-context-freshness.sh --json`. If the script is not executable or fails, the hook exits without blocking.
4. **Decision:** Parses the JSON result for `stale: true`. If stale, the hook returns a remediation block to the agent with a human-readable summary of which context files have drifted and what needs updating. If clean, it exits (`{}`), allowing stop.

---

## 2. Developer & AI Ecosystem Governance Scripts (`scripts/`)

All scripts in this directory are run from the **repository root** unless stated otherwise.

### `setup-hooks.sh`

**Type:** Shell script  
**Run:** Once after cloning, or whenever `pre-push-check.sh` changes.

Installs the `pre-push` Git hook into `.git/hooks/pre-push`. The installed hook is a thin wrapper that calls `scripts/pre-push-check.sh` (if present and executable) and exits 0 if not found. This allows developers to receive the actual logic from source control while the Git hook entry point stays stable.

```bash
./scripts/setup-hooks.sh
```

---

### `pre-push-check.sh`

**Type:** Shell script  
**Triggered by:** `.git/hooks/pre-push` (installed via `setup-hooks.sh`)

Fast local quality gate that runs before every `git push`. Targets only Python files inside `divical-api/app/` that were changed relative to `origin/master` (new, modified, or added). Tests are intentionally excluded — they run in CI.

**Steps:**

1. Resolves Python: uses `divical-api/.venv/bin/python` if available, falls back to `python3`.
2. Collects changed Python files with `git diff --name-only --diff-filter=ACM origin/master...HEAD`.
3. If no files changed, exits 0 immediately (skip message).
4. **[1/2] Lint:** Runs `ruff check` on all changed files. Exits 1 on any violation.
5. **[2/2] Type check — changed files:** Runs `pyright` against only the changed files (paths made relative to `divical-api/` so `pyrightconfig.json` is picked up).
6. **[2b/2] Type check — full scope:** Runs `pyright app/` against the entire app directory. This mirrors CI and catches pre-existing errors that happened to be in the push scope.

> **Design rationale (from runbook entry `[2026-03-14]`):** Full-scope pyright was added because a CI failure was caused by a type-ignore fix in `adapter.py` that wasn't in the changed-files diff.

---

### `verify-AI Ecosystem-freshness.sh`

**Type:** Shell script  
**Usage modes:**

```bash
./scripts/verify-AI Ecosystem-freshness.sh          # Check: exit 1 if counts mismatch
./scripts/verify-AI Ecosystem-freshness.sh --fix     # Fix: update freshness table from disk
./scripts/verify-AI Ecosystem-freshness.sh --lint    # Lint: structural validation
```

Verifies or updates the artifact inventory counts in `.github/context/AI Ecosystem-artifact-freshness.md`.

**Check mode (default):** Counts actual files in each artifact category on disk:

- `.github/agents/*.agent.md` (split into visible and hidden)
- `.github/instructions/*.instructions.md`
- `.github/prompts/*.prompt.md`
- `.github/skills/*/assets/*.template.md`
- `.github/skills/*/SKILL.md`
- `.github/context/*.md`

Compares each count against the corresponding row in the freshness table. Exits 1 if any count mismatches.

**Fix mode (`--fix`):** Updates mismatched counts in-place using `sed`. Reports each change.

**Lint mode (`--lint`):** Runs six structural checks:

| Check                             | What it validates                                                                                                                             |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 – applyTo Glob Validation       | Every `applyTo` pattern in `.instructions.md` and `.agent.md` frontmatter matches at least one tracked file                                   |
| 2 – Cross-Reference Validation    | Every `.github/**` path referenced inside `.github/` files exists on disk (runtime artifacts are downgraded to warnings)                      |
| 3 – Orphan Detection              | Every agent file is referenced in at least one other `.github/` markdown; every `applyTo`-scoped instruction matches files outside `.github/` |
| 4 – Agent Reference Validation    | Every agent name in an `agents:` frontmatter list corresponds to an existing `.agent.md` file                                                 |
| 5 – Skill Context Path Validation | Backtick-quoted paths referenced in `SKILL.md` files exist on disk                                                                            |
| 6 – JSON Schema Validation        | All `.json` files under `.github/schemas/` and `.github/hooks/` are valid JSON                                                                |

Exits 1 on errors; exits 0 on warnings-only.

---

### `verify-context-freshness.sh`

**Type:** Shell script  
**Usage modes:**

```bash
./scripts/verify-context-freshness.sh            # Human-readable report (exit 1 on drift)
./scripts/verify-context-freshness.sh --json      # JSON output (for Stop hook)
./scripts/verify-context-freshness.sh --check     # Silent exit-code check
```

Detects staleness in `.github/context/` documentation by validating extractable facts against the actual repository state. This is designed to be called by the Stop hook (`stop-context-check.sh`) to automatically surface drift when an agent has made code changes.

**Checks performed:**

- **`project-paths.md`:** Extracts backtick-quoted paths from the Markdown tables and verifies each path exists on disk. Also checks for top-level `divical-api/app/` module directories that appear on disk but are not listed in the file. Validates that `applyTo` patterns listed in tables match the actual frontmatter of the referenced instruction files.

Output shape in `--json` mode:

```json
{
  "stale": true,
  "errors": 2,
  "warnings": 1,
  "findings": [
    "ERROR|project-paths.md|Listed path missing: divical-api/app/newmodule/"
  ]
}
```

---

### `verify-feature-slice.sh`

**Type:** Shell script  
**Usage:**

```bash
scripts/verify-feature-slice.sh api           # Backend only
scripts/verify-feature-slice.sh web           # Frontend only
scripts/verify-feature-slice.sh both          # Both
scripts/verify-feature-slice.sh api feature-wide   # (mode flag, currently unused)
```

Full verification gate for a feature delivery slice. Used in the feature delivery lifecycle to validate a completed implementation before handoff.

**Backend checks (`api` target):**

- `ruff check .` — lint
- `pyright app/` — type check
- `pytest tests/ -x -q` — test suite (stop on first failure)

**Frontend checks (`web` target):**

- `npx eslint src/` — lint
- `npx tsc --noEmit` — type check
- `npm test -- --run` — test suite

Results are collected into a structured pass/fail report printed to stdout. Exits 1 if any check fails.

---

### `verify-instruction-conflicts.sh`

**Type:** Shell script  
**Usage:**

```bash
./scripts/verify-instruction-conflicts.sh             # Show overlap matrix
./scripts/verify-instruction-conflicts.sh --verbose   # Show matched files per overlap
```

Detects overlapping `applyTo` patterns across instruction files. Two instructions conflict when both match the same source file — this means the agent receives both instruction sets for that file, which can produce contradictory guidance.

**Algorithm:**

1. Reads `applyTo` frontmatter from every `.instructions.md` file under `.github/`.
2. Expands brace patterns (`{a,b,c}` → three separate globs).
3. For each instruction, collects the set of matching source files via `git ls-files`.
4. Builds a reverse map: source file → list of matching instructions.
5. Reports files matched by more than one instruction as conflicts.
6. In `--verbose` mode, lists the matched files for each conflicting pair.

> Instructions with `applyTo: "**"` (always-on, global) are treated as matching everything and reported separately.

---

### `capture-prompt-baseline.sh`

**Type:** Shell script  
**Usage:**

```bash
./scripts/capture-prompt-baseline.sh                   # Capture snapshot to reports/prompt-baselines/
./scripts/capture-prompt-baseline.sh --diff <file>     # Diff current state against a baseline
```

Captures a structural snapshot of every `.prompt.md` file in `.github/prompts/`. Output goes to a timestamped file under `reports/prompt-baselines/`.

**Per-prompt metadata captured:**

- File name
- `agent` frontmatter field
- `model` frontmatter field
- `description` frontmatter field
- Line count
- MD5 checksum
- Section headings (`##` and `###`)

**Diff mode (`--diff`):** Creates a temporary snapshot, strips volatile fields (timestamps, md5), and runs a unified diff against the provided baseline file. Useful for verifying that a prompt migration is structurally identical before deleting the old version.

---

### `generate-repo-map.sh`

**Type:** Shell script  
**Usage:**

```bash
./scripts/generate-repo-map.sh          # Generate .github/context/repo-map.md
./scripts/generate-repo-map.sh --check  # Verify map is current (exit 1 on mismatch)
```

Auto-generates `.github/context/repo-map.md`, which is the canonical index of all AI Ecosystem artifacts. The file is marked "Do not edit manually" — this script is the only authorised way to update it.

**Sections generated:**

- **Agents** — table of every `.agent.md` with description, tools, and visibility flag.
- **Instructions** — table of every `.instructions.md` with description and `applyTo` pattern.
- **Skills** — table of every `SKILL.md` with the skill name and path.
- **Procedures** — table of procedures (if any exist).

In `--check` mode, the script generates to a temp file and diffs against the committed version. Exits 1 on any difference — used in CI or pre-push gates to ensure the map is not outdated.

---

### `generate_research_report.py`

**Type:** Python script  
**Requires:** `OPENROUTER_API_KEY` environment variable.

Entry point for running the 4-stage research pipeline outside of the normal ARQ worker schedule. Adds `divical-api/` to `sys.path`, then imports and runs `app.services.research.pipeline.run_pipeline()` asynchronously.

**Pipeline stages (executed inside the module):**

1. Research prompt loading and multi-model consolidation.
2. Feasibility analysis via Tavily web search.
3. Analyst swarm + consensus synthesis.
4. Strategy proposal extraction to JSON.

On completion, prints output file paths per stage. Read-only regarding the repository — it writes to configured output directories, not to source files.

This script is also the execution target of the `rbi-research.yml` GitHub Actions workflow.

---

### `gen_model_list.py`

**Type:** Python script  
**Requires:** `docs/openrouter-all-models.md` to exist (raw JSON dump from the OpenRouter API).

Parses the raw JSON in `docs/openrouter-all-models.md`, extracts each model's `name` and `id` (slug), and writes a clean Markdown table to `docs/openrouter-models.md`. The table header includes a model count and the date of the source dump.

Purely a formatting utility — no API calls, no side effects beyond writing `docs/openrouter-models.md`.

---

## 3. Dev Container Lifecycle Scripts (`.devcontainer/`)

These scripts are invoked by `devcontainer.json` directives and are not normally run manually. They manage the container lifecycle for development.

> **Runbook entry `[2026-03-15]`:** `postCreateCommand` fires once on container creation; `postStartCommand` fires on every start. Long-running services go in `post-start.sh`; one-time setup goes in `post-create.sh`.

---

### `.devcontainer/post-create.sh`

**Triggered by:** `devcontainer.json` → `postCreateCommand` (once, at container creation).

Performs full initial setup:

1. **Python backend**
   - Creates `.venv` in `divical-api/` if it does not exist (or if the existing one is from a Windows environment).
   - Detects GPU availability via `nvidia-smi`. If a GPU is present, installs `.[dev,gpu,ml]` extras; otherwise installs `.[dev,ml]` (CPU-only, avoids downloading large CUDA wheels).
   - Uses `--find-links /opt/pip-prefetch` if that path exists (pre-cached wheels baked into the Docker image) to avoid re-downloading on rebuilds.

2. **Node frontend**
   - Runs `npm install` in `divical-web/` (not `npm ci` — incremental update preserves existing `node_modules/` on persisted volumes).

3. **Database**
   - Runs `alembic upgrade head` to apply pending migrations. If this fails (e.g., `.env` is not configured), logs a warning and continues.

---

### `.devcontainer/post-start.sh`

**Triggered by:** `devcontainer.json` → `postStartCommand` (on every container start).

Auto-starts all three Divical services as background daemons using `nohup`. Logs are written to `.devcontainer/logs/`:

| Service             | Command                                                    | Log file            |
| ------------------- | ---------------------------------------------------------- | ------------------- |
| Backend API         | `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` | `logs/backend.log`  |
| Frontend dev server | `npm run dev`                                              | `logs/frontend.log` |
| ARQ worker          | `arq app.worker.WorkerSettings`                            | `logs/worker.log`   |

The script prints each PID and reports final URLs on completion.

---

### `.devcontainer/stop-all.sh`

**Type:** Shell script  
**Run manually** to kill all services started by `post-start.sh`.

Uses `pkill` patterns to kill processes by name:

- `pkill -f "uvicorn app.main:app"` — kills the backend.
- `pkill -f "vite"` — kills the frontend dev server.
- `pkill -f "arq app.worker"` — kills the ARQ worker.

Each kill reports whether the target was running. Non-destructive: exits 0 regardless.

---

## 4. Root-Level Convenience Scripts

These scripts are for developers who want to start services without relying on the dev container auto-start. They are not invoked by any automation.

### `start-all.sh` (Linux/macOS)

Launches both backend and frontend in separate background processes. Waits for `Ctrl+C`, then kills both processes. Also waits 2 seconds after starting the backend before launching the frontend.

```bash
./start-all.sh
# Backend → http://localhost:8000
# Frontend → http://localhost:5173
```

---

### `start-backend.sh` (Linux/macOS)

Activates the Python virtual environment at `divical-api/.venv` and starts uvicorn in reload mode on `localhost:8000`.

```bash
./start-backend.sh
```

---

### `start-frontend.sh` (Linux/macOS)

Changes directory to `divical-web/` and runs `npm run dev` (Vite development server, default port 5173).

```bash
./start-frontend.sh
```

---

### `AI Ecosystem-v3-migrate.sh`

**Type:** One-time migration script (already executed — do not re-run)

This script was used to perform the AI Ecosystem v3 restructuring. It is preserved in the repository for historical record.

**What it did (6 phases):**

1. Created a `AI Ecosystem-v3-restructuring` git branch.
2. Added new instruction files (`architecture.instructions.md`, and others) and updated the system context doc.
3. Replaced three agent files (engineer, reviewer, thinker).
4. Rewired five prompt frontmatters.
5. Deleted four agents, three instructions, eight prompts, one procedure, five templates, three context files, and standalone checklists.
6. Committed all changes.

The script had a pre-flight check for uncommitted changes and prompted the user before proceeding if any were found.

---

## 5. GitHub Actions Workflows (`.github/workflows/`)

These are not scripts per se, but they invoke scripts from this repository.

### `ci.yml`

**Trigger:** Pull requests, pushes to `master`, manual `workflow_dispatch`.

Runs two parallel jobs:

**`backend` job:**

1. Installs Python 3.12 + `pip install -e "divical-api[dev]"`.
2. `ruff check divical-api/app/` — lint.
3. `cd divical-api && pyright app/` — type check.
4. `cd divical-api && pytest -q --tb=short --cov=app --cov-report=term-missing` — test suite with coverage.

**`frontend` job:**

1. Installs Node 20 + `npm ci`.
2. `npm run build` — production build.
3. `npm run lint` — ESLint.
4. `npm test -- --run` — test suite.

---

### `rbi-research.yml`

**Trigger:** Schedule (every 3 days at 01:00 UTC), plus manual `workflow_dispatch`.

Runs `scripts/generate_research_report.py` with `OPENROUTER_API_KEY`, `FMP_API_KEY`, and `TAVILY_API_KEY` secrets. On completion, creates a pull request against `master` with:

- Branch name: `research/auto-<run-id>`
- Added paths: `docs/research-output/**`

The PRs are meant to be reviewed by a developer before merging. The workflow has a `concurrency` group (`rbi-research`) so concurrent runs are never queued — a new trigger simply waits for the running instance.

---

## Ecosystem Diagram

```
Developer pushes code
        │
        ▼
.git/hooks/pre-push (installed by setup-hooks.sh)
        │
        └─► scripts/pre-push-check.sh
                 ├─ ruff (lint, changed files)
                 └─ pyright (changed files + full app/)

Copilot agent session
        │
        ├─► SessionStart → .github/hooks/session-start.sh
        │        injects branch, commits, workflow state
        │
        ├─► PreToolUse → .github/hooks/pre-tool-use.sh
        │        evaluates terminal commands vs command-policy.json
        │
        ├─► PostToolUse → .github/hooks/post-format.sh
        │        auto-formats .py / .ts / .js / .json / .md
        │
        └─► Stop → .github/hooks/stop-context-check.sh
                 runs verify-context-freshness.sh --json
                 blocks stop if .github/context/ is stale

Dev container start
        │
        ├─ postCreateCommand (once) → .devcontainer/post-create.sh
        │       pip install + npm install + alembic upgrade
        │
        └─ postStartCommand (every start) → .devcontainer/post-start.sh
                uvicorn (backend) + vite (frontend) + arq (worker)

GitHub Actions (CI)
        │
        ├─ ci.yml (PR / master push)
        │       ruff + pyright + pytest + eslint + tsc + vitest
        │
        └─ rbi-research.yml (every 3 days)
                scripts/generate_research_report.py → PR with research output
```

---

## Quick Reference

| Task                                | Command                                                             |
| ----------------------------------- | ------------------------------------------------------------------- |
| Install Git pre-push hook           | `./scripts/setup-hooks.sh`                                          |
| Run pre-push checks manually        | `./scripts/pre-push-check.sh`                                       |
| Verify AI Ecosystem artifact counts | `./scripts/verify-ai-ecosystem-freshness.sh`                        |
| Fix AI Ecosystem artifact counts    | `./scripts/verify-ai-ecosystem-freshness.sh --fix`                  |
| Lint AI Ecosystem structure         | `./scripts/verify-ai-ecosystem-freshness.sh --lint`                 |
| Check context freshness             | `./scripts/verify-context-freshness.sh`                             |
| Run feature verification (API)      | `./scripts/verify-feature-slice.sh api`                             |
| Run feature verification (both)     | `./scripts/verify-feature-slice.sh both`                            |
| Detect instruction conflicts        | `./scripts/verify-instruction-conflicts.sh`                         |
| Snapshot prompt baselines           | `./scripts/capture-prompt-baseline.sh`                              |
| Regenerate repo map                 | `./scripts/generate-repo-map.sh`                                    |
| Verify repo map is current          | `./scripts/generate-repo-map.sh --check`                            |
| Generate research report            | `OPENROUTER_API_KEY=... python scripts/generate_research_report.py` |
| Regenerate model list               | `python scripts/gen_model_list.py`                                  |
| Start all services (Linux)          | `./start-all.sh`                                                    |
| Stop dev container services         | `./.devcontainer/stop-all.sh`                                       |
