from textual.app import ComposeResult
from textual.widgets import Input, Static
from textual.containers import Center
from logo import C4Logo

class SignupMenu(Static):

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

        self.app.query_one("ContentSwitcher.MenuHolder").current = "snake"
        self.app.query_one("#snake").setup()

        self.thanks.styles.opacity = "100%"
        self.set_timer(5.0, self.clear_text)
        self.thanks.update(f"Thanks for signing up, [b][u][#BB66FF]{first_name}[/#BB66FF][/b][/u]!")
        self.thanks.styles.animate("opacity", value=0.0, duration=1.0, delay=4.0)
        
    def clear_text(self):
        self.thanks.update("")