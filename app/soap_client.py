# app/soap_client.py
from __future__ import annotations
import uuid
import time
from typing import Tuple
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
from app.config import settings
from app.logging import get_logger

log = get_logger(__name__)

# simple module-level client cache
_CLIENT: Client | None = None

def _get_client() -> Client:
    global _CLIENT
    if _CLIENT is None:
        sess = Session()
        # attach basic auth to HTTP layer if provided
        if settings.SOAP_USER and settings.SOAP_PASS:
            sess.auth = HTTPBasicAuth(settings.SOAP_USER, settings.SOAP_PASS)
        # optional: tune session/timeouts, pool, etc
        transport = Transport(session=sess, timeout=30)
        log.info("Creating Zeep client for WSDL=%s", settings.SOAP_WSDL_URL)
        _CLIENT = Client(wsdl=str(settings.SOAP_WSDL_URL), transport=transport)
    return _CLIENT

def send_record_to_soap(record, max_retries: int = 3, backoff_seconds: float = 1.0) -> Tuple[bool, str | None, str | None]:
    """
    Send a single Record to SOAP. Returns (success, correlation_id, error_message).
    correlation_id is a UUID created locally for tracing.
    Retries on any exception up to max_retries with exponential backoff.
    """
    client = _get_client()
    corr = str(uuid.uuid4())
    last_err = None

    for attempt in range(1, max_retries + 1):
        try:
            # Adjust operation name / parameter names to match your WSDL.
            # We assume an operation named ProcessTransaction that accepts these args.
            log.info("SOAP send attempt %d for record=%s (corr=%s)", attempt, getattr(record, "record_id", "<no-id>"), corr)
            res = client.service.ProcessTransaction(
                recordId=record.record_id,
                name=record.name,
                amount=float(record.amount),
                currency=record.currency,
                timestamp=record.timestamp,
                correlationId=corr,  # optional, some WSDLs accept correlation id
            )

            # Interpret result: Zeep may return an object or dict; handle both.
            ok = False
            try:
                if hasattr(res, "result"):
                    ok = (getattr(res, "result") == "SUCCESS")
                elif isinstance(res, dict):
                    ok = (res.get("result") == "SUCCESS")
                else:
                    # best-effort: if the response is truthy treat as success
                    ok = bool(res)
            except Exception:
                ok = bool(res)

            if ok:
                log.info("SOAP success for record=%s corr=%s", record.record_id, corr)
                return True, corr, None
            else:
                err_msg = f"Remote returned non-success: {res}"
                log.warning(err_msg)
                last_err = err_msg
                # Do not retry if remote explicitly returned non-success — but we do one attempt by default
                # We'll treat as failure without retrying further.
                return False, corr, err_msg

        except Fault as f:
            # SOAP fault — possibly permanent
            last_err = f"{type(f).__name__}: {str(f)}"
            log.warning("SOAP Fault for record=%s: %s", record.record_id, last_err)
            # don't retry on Fault? we will retry a couple times
        except Exception as exc:
            last_err = f"{type(exc).__name__}: {str(exc)}"
            log.warning("SOAP attempt %d failed for record=%s: %s", attempt, record.record_id, last_err)
        # exponential backoff before next attempt
        if attempt < max_retries:
            sleep = backoff_seconds * (2 ** (attempt - 1))
            log.info("Sleeping %.1fs before retry", sleep)
            time.sleep(sleep)

    # If we get here all retries exhausted
    log.error("SOAP send failed after %d attempts for record=%s: last_error=%s", max_retries, getattr(record, "record_id", "<no-id>"), last_err)
    return False, corr, last_err

