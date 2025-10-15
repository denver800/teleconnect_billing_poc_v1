# app/migrations/env.py
from __future__ import annotations
import os
import sys
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

# ensure project root importable
sys.path.insert(0, os.getcwd())

# import models and settings
from app.models import Base
from app.config import settings

config = context.config

# If alembic.ini doesn't provide url, set it from env/settings
if not config.get_main_option("sqlalchemy.url"):
    db_url = os.getenv("DATABASE_URL") or getattr(settings, "DATABASE_URL", None)
    if db_url:
        config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def _get_engine():
    """Return SQLAlchemy engine using configured DB URL."""
    url = config.get_main_option("sqlalchemy.url") or os.getenv("DATABASE_URL") or getattr(settings, "DATABASE_URL", None)
    if not url:
        raise RuntimeError("No database URL found. Set sqlalchemy.url in alembic.ini or DATABASE_URL in environment/.env")
    return create_engine(url, poolclass=pool.NullPool)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    engine = _get_engine()
    with engine.connect() as connection:
        # IMPORTANT: use connection.begin() - not begin_transaction()
        with connection.begin():
            context.configure(connection=connection, target_metadata=target_metadata)
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

