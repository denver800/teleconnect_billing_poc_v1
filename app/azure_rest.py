# app/azure_rest.py
import base64
import os
import xml.etree.ElementTree as ET
from typing import Iterator, NamedTuple
import requests
from app.config import settings
from app.logging import get_logger

log = get_logger(__name__)

class BlobItem(NamedTuple):
    name: str
    etag: str

def _base_url() -> str:
    if settings.AZURE_BASE_URL:
        return str(settings.AZURE_BASE_URL).rstrip("/")
    return f"https://{settings.AZURE_ACCOUNT}.blob.core.windows.net"

def _container_url() -> str:
    url = f"{_base_url()}/{settings.AZURE_CONTAINER}"
    if settings.AZURE_SAS_TOKEN:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}{settings.AZURE_SAS_TOKEN}"
    return url

def _auth_headers() -> dict:
    # SAS token is on URL; Basic header only used if you have a proxy that expects it
    if settings.AZURE_BASIC_USER and settings.AZURE_BASIC_PASS:
        token = base64.b64encode(f"{settings.AZURE_BASIC_USER}:{settings.AZURE_BASIC_PASS}".encode()).decode()
        return {"Authorization": f"Basic {token}"}
    return {}

def list_blobs(prefix: str | None = None) -> Iterator[BlobItem]:
    """
    List blobs in the container via the Azure REST 'List Blobs' XML API.
    Yields BlobItem(name, etag).
    """
    marker = None
    while True:
        params = {"restype": "container", "comp": "list"}
        if prefix:
            params["prefix"] = prefix
        if marker:
            params["marker"] = marker

        resp = requests.get(_container_url(), headers=_auth_headers(), params=params, timeout=30)
        resp.raise_for_status()

        root = ET.fromstring(resp.content)
        for blob in root.findall(".//Blobs/Blob"):
            name = blob.findtext("Name")
            etag = blob.findtext("Properties/Etag") or ""
            yield BlobItem(name=name, etag=etag.strip('"'))

        marker = root.findtext(".//NextMarker")
        if not marker:
            break

def download_blob(blob_name: str, dest_path: str) -> str:
    """
    Download a blob to dest_path. Returns the blob's ETag (without quotes).
    """
    url = f"{_base_url()}/{settings.AZURE_CONTAINER}/{blob_name}"
    if settings.AZURE_SAS_TOKEN:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}{settings.AZURE_SAS_TOKEN}"

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with requests.get(url, headers=_auth_headers(), stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        etag = r.headers.get("ETag", "").strip('"')
    log.info("Downloaded %s → %s (etag=%s)", blob_name, dest_path, etag)
    return etag

