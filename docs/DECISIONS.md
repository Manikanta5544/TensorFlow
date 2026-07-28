# Architecture Decision Records

Each ADR documents context, the decision, alternatives considered, tradeoffs, and consequences — written at the time the decision was made, not reconstructed afterward.

---

## ADR-001: Vertical-slice + layered architecture over technical-layer-only

**Context.** The brief needs to show both backend and frontend maturity within a tight timeline, while staying easy for a reviewer to navigate feature-by-feature.

**Decision.** Organize by feature first (`auth/`, `jobs/`, `applications/`, `ai/`), with a consistent internal layering inside each (`api/ → application/ → domain/ → infrastructure/`), plus a `shared/` kernel for cross-cutting concerns (config, database, security, logging, exceptions, responses).

**Alternatives considered.**
- *Pure technical layering* (`routers/`, `models/`, `crud/` at the top level): the most common structure in tutorials. Easy to start, but every new feature touches four unrelated top-level folders, and it's harder to see feature ownership at a glance.
- *Full Clean Architecture / hexagonal with use-case objects per operation*: more rigorous, but for four features in a few days it would add ceremony (a class per use case, mapper layers) without a corresponding payoff at this scale.

**Tradeoffs.** Vertical slicing means a little duplication across features (each has its own `schemas.py`, its own repository pattern) rather than one shared generic repository. That's accepted deliberately — shared abstractions that aren't yet needed by more than one caller tend to guess wrong about what the second caller will need.

**Consequences.** Adding a fifth feature means adding a fifth folder with the same four sub-layers — the pattern is now a template, not a one-off. Reviewers can evaluate one feature end-to-end without reading the whole codebase.

---

## ADR-002: FastAPI + React over a full-stack framework (e.g. Next.js, Django)

**Context.** A single full-stack framework (Next.js with API routes, or Django with templates) would reduce the number of moving pieces and deployment targets.

**Decision.** Keep FastAPI and React as separate deployables communicating over a versioned JSON API.

**Alternatives considered.**
- *Next.js end-to-end*: one deploy target, one language. Rejected because it would sideline the Python/FastAPI backend depth this assessment is meant to demonstrate, and because a separate API is the more common shape for a product that expects a mobile client or third-party integrations later.
- *Django + server-rendered templates*: fast to build, but doesn't showcase a modern TanStack Query-driven frontend, and testing the two layers independently is harder when they're not decoupled by a wire contract.

**Tradeoffs.** Two codebases, two CI jobs, two deploy targets, and CORS to configure — real overhead versus a monolith. In exchange: the backend is a reusable API from day one (a future mobile app or partner integration needs zero backend changes), and each layer can be scaled, tested, and deployed independently.

**Consequences.** This is why ADR-005 (Vercel + Render) exists as a separate decision — the two-deployable choice here is what makes that split necessary.

---

## ADR-003: TanStack Query for server state, React Context for client state — no Redux

**Context.** The frontend needs to manage two very different kinds of state: data that lives on the server (jobs, applications, the current user) and small pieces of local UI state (which filter is selected, whether a modal is open, the logged-in user object for rendering).

**Decision.** TanStack Query owns all server state (fetching, caching, invalidation, loading/error states). React Context (`AuthProvider`) owns the one piece of genuinely global client state — the current user. Everything else is local `useState`.

**Alternatives considered.**
- *Redux (or Redux Toolkit) for everything*: would mean hand-rolling loading/error/cache-invalidation logic that TanStack Query already provides, and modeling server data as client state that has to be manually kept in sync — a well-known source of bugs (stale caches, duplicated fetch logic).
- *Context for everything, including server data*: works for the single current-user object, but doesn't scale to lists of jobs/applications — no caching, no request de-duplication, no background refetch, and every consumer re-renders on every context update.

**Tradeoffs.** A developer joining the project needs to know two state models instead of one uniform store, and has to correctly classify new state as "server" or "client." In practice this classification is usually obvious (does it come from an API call?), and the payoff is real: job listing pagination, filter changes, and applicant status updates all get correct caching and invalidation for free from `useJobs`/`useApplicationsForJob` hooks, with no custom cache code written by hand.

**Consequences.** Any new feature needs to ask "is this server state?" before reaching for `useState` — the convention is now: server data → a hook in `features/*/hooks`, wrapping TanStack Query; everything else → local state or, if truly global, a new Context.

---

## ADR-004: JWT with two-role RBAC, 24-hour access tokens, no refresh-token rotation

**Context.** The platform has two distinct actors (recruiter, candidate) with materially different permissions, and needs stateless, horizontally-scalable auth suitable for a serverless-adjacent deployment (Render can spin multiple instances with no shared session store).

**Decision.** JWT access tokens (HS256, 24-hour expiry) carry `sub` (user id) and `role`. A `require_role(...)` dependency factory gates recruiter-only and candidate-only endpoints. No refresh tokens, no rotation.

**Alternatives considered.**
- *Server-side sessions (cookie + session store)*: requires a session store (Redis or a sessions table) purely for auth, adding infrastructure for a scope this small, and complicates horizontal scaling (sticky sessions or a shared store).
- *Short-lived (15 min) access token + refresh token rotation*: the more production-typical choice for a consumer app with long-lived sessions and a meaningful blast-radius-reduction need. Explicitly deferred — see Scope Control below.

