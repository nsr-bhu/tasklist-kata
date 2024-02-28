
from datetime import datetime
from typing import Dict, List

class Task:

    def __init__(self, id_: int, description: str, done: bool) -> None:
        self.id = id_
        self.description = description
        self.done = done
        self.deadline : datetime = None
 
    def set_done(self, done: bool) -> None:
        self.done = done

    def set_deadline(self, deadline: datetime) -> None:
        self.deadline = deadline

    def is_done(self) -> bool:
        return self.done
    
    def has_deadline(self) -> bool:
        return self.deadline != None  

class TaskCollection:

    def __init__(self):
        self.tasks: Dict[str, List[Task]] = dict()
        self.last_id: int = 0

    def get_tasks_with_deadline(self, deadline: datetime):
        tasks_with_deadline: Dict[str, List[Task]] = dict()
        for project, task_list in self.tasks.items():
            task_list_with_deadline = [t for t in task_list if t.has_deadline and t.deadline == deadline]
            if (task_list_with_deadline):
                tasks_with_deadline[project] = task_list_with_deadline
        return tasks_with_deadline

    def get_task(self, id):
        for project, task_list in self.tasks.items():
            for task in task_list:
                if task.id == id:
                    return task
        return None

    def next_id(self) -> int:
        self.last_id += 1
        return self.last_id
