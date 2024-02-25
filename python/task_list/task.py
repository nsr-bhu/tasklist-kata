
from datetime import datetime

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

