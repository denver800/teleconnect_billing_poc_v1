# app/parsing.py
from __future__ import annotations
import os
import traceback
from decimal import Decimal
from google.protobuf.message import DecodeError
from app.config import settings
from app.db import session_scope
from app.models import File, FileStatus, Record, RecordStatus
from app.logging import get_logger

log = get_logger("parsing")

# Try to be permissive with protobuf field names (some protos use camelCase)
def _get_field(obj, *names, default=None):
    for n in names:
        if hasattr(obj, n):
            return getattr(obj, n)
    return default

def parse_new_files():
    """
    Find File rows with status == NEW, parse the associated .pb file into
    Record rows, update file.total_records and mark file.status -> PROCESSING.
    """
    parsed_files = 0
    created_records = 0

    with session_scope() as s:
        files = s.query(File).filter(File.status == FileStatus.NEW.value).all()
        log.info("Found %d files with status NEW", len(files))
        for f in files:
            path = f.local_path
            if not path or not os.path.exists(path):
                log.error("Local path missing for File id=%s path=%s; marking FAILED", f.id, path)
                f.status = FileStatus.FAILED.value
                continue

            try:
                with open(path, "rb") as fh:
                    data = fh.read()
                # Import protobuf message class here to avoid heavy import at module import time
                from app.proto.transactions_pb2 import TransactionBatch
                batch = TransactionBatch()
                batch.ParseFromString(data)
            except DecodeError as e:
                log.error("Failed to parse protobuf for File id=%s path=%s: %s", f.id, path, str(e))
                f.status = FileStatus.FAILED.value
                f.error_message = f"ParseError: {str(e)}" if hasattr(f, "error_message") else None
                continue
            except Exception as e:
                # unexpected IO / import error
                log.error("Unexpected error while parsing File id=%s path=%s: %s", f.id, path, e)
                log.debug("Traceback: %s", traceback.format_exc())
                f.status = FileStatus.FAILED.value
                continue

            # Insert records
            count = 0
            for tx in batch.transactions:
                # tolerant field lookups
                record_id = _get_field(tx, "recordId", "record_id", "id", default=None)
                name = _get_field(tx, "name", default="")
                amount_raw = _get_field(tx, "amount", "amt", default=0)
                currency = _get_field(tx, "currency", default="") or ""
                timestamp = _get_field(tx, "timestamp", "time", default="") or ""

                # convert amount to Decimal (Numeric DB type expects Decimal)
                try:
                    # tx.amount might already be float or Decimal; wrap safely
                    amount = Decimal(str(amount_raw))
                except Exception:
                    amount = Decimal("0.00")

                rec = Record(
                    file_id=f.id,
                    record_id=str(record_id) if record_id is not None else "",
                    name=str(name),
                    amount=amount,
                    currency=str(currency),
                    timestamp=str(timestamp),
                    status=RecordStatus.NEW.value,
                )
                s.add(rec)
                count += 1

            # flush so counts are persisted and to catch DB errors early
            try:
                s.flush()
            except Exception as e:
                log.error("DB error inserting records for File id=%s: %s", f.id, e)
                log.debug("Traceback: %s", traceback.format_exc())
                s.rollback()
                f.status = FileStatus.FAILED.value
                continue

            # update file counters and state
            f.total_records = count
            f.status = FileStatus.PROCESSING.value
            parsed_files += 1
            created_records += count
            log.info("Parsed File id=%s (%s) → %d records; set status=%s", f.id, f.blob_name, count, f.status)

    log.info("Parsing complete: files_parsed=%d records_created=%d", parsed_files, created_records)
    return parsed_files, created_records

