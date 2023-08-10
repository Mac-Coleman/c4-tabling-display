from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Input, Static, ContentSwitcher
import random

class AsciiImage(Static):
    """A class that loads a string of characters that can appear like an image."""

    def __init__(self, image_file: str, fg_color: str, bg_color=None):
        super().__init__()
        ascii_text = open(image_file, "r").readlines()
        width = max([len(line) for line in ascii_text])

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

class C4Logo(Static):

    def compose(self) -> ComposeResult:
        yield AsciiImage("assets/logo_small/less_than.txt", "white") #RGBA, 0 alpha
        yield AsciiImage("assets/logo_small/c4.txt", "#BB66FF")
        yield AsciiImage("assets/logo_small/greater_than.txt", "white")

class SignupMenu(Static):

    def compose(self) -> ComposeResult:
        yield C4Logo()
        yield Static("Enter your [b][u]name[/u][/b] and [b][u]email address[/b][/u] to stay up to date with Cornell College Computer Science happenings!", classes="Prompt")
        self.name_input = Input(placeholder="Name", id="name")
        self.email_input = Input(placeholder="Email address (@cornellcollege.edu)", id="email")
        self.thanks = Static("", classes="Status")

        yield self.name_input
        yield self.email_input
        yield self.thanks

    def on_input_submitted(self, message: Input.Submitted):
        if message.control == self.name_input:
            self.email_input.focus()
            return

        if message.control != self.email_input:
            return

        first_name = self.name_input.value.split(" ")[0]

        with open('tabling_names.csv', 'a') as file:
            file.write(f"{self.name_input.value}, {self.email_input.value}\n")
            self.name_input.value = ""
            self.email_input.value = ""
            self.name_input.focus()

        self.thanks.styles.opacity = "100%"
        self.set_timer(5.0, self.clear_text)
        self.thanks.update(f"Thanks for signing up, [b][u][#BB66FF]{first_name}[/#BB66FF][/b][/u]!")
        self.thanks.styles.animate("opacity", value=0.0, duration=1.0, delay=4.0)
        
    def clear_text(self):
        self.thanks.update("")

class QrCodeDisplay(Static):

    def compose(self) -> ComposeResult:
        yield C4Logo() # placeholder


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
            with Static(classes="SwitcherContainer"):
                with ContentSwitcher(initial="signup-menu", id="MenuHolder", classes="MenuHolder"):
                    yield SignupMenu(id="signup-menu")
                    yield QrCodeDisplay(id="qr-code")

    def action_switch_qr_code_display(self, params=None):
        if self.qr_code:
            self.query_one("#MenuHolder").current = "signup-menu"
        else:
            self.query_one("#MenuHolder").current = "qr-code"

        self.qr_code = not self.qr_code



if __name__ == "__main__":
    TablingApp().run()
