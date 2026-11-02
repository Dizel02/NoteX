import sys
from src.manager import NoteManager

def main():
    manager = NoteManager()
    
    # Предзаполнение базы демонстрационными данными
    manager.add_note("План на практику", "Выполнить все задачи по разработке модуля заметок.", ["учеба", "практика"])
    manager.add_note("Купить продукты", "Хлеб, молоко, сыр, зерновой кофе.", ["покупки"])
    manager.add_note("Идеи для проекта", "Добавить полноценный GUI интерфейс на Python с помощью Tkinter.", ["идеи", "code"])

    print("=" * 60)
    print(" СИСТЕМА УПРАВЛЕНИЯ ЗАМЕТКАМИ С ТЕГАМИ И ПОИСКОМ")
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
            if not manager.notes:
                print("База заметок пуста.")
            for note in manager.notes:
                tags_str = ", ".join([f"#{t.name}" for t in note.tags])
                print(f"\nID: {note.id} | {note.title}")
                print(f"Текст: {note.content}")
                print(f"Теги: {tags_str if tags_str else 'нет'}")
                print("-" * 40)
                
        elif choice == "2":
            title = input("Введите заголовок: ").strip()
            content = input("Введите текст заметки: ").strip()
            tags_raw = input("Введите теги через запятую (например: работа, важно): ").strip()
            tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else []
            
            note = manager.add_note(title, content, tags)
            print(f" Заметка успешно создана! Ей присвоен ID: {note.id}")
            
        elif choice == "3":
            query = input("Введите поисковый запрос: ").strip()
            results = manager.search_full_text(query)
            print(f"\nНайдено совпадений: {len(results)}")
            for note in results:
                print(f" -> [ID: {note.id}] {note.title} (Текст: {note.content[:30]}...)")
                
        elif choice == "4":
            tag_input = input("Введите тег для фильтрации: ").strip()
            results = manager.filter_by_tags([tag_input])
            print(f"\nНайдено заметок с тегом '{tag_input}': {len(results)}")
            for note in results:
                print(f" -> [ID: {note.id}] {note.title}")
                
        elif choice == "5":
            try:
                note_id = int(input("Введите ID заметки для удаления: "))
                if manager.delete_note(note_id):
                    print(" Заметка успешно удалена.")
                else:
                    print(" Заметка с таким ID не найдена.")
            except ValueError:
                print(" Ошибка: ID должен быть числом.")
                
        elif choice == "0":
            print("Программа завершена. Удачной сдачи практики!")
            sys.exit(0)
        else:
            print(" Некорректный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()

