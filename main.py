from src.manager import NoteManager

def main():
    manager = NoteManager()
    
    # Сразу добавим несколько тестовых заметок для демонстрации поиска
    manager.add_note(
        title="План на учебную практику", 
        content="Изучить Git, развернуть структуру проекта на Python и реализовать поиск по тегам.", 
        tag_names=["учеба", "практика"]
    )
    manager.add_note(
        title="Список покупок", 
        content="Купить кофе, блокнот для записей алгоритмов и фрукты.", 
        tag_names=["покупки", "личные"]
    )
    manager.add_note(
        title="Разработка на Python", 
        content="Полнотекстовый поиск работает через проверку вхождения подстроки в нижнем регистре.", 
        tag_names=["учеба", "code"]
    )

    print("=== Модуль заметок успешно запущен ===")
    print(f"Загружено заметок по умолчанию: {len(manager.notes)}")
    
    while True:
        print("\nДоступные команды:")
        print("1. Показать все заметки")
        print("2. Полнотекстовый поиск")
        print("3. Фильтрация по тегам")
        print("4. Выход")
        
        choice = input("Выберите действие (1-4): ").strip()
        
        if choice == "1":
            print("\n--- Список всех заметок ---")
            for note in manager.notes:
                tags_str = ", ".join([t.name for t in note.tags])
                print(f"[{note.id}] {note.title} | Теги: {tags_str}")
                print(f"Текст: {note.content}\n")
                
        elif choice == "2":
            query = input("\nВведите поисковый запрос (слово или фразу): ").strip()
            found = manager.search_full_text(query)
            print(f"\n--- Результаты поиска по запросу '{query}' (Найдено: {len(found)}) ---")
            for note in found:
                print(f"[{note.id}] {note.title}\nТекст: {note.content}\n")
                
        elif choice == "3":
            tag_input = input("\nВведите тег для фильтрации: ").strip()
            found = manager.filter_by_tags([tag_input])
            print(f"\n--- Заметки с тегом '{tag_input}' (Найдено: {len(found)}) ---")
            for note in found:
                print(f"[{note.id}] {note.title}")
                
        elif choice == "4":
            print("\nРабота завершена. До встречи!")
            break
        else:
            print("Неверный ввод, попробуйте еще раз.")

if __name__ == "__main__":
    main()
