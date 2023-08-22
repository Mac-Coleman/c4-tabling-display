from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Input, Static, ContentSwitcher
from textual.containers import Center

from ascii_image import AsciiImage
from logo import C4Logo
from signup_menu import SignupMenu
from qr_code_menu import QrCodeMenu
from snake import SnakeMenu, SnakeGame

import random
import argparse
import sys

try:
    import segno
except ImportError as e:
    print("Failed to import segno.")
    print("Warning: package 'segno' is required to generate QR codes.")
    print("Install it and try again.")
    raise e

class TablingApp(App):
    """Displays the tabling app."""

    CSS_PATH = "main.tcss"

    BINDINGS = [
        Binding("escape", "switch_qr_code_display()", 'display_qr_code', show=False, priority=True),
    ]


    def compose(self) -> ComposeResult:

        self.current_user = ("EMPTY", "EMPTY")
        
        self.qr_code = False
        with Static("", classes="Background") as b:
            numbers = 5000
            l = " ".join(["{:02X}".format(random.randint(0,255)) for x in range(numbers)])
            b.update(l)
            with ContentSwitcher(initial="signup", id="menus", classes="MenuHolder"):
                yield SignupMenu(id="signup")
                yield QrCodeMenu(id="qr-code")
                yield SnakeMenu(id="snake")
    
    def on_signup_menu_name_entered(self, message: SignupMenu.NameEntered):
        self.current_user = (message.name, message.email_address)
        with open("tabling_names.csv", 'a') as file:
            file.write(f"{message.name},{message.email_address}\n")
        
    def on_snake_game_game_ended(self, message: SnakeGame.GameEnded):
        n = self.current_user[0]
        e = self.current_user[1]

        with open("tabling_scores.csv", 'a') as file:
            file.write(f"{n},{e},{message.score},{message.game_time}\n")

    def action_switch_qr_code_display(self, params=None):
        if self.qr_code:
            self.query_one("ContentSwitcher.MenuHolder").current = "signup"
        else:
            self.query_one("ContentSwitcher.MenuHolder").current = "qr-code"

        self.qr_code = not self.qr_code


def write_qr_code(data: str, density: int, allow_micro=False):

    if allow_micro == True:
        allow_micro = None
    qr_code = segno.make(data, micro=allow_micro)
        
    if density == 1:
        output = ""
        for row in qr_code.matrix:
            for byte in row:
                if byte == 1:
                    output += '██'
                else:
                    output += '  '
                
            output += '\n'
        
        with open('assets/qr_code/qr_code.txt', 'w') as file:
            file.write(output)
        return output
    
    if density == 2:
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
        return output
    
    if density == 3:
        output = ""
        resized_code = list(qr_code.matrix)
        empty = bytearray([0]*((len(qr_code.matrix[0])//2 + 1)*2))
        resized_code.extend([empty]*((len(qr_code.matrix)//3 + 1)*3 - len(qr_code.matrix)))

        for i in range(0, len(resized_code)-1, 3):

            tr = resized_code[i]
            mr = resized_code[i+1]
            br = resized_code[i+2]

            tr.extend([0]*(len(tr)%2))
            mr.extend([0]*(len(mr)%2))
            br.extend([0]*(len(br)%2))

            for j in range(0, len(tr)-1, 2):
                value = tr[j] * 1 \
                    + tr[j+1] * 2 \
                    + mr[j]   * 4 \
                    + mr[j+1] * 8 \
                    + br[j]   * 16 \
                    + br[j+1] * 32

                if value == 0:
                    output += ' '
                    continue

                if value == 21:
                    output += '▌' # Character does not exist in this set.
                    continue
                
                if value == 42:
                    output += '▐' # Character does not exist in this set.
                    continue
                
                if value == 63:
                    output += '█' # Character does not exist in this set.
                    continue
                
                if value > 21:
                    value -= 1
                
                if value > 41:
                    value -= 1
                
                value += 0x1FAFF # Space before block characters
                output += chr(value)
            output += "\n"

        with open('assets/qr_code/qr_code.txt', 'w') as f:
            f.write(output)
        return output

def handle_run(args):
    TablingApp().run()

def handle_qr_codes(args):

    if not args.density in (1, 2, 3):
        print(f"Error: Invalid density: {args.density}")
        print("Density must be one of...")
        print("\t1: 2 characters per bit")
        print("\t2: 2 bits per character")
        print("\t3: 6 bits per character")
        return

    print(f"Encoding '{args.data}' with density {args.density}, {'dis' if not args.allow_micro else ''}allowing Micro QR codes...")
    q = write_qr_code(args.data, args.density, allow_micro=args.allow_micro)
    print("QR code successfully written.")

    if len(q.split('\n')) >= 28:
        print("WARNING: This QR code may be too big to properly display!")
        print("Note: If this QR code displays improperly or is cut off, you might be trying to encode too much data.")
        print("    : If this occurs, shorten the data you are encoding. Removing unnecessary query strings might help.")
        print("    : You may also retry this command with the --density option.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="C4 Tabling App", description="A program to attract new members to Cornell College Computing Club")
    subparsers = parser.add_subparsers(help="Subcommands to choose program behavior.")

    parser.add_argument("-v", "--version", action="version", version="%(prog)s v0.0.1")

    main_parser = subparsers.add_parser('run', description='run the tabling program', help='run the tabling program')
    qr_code_parser = subparsers.add_parser('code', description="generate QR codes to display in the tabling program", help='generate QR codes to display in the tabling program')

    main_parser.set_defaults(func=handle_run)
    qr_code_parser.set_defaults(func=handle_qr_codes)

    main_parser.add_argument("-s", "--signup-only", action="store_const", help="only display sign up window", const=True, default=False)

    background_group = main_parser.add_mutually_exclusive_group()
    background_group.add_argument("-n", "--no-backgrounds", action="store_const", help="use only a static background", const=True, default=False)
    background_group.add_argument("-b", "--backgrounds", action="extend", nargs='+', type=str, metavar="BACKGROUNDS", help="use BACKGROUNDS as backgrounds for the tabling app")

    qr_code_parser.add_argument('data', action='store', help="the data to encode")
    qr_code_parser.add_argument('-m', '--allow-micro', action="store_true", help="allow Micro QR codes. Warning: most mobile phones do not natively support Micro QR codes.")
    qr_code_parser.add_argument('-d', '--density', action='store', type=int, default=2, help="Set the information density of the code. 1: 2 characters per bit. 2: 2 bits per characters. 3: 6 bits per characters.")


    argument_namespace = parser.parse_args()
    argument_namespace.func(argument_namespace)