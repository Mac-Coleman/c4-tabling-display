from textual import on
from textual.app import ComposeResult
from textual.widgets import Input, Static
from textual.containers import Center
from textual.message import Message
from logo import C4Logo

class SignupMenu(Static):

    class NameEntered(Message):
        def __init__(self, name, email_address):
            self.name = name
            self.email_address = email_address
            super().__init__()

    def compose(self) -> ComposeResult:
        with Center():
            yield C4Logo()
        yield Static("Enter your [b][u]name[/u][/b] and [b][u]email address[/b][/u] to stay up to date with Cornell College Computer Science happenings!", classes="Prompt")
        self.name_input = Input(placeholder="Name", id="name")
        self.email_input = Input(placeholder="Email address (@cornellcollege.edu)", id="email")
        self.thanks = Static("", classes="Status")

        yield self.name_input
        yield self.email_input
        yield self.thanks

    @on(Input.Submitted, "#name")
    def name_entered(self, message: Input.Submitted):
        self.email_input.focus()
    
    @on(Input.Submitted, "#email")
    def email_entered(self, message: Input.Submitted):
        self.post_message(self.NameEntered(self.name_input.value, self.email_input.value))

        self.name_input.value = ""
        self.email_input.value = ""

    def display_thanks(self, name: str):
        self.name_input.focus()

        self.thanks.styles.opacity = "100%"
        self.set_timer(5.0, self.clear_text)
        self.thanks.update(f"Thanks for signing up, [b][u][#BB66FF]{name}[/#BB66FF][/b][/u]!")
        self.thanks.styles.animate("opacity", value=0.0, duration=1.0, delay=4.0)
    
    def on_mount(self) -> None:
        self.name_input.focus()
        
    def clear_text(self):
        self.thanks.update("")