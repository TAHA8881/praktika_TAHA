import tkinter as tk
from tkinter import ttk, messagebox

class TaskApp:
    def __init__(self, service):
        self.service = service
        self.root = tk.Tk()
        self.root.title("Менеджер задач")
        self.root.geometry("500x400")

        # Поле ввода
        self.entry_var = tk.StringVar()
        ttk.Label(self.root, text="Название задачи:").pack(pady=(10, 0))
        self.entry = ttk.Entry(self.root, textvariable=self.entry_var, width=50)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda e: self.add_task())

        # Кнопки
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Добавить", command=self.add_task).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Обновить список", command=self.load_tasks).pack(side="left", padx=5)

        # Таблица задач
        columns = ("id", "title", "status")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Название")
        self.tree.heading("status", text="Статус")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("title", width=250)
        self.tree.column("status", width=100, anchor="center")
        self.tree.pack(pady=10, fill="both", expand=True)

        # Нижняя панель
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(pady=5)
        ttk.Button(bottom_frame, text="Отметить выполненной", command=self.mark_done).pack(side="left", padx=5)

        # Загрузка начальных данных
        self.load_tasks()

    def add_task(self):
        title = self.entry_var.get()
        try:
            self.service.add_task(title)
            self.entry_var.set("")
            self.load_tasks()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def load_tasks(self):
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
        tasks = self.service.get_all_tasks()
        for task in tasks:
            self.tree.insert("", "end", values=(task.id, task.title, task.status))

    def mark_done(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите задачу для отметки")
            return
        # Получаем ID из первой колонки
        item = self.tree.item(selected[0])
        task_id = item["values"][0]
        try:
            self.service.mark_as_done(task_id)
            self.load_tasks()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def run(self):
        self.root.mainloop()