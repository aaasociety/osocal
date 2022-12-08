#!/bin/python3
# A file containing shared data and variables

# Shared, global curses window.
import curses
w = curses.initscr()
w.keypad(True)

# Shared data values for various things.
row = 5
col = 5
cal = ""
ErrType = None

# Global debug mode.
debug = True

# Shared data values for years, months and days.
year = 0
