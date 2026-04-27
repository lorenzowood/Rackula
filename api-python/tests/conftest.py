import pytest
from fastapi.testclient import TestClient

TEST_UUID = "550e8400-e29b-41d4-a716-446655440000"
OTHER_UUID = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"

VALID_YAML = f"""\
version: "1"
name: Test Layout
metadata:
  id: {TEST_UUID}
  name: Test Layout
  schema_version: "1"
racks: []
"""


@pytest.fixture
def data_dir(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    return d


@pytest.fixture
def client(data_dir, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    monkeypatch.delenv("RACKULA_API_WRITE_TOKEN", raising=False)
    from app import app
    return TestClient(app)


@pytest.fixture
def client_with_token(data_dir, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    monkeypatch.setenv("RACKULA_API_WRITE_TOKEN", "secret-token")
    from app import app
    return TestClient(app, headers={"Authorization": "Bearer secret-token"})
