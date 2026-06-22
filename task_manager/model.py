class Task:
    """Модель задачи."""
    def __init__(self, title, status="Новая", id=None):
        self.id = id
        self.title = title
        self.status = status

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"