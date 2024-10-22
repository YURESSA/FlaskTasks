import sqlite3
from models.task import Task


class TaskManager:
    def __init__(self, db_name='data/flask-tasks.db3'):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT,
                    priority INTEGER
                )
            ''')
            connection.commit()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_all_tasks_ids(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT id FROM tasks')
            tasks_ids = cursor.fetchall()
            return [int(task_id[0]) for task_id in tasks_ids]

    def get_task_by_id(self, task_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task_data = cursor.fetchone()
            return Task(task_data[0], task_data[1], task_data[2], task_data[3], task_data[4]) if task_data else None

    def find_task(self, status=None, priority=None):
        query = 'SELECT * FROM tasks'
        params = []
        conditions = []

        if status:
            conditions.append('status = ?')
            params.append(status)
        if priority:
            conditions.append('priority = ?')
            params.append(priority)

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            tasks_data = cursor.fetchall()
            return [Task(task[0], task[1], task[2], task[3], task[4]) for task in tasks_data]

    def create_task(self, title, description, status, priority):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO tasks (title, description, status, priority)
                VALUES (?, ?, ?, ?)
            ''', (title, description, status, priority))
            connection.commit()
            new_id = cursor.lastrowid
            return Task(new_id, title, description, status, priority)

    def delete_task(self, task_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            connection.commit()

    def edit_task(self, task_id, title, description, status, priority):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE tasks
                SET title = ?, description = ?, status = ?, priority = ?
                WHERE id = ?
            ''', (title, description, status, priority, task_id))
            connection.commit()
            return self.get_task_by_id(task_id)
