from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Input, Static
from textual.containers import Center, Middle

class AsciiImage(Static):
    """A class that loads a string of characters that can appear like an image."""

    def __init__(self, image_file: str, fg_color: str, bg_color: str):
        super().__init__()
        ascii_text = open(image_file, "r").readlines()
        width = max([len(line) for line in ascii_text])

        self.content = "".join(ascii_text)
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.styles.max_width = width
        self.styles.max_height = len(ascii_text)

    def compose(self) -> ComposeResult:
        image = Static(self.content)
        image.styles.color = self.fg_color
        image.styles.background = self.bg_color
        yield image

class C4Logo(Static):

    def compose(self) -> ComposeResult:
        yield AsciiImage("assets/logo_small/less_than.txt", "white", "rgba(0,0,0,0)") #RGBA, 0 alpha
        yield AsciiImage("assets/logo_small/c4.txt", "purple", "rgba(0,0,0,0)")
        yield AsciiImage("assets/logo_small/greater_than.txt", "white", "rgba(0,0,0,0)")

class PageWrapper(Static):

    def compose(self) -> ComposeResult:
        yield C4Logo()
        yield Static("Enter your name and email address to stay up to date with Cornell College Computer Science happenings!")
        yield Input(placeholder="Name", id="name")
        yield Input(placeholder="Email address (@cornellcollege.edu)", id="email")

class TablingApp(App):
    """Displays the tabling app."""

    CSS_PATH = "textual_attempt.css"

    def on_input_submitted(self, message: Input.Submitted):
        if message.control.id == "name":
            self.query_one("#email").focus()
            return

        if message.control.id != "email":
            return

        with open('tabling_names.csv', 'a') as file:
            file.write(f"{self.query_one('#name').value}, {message.control.value}\n")
            self.query_one("#name").value = ""
            message.control.value = ""
        
        

    def compose(self) -> ComposeResult:
        with Middle(id="MainContainer"):
            with Center():
                yield PageWrapper()

if __name__ == "__main__":
    TablingApp().run()
