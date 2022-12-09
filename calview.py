#!/bin/python3
# © abdul karim kikar 2022
# licenseret under GNU GPL version 3 og nyere versioner.

# This creates the "w" window object.
import src.lib as lib

import sys,curses # For terminal handling
import src.term as term # For even better terminal handling
import curses.ascii as ascii # For decoding keys provided by getch()
import src.dialog as dialog # For dialogue
import src.date as date # For parsing dates and whatnot
import src.cal as cal # For parsing the calendar

# These are here for backwards-compatability purposes
# Eventually, I will get around to fixing each individual
# variable to use the one from lib.py
w = lib.w
debug=lib.debug
calFile = lib.cal
row = lib.row
col = lib.col
ERR = lib.ErrType

def calview(w):
    try:
            month = date.getStartingDate().split("-")[0]
            year = date.getStartingDate().split("-")[1]
            CellList = term.renderCalendar(month,year) # Render the actual calendar.
            def setCursor():
                curses.setsyx(cal.extractRow(CellList,item),cal.extractRow(CellList,item))

            # Get the Col and Row values from CellList
            col = 0
            row = int(CellList[len(CellList) - 1].split("-")[1]) + 1
            item = 0
            while True:
                curses.curs_set(2)
                setCursor()
                cmd = w.getch()
                
            
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
            if calFile == "":
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
    main()
#    curses.wrapper(calview)
    
else:
    print("Do not import this program")
    sys.exit(1)

