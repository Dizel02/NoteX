import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.manager import NoteManager
from src.models import NoteVersion

# Тестируем на независимой SQLite в памяти, чтобы не ломать MySQL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_add_note_and_version(db_session):
    manager = NoteManager(db_session)
    note = manager.add_note("Заголовок", "Текст заметки", ["тест", "python"])
    
    assert note.id is not None
    assert note.title == "Заголовок"
    assert len(note.tags) == 2

    # Проверяем, создалась ли автоматически история изменений (Версия 1)
    version = db_session.query(NoteVersion).filter(NoteVersion.note_id == note.id).first()
    assert version is not None
    assert version.version_number == 1
    assert version.title_snapshot == "Заголовок"
