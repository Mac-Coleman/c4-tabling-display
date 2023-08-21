from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label
from textual.containers import Middle, Center
from textual.color import Color

import random
import copy
from enum import Enum

from logo import C4Logo

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class SnakeCell(Widget):
    def set_background_type(self, light: bool):
        self.background_light = light
        self.is_snake = False

        if light:
            self.styles.color = "#333B42"
            self.styles.background = "#212A31"
        else:
            self.styles.color = "#0F1921"
            self.styles.background = "#080d12"
    
    def set_snake(self, is_snake: bool):
        self.is_snake = is_snake
    
    def render(self):
        if self.is_snake:
            self.styles.color = "#FFFFFF"
            return "████\n████"
        
        self.set_background_type(self.background_light)
        return "▀▄▀▄\n▀▄▀▄"

class SnakeGame(Static):

    def compose(self) -> ComposeResult:

        row = [None] * 15
        self.grid = [copy.deepcopy(row) for i in range(15)]
        
        for i in range(15 * 15):
            s = SnakeCell()
            if i % 2 == 1:
                s.set_background_type(False)
            else:
                s.set_background_type(True)
            self.grid[i//15][i%15] = s
            yield s
    
    def start(self):

        self.head = (11, 7)
        self.snake_list = [self.head, (12, 7), (13, 7)]
        self.direction = Direction.UP

        for block in self.snake_list:
            self.grid[block[0]][block[1]].set_snake(True)

        self.timer = self.set_interval(0.5, callback=self.update)
    
    def get_block_at(self, position):
        return self.grid[position[0]][position[1]]
    
    def update(self):
        dx = 0
        dy = 0
        match self.direction:
            case Direction.UP:
                dy = -1
            case Direction.RIGHT:
                dx = 1
            case Direction.DOWN:
                dy = 1
            case Direction.LEFT:
                dx = -1
        
        self.head = (self.head[0] + dy, self.head[1] + dx)

        if self.head[0] < 0 or self.head[0] >= 15 or self.head[1] < 0 or self.head[1] >= 15:
            self.timer.stop()
            return
        
        self.snake_list.insert(0, self.head)

        tail = self.get_block_at(self.snake_list.pop())
        tail.set_snake(False)
        tail.refresh()

        for snake_block in self.snake_list:
            b = self.get_block_at(snake_block)
            b.set_snake(True)
            b.refresh()
    
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