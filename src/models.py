from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

# Связующая таблица для связи Многие-со-Многими
note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)

    def __repr__(self):
        return f"Tag(id={self.id}, name='{self.name}')"

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)

    # Связь с тегами через связующую таблицу
    tags = relationship("Tag", secondary=note_tags, backref="notes")

    def __repr__(self):
        return f"Note(id={self.id}, title='{self.title}', tags={[t.name for t in self.tags]})"

