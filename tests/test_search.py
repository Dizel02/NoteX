import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.manager import NoteManager

class TestNoteSearch(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовой базы заметок"""
        self.manager = NoteManager()
        self.manager.add_note("Купить кофе", "Нужно купить зерновой кофе и молоко.", ["покупки"])
        self.manager.add_note("Учёба Python", "Полнотекстовый поиск работает отлично.", ["учёба", "code"])

    def test_full_text_search_success(self):
        """Тест: успешный поиск по ключевому слову"""
        results = self.manager.search_full_text("зерновой")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Купить кофе")

    def test_full_text_search_case_insensitive(self):
        """Тест: поиск без учёта регистра букв"""
        results = self.manager.search_full_text("PYTHON")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Учёба Python")

    def test_full_text_search_no_results(self):
        """Тест: поиск по отсутствующему слову"""
        results = self.manager.search_full_text("джаваскрипт")
        self.assertEqual(len(results), 0)
        self.assertIsInstance(results, list)

    def test_filter_by_tags(self):
        """Тест: фильтрация заметок по тегам"""
        results = self.manager.filter_by_tags(["учёба"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Учёба Python")

if __name__ == "__main__":
    unittest.main()

