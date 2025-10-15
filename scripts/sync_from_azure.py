# scripts/sync_from_azure.py
"""
List blobs in Azure container, download unseen blobs to INCOMING_DIR,
and insert a File row for each downloaded blob (idempotent on blob_name+etag).
Run: python -m scripts.sync_from_azure
"""
import os
import sys
import pathlib
import traceback
from urllib.parse import unquote
from app.azure_rest import list_blobs, download_blob
from app.config import settings
from app.db import session_scope
from app.models import File, FileStatus
from sqlalchemy.exc import IntegrityError
from app.logging import get_logger

log = get_logger("sync_from_azure")

def local_path_for_blob(blob_name: str) -> str:
    # Save by basename to INCOMING_DIR to avoid nesting; keep original name in DB
    base = os.path.basename(blob_name)
    # ensure safe filesystem name (unquote in case blob names are URL-encoded)
    base = unquote(base)
    dest = os.path.join(settings.INCOMING_DIR, base)
    # create directory if missing
    pathlib.Path(os.path.dirname(dest)).mkdir(parents=True, exist_ok=True)
    return dest

def sync_once():
    """
    Lists blobs, downloads unseen, inserts File rows.
    """
    seen = 0
    downloaded = 0
    with session_scope() as s:
        for item in list_blobs():
            seen += 1
            # quick existence check
            exists = s.query(File.id).filter(
                File.blob_name == item.name,
                File.etag == item.etag,
            ).first()
            if exists:
                log.info("Skipping already-seen blob %s (etag=%s)", item.name, item.etag)
                continue

            # download to local path
            try:
                dest = local_path_for_blob(item.name)
                log.info("Downloading %s -> %s", item.name, dest)
                etag = download_blob(item.name, dest) or item.etag
            except Exception as e:
                log.info("Failed to download %s: %s", item.name, e)
                log.debug("Download traceback: %s", traceback.format_exc())
                # do not create a DB row for failed downloads
                continue

            # attempt to insert File row
            try:
                f = File(
                    blob_name=item.name,
                    etag=etag,
                    local_path=dest,
                    status=FileStatus.NEW.value,
                )
                s.add(f)
                # commit happens at session_scope exit; flush now to detect integrity errors immediately
                s.flush()
                downloaded += 1
                log.info("Recorded File row for %s (etag=%s) id=%s", item.name, etag, f.id)
            except IntegrityError:
                # race: another process inserted the same blob_name+etag between our check & insert
                s.rollback()
                log.info("File row already inserted by another process for %s (etag=%s)", item.name, etag)
            except Exception as e:
                s.rollback()
                log.error("Failed to insert File row for %s: %s", item.name, e)
                log.debug("Insert traceback: %s", traceback.format_exc())

    log.info("Sync complete: listed %d blobs, downloaded %d new files", seen, downloaded)

if __name__ == "__main__":
    # ensure INCOMING_DIR exists
    os.makedirs(settings.INCOMING_DIR, exist_ok=True)
    log.info("Starting sync_from_azure; INCOMING_DIR=%s", settings.INCOMING_DIR)
    try:
        sync_once()
    except Exception:
        log.error("Unhandled error running sync", exc_info=True)
        sys.exit(2)

