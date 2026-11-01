from datetime import datetime
from typing import List

class Tag:
    def __init__(self, tag_id: int, name: str):
        self.id = tag_id
        self.name = name

class Note:
    def __init__(self, note_id: int, title: str, content: str, tags: List[Tag] = None):
        self.id = note_id
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.tags = tags if tags is not None else []

    def add_tag(self, tag: Tag) -> None:
        """Заглушка: добавление тега к заметке"""
        pass

    def remove_tag(self, tag_id: int) -> None:
        """Заглушка: удаление тега по id"""
        pass
