def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["status"] == "ok"
    assert body["service"] == "rackula-persistence-api"
    assert body["version"] == 1


def test_health_api_prefix(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True
