from __future__ import annotations

import os
import re
import shutil
from src.utils.paths import get_project_root, get_assets_dir

PROJECT_ROOT = get_project_root()
MENU_IMAGE_DIR = os.path.join(get_assets_dir(), "menu")


def _slug(texto: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", str(texto).lower()).strip("_")
    return value or "plato"


def guardar_imagen_local(nombre: str, source_path: str | None) -> str | None:
    if not source_path:
        return buscar_imagen_local(nombre)
    source = source_path
    if not os.path.isabs(source):
        source = os.path.join(PROJECT_ROOT, source)
    if not os.path.isfile(source):
        return buscar_imagen_local(nombre)
    os.makedirs(MENU_IMAGE_DIR, exist_ok=True)
    extension = os.path.splitext(source)[1].lower() or ".png"
    target = os.path.join(MENU_IMAGE_DIR, f"{_slug(nombre)}{extension}")
    if os.path.abspath(source) != os.path.abspath(target):
        shutil.copy2(source, target)
    return os.path.relpath(target, PROJECT_ROOT).replace(os.sep, "/")


def buscar_imagen_local(nombre: str) -> str | None:
    if not os.path.isdir(MENU_IMAGE_DIR):
        return None
    base = _slug(nombre)
    for extension in (".png", ".jpg", ".jpeg", ".webp"):
        path = os.path.join(MENU_IMAGE_DIR, f"{base}{extension}")
        if os.path.isfile(path):
            return path
    return None
