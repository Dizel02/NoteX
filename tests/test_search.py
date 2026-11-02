import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.manager import NoteManager

class TestNoteSearch(unittest.TestCase):
    def setUp(self):
        """Создание временной тестовой БД в памяти"""
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(bind=self.engine)
        self.db = SessionLocal()
        
        self.manager = NoteManager(self.db)
        self.manager.add_note("Купить кофе", "Нужно купить зерновой кофе и молоко.", ["покупки"])
        self.manager.add_note("Учёба Python", "Полнотекстовый поиск работает отлично.", ["учёба", "code"])

    def tearDown(self):
        """Закрытие сессии и уничтожение тестовой БД"""
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)

    def test_full_text_search_success(self):
        results = self.manager.search_full_text("зерновой")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Купить кофе")

    def test_full_text_search_case_insensitive(self):
        results = self.manager.search_full_text("PYTHON")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Учёба Python")

    def test_full_text_search_no_results(self):
        results = self.manager.search_full_text("джаваскрипт")
        self.assertEqual(len(results), 0)

    def test_filter_by_tags(self):
        results = self.manager.filter_by_tags(["учёба"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Учёба Python")

if __name__ == "__main__":
    unittest.main()

