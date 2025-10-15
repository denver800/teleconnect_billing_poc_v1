# scripts/list_blobs.py
from app.azure_rest import list_blobs
from app.config import settings

if __name__ == "__main__":
    print("Using container URL:", settings.AZURE_BASE_URL or f"https://{settings.AZURE_ACCOUNT}.blob.core.windows.net/{settings.AZURE_CONTAINER}")
    found = False
    for b in list_blobs():
        print(" -", b.name, "etag=", b.etag)
        found = True
    if not found:
        print("No blobs found (container empty or permissions issue).")

