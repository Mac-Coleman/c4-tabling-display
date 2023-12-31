from textual import on
from textual.widgets import Static
from textual.geometry import Size
from textual import events

import random
from .background import BackgroundBase, BackgroundMetaClass

class DefaultBackground(Static, BackgroundBase, metaclass=BackgroundMetaClass):

    DEFAULT_CSS = """
    DefaultBackground {
        align: center middle;
	    color: #320045;
	    height: 1fr;
	    width: 1fr;
    }
    """

    def __init__(self, id=None):
        self.old_size = Size()
        super().__init__(id=id)

    def author(self) -> str:
        return "Mac Coleman"
    
    def title(self) -> str:
        return "Purple Hexadecimal"
    
    def start(self) -> None:
        self.styles.opacity = 0.0
        self.styles.animate("opacity", 1.0, duration=2.0)

    def stop(self) -> None:
        self.styles.opacity = 1.0
        self.styles.animate("opacity", 0.0, duration=2.0, on_complete=self.finish)
    
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

class DefaultBackgroundRed(Static, BackgroundBase, metaclass=BackgroundMetaClass):
    DEFAULT_CSS = """
    DefaultBackgroundRed {
        align: center middle;
	    color: #990045;
	    height: 1fr;
	    width: 1fr;
    }
    """

    def __init__(self, id=None):
        self.old_size = Size()
        super().__init__(id=id)

    def author(self) -> str:
        return "Mac Coleman"
    
    def title(self) -> str:
        return "Red Hexadecimal"
    
    def start(self) -> None:
        self.styles.opacity = 0.0
        self.styles.animate("opacity", 1.0, duration=2.0)
        pass

    def stop(self) -> None:
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