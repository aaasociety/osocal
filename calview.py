#!/bin/python3
# © abdul karim kikar 2022
# licenseret under GNU GPL version 3 og nyere versioner.

# This creates the "w" window object.
import src.win as win

import sys,curses # For terminal handling
import src.lib as lib # Shared values and data.
import src.term as term # For even better terminal handling
import curses.ascii as ascii # For decoding keys provided by getch()
import src.dialog as dialog # For dialogue
import src.date as date # For parsing dates and whatnot
import src.cal as cal # For parsing the calendar

# These are here for backwards-compatability purposes
# Eventually, I will get around to fixing each individual
# variable to use the one from lib.py
w = win.w
debug=lib.debug
calFile = lib.cal
row = lib.row
col = lib.col
ERR = lib.ErrType

def calview2(w):
    try:
        # Open the calendar and store the list of events
        eventList = cal.parse("cal.txt")
        
        month = date.getStartingDate().split("-")[0] # Get Month
        year = date.getStartingDate().split("-")[1] # Get year
        # Set global year to starting year
        lib.year = year
        CellList = term.renderCalendar(month,year)# Render the actual calendar.
        w.getch()
            
    except KeyboardInterrupt:
        w.clear()
        w.addstr("Leaving...")
        term.leave()

def calOpenPrompt():
    try:
        result = term.editablePrompt(dialog.cal.open)
        
        if result == "quit":
            w.addstr("Aborting...")
            term.leave()

        if term.ynPrompt("Is this correct: " + str(result)) == False:
            leave()

        calview(result)
    except KeyboardInterrupt:
        w.addstr("\nAborting...\n")
        term.leave()
        sys.exit(1)
    

def main():
    try:
        clear = True
        while 1:
            if clear == True and debug == False:
                w.clear()
            term.print(dialog.main.intro)
            if calFile == "":
                term.print(dialog.main.calmissing)
            term.print(dialog.main.basichelp)
            w.refresh()
            w.addstr("> ")
            cmd = w.getch()
            # Clear "clear" var if it is set
            if clear == False:
                clear = True

            # Parse commands
            # q is for quitting
            # o is for opening a calendar
            # i is for information about the program and its features
            # c is for copyright information
            # h is for a basic help dialog.
            truecmd = ascii.unctrl(cmd).lower()
            if truecmd == 'q':
                term.leave()
            elif truecmd == 'o':
                calOpenPrompt()
            elif truecmd == 'i':
                term.scrollablePrompt(dialog.info)
            elif truecmd == 'c':
                term.scrollablePrompt(dialog.copyright)
            elif truecmd == 'h':
                term.scrollablePrompt(dialog.main.basichelp)
            else:
                if debug == True:
                    w.addstr("\npure: " + str(cmd))
                    w.addstr("\nunctrl: " + str(truecmd))
                else:
                    clear = False
                    w.addstr(str("Invalid command"))
            w.refresh()            
        
    except KeyboardInterrupt:
        w.addstr("\nAborting...\n")
        term.leave()
        sys.exit(1)

if __name__ == "__main__":
    curses.wrapper(calview2)
   # main()
#    curses.wrapper(calview2)
    
else:
    print("Do not import this program")
    sys.exit(1)

