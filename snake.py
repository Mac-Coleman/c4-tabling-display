from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label
from textual.containers import Middle, Center
from textual.color import Color

import random

from logo import C4Logo

class SnakeCell(Widget):
    def set_background_type(self, light: bool):
        self.background_light = light

        if light:
            self.styles.color = "#333B42"
            self.styles.background = "#212A31"
        else:
            self.styles.color = "#0F1921"
            self.styles.background = "#080d12"
    
    def render(self):
        return "▀▄▀▄\n▀▄▀▄"

class SnakeGame(Static):

    def compose(self) -> ComposeResult:
        for i in range(15 * 15):
            s = SnakeCell()
            if i % 2 == 1:
                s.set_background_type(False)
            else:
                s.set_background_type(True)
            yield s
    
    def start(self):

        self.head = (7, 7)
        self.snake_list = [self.head, (7, 8), (7, 9)]

        self.set_interval(0.1, callback=self.update)
    
    def update(self):
        self.border_title = str(random.randint(0, 10))
    
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

        game = self.query_one(SnakeGame)
        game.start()