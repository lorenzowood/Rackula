"""Filesystem storage for Rackula layouts and assets."""
import os
import re
import uuid as uuid_module
import shutil
import tempfile
from pathlib import Path
from typing import Optional

import yaml
from datetime import datetime, timezone


def _mtime_iso(path: Path) -> str:
    """Return mtime as ISO 8601 matching JS Date.toISOString(): ...mmmZ"""
    dt = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.') + f'{dt.microsecond // 1000:03d}Z'

UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I
)
UUID_EXTRACT_RE = re.compile(
    r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I
)
DEVICE_SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9_-]*[a-z0-9]$|^[a-z0-9]$')
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp"}
ALLOWED_EXTS = {"png": "image/png", "jpg": "image/jpeg", "webp": "image/webp"}
MAX_ASSET_SIZE = 5 * 1024 * 1024

CONTENT_TYPE_TO_EXT = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}


def get_data_dir() -> Path:
    return Path(os.environ.get("DATA_DIR", "./data"))


def is_uuid(s: str) -> bool:
    return bool(UUID_RE.match(s))


def is_valid_device_slug(s: str) -> bool:
    return bool(DEVICE_SLUG_RE.match(s))


def _extract_uuid_from_folder(name: str) -> Optional[str]:
    m = UUID_EXTRACT_RE.search(name)
    return m.group(0) if m else None


def _sanitize_for_path(name: str) -> str:
    s = re.sub(r'[/\\:*?"<>|]', '-', name)
    s = s.replace('..', '-')
    s = re.sub(r'-+', '-', s).strip('-').strip()[:100]
    return s or "untitled"


