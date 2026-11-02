from typing import List
from sqlalchemy.orm import Session
from src.models import Note, Tag

class NoteManager:
    def __init__(self, db: Session):
        self.db = db

    def add_note(self, title: str, content: str, tag_names: List[str] = None) -> Note:
        """Создание новой заметки с тегами в MySQL"""
        new_note = Note(title=title, content=content)
        
        if tag_names:
            for name in tag_names:
                clean_name = name.strip()
                if not clean_name:
                    continue
                # Проверяем, существует ли уже такой тег
                tag = self.db.query(Tag).filter(Tag.name == clean_name).first()
                if not tag:
                    tag = Tag(name=clean_name)
                    self.db.add(tag)
                new_note.tags.append(tag)

        self.db.add(new_note)
        self.db.commit()
        self.db.refresh(new_note)
        return new_note

    def delete_note(self, note_id: int) -> bool:
        """Удаление заметки по её ID из MySQL"""
        note = self.db.query(Note).filter(Note.id == note_id).first()
        if note:
            self.db.delete(note)
            self.db.commit()
            return True
        return False

    def get_all_notes(self) -> List[Note]:
        """Получение всех заметок из базы данных"""
        return self.db.query(Note).all()

    def search_full_text(self, query: str) -> List[Note]:
        """Полнотекстовый поиск по заголовку и тексту в MySQL (ILIKE-аналог)"""
        if not query:
            return []
        
        search_filter = f"%{query.lower()}%"
        return self.db.query(Note).filter(
            (Note.title.like(search_filter)) | 
            (Note.content.like(search_filter))
        ).all()

    def filter_by_tags(self, tag_names: List[str]) -> List[Note]:
        """Фильтрация заметок по тегам через SQL-запрос"""
        if not tag_names:
            return []

        search_tags = [name.lower().strip() for name in tag_names]
        return self.db.query(Note).join(Note.tags).filter(
            Tag.name.in_(search_tags)
        ).distinct().all()

