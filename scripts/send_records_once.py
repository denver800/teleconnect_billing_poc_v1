# scripts/send_records_once.py
"""
One-shot sender: find Record.status == NEW, send via SOAP, update DB.
Run: python -m scripts.send_records_once
"""
from app.db import session_scope
from app.models import Record, RecordStatus, File, FileStatus
from app.soap_client import send_record_to_soap
from app.logging import get_logger

log = get_logger("send_records_once")

def rollup_file_status(s, file_obj: File):
    """Recompute processed_count and file status based on child records."""
    records = file_obj.records  # relationship
    processed = sum(1 for r in records if r.status in (RecordStatus.PROCESSED.value, RecordStatus.FAILED.value))
    file_obj.processed_count = processed
    # decide final status
    statuses = {r.status for r in records}
    if statuses and all(st == RecordStatus.PROCESSED.value for st in statuses):
        file_obj.status = FileStatus.PROCESSED.value
    elif any(st == RecordStatus.FAILED.value for st in statuses):
        # any failed => mark FAILED
        file_obj.status = FileStatus.FAILED.value
    else:
        file_obj.status = FileStatus.PROCESSING.value

def send_once(limit:int=100):
    with session_scope() as s:
        # pick a batch of NEW records (limit)
        rows = s.query(Record).filter(Record.status == RecordStatus.NEW.value).order_by(Record.id).limit(limit).all()
        log.info("Found %d NEW records to send", len(rows))
        # group by file for rollups later
        touched_files: dict[int, File] = {}
        for r in rows:
            try:
                # mark as PROCESSING so other workers skip it
                r.status = RecordStatus.PROCESSING.value
                s.flush()
                ok, corr, err = send_record_to_soap(r)
                if ok:
                    r.status = RecordStatus.PROCESSED.value
                    r.soap_corr_id = corr
                    r.error_message = None
                    log.info("Record %s -> PROCESSED (corr=%s)", r.id, corr)
                else:
                    r.status = RecordStatus.FAILED.value
                    r.soap_corr_id = corr
                    r.error_message = err
                    log.warning("Record %s -> FAILED err=%s", r.id, err)
                # remember file for rollup
                touched_files.setdefault(r.file_id, None)
            except Exception as exc:
                # unexpected error while processing this record
                r.status = RecordStatus.FAILED.value
                r.error_message = f"Exception: {type(exc).__name__}: {str(exc)}"
                log.exception("Unexpected error processing record id=%s", r.id)
                touched_files.setdefault(r.file_id, None)

        # roll up file statuses
        for fid in list(touched_files.keys()):
            f = s.query(File).filter(File.id == fid).one_or_none()
            if not f:
                continue
            rollup_file_status(s, f)
            log.info("Rolled up File id=%s -> status=%s processed_count=%s total_records=%s", f.id, f.status, f.processed_count, f.total_records)

if __name__ == "__main__":
    send_once()