def _slugify(name: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', name.lower().strip()).strip('-')[:100].rstrip('-')
    return s or "untitled"


def _folder_name(name: str, uid: str) -> str:
    return f"{_sanitize_for_path(name)}-{uid}"


def _yaml_filename(name: str) -> str:
    return f"{_slugify(name)}.rackula.yaml"


def _find_folder_by_uuid(uid: str) -> Optional[Path]:
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    uid_lower = uid.lower()
    for entry in data_dir.iterdir():
        if entry.is_dir():
            extracted = _extract_uuid_from_folder(entry.name)
            if extracted and extracted.lower() == uid_lower:
                return entry
    return None


def _find_yaml_in_folder(folder: Path) -> Optional[Path]:
    for f in folder.iterdir():
        if f.name.endswith(".rackula.yaml"):
            return f
    return None


def _count_devices(racks: list) -> int:
    return sum(len(r.get("devices", [])) for r in racks if isinstance(r, dict))


def _is_safe_legacy_slug(s: str) -> bool:
    if not s or '/' in s or '\\' in s or '.' in s:
        return False
    return all(0x20 <= ord(c) < 0x7f for c in s)


# ---------------------------------------------------------------------------
# Layout storage
# ---------------------------------------------------------------------------

def list_layouts() -> list:
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    items = []
    migrated_slugs: set[str] = set()

    for entry in data_dir.iterdir():
        if not entry.is_dir():
            continue
        uid = _extract_uuid_from_folder(entry.name)
        if not uid:
            continue
        yaml_file = _find_yaml_in_folder(entry)
        if yaml_file:
            migrated_slugs.add(yaml_file.stem.replace(".rackula", ""))
        item = _read_layout_from_folder(entry, yaml_file)
        if item:
            items.append(item)

    # Legacy flat files
    for entry in data_dir.iterdir():
        if entry.is_file() and entry.suffix.lower() in ('.yaml', '.yml'):
            slug = entry.stem
            if slug in migrated_slugs:
                continue
            item = _read_legacy_layout(entry)
            if item:
                items.append(item)

    items.sort(key=lambda x: x["updatedAt"], reverse=True)
    return items


def _read_layout_from_folder(folder: Path, yaml_file: Optional[Path] = None) -> Optional[dict]:
    uid = _extract_uuid_from_folder(folder.name)
    if not uid:
        return None
    yf = yaml_file or _find_yaml_in_folder(folder)
    if not yf:
        return None
    try:
        content = yf.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        stat = yf.stat()
        updated = _mtime_iso(yf)
        if isinstance(data, dict) and data.get("name") and data.get("version"):
            racks = data.get("racks") or []
            return {
                "id": uid,
                "name": data["name"],
                "version": str(data["version"]),
                "updatedAt": updated,
                "rackCount": len(racks),
                "deviceCount": _count_devices(racks),
                "valid": True,
            }
        human_name = folder.name.replace(f"-{uid}", "")
        return {"id": uid, "name": human_name, "version": "unknown",
                "updatedAt": updated, "rackCount": 0, "deviceCount": 0, "valid": False}
    except Exception:
        updated = _mtime_iso(folder)
        return {"id": uid, "name": folder.name.replace(f"-{uid}", ""),
                "version": "unknown", "updatedAt": updated,
                "rackCount": 0, "deviceCount": 0, "valid": False}


def _read_legacy_layout(path: Path) -> Optional[dict]:
    slug = path.stem
    try:
        content = path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        updated = _mtime_iso(path)
        if isinstance(data, dict) and data.get("name"):
            racks = data.get("racks") or []
            return {
                "id": slug, "name": data["name"],
                "version": str(data.get("version", "unknown")),
                "updatedAt": updated, "rackCount": len(racks),
                "deviceCount": _count_devices(racks), "valid": True,
            }
        return {"id": slug, "name": slug, "version": "unknown",
                "updatedAt": updated, "rackCount": 0, "deviceCount": 0, "valid": False}
    except Exception:
        updated = _mtime_iso(path)
        return {"id": slug, "name": slug, "version": "unknown",
                "updatedAt": updated, "rackCount": 0, "deviceCount": 0, "valid": False}


def get_layout(uid: str) -> Optional[str]:
    if is_uuid(uid):
        folder = _find_folder_by_uuid(uid)
        if folder:
            yf = _find_yaml_in_folder(folder)
            if yf:
                return yf.read_text(encoding="utf-8")

    # Legacy fallback
    if not _is_safe_legacy_slug(uid):
        return None
    data_dir = get_data_dir()
    for ext in ('.yaml', '.yml'):
        p = data_dir / f"{uid}{ext}"
        if p.exists():
            return p.read_text(encoding="utf-8")
    return None


def save_layout(yaml_content: str, existing_id: Optional[str] = None) -> dict:
    get_data_dir().mkdir(parents=True, exist_ok=True)

    # Parse and validate
    try:
        data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")

    if not isinstance(data, dict):
        raise ValueError("Invalid YAML: must be a mapping")
    name = data.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        raise ValueError("Invalid layout metadata: name is required")
    if "version" not in data:
        raise ValueError("Invalid layout metadata: version is required")

    # UUID mismatch check
    metadata = data.get("metadata")
    metadata_id = metadata.get("id") if isinstance(metadata, dict) else None
    if metadata_id and is_uuid(metadata_id) and existing_id and is_uuid(existing_id):
        if metadata_id.lower() != existing_id.lower():
            raise ValueError(
                f"UUID mismatch: URL has {existing_id} but metadata.id has {metadata_id}"
            )

    # Resolve final UUID
    if metadata_id and is_uuid(metadata_id):
        uid = metadata_id
    elif existing_id and is_uuid(existing_id):
        uid = existing_id
    else:
        uid = str(uuid_module.uuid4())

    # Legacy migration
    legacy_slug = existing_id if (existing_id and not is_uuid(existing_id)
                                  and _is_safe_legacy_slug(existing_id)) else None
    if legacy_slug:
        return _migrate_legacy(legacy_slug, yaml_content, uid, name)

    folder_name = _folder_name(name, uid)
    folder_path = get_data_dir() / folder_name
    yaml_filename = _yaml_filename(name)

    existing_folder = _find_folder_by_uuid(uid)
    is_new = existing_folder is None

    # Rename folder if layout name changed
    if existing_folder and existing_folder != folder_path:
        try:
            existing_folder.rename(folder_path)
        except FileNotFoundError:
            is_new = True
        else:
            # Remove old yaml file if name changed
            old_yf = _find_yaml_in_folder(folder_path)
            if old_yf and old_yf.name != yaml_filename:
                try:
                    old_yf.unlink()
                except FileNotFoundError:
                    pass

    folder_path.mkdir(parents=True, exist_ok=True)
    (folder_path / yaml_filename).write_text(yaml_content, encoding="utf-8")
    return {"id": uid, "is_new": is_new}


def _migrate_legacy(slug: str, yaml_content: str, uid: str, name: str) -> dict:
    data_dir = get_data_dir()
    folder_path = data_dir / _folder_name(name, uid)
    yaml_filename = _yaml_filename(name)
    old_assets = data_dir / "assets" / slug
    new_assets = folder_path / "assets"

    folder_path.mkdir(parents=True, exist_ok=True)
    (folder_path / yaml_filename).write_text(yaml_content, encoding="utf-8")

    if old_assets.exists():
        shutil.move(str(old_assets), str(new_assets))

    for ext in ('.yaml', '.yml'):
        p = data_dir / f"{slug}{ext}"
        try:
            p.unlink()
        except FileNotFoundError:
            pass

    return {"id": uid, "is_new": False}


def delete_layout(uid: str) -> bool:
    if not is_uuid(uid):
        return False
    folder = _find_folder_by_uuid(uid)
    if not folder:
        return False
    shutil.rmtree(folder, ignore_errors=False)
    return True


def delete_layout_assets(uid: str) -> None:
    if not is_uuid(uid):
        return
    folder = _find_folder_by_uuid(uid)
    if not folder:
        return
    assets_dir = folder / "assets"
    if assets_dir.exists():
        shutil.rmtree(assets_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Asset storage
# ---------------------------------------------------------------------------

def _asset_dir(layout_id: str, device_slug: str) -> Optional[Path]:
    folder = _find_folder_by_uuid(layout_id)
    if not folder:
        return None
    return folder / "assets" / device_slug


def get_asset(layout_id: str, device_slug: str, face: str) -> Optional[dict]:
    folder = _find_folder_by_uuid(layout_id)
    if not folder:
        return None
    assets = folder / "assets" / device_slug
    for ext, mime in ALLOWED_EXTS.items():
        p = assets / f"{face}.{ext}"
        if p.exists():
            return {"data": p.read_bytes(), "content_type": mime}
    return None


def save_asset(layout_id: str, device_slug: str, face: str,
               data: bytes, content_type: str) -> None:
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(f"Invalid content type: {content_type}")
    if len(data) > MAX_ASSET_SIZE:
        raise ValueError(f"Image too large: {len(data)} bytes")

    folder = _find_folder_by_uuid(layout_id)
    if not folder:
        raise FileNotFoundError(f"Layout not found: {layout_id}")

    ext = CONTENT_TYPE_TO_EXT[content_type]
    device_dir = folder / "assets" / device_slug
    device_dir.mkdir(parents=True, exist_ok=True)
    target = device_dir / f"{face}.{ext}"

    # Atomic write via temp file
    tmp_fd, tmp_path = tempfile.mkstemp(dir=device_dir, suffix=".tmp")
    try:
        os.write(tmp_fd, data)
        os.close(tmp_fd)
        os.replace(tmp_path, target)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    # Remove stale other-extension files
    for old_ext in ALLOWED_EXTS:
        if old_ext != ext:
            old = device_dir / f"{face}.{old_ext}"
            try:
                old.unlink()
            except FileNotFoundError:
                pass


def delete_asset(layout_id: str, device_slug: str, face: str) -> bool:
    folder = _find_folder_by_uuid(layout_id)
    if not folder:
        return False
    deleted = False
    device_dir = folder / "assets" / device_slug
    for ext in ALLOWED_EXTS:
        p = device_dir / f"{face}.{ext}"
        try:
            p.unlink()
            deleted = True
        except FileNotFoundError:
            pass
    return deleted
