# app/pipeline.py
from __future__ import annotations
import os
import time
import logging
from typing import List

from app.config import settings
from app.db import session_scope, try_advisory_lock, advisory_unlock
from app.models import File, FileStatus, Record, RecordStatus
from app.azure_rest import list_blobs, download_blob
from app.parsing import parse_new_files
from app.soap_client import send_record

log = logging.getLogger(__name__)
LOCK_KEY = 424242  # choose a project-unique integer

def sync_from_azure() -> List[str]:
    downloaded: List[str] = []
    os.makedirs(str(settings.INCOMING_DIR), exist_ok=True)

    with session_scope() as s:
        for item in list_blobs():
            exists = s.query(File.id).filter(
                File.blob_name == item.name,
                File.etag == item.etag,
            ).first()
            if exists:
                log.debug("Skipping seen blob %s (etag=%s)", item.name, item.etag)
                continue

            local_name = os.path.basename(item.name)
            local_path = os.path.join(str(settings.INCOMING_DIR), local_name)
            try:
                etag = download_blob(item.name, local_path)
            except Exception as e:
                log.exception("Failed downloading blob %s: %s", item.name, e)
                continue

            f = File(
                blob_name=item.name,
                etag=etag or item.etag,
                local_path=local_path,
                status=FileStatus.NEW.value,
            )
            s.add(f)
            log.info("Recorded new File for blob=%s etag=%s path=%s", item.name, f.etag, local_path)
            downloaded.append(local_path)
    return downloaded


def process_records_via_soap():
    with session_scope() as s:
        recs = s.query(Record).filter(Record.status == RecordStatus.NEW.value).all()
        log.info("Found %d NEW records to send", len(recs))
        for r in recs:
            try:
                ok, corr_id, err = send_record(r)
            except Exception as e:
                ok = False
                corr_id = None
                err = f"Exception: {e}"
            if ok:
                r.status = RecordStatus.PROCESSED.value
                r.soap_corr_id = corr_id
                r.error_message = None
                log.info("Record id=%s -> PROCESSED corr=%s", r.record_id, corr_id)
            else:
                r.status = RecordStatus.FAILED.value
                r.error_message = err
                log.warning("Record id=%s -> FAILED: %s", r.record_id, err)

        files = s.query(File).all()
        for f in files:
            child_statuses = [rc.status for rc in f.records]
            f.processed_count = sum(1 for st in child_statuses if st == RecordStatus.PROCESSED.value)
            if not child_statuses:
                continue
            if all(st == RecordStatus.PROCESSED.value for st in child_statuses):
                f.status = FileStatus.PROCESSED.value
                log.info("File id=%s marked PROCESSED", f.id)
            elif any(st == RecordStatus.FAILED.value for st in child_statuses) and \
                 not all(st == RecordStatus.PROCESSED.value for st in child_statuses):
                f.status = FileStatus.FAILED.value
                log.info("File id=%s marked FAILED (some records failed)", f.id)
            else:
                f.status = FileStatus.PROCESSING.value
                log.debug("File id=%s remains PROCESSING", f.id)


def pipeline_tick():
    start = time.time()
    with session_scope() as s:
        got = try_advisory_lock(s, LOCK_KEY)
    if not got:
        log.info("Another worker holds the lock; skipping this tick")
        return

    log.info("Acquired lock; running pipeline tick")
    try:
        try:
            new_files = sync_from_azure()
            if new_files:
                log.info("Downloaded %d new files", len(new_files))
            else:
                log.debug("No new files downloaded")
        except Exception:
            log.exception("Error during sync_from_azure")

        try:
            parse_new_files()
        except Exception:
            log.exception("Error during parse_new_files")

        try:
            process_records_via_soap()
        except Exception:
            log.exception("Error during process_records_via_soap")

    finally:
        try:
            with session_scope() as s:
                advisory_unlock(s, LOCK_KEY)
            log.info("Released advisory lock")
        except Exception:
            log.exception("Failed to release advisory lock")

    log.info("Pipeline tick finished (elapsed %.2fs)", time.time() - start)
