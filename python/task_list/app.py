from datetime import datetime
from typing import Dict, List

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

    def help(self) -> None:
        self.console.print("Commands:")
        self.console.print("  show")
        self.console.print("  add project <project name>")
        self.console.print("  add task <project name> <task description>")
        self.console.print("  check <task ID>")
        self.console.print("  uncheck <task ID>")
        self.console.print()

    def error(self, command: str) -> None:
        self.console.print(f"I don't know what the command {command} is.")
        self.console.print()
