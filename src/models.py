from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

class NoteTag(Base):
    __tablename__ = "note_tags"
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    tags = relationship("Tag", secondary="note_tags", back_populates="notes")
    versions = relationship("NoteVersion", back_populates="note", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ft_notes_search', 'title', 'content', mysql_prefix='FULLTEXT'),
    )

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    notes = relationship("Note", secondary="note_tags", back_populates="tags")

class NoteVersion(Base):
    __tablename__ = "note_versions"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    title_snapshot = Column(String(255), nullable=False)
    content_snapshot = Column(Text, nullable=False)
    updated_at = Column(DateTime, server_default=func.now())

    note = relationship("Note", back_populates="versions")
