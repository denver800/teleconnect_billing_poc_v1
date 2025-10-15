# app/db.py
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings

# create engine lazily using the DATABASE_URL from settings
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.
    Usage:
        with session_scope() as s:
            s.add(obj)
    """
    s = SessionLocal()
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()

def try_advisory_lock(s, key: int) -> bool:
    """
    Try to acquire a Postgres advisory lock. Returns True if acquired.
    NOTE: requires a live DB connection and Postgres support.
    """
    # pg_try_advisory_lock returns boolean; use text() to avoid SQLAlchemy text compilation issues
    return bool(s.execute(text("SELECT pg_try_advisory_lock(:k)"), {"k": key}).scalar())

def advisory_unlock(s, key: int) -> None:
    """Release a Postgres advisory lock."""
    s.execute(text("SELECT pg_advisory_unlock(:k)"), {"k": key})

