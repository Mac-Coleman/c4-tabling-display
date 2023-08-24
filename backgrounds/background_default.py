from textual.widgets import Static
import random

class DefaultBackground(Static):

    DEFAULT_CSS = """
    DefaultBackground {
        align: center middle;
	    color: #320045;
	    height: 1fr;
	    width: 1fr;
        layer: background;
    }
    """

    def on_mount(self) -> None:
        numbers = 5000
        l = " ".join(["{:02X}".format(random.randint(0,255)) for x in range(numbers)])
        self.update(l)