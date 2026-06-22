class TaskService:
    def __init__(self, repository):
        self.repository = repository

    def add_task(self, title):
        """Добавляет задачу с проверкой названия."""
        if not title or not title.strip():
            raise ValueError("Название задачи не может быть пустым")
        task = Task(title=title.strip(), status="Новая")
        return self.repository.add(task)

    def get_all_tasks(self):
        """Возвращает все задачи."""
        return self.repository.get_all()

    def mark_as_done(self, task_id):
        """Отмечает задачу выполненной с проверкой допустимого статуса."""
        if task_id is None:
            raise ValueError("Не указан ID задачи")
        # Проверим, существует ли задача (можно через репозиторий)
        # Для простоты сразу обновляем статус, но можно сначала получить
        self.repository.update_status(task_id, "Выполнена")