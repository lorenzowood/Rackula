"""Rackula persistence API — Python/FastAPI rewrite."""
import os
import re
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import storage

MAX_LAYOUT_SIZE = 1 * 1024 * 1024  # 1 MB
MAX_ASSET_SIZE = 5 * 1024 * 1024   # 5 MB

UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I
)
DEVICE_SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9_-]*[a-z0-9]$|^[a-z0-9]$')

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_ORIGIN", "http://localhost:8080")],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.exception_handler(FastAPIHTTPException)
async def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)


def write_auth(request: Request) -> None:
    token = os.environ.get("RACKULA_API_WRITE_TOKEN", "")
    if not token:
        return
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {token}":
        raise HTTPException(status_code=401, detail="Unauthorized")


def _validate_uuid(value: str) -> str:
    if not UUID_RE.match(value):
        raise HTTPException(400, "Invalid layout UUID format")
    return value


def _validate_device_slug(value: str) -> str:
    if not DEVICE_SLUG_RE.match(value):
        raise HTTPException(400, "Invalid device slug format")
    return value


def _validate_face(value: str) -> str:
    if value not in ("front", "rear"):
        raise HTTPException(400, "Face must be 'front' or 'rear'")
    return value


router = APIRouter()

HEALTH_RESPONSE = {
    "ok": True, "status": "ok",
    "service": "rackula-persistence-api", "version": 1,
}


@router.get("/health")
def health():
    return HEALTH_RESPONSE


@router.get("/layouts")
def list_layouts():
    return {"layouts": storage.list_layouts()}


@router.get("/layouts/{uuid}")
def get_layout(uuid: str):
    _validate_uuid(uuid)
    content = storage.get_layout(uuid)
    if content is None:
        raise HTTPException(404, "Layout not found")
    return Response(content=content, media_type="text/yaml")


@router.put("/layouts/{uuid}", dependencies=[Depends(write_auth)])
async def put_layout(uuid: str, request: Request):
    _validate_uuid(uuid)
    body = await request.body()
    if len(body) > MAX_LAYOUT_SIZE:
        raise HTTPException(413, "Layout data too large")
    yaml_content = body.decode("utf-8")
    if not yaml_content.strip():
        raise HTTPException(400, "Request body is empty")
    try:
        result = storage.save_layout(yaml_content, uuid)
    except ValueError as e:
        raise HTTPException(400, str(e))
    status = 201 if result["is_new"] else 200
    msg = "Layout created" if result["is_new"] else "Layout updated"
    return JSONResponse({"id": result["id"], "message": msg}, status_code=status)


@router.delete("/layouts/{uuid}", dependencies=[Depends(write_auth)])
def delete_layout(uuid: str):
    _validate_uuid(uuid)
    if not storage.delete_layout(uuid):
        raise HTTPException(404, "Layout not found")
    return {"message": "Layout deleted"}


@router.get("/assets/{layout_id}/{device_slug}/{face}")
def get_asset(layout_id: str, device_slug: str, face: str):
    _validate_uuid(layout_id)
    _validate_device_slug(device_slug)
    _validate_face(face)
    asset = storage.get_asset(layout_id, device_slug, face)
    if asset is None:
        raise HTTPException(404, "Asset not found")
    return Response(
        content=asset["data"],
        media_type=asset["content_type"],
        headers={"Cache-Control": "public, max-age=3600, must-revalidate"},
    )


@router.put("/assets/{layout_id}/{device_slug}/{face}", dependencies=[Depends(write_auth)])
async def put_asset(layout_id: str, device_slug: str, face: str, request: Request):
    _validate_uuid(layout_id)
    _validate_device_slug(device_slug)
    _validate_face(face)
    content_type = request.headers.get("content-type", "")
    if content_type not in ("image/png", "image/jpeg", "image/webp"):
        raise HTTPException(
            400, "Invalid content type. Must be image/png, image/jpeg, or image/webp"
        )
    cl = request.headers.get("content-length")
    if cl and int(cl) > MAX_ASSET_SIZE:
        raise HTTPException(413, "File too large. Maximum size is 5MB")
    data = await request.body()
    if len(data) > MAX_ASSET_SIZE:
        raise HTTPException(413, "File too large. Maximum size is 5MB")
    try:
        storage.save_asset(layout_id, device_slug, face, data, content_type)
    except FileNotFoundError:
        raise HTTPException(404, "Layout not found")
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"message": "Asset uploaded"}


@router.delete("/assets/{layout_id}/{device_slug}/{face}", dependencies=[Depends(write_auth)])
def delete_asset(layout_id: str, device_slug: str, face: str):
    _validate_uuid(layout_id)
    _validate_device_slug(device_slug)
    _validate_face(face)
    if not storage.delete_asset(layout_id, device_slug, face):
        raise HTTPException(404, "Asset not found")
    return {"message": "Asset deleted"}


app.include_router(router)
app.include_router(router, prefix="/api")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse({"error": "Not found"}, status_code=404)
