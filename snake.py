from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label

class SnakeCell(Widget):
    
    def render(self):
        return "HI"

class SnakeGame(Static):
    def compose(self) -> ComposeResult:
        for i in range(15 * 15):
            yield SnakeCell()

class SnakeMenu(Static):
    def compose(self) -> ComposeResult:
        yield SnakeGame()