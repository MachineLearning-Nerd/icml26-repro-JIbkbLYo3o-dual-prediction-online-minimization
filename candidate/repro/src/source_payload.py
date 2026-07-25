"""Load the pinned arXiv source from its native or text-only release form."""
from __future__ import annotations

import base64
import io
import tarfile
from pathlib import Path


SOURCE_NAME = "arxiv-2606.05380.tar"


def source_bytes(root: Path) -> bytes:
    native = root / "source" / SOURCE_NAME
    if native.exists():
        return native.read_bytes()
    encoded = root / "source" / f"{SOURCE_NAME}.b64"
    payload = "".join(encoded.read_text(encoding="ascii").split())
    return base64.b64decode(payload, validate=True)


def open_source(root: Path) -> tarfile.TarFile:
    return tarfile.open(fileobj=io.BytesIO(source_bytes(root)), mode="r:*")
