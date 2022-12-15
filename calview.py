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

def calview(calFile = "cal.txt",month = date.getStartingDate().split("-")[0], year = date.getStartingDate().split("-")[1]):
    try:
        # Open the calendar and store the list of events
        events = cal.parse(str(calFile))
        
        lib.year = year # Set global year to starting year
        
        CellList = term.renderCalendar(month,year)# Render the actual calendar.

        lastrow = int(CellList[len(CellList) - 1].split("-")[1]) + 1 # This variable stores the row number that we can print to. This is used to print event info and debug info.
        item = 1 # This variable stores the cell we are currently on.
        curses.curs_set(2) # Set cursor to very visible mode.
        
        wasThereAnEvent = False # A flag to track whether or not an event was displayed, this is used to clear ther terminal at the correct time.
        while True:

            # Calculate the col and row of the cell we want to
            # access.
            colofitem = int(CellList[item - 1].split("-")[0]) + 2
            rowofitem = int(CellList[item - 1].split("-")[1])
            if lib.debug > 0:
                # Add debug information
                w.addstr(lastrow,0,str("Item: " + str(item)))
                w.addstr(lastrow + 1,0,str("Colofitem: " + str(colofitem)))
                w.addstr(lastrow + 2,0,str("Rowofitem: " + str(rowofitem)))

            # Delete any and all lines...
            for x in range(0,5):
                w.move(lastrow + x,0)
                w.clrtoeol()
                
            # Ok so here we display the actual event info, if it exists.
            if cal.dayHasEvent(item,month,year,events):
                eventid = cal.getId(item,month,year,events)
                w.addstr(lastrow,0,"Event name: " + str(cal.getName(eventid,events)))
                w.addstr(lastrow + 1,0,"Location: " + str(cal.getLocation(eventid,events)))
                w.addstr(lastrow + 2,0,"Starts at: " + date.prettifyDate(str(cal.getStartDate(eventid,events))))
                w.addstr(lastrow + 3,0,"Ends at: " + date.prettifyDate(str(cal.getEndDate(eventid,events))))
                w.addstr(lastrow + 4,0,"Notes: " + str(cal.getNotes(eventid,events)))            
                wasThereAnEvent = True
            elif wasThereAnEvent == True:
                wasThereAnEvent = False

            if wasThereAnEvent == False:
                w.addstr(lastrow,0, "No event here...")
                w.addstr(lastrow + 1,0, "Maybe check the next page?")
                w.addstr(lastrow + 2,0, "Days with events are marked with\nan asterisk.")
                
            # Move the cursor to the cell that the user has selected
            w.move(rowofitem,colofitem)
            cmd = w.getch()
            if term.compKey(cmd,curses.KEY_RIGHT,261): # Right arrow key
                # Increase by one IF we are not on or over 31.
                if not item >= 31:
                    item += 1
                else:
                    item = 31
            elif term.compKey(cmd,curses.KEY_LEFT,260): # Left arrow key
                # Decrease by one IF we are not on 1 or less than 1
                if not item <= 1:
                    item -= 1
                else:
                    item = 1
            else:
                pass
            
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
            if clear == True and debug > 0:
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
                if debug > 0:
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

    
else:
    print("Do not import this program")
    sys.exit(1)

