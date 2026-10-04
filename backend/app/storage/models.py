from datetime import datetime

from sqlalchemy import DateTime,ForeignKey,Integer,String,Text,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column

from app.storage.database import Base


class Document(Base):
    __tablename__="documents"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)

    doc_id:Mapped[str]=mapped_column(
        String(32),
        unique=True,
        index=True
    )

    filename:Mapped[str]=mapped_column(String(255))

    file_type:Mapped[str]=mapped_column(String(20))

    content_hash:Mapped[str]=mapped_column(
        String(64),
        unique=True,
        index=True
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Page(Base):
    __tablename__="pages"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)

    document_id:Mapped[int]=mapped_column(
        ForeignKey("documents.id"),
        index=True
    )

    page_number:Mapped[int]=mapped_column(Integer)

    text:Mapped[str]=mapped_column(Text)

    needs_ocr:Mapped[int]=mapped_column(
        Integer,
        default=0
    )

    __table_args__=(
        UniqueConstraint(
            "document_id",
            "page_number",
            name="uq_document_page"
        ),
    )


class Chunk(Base):
    __tablename__="chunks"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)

    document_id:Mapped[int]=mapped_column(
        ForeignKey("documents.id"),
        index=True
    )

    page_id:Mapped[int]=mapped_column(
        ForeignKey("pages.id"),
        index=True
    )

    chunk_index:Mapped[int]=mapped_column(Integer)

    section:Mapped[str|None]=mapped_column(
        String(255),
        nullable=True
    )

    text:Mapped[str]=mapped_column(Text)

    __table_args__=(
        UniqueConstraint(
            "document_id",
            "chunk_index",
            name="uq_document_chunk"
        ),
    )