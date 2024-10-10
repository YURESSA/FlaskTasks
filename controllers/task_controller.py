from models.task import Task
import json


class TaskManager:
    def __init__(self, filename='data/tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        with open(self.filename, mode='r', encoding='utf-8-sig') as file:
            tasks_data = json.load(file)['tasks']
            tasks = [Task(task['id'], task['title'], task['description'], task['status'], task['priority']) for task in
                     tasks_data]
        return tasks

    def save_tasks(self):
        tasks_data = {'tasks': [task.to_dict() for task in self.tasks]}
        with open(self.filename, 'w') as file:
            json.dump(tasks_data, file, indent=4)

    def get_task_by_id(self, task_id):
        return next((task for task in self.tasks if task.task_id == task_id), None)

    def find_task(self, status=None, priority=None):
        tasks = self.tasks
        if status:
            tasks = [task for task in tasks if task.status == status]
        if priority:
            tasks = [task for task in tasks if task.priority == priority]
        return tasks

    def create_task(self, title, description, status, priority):
        new_id = max(task.task_id for task in self.tasks) + 1 if self.tasks else 1
        new_task = Task(new_id, title, description, status, priority)
        self.tasks.append(new_task)
        self.save_tasks()

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]
        self.save_tasks()

    def edit_task(self, task_id, title, description, status, priority):
        task = self.get_task_by_id(task_id)
        if task:
            task.title = title
            task.description = description
            task.status = status
            task.priority = priority
            self.save_tasks()
            return task
        return None