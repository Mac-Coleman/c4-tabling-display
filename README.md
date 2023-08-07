# C4 Tabling App

This app is a small program to attract new members to the Cornell College Computing Club.
The app relies on the python module `textual` which can be found [here](https://github.com/Textualize/textual).

It displays an ASCII art version of the C4 logo in the Cornell College colors, and it has two text inputs with which student names and emails can be collected.
The names and emails are appended to a comma-separated value file named "tabling\_names.csv" each time a name is entered.
We hope that this will be an interesting way to engage with potential members.

This app may not appear the same on all terminals. It has only been tested with KDE Konsole on Manjaro Uranos 23.0.0 so far.
To try it out, simply clone this repository and run `python main.py`.
