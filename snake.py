from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label
from textual.containers import Middle, Center

from logo import C4Logo

class SnakeCell(Widget):
    
    def render(self):
        return "HI"

class SnakeGame(Static):

    def compose(self) -> ComposeResult:
        for i in range(15 * 15):
            yield SnakeCell()
    
    def on_mount(self) -> None:
        self.border_title = "[i]Snake[/i]"

class SnakeMenu(Static):
    def compose(self) -> ComposeResult:
        yield SnakeGame()
        with Middle(classes="FitShort"):
            with Center():
                yield C4Logo()
            with Center():
                yield Label("Ready...")
                yield Label("Set...")
                yield Label("Go!")