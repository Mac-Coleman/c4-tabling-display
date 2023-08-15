# C4 Tabling App

![A screenshot of the tabling app, with C4 logo and text entry fields.](assets/screenshot.png)
This app is a small program to attract new members to the Cornell College Computing Club (C4).
The app relies on the python module `textual` which can be found [here](https://github.com/Textualize/textual).

It displays an ASCII art version of the C4 logo in the Cornell College colors, and it has two text inputs with which student names and emails can be collected.
The names and emails are appended to a comma-separated value file named `tabling\_names.csv` each time a name is entered.

Additionally, the user can press the `ESC` key to toggle the display and instead show a QR code for users to scan, so that they can be connected with club resources.
We hope that this will be an interesting way to engage with potential members.

This app may not appear the same on all terminals. It has only been tested with KDE Konsole on Manjaro Uranos 23.0.0 so far.
To try it out, simply clone this repository and run `python main.py`.

## Usage
* `-h`, `--help`: learn more about program arguments
* `-v`, `--version`: display version information for the program
* `-q DATA`, `--qr-code DATA`: encodes and saves `DATA` into a text QR code with utf-8 characters. This sets the QR code to be displayed when the `ESC` key is pressed.

## Dependencies
* [textual](https://github.com/Textualize/textual) is the most critical dependency as it is what this program uses to create the terminal user interface.
* [segno](https://github.com/heuer/segno) is required for the generation of QR codes.