# API Reference

Base URL: `/api/v1` (interactive OpenAPI docs at `/api/docs`, raw schema at `/api/openapi.json`).

## Response envelope

Every endpoint returns one of two shapes.

**Success:**
```json
{
  "success": true,
  "data": { "...": "..." },
  "meta": { "page": 1, "page_size": 10, "total": 42, "total_pages": 5 }
}
```
`meta` fields are only present where relevant (e.g. pagination on list endpoints); omitted otherwise.

**Failure:**
```json
{
  "success": false,
  "error": {
    "code": "JOB_NOT_FOUND",
    "message": "Job not found.",
    "details": null
  }
}
```

`code` is a stable, machine-readable string safe to branch on in client code (see error codes table below). `message` is human-readable and safe to display directly.

## Authentication

Send `Authorization: Bearer <access_token>` on any authenticated endpoint. Tokens are issued by `/auth/login` and `/auth/register`, last 24 hours (see ADR-004), and carry the user's role — endpoints marked "Recruiter" or "Candidate" below reject the other role with `403 INSUFFICIENT_ROLE`.

---

## Auth

### `POST /auth/register`
Public. Body:
```json
{
  "email": "jane@example.com",
  "password": "SecurePass123!",
  "full_name": "Jane Doe",
  "role": "recruiter",
  "company_name": "Acme Corp"
}
```
`company_name` is required when `role` is `"recruiter"`, omitted/ignored for `"candidate"`. Returns `201` with `{ user, access_token, token_type }`.

### `POST /auth/login`
Public. Body: `{ "email": "...", "password": "..." }`. Returns `{ user, access_token, token_type }`. Wrong password and unknown email both return `401 INVALID_CREDENTIALS` (no user-enumeration).

### `GET /auth/me`
Authenticated. Returns the current user.

---

## Jobs

### `GET /jobs`
Public. Lists **open, non-deleted** jobs. Query params: `search` (matches title or description), `location`, `employment_type`, `experience_level`, `page` (default 1), `page_size` (default 10, max 50), `sort_by` (`created_at` | `title` | `salary_min`), `sort_dir` (`asc` | `desc`). Response `meta` includes pagination totals.

### `GET /jobs/{job_id}`
Public. Returns a single job, or `404 JOB_NOT_FOUND`.

### `POST /jobs`
Recruiter only. Body matches the job fields (title, company_name, location, description, requirements, employment_type, experience_level, salary_min, salary_max). `salary_min > salary_max` is rejected with `422`. Returns `201`.

### `PATCH /jobs/{job_id}`
Recruiter only, **and** must own the job (`403 NOT_JOB_OWNER` otherwise). Partial update — any subset of the create fields, plus `status` (`open`/`closed`).

### `DELETE /jobs/{job_id}`
Recruiter only, must own the job. Soft delete (`is_deleted = true`) — the job stops appearing in `/jobs` and `GET /jobs/{id}` returns `404` afterward, but the row (and its applications) are retained.

### `GET /jobs/mine/list`
Recruiter only. Returns *all* of the caller's own non-deleted jobs, including closed ones (unlike the public `/jobs` listing).

---

## Applications

### `POST /jobs/{job_id}/applications`
Candidate only. Body: `{ "cover_letter": "...", "resume_text": "..." }` (`resume_text` required, ≥20 chars; `cover_letter` optional). Applying twice to the same job returns `409 ALREADY_APPLIED` (idempotency guard via a DB unique constraint — see ADR in DECISIONS.md's Scope Control on idempotency). Returns `201`.

### `GET /jobs/{job_id}/applications`
Recruiter only, must own the job. Lists all applications for that job.

### `GET /applications/mine`
Candidate only. Lists the caller's own applications across all jobs.

### `PATCH /applications/{application_id}/status`
Recruiter only, must own the underlying job. Body: `{ "status": "reviewed" | "accepted" | "rejected" | "submitted" }`.

---

## AI

### `POST /ai/job-description`
Recruiter only. Body:
```json
{
  "role_title": "Senior Backend Engineer",
  "experience_level": "senior",
  "key_skills": ["Python", "FastAPI", "PostgreSQL"]
}
```
Returns `{ "generated_description": "..." }`. Uses whichever provider is configured via `AI_PROVIDER` (mock by default — see AI_USAGE.md). Every call is recorded to an internal audit log regardless of outcome.

---

## Operational endpoints (unversioned, no `/api/v1` prefix)

### `GET /health`
Liveness probe — process is up. No dependency checks. Always `200` if the process is running.

### `GET /ready`
Readiness probe — executes `SELECT 1` against the database. Returns `503` if the database is unreachable. Used by Render's health check (see `render.yaml`) and the CI/CD pipeline's post-deploy check.

---

## Error codes

| Code | HTTP status | Meaning |
|---|---|---|
| `VALIDATION_ERROR` | 422 | Request body failed schema validation |
| `MISSING_TOKEN` / `INVALID_TOKEN` | 401 | No/invalid/expired JWT |
| `INVALID_CREDENTIALS` | 401 | Login failed (wrong password or unknown email) |
| `ACCOUNT_INACTIVE` | 401 | Account deactivated |
| `INSUFFICIENT_ROLE` | 403 | Authenticated, but wrong role for this endpoint |
| `NOT_JOB_OWNER` | 403 | Recruiter authenticated, but doesn't own the target job |
| `JOB_NOT_FOUND` | 404 | Job doesn't exist or was soft-deleted |
| `APPLICATION_NOT_FOUND` | 404 | Application doesn't exist |
| `EMAIL_TAKEN` | 409 | Registration with an already-used email |
| `ALREADY_APPLIED` | 409 | Duplicate application to the same job |
| `COMPANY_REQUIRED` | 409 | Recruiter registration without `company_name` |
| `AI_PROVIDER_ERROR` | 400 | The configured AI provider call failed |
| `INTERNAL_ERROR` | 500 | Unhandled server error (logged with full traceback server-side) |
