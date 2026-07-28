# TensorFlow AI

> AI-assisted Job Board built with FastAPI, React, PostgreSQL, and LLM-powered job description generation.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![React](https://img.shields.io/badge/React-19-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791)

## Overview

TensorFlow AI is a production-inspired full-stack job board that connects recruiters and candidates through a modern, scalable web platform. Recruiters can create and manage job postings, generate high-quality job descriptions using AI, and review applicants, while candidates can discover opportunities, apply for roles, and track their applications.

The project emphasizes clean architecture, maintainability, type safety, and production-oriented engineering practices over feature quantity. It demonstrates how a small engineering team could design, build, test, and deploy a scalable MVP using modern technologies and industry-standard development workflows.

**Live Demo:** [TensorFlow AI](https://tensor-flow-eight.vercel.app)

**API Documentation:** [Swagger UI](https://tensorflow-ai-backend.onrender.com/api/docs)

## Architecture Philosophy

The application follows a production-oriented architecture that emphasizes separation of concerns, maintainability, and scalability. The backend adopts a layered architecture with clear domain boundaries, while the frontend follows a feature-first structure for modularity and long-term maintainability.

Rather than maximizing feature count, the implementation prioritizes clean abstractions, consistent API design, comprehensive validation, and engineering practices that translate well to production systems.

## Stack

| Layer | Choice |
|---|---|
| Backend | FastAPI, SQLAlchemy 2.x, Alembic, Pydantic v2, PostgreSQL |
| Frontend | React 19, TypeScript (strict), Vite, TanStack Query, React Hook Form, Zod, Tailwind CSS |
| Auth | JWT (python-jose), bcrypt (passlib) |
| AI | OpenAI-compatible provider abstraction (Groq for production, mock provider for testing) |
| Infra | GitHub Actions (CI/CD), Vercel (frontend), Render (backend), Supabase (Postgres) |

## Highlights

- Production-style layered backend architecture
- Feature-first React frontend
- JWT authentication with role-based authorization
- AI-powered job description generation using an OpenAI-compatible provider abstraction
- Repository, Service, Unit of Work  design patterns
- SQLAlchemy 2.0 with Alembic migrations
- PostgreSQL hosted on Supabase
- Structured logging and centralized exception handling
- API versioning and OpenAPI documentation
- Comprehensive validation using Pydantic v2 and Zod
- GitHub Actions CI pipeline
- Automated deployment with GitHub Actions, Render, and Vercel

## Features

### Recruiters

- Secure recruiter authentication
- Create, edit, and manage job postings
- AI-assisted job description generation
- Review and manage applications
- Recruiter dashboard

### Candidates

- Secure candidate authentication
- Browse and search job listings
- Filter jobs by multiple criteria
- Submit applications
- Candidate dashboard

## Deployment

| Service | Platform |
|----------|----------|
| Frontend | Vercel |
| Backend | Render |
| Database | Supabase PostgreSQL |
| CI | GitHub Actions |
| API Documentation | FastAPI OpenAPI (Swagger UI) |

## Repository layout

```
tensorflow-ai/
├── backend/          
│   ├── src/
│   │   ├── auth/         
│   │   ├── jobs/
│   │   ├── applications/
│   │   ├── ai/
│   │   └── shared/       
│   ├── tests/
│   ├── migrations/       
│   └── seed/               
├── frontend/         
│   └── src/
│       ├── features/{auth,jobs,applications,dashboard,ai}
│       └── shared/{components,hooks,lib,types,utils}
├── .github/workflows/ci-cd.yml
├── render.yaml      
└── docs/             
```

## Quickstart (local development)

### Prerequisites
- Python 3.12+
- Node.js 20+
- A PostgreSQL database (local, or a free [Supabase](https://supabase.com) project — see [DEPLOYMENT.md](docs/DEPLOYMENT.md))


### Backend

```bash
cd backend
```

#### Create a virtual environment

**Linux/macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements-dev.txt

cp .env.example .env

alembic upgrade head
python -m seed.seed

uvicorn src.main:app --reload --port 8000
```

API is now live at `http://localhost:8000`, interactive docs at `http://localhost:8000/api/docs`.

Run the test suite:
```bash
pytest --cov=src --cov-report=term-missing
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App is now live at `http://localhost:5173` — it proxies `/api` to `localhost:8000` automatically (see `vite.config.ts`), so no `.env` is needed for local dev.

Run lint / typecheck / tests / build:
```bash
npm run lint
npm run typecheck
npm run test
npm run build
```

### Demo accounts (after running the seed script)

| Role | Email | Password |
|---|---|---|
| Recruiter | `recruiter1@tensorflow.example.com` | `DemoPass123!` |
| Candidate | `candidate1@tensorflow.example.com` | `DemoPass123!` |

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — layered architecture, request lifecycle, module boundaries
- [API.md](docs/API.md) — endpoint reference and response envelope contract
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) — step-by-step Supabase + Render + Vercel + CI/CD setup
- [AI_USAGE.md](docs/AI_USAGE.md) — how AI was used to build this, and how AI is used *in* the product
- [DECISIONS.md](docs/DECISIONS.md) — six ADRs covering the major architectural choices
- [CONTRIBUTING.md](docs/CONTRIBUTING.md) — git strategy, commit conventions, local dev workflow

## Design Decisions

To prioritize quality over breadth, the application intentionally focuses on the core hiring workflow. Features such as refresh-token rotation, background workers, real-time notifications, recommendation engines, analytics dashboards, caching layers, and microservices were intentionally excluded to keep the implementation cohesive and production-ready within the project's scope.

The rationale behind each architectural and scope decision is documented in `docs/DECISIONS.md`.

## Future Improvements

- Resume parsing and AI-assisted candidate matching
- Semantic job search using vector embeddings
- Email notifications
- OAuth authentication
- Refresh-token rotation
- Background task processing
- WebSocket-based real-time notifications
- Docker Compose for local orchestration
- Observability with Prometheus and Grafana

## License

This project is provided for demonstration and portfolio purposes.