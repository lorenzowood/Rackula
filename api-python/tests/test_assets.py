import pytest
from .conftest import TEST_UUID, VALID_YAML

SLUG = "dell-r640"
PNG_1X1 = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00"
    b"\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _create_layout(client):
    client.put(f"/layouts/{TEST_UUID}", content=VALID_YAML,
               headers={"Content-Type": "text/yaml"})


def test_upload_asset(client):
    _create_layout(client)
    r = client.put(f"/assets/{TEST_UUID}/{SLUG}/front",
                   content=PNG_1X1, headers={"Content-Type": "image/png"})
    assert r.status_code == 200
    assert r.json()["message"] == "Asset uploaded"


def test_get_asset(client):
    _create_layout(client)
    client.put(f"/assets/{TEST_UUID}/{SLUG}/front",
               content=PNG_1X1, headers={"Content-Type": "image/png"})
    r = client.get(f"/assets/{TEST_UUID}/{SLUG}/front")
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"
    assert r.content == PNG_1X1


def test_delete_asset(client):
    _create_layout(client)
    client.put(f"/assets/{TEST_UUID}/{SLUG}/front",
               content=PNG_1X1, headers={"Content-Type": "image/png"})
    r = client.delete(f"/assets/{TEST_UUID}/{SLUG}/front")
    assert r.status_code == 200
    assert r.json()["message"] == "Asset deleted"


def test_get_asset_after_delete(client):
    _create_layout(client)
    client.put(f"/assets/{TEST_UUID}/{SLUG}/front",
               content=PNG_1X1, headers={"Content-Type": "image/png"})
    client.delete(f"/assets/{TEST_UUID}/{SLUG}/front")
    r = client.get(f"/assets/{TEST_UUID}/{SLUG}/front")
    assert r.status_code == 404


def test_get_asset_not_found(client):
    _create_layout(client)
    r = client.get(f"/assets/{TEST_UUID}/{SLUG}/front")
    assert r.status_code == 404


def test_asset_invalid_layout_id(client):
    r = client.get("/assets/not-a-uuid/dell-r640/front")
    assert r.status_code == 400


def test_asset_invalid_device_slug(client):
    _create_layout(client)
    # Slug starting with '-' fails the regex; '..'-style traversal gets normalized by HTTP layer
    r = client.get(f"/assets/{TEST_UUID}/-invalid-slug/front")
    assert r.status_code == 400


def test_asset_invalid_face(client):
    _create_layout(client)
    r = client.get(f"/assets/{TEST_UUID}/{SLUG}/side")
    assert r.status_code == 400


def test_asset_invalid_content_type(client):
    _create_layout(client)
    r = client.put(f"/assets/{TEST_UUID}/{SLUG}/front",
                   content=b"data", headers={"Content-Type": "image/gif"})
    assert r.status_code == 400


def test_asset_too_large(client):
    _create_layout(client)
    big = b"x" * (5 * 1024 * 1024 + 1)
    r = client.put(f"/assets/{TEST_UUID}/{SLUG}/front",
                   content=big, headers={"Content-Type": "image/png"})
    assert r.status_code == 413


def test_delete_asset_not_found(client):
    _create_layout(client)
    r = client.delete(f"/assets/{TEST_UUID}/{SLUG}/front")
    assert r.status_code == 404


def test_rear_face(client):
    _create_layout(client)
    r = client.put(f"/assets/{TEST_UUID}/{SLUG}/rear",
                   content=PNG_1X1, headers={"Content-Type": "image/png"})
    assert r.status_code == 200


def test_device_slug_with_underscores(client):
    _create_layout(client)
    r = client.put(f"/assets/{TEST_UUID}/dell_r640/front",
                   content=PNG_1X1, headers={"Content-Type": "image/png"})
    assert r.status_code == 200


def test_delete_layout_removes_assets(client):
    _create_layout(client)
    client.put(f"/assets/{TEST_UUID}/{SLUG}/front",
               content=PNG_1X1, headers={"Content-Type": "image/png"})
    client.delete(f"/layouts/{TEST_UUID}")
    r = client.get(f"/assets/{TEST_UUID}/{SLUG}/front")
    assert r.status_code == 404
