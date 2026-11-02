from typing import List

class Tag:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Tag(id={self.id}, name='{self.name}')"

class Note:
    def __init__(self, id: int, title: str, content: str, tags: List[Tag] = None):
        self.id = id
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []

    def __repr__(self):
        return f"Note(id={self.id}, title='{self.title}', tags={[t.name for t in self.tags]})"

