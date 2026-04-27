import pytest
from .conftest import TEST_UUID, OTHER_UUID, VALID_YAML


def test_list_layouts_empty(client):
    r = client.get("/layouts")
    assert r.status_code == 200
    assert r.json() == {"layouts": []}


def test_create_layout(client):
    r = client.put(f"/layouts/{TEST_UUID}", content=VALID_YAML,
                   headers={"Content-Type": "text/yaml"})
    assert r.status_code == 201
    body = r.json()
    assert body["id"] == TEST_UUID
    assert body["message"] == "Layout created"


def test_list_layouts_after_create(client):
    client.put(f"/layouts/{TEST_UUID}", content=VALID_YAML,
               headers={"Content-Type": "text/yaml"})
    r = client.get("/layouts")
    assert r.status_code == 200
    layouts = r.json()["layouts"]
    assert len(layouts) == 1
    assert layouts[0]["id"] == TEST_UUID
    assert layouts[0]["name"] == "Test Layout"


def test_get_layout(client):
    client.put(f"/layouts/{TEST_UUID}", content=VALID_YAML,
               headers={"Content-Type": "text/yaml"})
    r = client.get(f"/layouts/{TEST_UUID}")
    assert r.status_code == 200
    assert "Test Layout" in r.text


def test_update_layout(client):
    client.put(f"/layouts/{TEST_UUID}", content=VALID_YAML,
               headers={"Content-Type": "text/yaml"})
    r = client.put(f"/layouts/{TEST_UUID}", content=VALID_YAML,
                   headers={"Content-Type": "text/yaml"})
    assert r.status_code == 200
    assert r.json()["message"] == "Layout updated"


def test_delete_layout(client):
    client.put(f"/layouts/{TEST_UUID}", content=VALID_YAML,
               headers={"Content-Type": "text/yaml"})
    r = client.delete(f"/layouts/{TEST_UUID}")
    assert r.status_code == 200
    assert r.json()["message"] == "Layout deleted"


def test_get_layout_after_delete(client):
    client.put(f"/layouts/{TEST_UUID}", content=VALID_YAML,
               headers={"Content-Type": "text/yaml"})
    client.delete(f"/layouts/{TEST_UUID}")
    r = client.get(f"/layouts/{TEST_UUID}")
    assert r.status_code == 404


def test_delete_layout_not_found(client):
    r = client.delete(f"/layouts/{TEST_UUID}")
    assert r.status_code == 404


def test_get_layout_not_found(client):
    r = client.get(f"/layouts/{TEST_UUID}")
    assert r.status_code == 404


def test_invalid_uuid_get(client):
    r = client.get("/layouts/not-a-uuid")
    assert r.status_code == 400


def test_invalid_uuid_put(client):
    r = client.put("/layouts/not-a-uuid", content=VALID_YAML,
                   headers={"Content-Type": "text/yaml"})
    assert r.status_code == 400


def test_invalid_uuid_delete(client):
    r = client.delete("/layouts/not-a-uuid")
    assert r.status_code == 400


def test_uuid_mismatch_in_body(client):
    yaml_with_different_id = f"""\
version: "1"
name: Test Layout
metadata:
  id: {OTHER_UUID}
  name: Test Layout
  schema_version: "1"
racks: []
"""
    r = client.put(f"/layouts/{TEST_UUID}", content=yaml_with_different_id,
                   headers={"Content-Type": "text/yaml"})
    assert r.status_code == 400
    assert "mismatch" in r.json()["error"].lower()


def test_empty_body(client):
    r = client.put(f"/layouts/{TEST_UUID}", content="   ",
                   headers={"Content-Type": "text/yaml"})
    assert r.status_code == 400


def test_invalid_yaml(client):
    r = client.put(f"/layouts/{TEST_UUID}", content=": invalid: [yaml",
                   headers={"Content-Type": "text/yaml"})
    assert r.status_code == 400


def test_layout_missing_name(client):
    r = client.put(f"/layouts/{TEST_UUID}", content="version: '1'\nracks: []",
                   headers={"Content-Type": "text/yaml"})
    assert r.status_code == 400


def test_layout_too_large(client):
    big = "x" * (1024 * 1024 + 1)
    r = client.put(f"/layouts/{TEST_UUID}", content=big,
                   headers={"Content-Type": "text/yaml"})
    assert r.status_code == 413


def test_api_prefix_layouts(client):
    r = client.get("/api/layouts")
    assert r.status_code == 200
    assert "layouts" in r.json()


def test_write_token_required(client_with_token):
    r = client_with_token.put(f"/layouts/{TEST_UUID}", content=VALID_YAML,
                              headers={"Content-Type": "text/yaml"})
    assert r.status_code == 201


def test_write_token_rejected(client_with_token):
    r = client_with_token.put(
        f"/layouts/{TEST_UUID}", content=VALID_YAML,
        headers={"Content-Type": "text/yaml", "Authorization": "Bearer wrong"},
    )
    assert r.status_code == 401


def test_write_token_missing(client_with_token):
    r = client_with_token.put(
        f"/layouts/{TEST_UUID}", content=VALID_YAML,
        headers={"Content-Type": "text/yaml", "Authorization": ""},
    )
    assert r.status_code == 401
