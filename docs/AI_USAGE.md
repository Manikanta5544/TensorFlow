# AI Usage

This document covers two different things the brief asked for: how AI was used *to build* this submission, and how AI is used *inside* the product itself.

## How AI was used to build this submission

The assessment brief explicitly asks candidates to build using AI, write the CI/CD pipeline using AI, and write documentation using AI. All of that applies here: the codebase, tests, CI/CD pipeline, and this documentation set were produced with AI assistance, followed by manual implementation, verification, testing, and refinement throughout the development process, with the following review discipline applied throughout rather than accepting output uncritically:

- **Every backend claim was executed, not assumed.** The backend test suite was executed rather than simply written, and several real bugs were caught and fixed in the process: a Postgres-only UUID type breaking against the SQLite test database, a JSON-serialization crash on nested Pydantic validation errors, a connection-pooling bug that only manifested with file-based SQLite, and a stale-dependency warning from a bcrypt/passlib version mismatch. None of these were hypothetical each was reproduced, diagnosed, and fixed with a passing test as the proof.
- **The database migration was verified, not hand-waved.** Rather than trusting that a hand-authored Alembic migration matches the ORM models, `alembic upgrade head --sql` was run in offline mode to generate the actual Postgres DDL and visually confirm every table, enum, foreign key, and index matches the entity definitions exactly.
- **The frontend was actually built and typechecked.** `npm run build`, `tsc -b --noEmit`, `eslint . --max-warnings 0`, and the Vitest suite were all run for real — which caught a genuine dependency version conflict (Vitest 2.x bundling an incompatible nested Vite 5 copy against a Vite 6 project) that was fixed by upgrading to Vitest 3.
- **The seed script was run end-to-end**, including a second run to verify its idempotency guard actually prevents duplicate data.

The takeaway: AI-assisted code was treated as generated code requiring the same review, testing, and validation standards as manually written code. AI accelerated implementation, but correctness was established through execution, testing, and manual review rather than assumption.

## How AI is used inside the product

**Feature: AI-generated job descriptions** (`POST /api/v1/ai/job-description`, recruiter-only).

A recruiter posting a job can enter a title, experience level, and a few key skills, and get a structured draft description (role summary, responsibilities, requirements, nice-to-haves) to start from and edit — rather than writing one from scratch. The generated text populates the description field but is fully editable before publishing; nothing is auto-published.

### Provider architecture (see ADR-006 for the full reasoning)

```
AIService (application layer)
  → PromptFactory (ai/application/prompts.py — builds the system + user prompt)
    → LLMProvider (abstract port, ai/domain/provider.py)
      → MockLLMProvider          (default — deterministic, offline, zero cost)
      → OpenAICompatibleProvider  (real inference — any OpenAI-compatible provider (such as OpenAI, Groq, or OpenRouter))
```

**Default: mock provider.** `AI_PROVIDER=mock` by default (see `backend/.env.example`). This is a deliberate choice, not a fallback bolted on afterward: it means the entire platform — including the AI feature — runs, is fully testable, and is reviewable with zero API keys and zero cost. The mock provider returns deterministic responses suitable for local development, testing, and demonstration without requiring external API access.

**Switching to a real model.** Set three environment variables (locally via .env or in production through Render environment variables):
```
AI_PROVIDER=openai_compatible
AI_API_KEY=sk-...
AI_MODEL=gpt-4o-mini          # or any OpenAI-compatible model name
AI_BASE_URL=https://api.openai.com/v1   # or Groq's / OpenRouter's endpoint
```
No code changes, no redeploy of business logic — only the adapter selected by `ai/infrastructure/factory.py` changes.

### Safety and reliability

- **Every AI request is recorded for auditing.** Regardless of success or failure, a row is written to the `ai_requests` table (requester, request type, provider, model, success/failure) — this is what would let a real deployment track usage, cost, and failure rates over time; it's also what the tests assert on (`tests/ai/test_ai_api.py::test_ai_request_is_audited`).
- **Failure is contained.** If the real provider adapter's HTTP call fails (timeout, bad response shape, rate limit), it's caught and re-raised as an `AppError` with a clear `AI_PROVIDER_ERROR` code and a user-facing message — never a raw stack trace, never a silent hang.
- **The AI feature is non-blocking to the core product.** Job posting works completely without ever touching the AI endpoint — a recruiter can write their own description and skip AI assist entirely. The AI feature enhances the workflow; it isn't a dependency of it.
- **No prompt injection surface from user data into privileged operations.** The AI feature only ever takes structured, recruiter-authored input (role title, skill list) — it doesn't ingest untrusted third-party content (e.g. a candidate's resume text) into a prompt whose output could influence a privileged action.
