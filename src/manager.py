from typing import List
from src.models import Note, Tag

class NoteManager:
    def __init__(self):
        self.notes: List[Note] = []
        self._note_id_counter = 1
        self._tag_id_counter = 1

    def add_note(self, title: str, content: str, tag_names: List[str] = None) -> Note:
        """Создание новой заметки с тегами"""
        tags = []
        if tag_names:
            for name in tag_names:
                tags.append(Tag(self._tag_id_counter, name.strip()))
                self._tag_id_counter += 1
                
        new_note = Note(self._note_id_counter, title, content, tags)
        self.notes.append(new_note)
        self._note_id_counter += 1
        return new_note

    def delete_note(self, note_id: int) -> bool:
        """Удаление заметки по её ID"""
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                self.notes.pop(i)
                return True
        return False

    def search_full_text(self, query: str) -> List[Note]:
        """Полнотекстовый поиск (ищет совпадения в заголовке и тексте без учета регистра)"""
        if not query:
            return []
        
        query = query.lower()
        results = []
        for note in self.notes:
            if query in note.title.lower() or query in note.content.lower():
                results.append(note)
        return results

    def filter_by_tags(self, tag_names: List[str]) -> List[Note]:
        """Фильтрация заметок: находит те, у которых есть хотя бы один из указанных тегов"""
        if not tag_names:
            return []
            
        search_tags = {name.lower() for name in tag_names}
        results = []
        for note in self.notes:
            note_tag_names = {tag.name.lower() for tag in note.tags}
            # Если есть пересечение множеств тегов
            if search_tags.intersection(note_tag_names):
                results.append(note)
        return results
