from textual.widgets import Static
from textual.geometry import Size
from textual.color import Color
from textual import events, on

import random

from .background import BackgroundBase, BackgroundMetaClass

class RainbowHex(Static, BackgroundBase, metaclass=BackgroundMetaClass):
    DEFAULT_CSS = """
    RainbowHex {
        align: center middle;
	    color: #990045;
	    height: 1fr;
	    width: 1fr;
    }
    """

    def __init__(self, *args, **kwargs):
        self.old_size = Size()
        self.color_list = [Color.from_hsl(x/100, 1.0, 0.25) for x in range(0, 100, 5)]
        self.color_index = 0
        super().__init__(*args, **kwargs)

    def author(self) -> str:
        return "Mac Coleman"
    
    def title(self) -> str:
        return "Rainbow Hexadecimal"
    
    def start(self) -> None:
        self.styles.opacity = 0.0
        self.styles.animate("opacity", 1.0, duration=2.0, on_complete=self.next_color)
        pass

    def next_color(self) -> None:
        self.styles.animate("color", self.color_list[self.color_index].css, duration=0.5, on_complete=self.next_color)
        self.color_index = (self.color_index + 1) % len(self.color_list)

    def stop(self) -> None:
        self.stop_animation("color")
        self.styles.opacity = 1.0
        self.styles.animate("opacity", 0.0, duration=2.0, on_complete=self.finish)
        pass
    
    def finish(self) -> None:
        self.post_message(BackgroundBase.BackgroundEnded())
    
    @on(events.Resize)
    def on_event_resize(self, message: events.Resize) -> None:
        if (message.size == self.old_size):
            return None

        self.update_hex_text(message.size.width, message.size.height)
        self.old_size = message.size
    
    def update_hex_text(self, width: int, height: int) -> str:
        numbers = height * (width//3)
        string = " ".join(["{:02X}".format(random.randint(0,255)) for x in range(numbers)])
        self.update(string)