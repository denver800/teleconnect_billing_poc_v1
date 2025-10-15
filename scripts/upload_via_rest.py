# scripts/upload_via_rest.py
"""
Upload all files from app/runtime/generated -> Azure Blob (container from settings).
Uses SAS token (if set) or Basic auth (if BASIC user/pass set in .env).
"""

from pathlib import Path
import sys
import os
import base64
import mimetypes
import requests

from app.config import settings

OUT_DIR = Path("app/runtime/generated")
if not OUT_DIR.exists():
    print("No generated files dir:", OUT_DIR, file=sys.stderr)
    sys.exit(1)

def _base_url() -> str:
    if settings.AZURE_BASE_URL:
        return str(settings.AZURE_BASE_URL).rstrip("/")
    return f"https://{settings.AZURE_ACCOUNT}.blob.core.windows.net"

def _container_url(blob_name: str) -> str:
    # Return full URL to upload a blob. If SAS present, append it (SAS typically contains leading ? or not)
    base = f"{_base_url()}/{settings.AZURE_CONTAINER}/{blob_name}"
    if settings.AZURE_SAS_TOKEN:
        sep = "" if settings.AZURE_SAS_TOKEN.startswith("?") else "?"
        return f"{base}{sep}{settings.AZURE_SAS_TOKEN}"
    return base

def _auth_headers() -> dict:
    # If Basic credentials present, set Authorization header (base64 user:pass)
    if settings.AZURE_BASIC_USER and settings.AZURE_BASIC_PASS:
        token = base64.b64encode(f"{settings.AZURE_BASIC_USER}:{settings.AZURE_BASIC_PASS}".encode()).decode()
        return {"Authorization": f"Basic {token}"}
    return {}

def upload_file(path: Path) -> tuple[int,str]:
    blob_name = path.name
    url = _container_url(blob_name)
    headers = _auth_headers()
    # required header for Azure Put Blob when uploading raw content
    headers.update({
        "x-ms-blob-type": "BlockBlob",
        "Content-Type": mimetypes.guess_type(str(path))[0] or "application/octet-stream",
    })
    # Use PUT to create/replace the blob
    with open(path, "rb") as fh:
        data = fh.read()
    resp = requests.put(url, headers=headers, data=data, timeout=60)
    return resp.status_code, resp.text[:500]

def main():
    files = sorted(OUT_DIR.glob("*.pb"))
    if not files:
        print("No .pb files found in", OUT_DIR)
        return 0

    print(f"Uploading {len(files)} files to container='{settings.AZURE_CONTAINER}' on account='{settings.AZURE_ACCOUNT}'")
    for p in files:
        print("->", p.name, end=" ... ", flush=True)
        try:
            status, body = upload_file(p)
            if 200 <= status < 300:
                print("OK", status)
            else:
                print("FAIL", status)
                print("   response:", body)
        except Exception as e:
            print("ERROR:", e)
    return 0

if __name__ == "__main__":
    sys.exit(main())

