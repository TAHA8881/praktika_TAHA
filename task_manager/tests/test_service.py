import pytest
from model import Task
from service import TaskService

class FakeRepository:
    """Имитационный репозиторий для тестов."""
    def __init__(self):
        self.tasks = []
        self.counter = 1

    def add(self, task):
        task.id = self.counter
        self.counter += 1
        self.tasks.append(task)
        return task

    def get_all(self):
        return self.tasks

    def update_status(self, task_id, new_status):
        for task in self.tasks:
            if task.id == task_id:
                task.status = new_status
                return

def test_add_task_success():
    repo = FakeRepository()
    service = TaskService(repo)

    task = service.add_task("Проверить тесты")
    assert task.id == 1
    assert task.title == "Проверить тесты"
    assert task.status == "Новая"
    assert len(repo.tasks) == 1

def test_add_task_empty_title_raises_value_error():
    repo = FakeRepository()
    service = TaskService(repo)

    with pytest.raises(ValueError, match="Название задачи не может быть пустым"):
        service.add_task("")
    with pytest.raises(ValueError):
        service.add_task("   ")

def test_mark_as_done_updates_status():
    repo = FakeRepository()
    service = TaskService(repo)
    task = service.add_task("Тест")
    assert task.status == "Новая"

    service.mark_as_done(task.id)
    updated = service.get_all_tasks()[0]
    assert updated.status == "Выполнена"