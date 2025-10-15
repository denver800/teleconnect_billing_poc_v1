# app/models.py
from datetime import datetime, timezone
from enum import StrEnum
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, Numeric, Text, Index, UniqueConstraint, TIMESTAMP, func

Base = declarative_base()

class FileStatus(StrEnum):
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

class RecordStatus(StrEnum):
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

class File(Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    blob_name: Mapped[str] = mapped_column(String(512), index=True, nullable=False)
    etag: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    local_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    status: Mapped[str] = mapped_column(String(12), default=FileStatus.NEW.value, nullable=False)
    total_records: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    processed_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    records: Mapped[list["Record"]] = relationship(back_populates="file", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("blob_name", "etag", name="uq_blob_etag"),
    )

class Record(Base):
    __tablename__ = "records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id", ondelete="CASCADE"), index=True)
    record_id: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    amount: Mapped[Numeric] = mapped_column(Numeric(18, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False)
    timestamp: Mapped[str] = mapped_column(String(64), nullable=False)
    soap_corr_id: Mapped[str | None] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(12), default=RecordStatus.NEW.value, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    file: Mapped[File] = relationship(back_populates="records")

Index("ix_records_file_status", Record.file_id, Record.status)

