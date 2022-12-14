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
import src.weather as wth # For calling the weather API

# These are here for backwards-compatability purposes
# Eventually, I will get around to fixing each individual
# variable to use the one from lib.py
w = win.w
debug=lib.debug
calFile = lib.cal
row = lib.row
col = lib.col
ERR = lib.ErrType

# The weather prompt feature
def weatherPrompt(location = "Odense, Denmark", events = lib.events):   
    try:
        weatherresult = wth.getWeatherData(location)
        w.clear()
        row = 0
        col = 0
        term.print("Vejret for " + location,0,col)
        term.print("Vejr: " + weatherresult[1],2)
        term.print("Temperatur: " + weatherresult[0],4)
        term.print("Men det føler som " + weatherresult[3],5)
        term.print("Vindhastighed: " + weatherresult[2],6)
        row = 7
        if float(weatherresult[0]) < 15:
            row += 1
            term.print("Det er kold, tag en jakke på!",row)
        if float(weatherresult[0]) < 10:
            row += 1
            term.print("Tage en hue på ellers så kommer du til at fryse",row)
            row += 1
            term.print("Det er også en god ide at tage handsker på",row)
        if float(weatherresult[0]) < 3:
            row += 1
            term.print("Husk at tage en halstørklæde på.",row)
        row += 1
        term.print("Temperaturen er I celsius og vindhastigheden er I kilometer om timen.",row)
        w.move(row,col)
        w.getch()
        return
    except KeyboardInterrupt:
        w.clear()
        w.addstr("Leaving...")
        term.leave()


# This will be implemented sometime later
# I have to focus on the weather feature
def editEntry(day,month,year = lib.year, events = lib.events,calFile = "cal.txt"):
    try:
        curses.cbreak() # We will handle special keys ourselves.
        w.keypad(True) # We want to handle pure curses keycodes.
        curses.noecho() # We will handle echoing characters ourselves.

        w.clear()
        row = 0
        col = 0
        if cal.dayHasEvent(day,month,year,events):
            eventid = cal.getId(day,month,year,events)
            w.addstr(row,col,"Redigere eksisterende begivenhed")
            w.addstr(row + 1,0,"Navn: " + str(cal.getName(eventid,events)))
        else:
            w.addstr(row,col,"Tilsæt nyt begivenhed")
            w.addstr(row + 1,0,"Navn: ")
        event = [0,"","","","",""]
        editables = ["Navn: ", "Sted: ", "Begynder (YYYY-mm-dd-hh-mm): ","Slutter (YYYY-mm-dd-hh-mm):","Noter: "]
        cur = 1
        assembledstring = ""
    
        while True:
            curlen = len(editables[cur - 1])
            w.move(row + cur, col + curlen)
            w.refresh()
            cmd = w.getch()
            if term.compKey(cmd,curses.KEY_ENTER,10):
                # Detected enter key
                # So save assembledstring.
                # And set cur to +1
                event[cur] = assembledstring
                cur += 1
            elif term.compKey(cmd,curses.KEY_BACKSPACE,127):
                # Remove one character
                assembledstring = assembledstring[:len(assembledstring)-1]
            else:
                # Here we convert the int provided by
                # getch() and add it assembledstring.
                # But first we detect if we caught some
                # strange control key.
                if len(ascii.unctrl(cmd)) > 1:
                    continue # Other invalid key detected.
            
                assembledstring += ascii.unctrl(cmd) # The key is completely valid so we add it to assembledstring.
            
                col = len(assembledstring) # Set col to the length of assembled string
            return
    except curses.error:
        w.clear()
        w.addstr("Leaving...")
        term.leave()
        
def calview(calFile = "cal.txt",month = int(date.getStartingDate().split("-")[0]), year = int(date.getStartingDate().split("-")[1])):
    try:
        # Make sure month and years are integers
        month = int(month)
        year = int(year)
        
        # If calFile is empty then
        # replace it with the sane default that is "cal.txt"
        if calFile == "":
            calFile = "cal.txt"
        
        # Open the calendar and store the list of events
        events = cal.parse(str(calFile))
        
        lib.year = year # Set global year to starting year
        
        CellList = term.renderCalendar(str(month),year)# Render the actual calendar.

        lastrow = int(CellList[len(CellList) - 1].split("-")[1]) + 2 # This variable stores the row number that we can print to. This is used to print event info and debug info.
        item = 1 # This variable stores the cell we are currently on.
        curses.curs_set(2) # Set cursor to very visible mode.
        
        wasThereAnEvent = False # A flag to track whether or not an event was displayed, this is used to clear ther terminal at the correct time.
        w.addstr(lastrow - 1,0,"--")
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
            for x in range(0,10):
                w.move(lastrow + x,0)
                w.clrtoeol()
                
            # Ok so here we display the actual event info, if it exists.
            if cal.dayHasEvent(item,month,year,events):
                eventid = cal.getId(item,month,year,events)
                try:
                    w.addstr(lastrow,0,"Navn: " + str(cal.getName(eventid,events)))
                    w.addstr(lastrow + 1,0,"Sted: " + str(cal.getLocation(eventid,events)))
                    w.addstr(lastrow + 2,0,"Begynder: " + date.prettifyDate(str(cal.getStartDate(eventid,events))))
                    w.addstr(lastrow + 3,0,"Slutter " + date.prettifyDate(str(cal.getEndDate(eventid,events))))
                    w.addstr(lastrow + 4,0,"Noter/Andre information: " + str(cal.getNotes(eventid,events)))
                except curses.error:
                    pass
                wasThereAnEvent = True
            elif wasThereAnEvent == True:
                wasThereAnEvent = False

            # Print the basic calendar help dialog if
            # we are not on an event
            if wasThereAnEvent == False:
                w.addstr(lastrow,0,dialog.basiccalhelp)
                
            # Move the cursor to the cell that the user has selected
            # And then wait for a command
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
            elif term.compKey(cmd,curses.KEY_UP,259): # Up arrow key
                if month >= 12:
                    month = 1
                    year += 1
                else:
                    month += 1
                calview(calFile,month,year)
            elif term.compKey(cmd,curses.KEY_DOWN,258): # Down arrow key
                if month <= 1:
                    month = 12
                    year -= 1
                else:
                    month -= 1
                calview(calFile,month,year)
            elif term.compKey(cmd,curses.KEY_ENTER,10): # Enter key (Edit)
                if cal.dayHasEvent(item,month,year,events):
                    weatherPrompt(cal.getLocation(eventid,events),events)
                    CellList = term.renderCalendar(str(month),year)# Render the actual calendar.
            elif ascii.unctrl(cmd) == 'e':
                editEntry(item,month,year,events,calFile)
                CellList = term.renderCalendar(str(month),year)# Render the actual calendar.
            else:
                pass
            
    except KeyboardInterrupt:
        w.clear()
        w.addstr("Leaving...")
        term.leave()


# Yes, I know what you are thinking
# "Why did you remove this?"
# Well it's for presentation reasons
# but you are welcome to add the code
# back in.
def calOpenPrompt():
    calview("cal.txt",int(date.getStartingDate().split("-")[0]))
    
def main():
    try:
        clear = True
        while 1:
            if clear == True and debug < 1:
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
                    w.addstr(str(" "))
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

