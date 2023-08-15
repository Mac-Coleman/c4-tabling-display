from textual.app import ComposeResult
from textual.widgets import Label, Static
from textual.containers import Center, Middle

from ascii_image import AsciiImage
from logo import C4Logo


message_text = "Scan the QR code to join our discord server!\n" \
    " - Stay up-to-date with club plans\n"\
    " - Meet other comp sci students\n"\
    " - Get help with your urgent questions\n"\
    " - Show off your projects\n"\
    " - Get career advice\n"\
    " - And much more!"

class QrCodeMenu(Static):

    def compose(self) -> ComposeResult:
        with Center(classes="LeftBar") as c:
            with Center():
                yield C4Logo()
            yield Label("[u][b][#BB66FF]Join the C4 Discord![/#BB66FF][/b][/u]")
            yield Label(message_text, classes="Prompt")
        with Middle():
            with Static(classes="QrCodeContainer"):
                yield AsciiImage("assets/qr_code/qr_code.txt", "black", "white")
            with Center(id="link-holder"):
                yield Label("LINK HERE", id="link")