
from datetime import datetime
from typing import List

from task_list.task import Task, TaskCollection
from task_list.console import Console

class Command:

    def __init__(self, name: str, argumentString: str, task_collection: TaskCollection):
        self.name = name
        self.argumentString = argumentString
        self.task_collection = task_collection

    def get_arguments(self) -> str:
        return self.argumentString
    
    def execute(self) -> None:
        pass

class CommandParser:

    def __init__(self, task_collection, console):
        self.console = console
        self.task_collection = task_collection
 
    def parse(self, command_line: str) -> Command:
        self.command_line = command_line
        parts = self.command_line.split(" ",1)
        self.name = parts[0]

        if (len(parts) == 1):
            self.argumentString = None
        else:
            self.argumentString = parts[1]

        if (self.name == "deadline"):
           return DeadlineCommand(self.name, self.argumentString, self.task_collection)
        elif(self.name == "show"):
           return ShowCommand(self.name, self.argumentString, self.task_collection, self.console)
        elif(self.name == "today"):
           return TodayCommand(self.name, self.argumentString, self.task_collection, self.console)
        elif(self.name == "add"):
           return AddCommand(self.name, self.argumentString, self.task_collection, self.console)
        elif(self.name == "check"):
           return CheckCommand(self.name, self.argumentString, self.task_collection, self.console)
        elif(self.name == "uncheck"):
           return UncheckCommand(self.name, self.argumentString, self.task_collection, self.console)
        elif(self.name == "help"):
           return HelpCommand(self.console)
        else:    
           return ErrorCommand(self.name, self.console)
        
class ErrorCommand(Command):
    def __init__(self, name: str, console: Console):
        self.command = name          
        self.console = console

    def execute(self) -> None:
        self.console.print(f"I don't know what the command {self.command} is.")
        self.console.print()

class HelpCommand(Command):
    def __init__(self, console: Console):
        self.console = console

    def execute(self) -> None:
        self.console.print("Commands:")
        self.console.print("  show")
        self.console.print("  add project <project name>")
        self.console.print("  add task <project name> <task description>")
        self.console.print("  check <task ID>")
        self.console.print("  deadline <TaskID> <YYYY-MM-DD>")
        self.console.print("  today")
        self.console.print("  uncheck <task ID>")
        self.console.print("  uncheck <task ID>")
        self.console.print()    

   
class ShowCommand(Command):

    def __init__(self, name: str, argumentString: str, task_collection:  TaskCollection, console: Console):
        super().__init__(name, argumentString, task_collection)
        self.console = console
    
    def execute(self) -> None:
       for project, tasks in self.task_collection.tasks.items():
            self.console.print(project)
            for task in tasks:
                self.console.print(f"  [{'x' if task.is_done() else ' '}] {task.id}: {task.description}")
            self.console.print()
   
class DeadlineCommand(Command): 

    def __init__(self, name: str, argumentString: str, task_collection: TaskCollection):
        super().__init__(name, argumentString, task_collection)
        self.id = int(argumentString.split(" ")[0])
        deadlineStr = argumentString.split(" ")[1]
        self.deadline = datetime.strptime(deadlineStr, "%Y-%m-%d").date()
    
    def execute(self) -> None:
        task = self.task_collection.get_task(self.id)
        task.set_deadline(self.deadline)

class TodayCommand(Command): 

    def __init__(self, name: str, argumentString: str, task_collection:  TaskCollection, console: Console):
        super().__init__(name, argumentString, task_collection)
        self.console = console
    
    def execute(self) -> None:
        today = datetime.now().date()
        tasks_with_deadline = self.task_collection.get_tasks_with_deadline(today)
        if len(tasks_with_deadline.items()) == 0:
            self.console.print("Nothing to do")
            self.console.print("")
        else:
            self.console.print("todos")
            self.console.print("  [ ] 1: Do the thing.")
            self.console.print("")

class AddCommand(Command):

    def __init__(self, name: str, argumentString: str, task_collection:  TaskCollection, console: Console):
        super().__init__(name, argumentString, task_collection)
        self.console = console
    
    def execute(self) -> None:
        sub_command_rest = self.argumentString.split(" ", 1)
        sub_command = sub_command_rest[0]
        if sub_command == "project":
            self.add_project(sub_command_rest[1])
        elif sub_command == "task":
            project_task = sub_command_rest[1].split(" ", 1)
            self.add_task(project_task[0], project_task[1])

    def add_project(self, name: str) -> None:
        self.task_collection.tasks[name] = []

    def add_task(self, project: str, description: str) -> None:
        project_tasks = self.task_collection.tasks.get(project)
        if project_tasks is None:
            self.console.print(f"Could not find a project with the name {project}.")
            self.console.print()
            return
        project_tasks.append(Task(self.task_collection.next_id(), description, False))

class SetDoneCommand(Command):
    DONE: bool = True

    def __init__(self, name: str, argumentString: str, task_collection:  TaskCollection, console: Console, done: bool):
        super().__init__(name, argumentString, task_collection)
        self.console = console
        self.done = done
        self.id_string = argumentString

    def execute(self) -> None:
        id_ = int(self.id_string)
        task = self.task_collection.get_task(id_)
        if task:
            task.set_done(self.done)
            return
        self.console.print(f"Could not find a task with an ID of {id_}")
        self.console.print()

class CheckCommand(SetDoneCommand):

    def __init__(self, name: str, argumentString: str, task_collection:  TaskCollection, console: Console):
        super().__init__(name, argumentString, task_collection, console, self.DONE)

class UncheckCommand(SetDoneCommand):

    def __init__(self, name: str, argumentString: str, task_collection:  TaskCollection, console: Console):
        super().__init__(name, argumentString, task_collection, console, not self.DONE)

