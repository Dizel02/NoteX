import tkinter as tk
from tkinter import ttk, messagebox
from src.database import engine, Base, SessionLocal, db_type
from src import NoteManager
from src.models import Note, Tag

class NoteXApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteX — Менеджер заметок с тегами и поиском")
        self.root.geometry("820x540")
        self.root.resizable(False, False)

        # Инициализация таблиц и сессии точно как в run_cli.py
        Base.metadata.create_all(bind=engine)
        self.db_session = SessionLocal()
        self.manager = NoteManager(self.db_session)

        self.setup_ui()
        self.load_notes()

    def setup_ui(self):
        # Верхняя панель поиска и фильтрации
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text="Поиск по тексту:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(top_frame, width=22)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Найти", command=self.search_notes).pack(side=tk.LEFT, padx=2)

        ttk.Label(top_frame, text="   Фильтр по тегу:").pack(side=tk.LEFT)
        self.tag_entry = ttk.Entry(top_frame, width=18)
        self.tag_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Фильтр", command=self.filter_by_tag).pack(side=tk.LEFT, padx=2)

        ttk.Button(top_frame, text="Показать все", command=self.load_notes).pack(side=tk.RIGHT)

        # Центральная область: слева список заметок, справа форма добавления
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Левая колонка (Таблица заметок)
        left_frame = ttk.LabelFrame(main_frame, text="Реестр заметок", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        columns = ("id", "title", "tags")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=16)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Заголовок")
        self.tree.heading("tags", text="Теги")
        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("title", width=210)
        self.tree.column("tags", width=160)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_note)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(btn_frame, text="Удалить выбранную (Cascade)", command=self.delete_note).pack(side=tk.LEFT)

        # Правая колонка (Создание и просмотр заметки)
        right_frame = ttk.LabelFrame(main_frame, text="Карточка заметки", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        ttk.Label(right_frame, text="Заголовок:").pack(anchor=tk.W)
        self.title_input = ttk.Entry(right_frame, width=38)
        self.title_input.pack(fill=tk.X, pady=(2, 8))

        ttk.Label(right_frame, text="Теги (через запятую):").pack(anchor=tk.W)
        self.tags_input = ttk.Entry(right_frame, width=38)
        self.tags_input.pack(fill=tk.X, pady=(2, 8))

        ttk.Label(right_frame, text="Текст заметки:").pack(anchor=tk.W)
        self.content_input = tk.Text(right_frame, width=38, height=11, font=("Segoe UI", 9))
        self.content_input.pack(fill=tk.BOTH, expand=True, pady=(2, 10))

        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill=tk.X)
        ttk.Button(action_frame, text="Сохранить новую заметку", command=self.add_note).pack(side=tk.LEFT)
        ttk.Button(action_frame, text="Очистить поля", command=self.clear_fields).pack(side=tk.RIGHT)

        # Нижняя строка статуса БД с вашей переменной db_type
        status_bar = ttk.Label(self.root, text=f" АКТИВНАЯ БД: {db_type} | Версионирование: Включено (v1)", relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_notes(self, notes=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if notes is None:
            notes = self.manager.get_all_notes()
        for n in notes:
            tags_str = ", ".join([f"#{t.name}" for t in n.tags])
            self.tree.insert("", tk.END, values=(n.id, n.title, tags_str))

    def add_note(self):
        title = self.title_input.get().strip()
        content = self.content_input.get("1.0", tk.END).strip()
        tags = [t.strip() for t in self.tags_input.get().split(",") if t.strip()]

        if not title or not content:
            messagebox.showwarning("Ошибка", "Заполните заголовок и текст заметки!")
            return

        self.manager.create_note(title, content, tags)
        messagebox.showinfo("Успех", "Заметка сохранена! Создана начальная версия.")
        self.clear_fields()
        self.load_notes()

    def search_notes(self):
        kw = self.search_entry.get().strip()
        if not kw:
            self.load_notes()
            return
        results = self.manager.search_notes(kw)
        self.load_notes(results)

    def filter_by_tag(self):
        tag_name = self.tag_entry.get().strip()
        if not tag_name:
            self.load_notes()
            return
        notes = self.db_session.query(Note).join(Note.tags).filter(Tag.name == tag_name).all()
        self.load_notes(notes)

    def delete_note(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заметку в таблице слева!")
            return
        note_id = self.tree.item(selected[0])["values"][0]
        if self.manager.delete_note(note_id):
            messagebox.showinfo("Удалено", f"Заметка ID {note_id} и её история удалены.")
            self.clear_fields()
            self.load_notes()

    def on_select_note(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        note_id = self.tree.item(selected[0])["values"][0]
        note = self.db_session.query(Note).filter_by(id=note_id).first()
        if note:
            self.clear_fields()
            self.title_input.insert(0, note.title)
            self.tags_input.insert(0, ", ".join([t.name for t in note.tags]))
            self.content_input.insert("1.0", note.content)

    def clear_fields(self):
        self.title_input.delete(0, tk.END)
        self.tags_input.delete(0, tk.END)
        self.content_input.delete("1.0", tk.END)

    def on_closing(self):
        self.db_session.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteXApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
