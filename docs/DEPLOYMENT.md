# Deployment Guide

This gets the repo from "code on your machine" to a live URL. Total time: roughly 15–20 minutes, almost all of it clicking through free-tier signup forms. See ADR-005 in [DECISIONS.md](DECISIONS.md) for why the deployment is split across three platforms.

## 0. Push to GitHub

```bash
git init
git add .
git commit -m "feat: initial commit — TensorFlow AI"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## 1. Database — Supabase

1. Create a free project at [supabase.com](https://supabase.com).
2. Go to **Project Settings → Database → Connection string**, select the **URI** tab, and choose the **Session pooler** connection (not "Direct connection" — the pooler handles connection limits correctly for a serverless-adjacent backend).
3. Copy that URI. It looks like:
   ```
   postgresql://postgres.xxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:5432/postgres
   ```
4. Replace `[YOUR-PASSWORD]` with your actual database password (set when you created the project). Save this full string — it's your `DATABASE_URL`.

## 2. Backend — Render

1. Create a free account at [render.com](https://render.com) and connect your GitHub account.
2. **New → Blueprint**, select this repository. Render detects `render.yaml` at the repository root and creates the backend service automatically.
3. Before the first deploy, configure the required secret environment variables (marked `sync: false` in `render.yaml`):
   - `DATABASE_URL` — the Supabase connection string from Step 1.
   - `JWT_SECRET_KEY` — generate one locally:
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(48))"
     ```
   - `CORS_ORIGINS` — temporarily set to `http://localhost:5173`; update it after deploying the frontend.
   - `AI_API_KEY` — optional. Leave blank to use the default mock provider, or provide a key for a real OpenAI-compatible provider.
4. Deploy. Render installs the dependencies, then starts the application using the `startCommand` defined in `render.yaml`, which automatically applies the latest Alembic migrations before launching the FastAPI server.
5. Once deployment completes, note the backend URL (for example, `https://tensorflow-ai-backend.onrender.com`).
6. Seed the database using your preferred approach (for example, by running `python -m seed.seed` locally against the production `DATABASE_URL`, or by temporarily executing the seed script during deployment if using Render's Free plan). This populates the demo accounts and sample data.
7. Verify the deployment by visiting:

- `https://<your-backend>.onrender.com/health`
- `https://<your-backend>.onrender.com/ready`

Both endpoints should return `200 OK`.

## 3. Frontend — Vercel

1. Create a free account at [vercel.com](https://vercel.com), connect GitHub.
2. **Add New → Project**, select this repository. When Vercel asks for the root directory, set it to `frontend/` (it will auto-detect the Vite framework from `frontend/vercel.json`).
3. Add one environment variable: `VITE_API_URL` = your Render backend URL from step 2.5 (no trailing slash, no `/api` suffix — the app appends `/api/v1` itself).
4. Deploy. Note the resulting URL: `https://tensorflow-ai.vercel.app` (or similar).

## 4. Close the loop — CORS

Go back to Render → your backend service → Environment, and update `CORS_ORIGINS` to your real Vercel URL from step 3.4. Redeploy (Render redeploys automatically on env var changes).

## 5. CI/CD — GitHub Actions

Already wired via `.github/workflows/ci-cd.yml` — it runs automatically on every push/PR to `main` (lint, typecheck, test, build, security audit for both frontend and backend). No setup needed for the quality-gate jobs.

**Optional — enable the post-deploy health check job:** in your GitHub repo, go to **Settings → Secrets and variables → Actions**, add a secret `BACKEND_URL` with your Render backend URL. The `post-deploy-health-check` job will then actually curl `/health` and `/ready` after each push to `main` and fail the pipeline if the live backend isn't healthy. Without this secret, that job is a no-op (it says so explicitly rather than failing silently).

**How deployment is actually triggered:** Vercel and Render both deploy automatically via their own GitHub integrations on every push to `main` — independent of this repo's GitHub Actions workflow. The Actions workflow is the quality gate (and, once `BACKEND_URL` is set, the post-deploy verifier); Vercel/Render are the deployers. This is standard practice and avoids re-implementing what those platforms already do well (see ADR-005).

## Local development (no cloud accounts needed)

You don't need Supabase/Render/Vercel to run this locally — see the Quickstart in the root [README.md](../README.md). A local PostgreSQL instance or a Supabase project is the only external dependency; the AI feature works offline via the mock provider by default.

## Rotating secrets

If `JWT_SECRET_KEY` is ever exposed, generate a new one and update it in the Render dashboard — this immediately invalidates all existing sessions (see ADR-004's tradeoff on no refresh-token rotation: this is the blast-radius mitigation available today). Database credentials rotate from the Supabase dashboard under **Project Settings → Database**.
