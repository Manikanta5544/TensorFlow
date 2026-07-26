def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_readiness_check(client):
    resp = client.get("/ready")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ready"


def test_request_id_header_is_echoed(client):
    resp = client.get("/health", headers={"X-Request-ID": "test-correlation-id-123"})
    assert resp.headers["x-request-id"] == "test-correlation-id-123"


def test_unknown_route_returns_404(client):
    resp = client.get("/api/v1/nonexistent")
    assert resp.status_code == 404
