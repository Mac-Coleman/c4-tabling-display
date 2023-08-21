from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label
from textual.containers import Middle, Center

from logo import C4Logo

class SnakeCell(Widget):
    
    def render(self):
        return "▀▄▀▄\n▀▄▀▄"

class SnakeGame(Static):

    def compose(self) -> ComposeResult:
        for i in range(15 * 15):
            s = SnakeCell()
            if i % 2 == 1:
                s.styles.color = "#333B42"
                s.styles.background = "#212A31"
            yield s
    
    def on_mount(self) -> None:
        self.border_title = "[i]Snake[/i]"

class SnakeMenu(Static):
    def compose(self) -> ComposeResult:
        yield SnakeGame()
        with Middle(classes="FitShort"):
            with Center(classes="FitShort"):
                yield C4Logo()
            with Center(classes="FitShort"):
                yield Label("Ready... ", id="ready", classes="prepare")
                yield Label("Set... ", id="set", classes="prepare")
                yield Label("Go!", id="go", classes="prepare")
    
    def start(self) -> None:
        r = self.query_one("#ready")
        s = self.query_one("#set")
        g = self.query_one("#go")

        r.styles.animate("opacity", value=1.0, duration=0.25)
        s.styles.animate("opacity", value=1.0, duration=0.25, delay=1.5)
        g.styles.animate("opacity", value=1.0, duration=0.25, delay=3)
        
        r.styles.animate("opacity", value=0.0, duration=2, delay=4.5)
        s.styles.animate("opacity", value=0.0, duration=2, delay=4.5)
        g.styles.animate("opacity", value=0.0, duration=2, delay=4.5)