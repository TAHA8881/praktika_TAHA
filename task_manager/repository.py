import psycopg2

class TaskRepository:
    def __init__(self, connection):
        self.connection = connection

    def add(self, task):
        """Добавляет задачу и возвращает её с присвоенным id."""
        with self.connection.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title, status) VALUES (%s, %s) RETURNING id",
                (task.title, task.status)
            )
            task_id = cur.fetchone()[0]
            self.connection.commit()
            task.id = task_id
            return task

    def get_all(self):
        """Возвращает список всех задач (сортировка по id)."""
        with self.connection.cursor() as cur:
            cur.execute("SELECT id, title, status FROM tasks ORDER BY id")
            rows = cur.fetchall()
            return [Task(id=row[0], title=row[1], status=row[2]) for row in rows]

    def update_status(self, task_id, new_status):
        """Обновляет статус задачи."""
        with self.connection.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET status = %s WHERE id = %s",
                (new_status, task_id)
            )
            self.connection.commit()