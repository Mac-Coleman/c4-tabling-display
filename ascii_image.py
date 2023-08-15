from textual.app import ComposeResult
from textual.widgets import Static

class AsciiImage(Static):
    """A class that loads a string of characters that can appear like an image."""

    def __init__(self, image_file: str, fg_color: str, bg_color=None):
        super().__init__()
        ascii_text = open(image_file, "r").readlines()
        width = max([len(line) for line in ascii_text]) - 1

        self.content = "".join(ascii_text)
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.styles.max_width = width
        self.styles.min_width = width
        self.styles.max_height = len(ascii_text)
        self.styles.min_height = len(ascii_text)

    def compose(self) -> ComposeResult:
        image = Static(self.content)
        image.styles.color = self.fg_color
        if self.bg_color:
            image.styles.background = self.bg_color
        yield image