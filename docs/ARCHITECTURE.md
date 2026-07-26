# Architecture

See [DECISIONS.md](DECISIONS.md) for *why* each of these choices was made. This document describes *what* the architecture is and how a request flows through it.

## Backend: vertical-slice + layered

Each feature (`auth`, `jobs`, `applications`, `ai`) is a self-contained slice with four internal layers:

```
src/<feature>/
├── api/              FastAPI router + Pydantic request/response schemas
├── application/       Use-case orchestration (the "service" class)
├── domain/            Entities (SQLAlchemy models), repository interfaces, business rules
└── infrastructure/    Repository implementations, external adapters
```

### Layer responsibilities (strict)

| Layer | Owns | Never contains |
|---|---|---|
| **api/** | Request validation (Pydantic), calling exactly one service method, mapping the result to the response envelope | Business logic, raw SQL, prompt construction |
| **application/** | Use-case workflows, transaction boundaries (`db.commit()`), authorization checks that depend on business state (e.g. "is this recruiter the job's owner?") | Framework-specific code (no `Request`/`Response`, no SQLAlchemy queries written inline — goes through the repository) |
| **domain/** | Entities, enums, repository *interfaces* (abstract base classes), pure business rules | SQLAlchemy session usage, HTTP status codes |
| **infrastructure/** | Repository *implementations* (SQLAlchemy queries), external API adapters (the AI provider adapters) | Business rules — infrastructure just persists/retrieves what the domain asks for |

A controller (router function) in `api/` is intentionally thin:

```python
@router.post("", status_code=201)
def create_job(payload: JobCreateRequest, current_user=Depends(require_role(UserRole.RECRUITER)), db=Depends(get_db)):
    job = JobService(db).create_job(recruiter_id=current_user.id, **payload.model_dump())
    return ok(JobResponse.model_validate(job).model_dump())
```

Validate → authorize (via the `Depends`) → call service → return envelope. Nothing else.

### Shared kernel (`src/shared/`)

Cross-cutting concerns that every feature needs, implemented once:

- **`config/`** — Pydantic `Settings`, validated at process startup (fail-fast: a missing `DATABASE_URL` crashes on boot, not on the first request).
- **`database/`** — SQLAlchemy engine/session setup, a `PortableUUID` type (native Postgres UUID in production, portable in the SQLite-backed test suite), UUID/timestamp mixins.
- **`security/`** — password hashing (bcrypt), JWT issuance/verification, the `get_current_user`/`require_role` FastAPI dependencies.
- **`exceptions/`** — a small hierarchy of domain exceptions (`NotFoundError`, `ForbiddenError`, `ConflictError`, ...) that carry a stable `code` and `http_status`, decoupling business logic from HTTP concerns.
- **`responses/`** — the `{success, data, meta}` / `{success, error}` envelope every endpoint returns.
- **`middleware/`** — request-ID correlation + structured access logging, applied once at the app level.
- **`logging/`** — JSON log formatter that pulls the current request ID from a context variable.

## Request lifecycle

```
Client
  │
  ▼
CORS middleware  ──────────────────────────────────────────────
  │
  ▼
RequestContextMiddleware   (assigns/reads X-Request-ID, times the request,
  │                         logs one structured line on completion)
  ▼
FastAPI routing → api/router.py
  │
  ▼
Pydantic validation of the request body (422 on failure, via the global
  │                                       RequestValidationError handler)
  ▼
Depends(require_role(...)) → JWT decoded, user loaded, role checked
  │                            (401/403 via AppError → global handler)
  ▼
application/service.py       (use case: authorization against business
  │                            state, orchestration, db.commit())
  ▼
infrastructure/repository_impl.py   (SQLAlchemy query execution)
  │
  ▼
domain/entities.py           (ORM model, mapped to/from the DB)
  │
  ▼
Response mapped through a Pydantic schema → wrapped in the envelope → JSON
```

Any `AppError` raised anywhere in this chain (from any layer) is caught once, centrally, by the global exception handler in `main.py` and translated to the correct HTTP status + the standard error envelope — no endpoint hand-writes its own error responses.

## Frontend: feature-first

```
frontend/src/
├── features/
│   ├── auth/          auth-context.tsx (client state), api/, components/, types/ (Zod schemas)
│   ├── jobs/           api/, hooks/ (TanStack Query), components/
│   ├── applications/
│   ├── dashboard/       role-aware: RecruiterDashboard vs CandidateDashboard
│   └── ai/               the job-description-generation hook, consumed inside jobs/PostJobPage
└── shared/
    ├── components/ui/    Button, TextField, SelectField, Card, Badge, Spinner, EmptyState
    ├── lib/                axios instance + JWT interceptor
    ├── types/              types mirroring the backend's Pydantic schemas
    └── utils/               formatting helpers (salary, dates)
```

**State model** (see ADR-003): server state lives in TanStack Query hooks (`useJobs`, `useApplicationsForJob`, ...) — caching, invalidation, and loading/error states come for free. Client state (the current user) lives in one React Context. Everything else is local `useState`.

**Data flow example — posting a job with AI assist:**
`PostJobPage` → `useGenerateJobDescription()` mutation → `POST /api/v1/ai/job-description` → response fills the `description` textarea via `setValue` (React Hook Form) → on submit, `useCreateJob()` mutation → `POST /api/v1/jobs` → on success, `queryClient.invalidateQueries(["jobs"])` so the listing page picks up the new job on next visit, and the user is navigated to the new job's detail page.

## Why AI features are a first-class slice, not a bolted-on call

`ai/` has the exact same four-layer structure as every other feature. The `LLMProvider` abstraction (domain layer) means `AIService` (application layer) has zero knowledge of which concrete provider is running — see ADR-006. This is what makes it possible for the whole platform, AI feature included, to run and be fully testable with zero external API keys.
