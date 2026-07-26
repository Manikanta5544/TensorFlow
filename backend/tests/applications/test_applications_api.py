def _create_job(client, recruiter_headers):
    payload = {
        "title": "Senior Backend Engineer",
        "company_name": "Acme Corp",
        "location": "Hyderabad, India",
        "description": "We are looking for an experienced backend engineer to join our team.",
        "requirements": "5+ years Python experience",
        "employment_type": "full_time",
        "experience_level": "senior",
    }
    return client.post("/api/v1/jobs", json=payload, headers=recruiter_headers).json()["data"]


def test_candidate_can_apply_to_job(client, recruiter_headers, candidate_headers):
    job = _create_job(client, recruiter_headers)
    resp = client.post(
        f"/api/v1/jobs/{job['id']}/applications",
        json={
            "cover_letter": "I'd love to join!",
            "resume_text": "5 years of Python and FastAPI experience.",
        },
        headers=candidate_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["data"]["status"] == "submitted"


def test_recruiter_cannot_apply_to_job(client, recruiter_headers):
    job = _create_job(client, recruiter_headers)
    resp = client.post(
        f"/api/v1/jobs/{job['id']}/applications",
        json={"cover_letter": "", "resume_text": "Trying to apply as a recruiter account."},
        headers=recruiter_headers,
    )
    assert resp.status_code == 403


def test_duplicate_application_is_rejected(client, recruiter_headers, candidate_headers):
    job = _create_job(client, recruiter_headers)
    body = {"cover_letter": "", "resume_text": "Applying once, then trying again to test idempotency."}

    first = client.post(f"/api/v1/jobs/{job['id']}/applications", json=body, headers=candidate_headers)
    second = client.post(f"/api/v1/jobs/{job['id']}/applications", json=body, headers=candidate_headers)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "ALREADY_APPLIED"


def test_recruiter_sees_applications_for_own_job_only(client, recruiter_headers, candidate_headers):
    job = _create_job(client, recruiter_headers)
    client.post(
        f"/api/v1/jobs/{job['id']}/applications",
        json={"cover_letter": "", "resume_text": "Applying to the only job in this test."},
        headers=candidate_headers,
    )
    resp = client.get(f"/api/v1/jobs/{job['id']}/applications", headers=recruiter_headers)
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 1


def test_candidate_can_list_own_applications(client, recruiter_headers, candidate_headers):
    job = _create_job(client, recruiter_headers)
    client.post(
        f"/api/v1/jobs/{job['id']}/applications",
        json={"cover_letter": "", "resume_text": "Applying to check my own applications list."},
        headers=candidate_headers,
    )
    resp = client.get("/api/v1/applications/mine", headers=candidate_headers)
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 1


def test_recruiter_can_update_application_status(client, recruiter_headers, candidate_headers):
    job = _create_job(client, recruiter_headers)
    application = client.post(
        f"/api/v1/jobs/{job['id']}/applications",
        json={"cover_letter": "", "resume_text": "Applying so status update can be tested."},
        headers=candidate_headers,
    ).json()["data"]

    resp = client.patch(
        f"/api/v1/applications/{application['id']}/status",
        json={"status": "accepted"},
        headers=recruiter_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "accepted"
