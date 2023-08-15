from textual.app import ComposeResult
from textual.widgets import Static
from ascii_image import AsciiImage

class C4Logo(Static):

    def compose(self) -> ComposeResult:
        yield AsciiImage("assets/logo_small/less_than.txt", "white") #RGBA, 0 alpha
        yield AsciiImage("assets/logo_small/c4.txt", "#BB66FF")
        yield AsciiImage("assets/logo_small/greater_than.txt", "white")