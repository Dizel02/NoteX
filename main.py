import sys
from src.database import engine, Base, SessionLocal
from src.manager import NoteManager

def main():
    # Автоматическое создание таблиц в MySQL при запуске
    Base.metadata.create_all(bind=engine)
    
    db_session = SessionLocal()
    manager = NoteManager(db_session)

    print("=" * 60)
    print("СИСТЕМА УПРАВЛЕНИЯ ЗАМЕТКАМИ (БАЗА ДАННЫХ: MYSQL)")
    print("=" * 60)

    while True:
        print("\n[Доступные действия]:")
        print("1. Показать все заметки")
        print("2. Добавить новую заметку")
        print("3. Полнотекстовый поиск")
        print("4. Фильтрация по тегам")
        print("5. Удалить заметку")
        print("0. Выход")

        choice = input("\nВыберите действие (0-5): ").strip()

        if choice == "1":
            notes = manager.get_all_notes()
            if not notes:
                print("База заметок пуста.")
            for note in notes:
                tags_str = ", ".join([f"#{t.name}" for t in note.tags])
                print(f"\nID: {note.id} | {note.title}")
                print(f"Текст: {note.content}")
                print(f"Теги: {tags_str if tags_str else 'нет'}")
                print("-" * 40)

        elif choice == "2":
            title = input("Введите заголовок: ").strip()
            content = input("Введите текст заметки: ").strip()
            tags_raw = input("Введите теги через запятую: ").strip()
            tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
            
            note = manager.add_note(title, content, tags)
            print(f"Заметка создана в MySQL. ID: {note.id}")

        elif choice == "3":
            query = input("Введите поисковый запрос: ").strip()
            results = manager.search_full_text(query)
            print(f"Найдено совпадений: {len(results)}")
            for note in results:
                print(f" -> [ID: {note.id}] {note.title} (Текст: {note.content[:30]}...)")

        elif choice == "4":
            tag_input = input("Введите тег для фильтрации: ").strip()
            results = manager.filter_by_tags([tag_input])
            print(f"Найдено заметок с тегом '{tag_input}': {len(results)}")
            for note in results:
                print(f" -> [ID: {note.id}] {note.title}")

        elif choice == "5":
            try:
                note_id = int(input("Введите ID заметки для удаления: "))
                if manager.delete_note(note_id):
                    print("Заметка удалена из MySQL.")
                else:
                    print("Заметка с таким ID не найдена.")
            except ValueError:
                print("Ошибка: ID должен быть числом.")

        elif choice == "0":
            db_session.close()
            print("Программа завершена.")
            sys.exit(0)
        else:
            print("Некорректный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()



