def test_register_recruiter_succeeds(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "email": "new.recruiter@talentflow.example.com",
            "password": "SecurePass123!",
            "full_name": "New Recruiter",
            "role": "recruiter",
            "company_name": "Acme Corp",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["user"]["role"] == "recruiter"
    assert "access_token" in body["data"]


def test_register_recruiter_without_company_fails(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "email": "no.company@talentflow.example.com",
            "password": "SecurePass123!",
            "full_name": "No Company",
            "role": "recruiter",
        },
    )
    assert resp.status_code == 422


def test_register_duplicate_email_conflicts(client):
    payload = {
        "email": "dup@talentflow.example.com",
        "password": "SecurePass123!",
        "full_name": "Dup User",
        "role": "candidate",
    }
    first = client.post("/api/v1/auth/register", json=payload)
    second = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "EMAIL_TAKEN"


def test_login_with_wrong_password_returns_401(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "loginuser@talentflow.example.com",
            "password": "SecurePass123!",
            "full_name": "Login User",
            "role": "candidate",
        },
    )
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "loginuser@talentflow.example.com", "password": "WrongPassword!"},
    )
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_login_with_nonexistent_email_returns_same_error_code(client):
    """Guards against user-enumeration: unknown email and wrong password
    must return the identical error code."""
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "ghost@talentflow.example.com", "password": "whatever123"},
    )
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_me_requires_auth(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401


def test_me_returns_current_user(client, candidate_headers):
    resp = client.get("/api/v1/auth/me", headers=candidate_headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["role"] == "candidate"
