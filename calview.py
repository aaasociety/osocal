#!/bin/python3
# © abdul karim kikar 2022
# licenseret under GNU GPL version 3 og nyere versioner.

import src.term as term
import sys,curses
import curses.ascii as ascii
import src.dialog as dialog

# This creates the "w" window object.
import src.lib as lib

# These are here for backwards-compatability purposes
# Eventually, I will get around to fixing each individual
# variable to use the one from lib.py
w = lib.w
debug=lib.debug
cal = lib.cal
row = lib.row
col = lib.col

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
        
        w.addstr("\n")
        if result == "quit":
            w.addstr("Aborting...")
            term.leave()

        w.getch()
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
    main()
#    curses.wrapper(calOpenPrompt)
    
else:
    print("Do not import this program")
    sys.exit(1)

