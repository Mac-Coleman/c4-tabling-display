from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Input, Static, ContentSwitcher
from textual.containers import Center
import random
from ascii_image import AsciiImage
from logo import C4Logo
from signup_menu import SignupMenu
from qr_code_menu import QrCodeMenu

class TablingApp(App):
    """Displays the tabling app."""

    CSS_PATH = "main.css"

    BINDINGS = [
        Binding("escape", "switch_qr_code_display()", 'display_qr_code', show=False, priority=True),
    ]


    def compose(self) -> ComposeResult:
        
        self.qr_code = False
        with Static("", classes="Background") as b:
            numbers = 5000
            l = " ".join(["{:02X}".format(random.randint(0,255)) for x in range(numbers)])
            b.update(l)
            with ContentSwitcher(initial="signup", classes="MenuHolder"):
                yield SignupMenu(id="signup")
                yield QrCodeMenu(id="qr-code")

    def action_switch_qr_code_display(self, params=None):
        if self.qr_code:
            self.query_one("ContentSwitcher.MenuHolder").current = "signup"
        else:
            self.query_one("ContentSwitcher.MenuHolder").current = "qr-code"

        self.qr_code = not self.qr_code



if __name__ == "__main__":
    TablingApp().run()
