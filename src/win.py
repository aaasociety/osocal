#!/bin/python3
# Shared window for curses
# lib.py includes useful data
# even for programs that don't need a curses window
# so this allows you to use lib.py without
# creating a curses window that breaks the terminal
import curses
w = curses.initscr()
w.keypad(True)
