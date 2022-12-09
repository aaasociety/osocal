#!/bin/python3
# © abdul karim kikar 2022
# licenseret under GNU GPL version 3 og nyere versioner.

# This creates the "w" window object.
import src.lib as lib

import src.term as term
import sys,curses
import curses.ascii as ascii
import src.dialog as dialog
import src.date as date

# These are here for backwards-compatability purposes
# Eventually, I will get around to fixing each individual
# variable to use the one from lib.py
w = lib.w
debug=lib.debug
cal = lib.cal
row = lib.row
col = lib.col
ERR = lib.ErrType

# The function that actualls views the calendar and let's the user edit it.
# [1] [2] [3] [4] [5] [6] [7]
def calview(w):
    try:
        row = 10
        col = 10
        month = date.getStartingDate().split("-")[0]
        year = date.getStartingDate().split("-")[1]
        while True:
            temp_row = 0 
            temp_col = 0
            w.clear()
            w.refresh()
            w.addstr("\t\t\t" + date.getMonth(month) + "\n")
            for x in range(1,date.getDays(month,year) + 1):
                w.addstr("[" + str(x) + "]")
            w.getch()
            
    except KeyboardInterrupt:
        w.clear()
        w.addstr("Leaving...")
        term.leave()

def infoPrompt():
    try:
        result = term.scrollablePrompt(dialog.info)
        if result == 1: # Check if everything went fine
            main()      # This also means that the user
                        # pressed the Enter key.
    except KeyboardInterrupt:
        w.clear()
        w.addstr("Aborting...")
        term.leave()

def calOpenPrompt():
    try:
        result = term.editablePrompt(dialog.cal.open)
        
        if result == "quit":
            w.addstr("Aborting...")
            term.leave()

        if term.ynPrompt("Is this correct: " + str(result)) == False:
            leave()

        calView(result)
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
            if cal == "":
                term.print(dialog.main.calmissing)
            term.print(dialog.main.basichelp)
            w.refresh()
            w.addstr("> ")
            cmd = w.getch()
            # Clear "clear" var if it is set
            if clear == False:
                clear = True
            w.addstr("\n");
            truecmd = ascii.unctrl(cmd).lower()
            if truecmd == 'q':
                term.leave()
            elif truecmd == 'o':
                calOpenPrompt()
            elif truecmd == 'i':
                infoPrompt()
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
    #main()
    curses.wrapper(calview)
    
else:
    print("Do not import this program")
    sys.exit(1)

