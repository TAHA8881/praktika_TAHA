import psycopg2
from model import Task
from repository import TaskRepository
from service import TaskService
from gui import TaskApp

def main():
    # Параметры подключения (можно задать через переменные окружения)
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="task_manager",
        user="postgres",
        password="postgres"
    )
    repo = TaskRepository(conn)
    service = TaskService(repo)
    app = TaskApp(service)
    app.run()
    conn.close()

if __name__ == "__main__":
    main()