def test_recruiter_can_generate_job_description(client, recruiter_headers):
    resp = client.post(
        "/api/v1/ai/job-description",
        json={
            "role_title": "Senior Backend Engineer",
            "experience_level": "senior",
            "key_skills": ["Python", "FastAPI", "PostgreSQL"],
        },
        headers=recruiter_headers,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert "generated_description" in body["data"]
    assert len(body["data"]["generated_description"]) > 0


def test_candidate_cannot_generate_job_description(client, candidate_headers):
    resp = client.post(
        "/api/v1/ai/job-description",
        json={"role_title": "Anything", "experience_level": "mid", "key_skills": ["Python"]},
        headers=candidate_headers,
    )
    assert resp.status_code == 403


def test_ai_request_is_audited(client, recruiter_headers, db_session):
    from src.ai.domain.entities import AIRequest

    client.post(
        "/api/v1/ai/job-description",
        json={"role_title": "QA Engineer", "experience_level": "mid", "key_skills": ["Selenium"]},
        headers=recruiter_headers,
    )
    audit_rows = db_session.query(AIRequest).all()
    assert len(audit_rows) == 1
    assert audit_rows[0].succeeded is True
    assert audit_rows[0].provider == "mock"
