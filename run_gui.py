import tkinter as tk
from tkinter import ttk, messagebox
from src.database import engine, Base, SessionLocal, db_type
from src import NoteManager
from src.models import Note, Tag


class NoteXApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteX — Менеджер заметок с тегами и поиском")
        self.root.geometry("920x640")
        self.root.minsize(900, 620)
        self.root.resizable(True, True)
        self.root.configure(bg="#F0F2F5")

        Base.metadata.create_all(bind=engine)
        self.db_session = SessionLocal()
        self.manager = NoteManager(self.db_session)

        self.configure_styles()
        self.setup_ui()
        self.load_notes()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        bg_main = "#F0F2F5"
        bg_card = "#FFFFFF"
        primary = "#F59E0B"
        primary_hover = "#D97706"
        danger = "#DC2626"
        danger_hover = "#B91C1C"
        text_dark = "#1E293B"

        style.configure("Main.TFrame", background=bg_main)
        style.configure("Card.TFrame", background=bg_card, relief="flat")
        style.configure("Card.TLabelframe", background=bg_card, foreground=text_dark, font=("Segoe UI", 10, "bold"))
        style.configure("Card.TLabelframe.Label", background=bg_card, foreground="#B45309", font=("Segoe UI", 10, "bold"))

        style.configure("TLabel", background=bg_card, foreground=text_dark, font=("Segoe UI", 9))
        style.configure("Top.TLabel", background=bg_main, foreground=text_dark, font=("Segoe UI", 9, "bold"))
        style.configure("TEntry", fieldbackground="#F8FAFC", foreground=text_dark, padding=5, font=("Segoe UI", 9))

        style.configure("Primary.TButton", background=primary, foreground="#1E293B", font=("Segoe UI", 9, "bold"), padding=(12, 6), borderwidth=0)
        style.map("Primary.TButton", background=[("active", primary_hover)])

        style.configure("Secondary.TButton", background="#E2E8F0", foreground=text_dark, font=("Segoe UI", 9), padding=(10, 6), borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#CBD5E1")])

        style.configure("Danger.TButton", background=danger, foreground="white", font=("Segoe UI", 9, "bold"), padding=(12, 6), borderwidth=0)
        style.map("Danger.TButton", background=[("active", danger_hover)])

        style.configure("Treeview", background=bg_card, foreground=text_dark, rowheight=28, fieldbackground=bg_card, font=("Segoe UI", 9), borderwidth=0)
        style.configure("Treeview.Heading", background="#E2E8F0", foreground=text_dark, font=("Segoe UI", 9, "bold"), padding=6, borderwidth=0)
        style.map("Treeview", background=[("selected", "#FEF3C7")], foreground=[("selected", "#92400E")])

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#1E293B", height=52)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text="NoteX", bg="#1E293B", fg="#FBBF24", font=("Segoe UI", 15, "bold")).pack(side=tk.LEFT, padx=(20, 6))
        tk.Label(header, text="|  Умный менеджер заметок с тегами и полнотекстовым поиском", bg="#1E293B", fg="#CBD5E1", font=("Segoe UI", 10)).pack(side=tk.LEFT)

        status_frame = tk.Frame(self.root, bg="#E2E8F0", height=28)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)

        db_color = "#15803D" if "MYSQL" in db_type.upper() else "#B45309"
        tk.Label(status_frame, text="●", bg="#E2E8F0", fg=db_color, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(15, 4))
        tk.Label(
            status_frame,
            text=f"Активная СУБД: {db_type}   |   Автоверсионирование: Включено (v1)",
            bg="#E2E8F0", fg="#334155", font=("Segoe UI", 8, "bold")
        ).pack(side=tk.LEFT)

        top_frame = ttk.Frame(self.root, style="Main.TFrame", padding=(20, 12, 20, 6))
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text="Поиск по тексту:", style="Top.TLabel").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(top_frame, width=22)
        self.search_entry.pack(side=tk.LEFT, padx=(6, 6))
        ttk.Button(top_frame, text="Найти", style="Primary.TButton", command=self.search_notes).pack(side=tk.LEFT, padx=(0, 16))

        ttk.Label(top_frame, text="Фильтр по тегу:", style="Top.TLabel").pack(side=tk.LEFT)
        self.tag_entry = ttk.Entry(top_frame, width=18)
        self.tag_entry.pack(side=tk.LEFT, padx=(6, 6))
        ttk.Button(top_frame, text="Фильтр", style="Secondary.TButton", command=self.filter_by_tag).pack(side=tk.LEFT)

        ttk.Button(top_frame, text="Показать все", style="Secondary.TButton", command=self.load_notes).pack(side=tk.RIGHT)

        main_frame = ttk.Frame(self.root, style="Main.TFrame", padding=(20, 8, 20, 12))
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.LabelFrame(main_frame, text="  Реестр заметок  ", style="Card.TLabelframe", padding=12)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))

        btn_frame = ttk.Frame(left_frame, style="Card.TFrame")
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        ttk.Button(btn_frame, text="Удалить выбранную (Cascade)", style="Danger.TButton", command=self.delete_note).pack(side=tk.LEFT)

        columns = ("id", "title", "tags")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=9)
        self.tree.heading("id", text="ID", anchor=tk.CENTER)
        self.tree.heading("title", text="Заголовок заметки", anchor=tk.W)
        self.tree.heading("tags", text="Привязанные теги", anchor=tk.W)
        self.tree.column("id", width=55, anchor=tk.CENTER, stretch=False)
        self.tree.column("title", width=260, anchor=tk.W)
        self.tree.column("tags", width=180, anchor=tk.W)

        self.tree.tag_configure("oddrow", background="#F8FAFC")
        self.tree.tag_configure("evenrow", background="#FFFFFF")

        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_note)

        right_frame = ttk.LabelFrame(main_frame, text="  Карточка заметки  ", style="Card.TLabelframe", padding=12)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        action_frame = ttk.Frame(right_frame, style="Card.TFrame")
        action_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        ttk.Button(action_frame, text="Сохранить заметку", style="Primary.TButton", command=self.add_note).pack(side=tk.LEFT)
        ttk.Button(action_frame, text="Очистить", style="Secondary.TButton", command=self.clear_fields).pack(side=tk.RIGHT)

        ttk.Label(right_frame, text="Заголовок:").pack(anchor=tk.W)
        self.title_input = ttk.Entry(right_frame, width=38)
        self.title_input.pack(fill=tk.X, pady=(3, 8))

        ttk.Label(right_frame, text="Теги (через запятую):").pack(anchor=tk.W)
        self.tags_input = ttk.Entry(right_frame, width=38)
        self.tags_input.pack(fill=tk.X, pady=(3, 8))

        ttk.Label(right_frame, text="Содержимое заметки:").pack(anchor=tk.W)
        self.content_input = tk.Text(
            right_frame, width=38, height=8, font=("Segoe UI", 9),
            bg="#F8FAFC", fg="#1E293B", relief="solid", borderwidth=1, padx=6, pady=6
        )
        self.content_input.pack(fill=tk.BOTH, expand=True, pady=(3, 0))
    def load_notes(self, notes=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if notes is None:
            notes = self.manager.get_all_notes()
        for idx, n in enumerate(notes):
            tags_str = ", ".join([f"#{t.name}" for t in n.tags])
            row_tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=(n.id, n.title, tags_str), tags=(row_tag,))

    def add_note(self):
        title = self.title_input.get().strip()
        content = self.content_input.get("1.0", tk.END).strip()
        tags = [t.strip() for t in self.tags_input.get().split(",") if t.strip()]

        if not title or not content:
            messagebox.showwarning("Внимание", "Заполните заголовок и текст заметки!")
            return

        self.manager.add_note(title, content, tags)
        messagebox.showinfo("Успех", "Заметка сохранена! Создана начальная версия (v1).")
        self.clear_fields()
        self.load_notes()

    def search_notes(self):
        kw = self.search_entry.get().strip()
        if not kw:
            self.load_notes()
            return
        results = self.db_session.query(Note).filter(
            (Note.title.ilike(f"%{kw}%")) | (Note.content.ilike(f"%{kw}%"))
        ).all()
        self.load_notes(results)

    def filter_by_tag(self):
        tag_name = self.tag_entry.get().strip().lstrip("#")
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
        note_id, _, _ = self.tree.item(selected)["values"]
        if self.manager.delete_note(int(note_id)):
            messagebox.showinfo("Удалено", f"Заметка ID {note_id} и её история версий удалены.")
            self.clear_fields()
            self.load_notes()

    def on_select_note(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        note_id, _, _ = self.tree.item(selected)["values"]
        note = self.db_session.query(Note).filter_by(id=int(note_id)).first()
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
