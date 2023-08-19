from textual.app import ComposeResult
from textual.widgets import Static, Label

class SnakeGame(Static):
    def compose(self) -> ComposeResult:
        yield Label("Hello!")

class SnakeMenu(Static):
    def compose(self) -> ComposeResult:
        yield SnakeGame()