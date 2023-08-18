from textual.app import ComposeResult
from textual.widgets import Static

class SnakeGame(Static):
    def compose() -> ComposeResult:
        yield Label("Hello!")

class SnakeMenu(Static):
    def compose() -> ComposeResult:
        yield SnakeGame()