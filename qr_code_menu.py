from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Center

from ascii_image import AsciiImage

class QrCodeMenu(Static):

    def compose(self) -> ComposeResult:
        yield Static("[u][b][#BB66FF]Join the C4 Discord![/#BB66FF][/b][/u]", classes="Status")
        with Center():
            with Static() as s:
                s.styles.background = "white"
                s.styles.color = "black"
                s.styles.padding = (2, 4)
                s.styles.width = "auto"
                s.styles.height = "auto"
                s.styles.margin = (1, 0, 0, 0)
                yield AsciiImage("assets/qr_code/qr_code.txt", "black", "white")
        yield Static("Scan the above QR code to join our discord server!", classes="Prompt")