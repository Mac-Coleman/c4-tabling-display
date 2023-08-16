from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Input, Static, ContentSwitcher
from textual.containers import Center

from ascii_image import AsciiImage
from logo import C4Logo
from signup_menu import SignupMenu
from qr_code_menu import QrCodeMenu

import random
import argparse
import sys

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


def write_qr_code(data: str):
    qr_code = segno.make(data)
        
    if qr_code.is_micro:
        with open('assets/qr_code/qr_code.txt', 'w') as file:
            for row in qr_code.matrix:
                for byte in row:
                    if byte == 1:
                        file.write('██')
                    else:
                        file.write('  ')
                    
                file.write('\n')
        return
    
    # Build upper and lower pairs
    lines = []
    for i in range(0, len(qr_code.matrix)-1, 2):
        lines.append([])
        for j in range(0, len(qr_code.matrix[0])):
            lines[i//2].append((qr_code.matrix[i][j], qr_code.matrix[i+1][j]))
    lines.append([])
    for j in range(0, len(qr_code.matrix[1])):
        lines[-1].append((qr_code.matrix[-1][j], 0))
    
    output = ""
    for line in lines:
        for couple in line:
            match couple:
                case (0, 0):
                    output += " "
                case (0, 1):
                    output += "▄"
                case (1, 0):
                    output += "▀"
                case (1, 1):
                    output += "█"
        output += "\n"
    
    with open('assets/qr_code/qr_code.txt', 'w') as file:
        file.write(output)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="C4 Tabling App", description="Displays a text user interface for tabling sign-up")
    parser.add_argument("-s", "--signup-only", action="store_const", help="only display sign up window", const=True, default=False)
    parser.add_argument("-n", "--no-backgrounds", action="store_const", help="use only a static background", const=True, default=False)
    parser.add_argument("-q", "--qr-code", action="store", metavar="DATA", help="encode and write DATA for display as a QR-code and exit")
    parser.add_argument("-b", "--backgrounds", action="extend", metavar="BACKGROUNDS", help="use BACKGROUNDS as backgrounds for the tabling app")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v0.0.1")

    argument_namespace = parser.parse_args()
    
    if argument_namespace.qr_code is not None:
        # Encode the data as a QR code and write it to assets/qr_code/qr_code.txt

        try:
            import segno
        except ImportError as e:
            print("Failed to import segno.")
            print("Warning: package 'segno' is required to generate QR codes.")
            print("Install it and try again.")
            sys.exit(-1)

        print(f"Encoding '{argument_namespace.qr_code}'...")
        write_qr_code(argument_namespace.qr_code)
        print("QR code successfully written.")
        print("Note: If this QR code displays improperly or is cut off, you might be trying to encode too much data.")
        print("    : If this occurs, shorten the data you are encoding. Removing unnecessary query strings might help.")
        sys.exit(0)

    
    TablingApp().run()
