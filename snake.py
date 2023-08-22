from textual.binding import Binding
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label, Digits
from textual.message import Message
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

class SnakeCellType(Enum):
    BACKGROUND = 0
    FOOD = 1
    SNAKE = 2
    GAMEOVER_SNAKE = 3

class SnakeGameState(Enum):
    WAITING = 0
    PLAYING = 1
    GAMEOVER = 2

class SnakeCell(Widget):

    cell_type = reactive(SnakeCellType.BACKGROUND)

    def set_background_type(self, light: bool):
        self.background_light = light
        self.cell_type = SnakeCellType.BACKGROUND

        if light:
            self.styles.color = "#333B42"
            self.styles.background = "#212A31"
        else:
            self.styles.color = "#0F1921"
            self.styles.background = "#080d12"
    
    def set_type(self, cell_type: SnakeCellType):
        self.cell_type = cell_type
    
    def render(self):
        if self.cell_type == SnakeCellType.SNAKE:
            self.styles.color = "#FFFFFF"
            return "████\n████"
        
        if self.cell_type == SnakeCellType.GAMEOVER_SNAKE:
            self.styles.color = "#FF5577"
            return "████\n████"
        
        if self.cell_type == SnakeCellType.FOOD:
            self.styles.color = "#FFCCCC"
            return "▄▀▀▄\n▀▄▄▀"
        
        self.set_background_type(self.background_light)
        return "▀▄▀▄\n▀▄▀▄"

class SnakeGame(Static, can_focus=True):

    BINDINGS = [
        Binding("w, up", "up", "Go up", show=False, priority=True),
        Binding("a, left", "left", "Go left", show=False, priority=True),
        Binding("s, down", "down", "Go down", show=False, priority=True),
        Binding("d, right", "right", "Go right", show=False, priority=True),
        Binding("r", "restart", "Restart the game", show=False, priority=True),
        Binding("space, enter", "finish", "Finish the game", show=False)
    ]

    class ScoreChanged(Message):
        """A message sent when the score is changed."""

        def __init__(self, score):
            self.score = score
            super().__init__()
    
    class GameEnded(Message):
        """A message sent when the game ends."""

        def __init__(self, score, game_time):
            self.score = score
            self.game_time = game_time
            super().__init__()
    
    class GameStarted(Message):
        """A message sent when the game starts."""

        def __init__(self):
            super().__init__()

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
        self.next_direction = self.direction
        self.food = (7, 7)
        self.score = 0
        self.state = SnakeGameState.PLAYING
        self.post_message(self.ScoreChanged(self.score)) # Make sure that score update is sent

        for block in self.snake_list:
            self.grid[block[0]][block[1]].set_type(SnakeCellType.SNAKE)
        self.interval = 0.25

        try:
            self.timer.stop()
        except AttributeError as e:
            pass
        self.timer = self.set_interval(self.interval, callback=self.update)
        self.focus()
        self.post_message(self.GameStarted())
        self.draw()

    def get_block_at(self, position):
        return self.grid[position[0]][position[1]]
    
    def draw(self):
        [[cell.set_type(SnakeCellType.BACKGROUND) for cell in row] for row in self.grid]
        
        self.get_block_at(self.food).set_type(SnakeCellType.FOOD)
        
        cell_type = SnakeCellType.SNAKE if self.state != SnakeGameState.GAMEOVER else SnakeCellType.GAMEOVER_SNAKE

        for position in self.snake_list:
            self.get_block_at(position).set_type(cell_type)
    
    
    def update(self):
        dx = 0
        dy = 0

        self.direction = self.next_direction
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
            self.post_message(self.GameEnded(self.score, 0))
            self.state = SnakeGameState.GAMEOVER
            self.draw()
            return
        
        if self.head in self.snake_list:
            self.timer.stop()
            self.post_message(self.GameEnded(self.score, 0))
            self.state = SnakeGameState.GAMEOVER
        
        self.snake_list.insert(0, self.head)

        found_food = False

        if self.food in self.snake_list:
            found_food = True
            self.score += 1
            self.timer.stop()
            self.interval *= 0.975
            self.timer = self.set_interval(self.interval, callback=self.update)
            self.food = (random.randint(0, 14), random.randint(0, 14))
            self.post_message(self.ScoreChanged(self.score))
        
        if not found_food:
            self.get_block_at(self.snake_list.pop())

        self.draw()
    
    def action_up(self) -> None:
        if self.direction != Direction.DOWN:
            self.next_direction = Direction.UP
    
    def action_left(self) -> None:
        if self.direction != Direction.RIGHT:
            self.next_direction = Direction.LEFT
    
    def action_down(self) -> None:
        if self.direction != Direction.UP:
            self.next_direction = Direction.DOWN

    def action_right(self) -> None:
        if self.direction != Direction.LEFT:
            self.next_direction = Direction.RIGHT
    
    def action_restart(self) -> None:
        self.start()
    
    def action_finish(self) -> None:
        self.timer.stop()
        self.app.query_one("ContentSwitcher.MenuHolder").current = "signup"
        
    def on_mount(self) -> None:
        self.border_title = "[i]Snake[/i]"

class SnakeMenu(Static):
    def compose(self) -> ComposeResult:
        yield SnakeGame()
        with Middle(classes="FitShort"):
            yield C4Logo()
            self.scoreboard = Digits("000")
            yield self.scoreboard

            self.timeboard = Digits("000")
            yield self.timeboard

            yield Label(" \n ", id="status")
    
    def on_mount(self) -> None:
        self.scoreboard.border_title = "Score:"
        self.timeboard.border_title = "Time:"
    
    def start(self) -> None:
        game = self.query_one(SnakeGame)
        game.start()
    
    def on_snake_game_score_changed(self, message: SnakeGame.ScoreChanged):
        self.scoreboard.update(f"{message.score:03}")
    
    def on_snake_game_game_started(self, message:SnakeGame.GameStarted):
        s = self.query_one("#status")
        s.update(" \n ")
        self.notify("Started")

    def on_snake_game_game_ended(self, message: SnakeGame.GameEnded):
        s = self.query_one("#status")
        s.update("Game Over!\nPress [b]R[/b] to retry, or [b]ENTER[/b] to quit.")