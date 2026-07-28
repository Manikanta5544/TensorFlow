import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


def _load_env_test() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env.test"
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ[key] = value


_load_env_test()

from src.main import app  # noqa: E402
from src.shared.database.session import Base, get_db  # noqa: E402


@pytest.fixture()
def db_session():
    """A fresh in-memory SQLite DB per test — fast, isolated, zero setup."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def recruiter_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "recruiter@tensorflow.example.com",
            "password": "SecurePass123!",
            "full_name": "Rita Recruiter",
            "role": "recruiter",
            "company_name": "Acme Corp",
        },
    )
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "recruiter@tensorflow.example.com", "password": "SecurePass123!"},
    )
    token = resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def candidate_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "candidate@tensorflow.example.com",
            "password": "SecurePass123!",
            "full_name": "Cody Candidate",
            "role": "candidate",
        },
    )
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "candidate@tensorflow.example.com", "password": "SecurePass123!"},
    )
    token = resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
