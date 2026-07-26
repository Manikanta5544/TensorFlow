def _create_job(client, headers, **overrides):
    payload = {
        "title": "Senior Backend Engineer",
        "company_name": "Acme Corp",
        "location": "Hyderabad, India",
        "description": "We are looking for an experienced backend engineer to join our team.",
        "requirements": "5+ years Python experience",
        "employment_type": "full_time",
        "experience_level": "senior",
        "salary_min": 2000000,
        "salary_max": 3500000,
    }
    payload.update(overrides)
    return client.post("/api/v1/jobs", json=payload, headers=headers)


def test_candidate_cannot_create_job(client, candidate_headers):
    resp = _create_job(client, candidate_headers)
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "INSUFFICIENT_ROLE"


def test_recruiter_can_create_job(client, recruiter_headers):
    resp = _create_job(client, recruiter_headers)
    assert resp.status_code == 201
    assert resp.json()["data"]["title"] == "Senior Backend Engineer"


def test_salary_min_greater_than_max_is_rejected(client, recruiter_headers):
    resp = _create_job(client, recruiter_headers, salary_min=5000000, salary_max=1000000)
    assert resp.status_code == 422


def test_list_jobs_is_public(client, recruiter_headers):
    _create_job(client, recruiter_headers)
    resp = client.get("/api/v1/jobs")
    assert resp.status_code == 200
    assert resp.json()["meta"]["total"] == 1


def test_list_jobs_search_filters_by_title(client, recruiter_headers):
    _create_job(client, recruiter_headers, title="Senior Backend Engineer")
    _create_job(
        client,
        recruiter_headers,
        title="Frontend Developer",
        description="We are looking for a UI specialist to craft delightful web experiences.",
    )
    resp = client.get("/api/v1/jobs", params={"search": "Backend"})
    data = resp.json()["data"]
    assert len(data) == 1
    assert data[0]["title"] == "Senior Backend Engineer"


def test_list_jobs_pagination(client, recruiter_headers):
    for i in range(15):
        _create_job(client, recruiter_headers, title=f"Job {i}")
    resp = client.get("/api/v1/jobs", params={"page": 2, "page_size": 10})
    body = resp.json()
    assert len(body["data"]) == 5
    assert body["meta"]["total"] == 15
    assert body["meta"]["total_pages"] == 2


def test_only_owner_can_update_job(client, recruiter_headers, candidate_headers):
    job = _create_job(client, recruiter_headers).json()["data"]

    # A candidate isn't even role-eligible.
    resp = client.patch(
        f"/api/v1/jobs/{job['id']}", json={"title": "Hacked Title"}, headers=candidate_headers
    )
    assert resp.status_code == 403


def test_another_recruiter_cannot_update_someone_elses_job(client, recruiter_headers, db_session):
    job = _create_job(client, recruiter_headers).json()["data"]

    other = client.post(
        "/api/v1/auth/register",
        json={
            "email": "other.recruiter@talentflow.example.com",
            "password": "SecurePass123!",
            "full_name": "Other Recruiter",
            "role": "recruiter",
            "company_name": "Other Corp",
        },
    ).json()["data"]["access_token"]
    other_headers = {"Authorization": f"Bearer {other}"}

    resp = client.patch(f"/api/v1/jobs/{job['id']}", json={"title": "Hijacked"}, headers=other_headers)
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "NOT_JOB_OWNER"


def test_get_nonexistent_job_returns_404(client):
    import uuid

    resp = client.get(f"/api/v1/jobs/{uuid.uuid4()}")
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "JOB_NOT_FOUND"


def test_delete_job_is_soft_and_excluded_from_listing(client, recruiter_headers):
    job = _create_job(client, recruiter_headers).json()["data"]
    del_resp = client.delete(f"/api/v1/jobs/{job['id']}", headers=recruiter_headers)
    assert del_resp.status_code == 204

    listing = client.get("/api/v1/jobs").json()
    assert listing["meta"]["total"] == 0

    detail = client.get(f"/api/v1/jobs/{job['id']}")
    assert detail.status_code == 404
