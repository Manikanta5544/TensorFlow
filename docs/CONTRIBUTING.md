# Contributing

## Branch strategy

```
main
  ↑
feature/<short-description>
  ↑
Pull Request → GitHub Actions (lint, typecheck, test, build, security audit)
  ↑
Merge → Vercel/Render auto-deploy from main
```

`main` is always deployable. All work happens on a `feature/*` branch and merges via PR once CI passes.

## Commit conventions

[Conventional Commits](https://www.conventionalcommits.org/), enforced by convention rather than a commit-lint bot for this scope:

```
feat(auth): implement JWT authentication
fix(jobs): correct salary range validation
refactor(applications): extract status transition into a service method
test(jobs): add repository pagination tests
docs: add architecture decision records
ci: configure GitHub Actions deployment
chore: bump vitest to 3.x
```

Format: `<type>(<optional scope>): <description>`. Types: `feat`, `fix`, `refactor`, `test`, `docs`, `ci`, `chore`.

## Local development workflow

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env   # edit DATABASE_URL and JWT_SECRET_KEY

alembic upgrade head
python -m seed.seed

uvicorn src.main:app --reload --port 8000
```

Before committing:
```bash
ruff check .                                  # lint
mypy src --ignore-missing-imports              # type check (advisory)
pytest --cov=src --cov-report=term-missing     # tests + coverage
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Before committing:
```bash
npm run lint
npm run typecheck
npm run test
npm run build
```

### Adding a new backend feature slice

Follow the existing pattern (see ARCHITECTURE.md):
1. `src/<feature>/domain/entities.py` — the SQLAlchemy model(s)
2. `src/<feature>/domain/repository.py` — the abstract repository interface
3. `src/<feature>/infrastructure/repository_impl.py` — the SQLAlchemy implementation
4. `src/<feature>/application/service.py` — use cases, authorization, transactions
5. `src/<feature>/api/schemas.py` + `router.py` — thin controllers
6. Register the router in `src/main.py`
7. A migration: `alembic revision --autogenerate -m "add <feature> tables"` (review the generated file before committing — autogenerate is a starting point, not gospel)
8. Tests in `tests/<feature>/`

### Adding a new frontend feature

1. `src/features/<feature>/api/` — API functions (axios calls)
2. `src/features/<feature>/hooks/` — TanStack Query hooks wrapping the API functions
3. `src/features/<feature>/types/` — Zod schemas for any forms
4. `src/features/<feature>/components/` — page/component components
5. Wire into `src/App.tsx`'s router if it's a new page

## Code review expectations

- CI must pass (lint, typecheck, tests, build) before merge — no exceptions for "just a small change."
- New business logic in `application/` layers should have a corresponding test — see the existing `tests/*/test_*_api.py` files for the pattern (register/login fixtures in `conftest.py` make this fast to write).
- Prefer extending an existing pattern over introducing a new one; if a genuinely new pattern is needed, note it in DECISIONS.md.
