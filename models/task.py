class Task:
    def __init__(self, task_id, title, description, status, priority):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority

    def to_dict(self):
        return {
            'id': self.task_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority
        }