**Tradeoffs.** A 24-hour token that's stolen is valid for up to 24 hours with no revocation mechanism short of rotating the server's signing secret (which invalidates every session). This is a real security tradeoff, accepted here because: (a) there's no sensitive PII or payment data behind these endpoints, (b) the assessment's 3-day scope doesn't accommodate building and testing a rotation flow correctly (rotation bugs are a common source of "logged out randomly" and "session fixation" issues), and (c) it's explicitly documented rather than silently shipped.

**Consequences.** If this were to go further toward production, refresh-token rotation with a `refresh_tokens` table (token family tracking, reuse detection) would be the very next security investment — noted here so it isn't mistaken for an oversight.

---

## ADR-005: Vercel (frontend) + Render (backend) + Supabase (Postgres) — not one platform

**Context.** ADR-002 established two separately deployable applications. They need hosting that fits each one's actual runtime shape.

**Decision.** Static/SSR-capable frontend → Vercel. Long-running stateful API process → Render. Managed Postgres → Supabase.

**Alternatives considered.**
- *Everything on Vercel, including the API as serverless functions*: FastAPI is designed around a long-lived process (connection pooling, background startup validation via Pydantic Settings) — forcing it into short-lived serverless functions means re-establishing DB connections per invocation (or adding a separate pooler) and losing the simple "one process, one pool" model. Rejected as fighting the framework rather than working with it.
- *Everything on Render, including the frontend as a static site*: technically workable, but Vercel's edge network, preview deployments per PR, and zero-config Vite integration are specifically better suited to a frontend team's workflow, and the brief explicitly asks for a Vercel deployment.
- *Self-managed Postgres on Render*: Supabase's free tier, connection pooling, and dashboard reduce operational surface for a project this size, and decouple the database's lifecycle from the API service's.

**Tradeoffs.** Three vendor dashboards to configure instead of one, and a cross-origin request from Vercel's domain to Render's domain (handled via `CORS_ORIGINS`, see `shared/middleware`). In exchange, each piece runs on the platform actually built for its runtime model, and any one service can be redeployed or scaled independently.

**Consequences.** `DEPLOYMENT.md` has three distinct setup sections as a direct result of this decision; the CI/CD pipeline's `post-deploy-health-check` job exists specifically because deployment is now decoupled from this repo's own CI (Vercel/Render deploy via their own GitHub integrations, not a custom `deploy` job here).

---

## ADR-006: AI provider abstraction, defaulting to a mock provider

**Context.** The platform's one AI feature (job description generation) needs to work for a reviewer cloning the repo with zero setup, while still being swappable to a real LLM provider without touching business logic.

**Decision.** `LLMProvider` is an abstract port (`ai/domain/provider.py`) with two adapters: `MockLLMProvider` (deterministic, offline, zero cost — the default) and `OpenAICompatibleProvider` (works with OpenAI, Groq, or OpenRouter by changing only `AI_BASE_URL`/`AI_MODEL`/`AI_API_KEY`). `AIService` depends only on the abstraction; a factory (`ai/infrastructure/factory.py`) picks the implementation from settings at request time.

**Alternatives considered.**
- *Call OpenAI's SDK directly from the service/router*: the common shortcut. Rejected because it means every AI feature is untestable without a real API key and network access, and switching providers means touching every call site.
- *Require a real API key with no fallback*: would make the AI feature — and therefore a meaningful part of the submission — unusable to a reviewer who doesn't want to provision an OpenAI key just to evaluate a take-home project.

**Tradeoffs.** The mock provider's output is templated, not genuinely generated — anyone testing it will immediately see it's not a real model call. That's accepted as the right default specifically *because* it's honest about what it is (the output text says so explicitly) rather than faking realism.

**Consequences.** Every AI call is also persisted to an `ai_requests` audit row (requester, provider, model, success/failure) — this exists because the provider abstraction alone doesn't give visibility into real-world usage/failure patterns; the audit table does, and became the source for `AI_USAGE.md`.

---

## Scope Control

To ship something polished within the assessment window rather than something broad but shaky, the following were deliberately excluded — each is a scope decision, not an oversight:

- **Admin role** — two roles (recruiter, candidate) cover the platform's core value; a third role with its own permission surface would roughly double the RBAC test matrix for no functional gain in this submission.
- **Refresh-token rotation** — see ADR-004.
- **Real-time notifications, chat** — no clear business requirement for either in a job board's core loop (post → search → apply → review).
- **Analytics dashboards, recommendation engines** — genuinely valuable in a mature product, but each is its own multi-day project; building either shallowly would look worse than not building it.
- **Background workers, caching layers, Kubernetes, Docker Compose, a `/metrics` endpoint** — real production concerns at scale, but premature for a single-instance, low-traffic submission; adding them here would be complexity theater rather than a signal of judgment.
- **`skills`/`resumes`/`saved_jobs` tables and the Resume Match Analyzer AI feature** from the original architecture proposal — cut to keep the four shipped features (auth, jobs, applications, one AI feature) deep and fully tested rather than six features shipped shallowly. The `resume_text` field on `applications` captures the same information a `resumes` table would, without the extra join.
