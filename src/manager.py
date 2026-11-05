from sqlalchemy.orm import Session
from sqlalchemy import text
from src.models import Note, Tag, NoteVersion

class NoteManager:
    def __init__(self, db: Session):
        self.db = db

    def get_all_notes(self):
        return self.db.query(Note).all()

    def add_note(self, title: str, content: str, tag_names: list):
        tags_list = []
        for name in tag_names:
            tag = self.db.query(Tag).filter(Tag.name == name).first()
            if not tag:
                tag = Tag(name=name)
                self.db.add(tag)
                self.db.commit()
                self.db.refresh(tag)
            tags_list.append(tag)

        note = Note(title=title, content=content, tags=tags_list)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)

        version = NoteVersion(
            note_id=note.id,
            version_number=1,
            title_snapshot=title,
            content_snapshot=content
        )
        self.db.add(version)
        self.db.commit()

        return note

    def search_full_text(self, query: str):
        if not query:
            return []
        sql = text("SELECT id FROM notes WHERE MATCH(title, content) AGAINST(:q IN NATURAL LANGUAGE MODE)")
        result_ids = [row[0] for row in self.db.execute(sql, {"q": query}).fetchall()]
        return self.db.query(Note).filter(Note.id.in_(result_ids)).all() if result_ids else []

    def filter_by_tags(self, tag_names: list):
        if not tag_names:
            return []
        return self.db.query(Note).join(Note.tags).filter(Tag.name.in_(tag_names)).all()

    def delete_note(self, note_id: int):
        note = self.db.query(Note).filter(Note.id == note_id).first()
        if note:
            self.db.delete(note)
            self.db.commit()
            return True
        return False
