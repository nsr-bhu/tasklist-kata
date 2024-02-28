from task_list.console import Console
from task_list.task import Task, TaskCollection
from task_list.command import Command, CommandParser


class TaskList:
    QUIT = "quit"

    def __init__(self, console: Console) -> None:
        self.console = console
        self.task_collection = TaskCollection()
        self.command_parser = CommandParser(self.task_collection, self.console)

    def run(self) -> None:
        while True:
            inputString = self.console.input("> ")
            if inputString == self.QUIT:
                break

            command = self.command_parser.parse(inputString)
            command.execute()
