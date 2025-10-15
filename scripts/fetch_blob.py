# scripts/fetch_blob.py
import sys
import os
from app.azure_rest import download_blob
from app.config import settings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.fetch_blob <blob_name>")
        raise SystemExit(1)
    blob = sys.argv[1]
    dest = os.path.join(settings.INCOMING_DIR, os.path.basename(blob))
    etag = download_blob(blob, dest)
    print("Saved to:", dest, "etag:", etag)

