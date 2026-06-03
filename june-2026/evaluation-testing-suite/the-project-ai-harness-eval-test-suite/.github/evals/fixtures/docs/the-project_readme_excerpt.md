# the project README Excerpt

the project is a dividend-capture strategy platform with a Python backend (`the-project-api`) and a React frontend (`the-project-web`).

## Active Codebases

| Component | Technology | Purpose |
|---|---|---|
| `the-project-api` | Python 3.12 / FastAPI | Backend API, ML models, research pipeline, data fetching |
| `the-project-web` | React 18 / TypeScript / Vite | Web UI |

## Key Capabilities

- Dividend capture prediction around ex-dividend dates
- Ensemble ML models with confidence scoring
- Optional quantile prediction enrichment
- Portfolio/run management with real-time progress updates
- Export-ready run results
- Automated research pipeline — daily multi-model LLM research with per-stage model routing, analyst swarm consensus, and structured proposal extraction
- Agent Guard prompt-injection defense for LLM interactions

## AI Governance (Agent Harness)

This repository uses Agent Harness (Controlled Layered Authority System for Prompts) to govern AI-assisted development. Agent Harness prevents hallucination, enforces evidence-based claims, and keeps AI outputs auditable.
