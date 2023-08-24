from textual import on
from textual.widgets import Static
from textual import events
import random

class DefaultBackground(Static):

    DEFAULT_CSS = """
    DefaultBackground {
        align: center middle;
	    color: #320045;
	    height: 1fr;
	    width: 1fr;
    }
    """
    
    @on(events.Resize)
    def on_event_resize(self, message: events.Resize) -> None:

        self.update_hex_text(message.size.width, message.size.height)
    
    def update_hex_text(self, width: int, height: int) -> str:
        numbers = height * (width//3)
        string = " ".join(["{:02X}".format(random.randint(0,255)) for x in range(numbers)])
        self.update(string)