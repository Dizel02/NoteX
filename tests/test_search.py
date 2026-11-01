import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.manager import NoteManager
from src.manager import NoteManager

class TestNoteSearch(unittest.TestCase):
    def setUp(self):
        """Этот метод запускается перед каждым тестом и готовит базу заметок"""
        self.manager = NoteManager()
        self.manager.add_note("Купить кофе", "Нужно купить зерновой кофе и молоко.", ["покупки"])
        self.manager.add_note("Учеба Python", "Полнотекстовый поиск работает отлично.", ["учеба", "code"])

    def test_full_text_search_success(self):
        """Тест: поиск должен находить заметку по тексту внутри неё"""
        results = self.manager.search_full_text("зерновой")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Купить кофе")

    def test_full_text_search_case_insensitive(self):
        """Тест: поиск не должен зависеть от регистра (большие/маленькие буквы)"""
        results = self.manager.search_full_text("PYTHON")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Учеба Python")

    def test_filter_by_tags(self):
        """Тест: фильтрация заметок по тегам"""
        results = self.manager.filter_by_tags(["учеба"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Учеба Python")

if __name__ == "__main__":
    unittest.main()

