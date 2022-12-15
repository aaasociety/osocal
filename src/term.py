#!/bin/python3
# term.py handles some terminal handling
# It mostly wraps around the curses module.
# This helps keep the codebase for the main
# app clean.

import sys,curses
import curses.ascii as ascii # For decoding things returned by curses
import src.lib as lib # Shared values across the app.
import src.date as date # For date parsing.
import src.cal as cal # For parsing the calendar.
import src.win as win


# An Internal function
# for checking if a
# prompt suits print()
# Mostly for future-proofing.
def isPrintable(prompt):
    # Check if the prompt given is valid for term.print()
    if prompt is None or not isinstance(prompt,list) or not isinstance(prompt,str):
        return False
    else:
        return True

w = win.w
row = lib.row
ERR = lib.ErrType
def leave():
    curses.echo()
    w.keypad(False)
    curses.nocbreak()
    curses.endwin()
    sys.exit(1)

# Print function with the
# ability to print entire
# arrays.
#
# The brute function tells the function to
# try and forcefully print, discarding any other
# text or messages.
def print(prompt,brute = False):
    if prompt is None:
        return ERR
    if isinstance(prompt,list):
        for i,msg in enumerate(prompt):
            try:
                w.addstr(msg)
            except curses.error:
                if brute == False:
                    pass
                else:
                    w.clear()
                    w.addstr(msg)
    else:
        w.addstr(str(prompt))
    
# A more readable function to compare
# if a getch() output is a key or a num
def compKey(cmd,key,seckey = None):
    if cmd == key or cmd == seckey:
        return True
    else:
        return False

def scrollablePrompt(promptarray):
    # Here is how this works:
    # We separate each line into an array so we can print the lines
    # we can and try to scroll with the lines we can't print.
    
    # Check if w is invalid
    if w is None or row is None:
        return ERR

    # Check if given array is bad
    if isinstance(promptarray,list) == False:
        return ERR

    # Clear up terminal & old stuff
    w.clear()
    w.refresh()
    
    y = 0 # int variable for storing the "minimum" point in the range that to print
    erri = 0 # int variable to store which line we fail at in the array
    mnum = 0 # int variable to store the number in ranges.
    
    # Now we enumerate promptarray and see
    # what lines we can print, the moment
    # we fail, we enter a condition where
    # you can scroll.
    for i,prompt in enumerate(promptarray):
        try:
            w.addstr(prompt)
        except curses.error:
            erri = i

    # Now we enter a Read-Eval-Print loop
    # Except we read user input
    # Evaluate scroll keys
    # Print the scrolled content
    while True:
        w.refresh()
        cmd = w.getch()
        if compKey(cmd,curses.KEY_DOWN,258): # If user presses Down arrow key
            if erri == 0:
                continue # Skip if user doesn't need to scroll down.
            
            w.clear() # Clear terminal
            
            # Check if we can scroll or if we can't
            if erri - 1 < 0 and erri + 1 > len(promptarray):
                y = erri
            else:
                y = erri - 10

            # Now we print whatever we can scroll
            for num in range(y,len(promptarray)):
                text = promptarray[num]
                # Remove linebreak if its the first
                # line
                if num == y:
                    text = text[1:]
                w.addstr(text)
                mnum = num
            w.addstr("\n: ")
        elif compKey(cmd,curses.KEY_UP,259): # If user presses Up arrow key
            # Don't scroll up if user did not scroll down or even scroll before
            if y == 0:
                continue

            # Here we check if we can scroll up
            # This might cause a weird, rare race
            # condition where if you scroll too much
            # down then you cannot go back up.
            # But that should not happen in the first
            # place.
            if y - 1 > len(promptarray):
                continue
            else:
                y = y - 1

            
            w.clear() # Clear the terminal in preparation of whats coming.
            
            # Same exact thing, except we wont
            # show a pretty little shell for user
            # input.
            for num in range(y,len(promptarray)):
                text = promptarray[num]
                # Remove \n character if its
                # the first line
                if num == y:
                    text = text[1:]                
                try:
                    w.addstr(text)
                except curses.error:
                    pass # Not sure why but scrolling up is quite buggy,
                         # So here we add a bit of code that catches any
                         # errors and ignores them.
        elif compKey(cmd,curses.KEY_ENTER,10): # If user presses enter
            w.clear()                          # then break and go back.
            return 1
        else:  
            w.clear() # If user presses any other key
            return 1  # then break and go back
            
        
def editablePrompt(prompt, userprompt = "\n> ", backspace = True):
    # Check if the prompt given is valid for term.print()
    if isPrintable(prompt) == False:
        return ERR

    if isPrintable(userprompt) == False:
        return ERR
    
    curses.cbreak() # We will handle special keys ourselves.
    w.keypad(True) # We want to handle pure curses keycodes.
    assembledstring = "" # A variable to store the finished string
    curses.noecho() # We will handle echoing characters ourselves.
    while True:
        w.clear()
        term.print(prompt,False) # Print a prompt if it exists
        term.print(userprompt + assembledstring,False)
        w.refresh()

        # Now we actually handle user input
        cmd = w.getch()
        if compKey(cmd,curses.KEY_ENTER,10): # If user presses Enter
            break
        if compKey(cmd,curses.KEY_BACKSPACE,127): # If user presses Backspace
            if backspace == True:
                l = len(assembledstring) # Get length of assembledstring to-
                assembledstring = assembledstring[:l-1] # Remove last letter
            else:
                continue # Skip if backspace feature is disabled
        else:
            
            # Here we convert the int provided by
            # getch() and add it assembledstring.
            # Enter is not properly parsed.
            if len(ascii.unctrl(cmd)) > 1:
                continue # Other invalid key detected.
            
            assembledstring += ascii.unctrl(cmd) # The key is completely valid
                                                 # So add it into the string.

    return assembledstring # Return the string.

# A Yes or no prompt
def ynPrompt(prompt,inputprompt = "[Y/n]:"):
    # Check if the prompt given is valid for term.print()
    if isPrintable(prompt) == False:
        return ERR

    if isPrintable(inputprompt):
        return ERR

    term.print(prompt) # Print the prompt
    term.print(inputprompt) # Print the little input prompt
    char = w.getch()
    
    if ascii.unctrl(char).lower() == "y":
        return True
    else:
        return False

# A function for rendering the calendar
def renderCalendar(month,year):
    w.clear()
    w.refresh()
    # This array stores the "col" and "row" value of each cell so it
    # can be browsed later on in the program.
    CellList = []
    row = 1 # Skip one line for displaying the year.
    col = 0 
    w.addstr("\t" + date.getMonth(month) + " " + str(year) + "\n")
    for x in range(1,date.getDays(month,year) + 1):
        # Make all of the cell numbers look uniform
        # By adding a "0" to the numbers below 10
        # so fx. 1 will look like [01]
        if x < 10:
            y = str("0" + str(x))
        else:
            y = x

        # cal.dayHasEvent() has not been implemented yet
        # But this allows me to render asterisks and test
        # it all out
        if cal.dayHasEvent(x,month,year,lib.events):
            tmp = 6
            z = "]*"
        else:
            tmp = 5
            z = "]"

        # Print the actual cell and store the value of row and col
        # on CellList which will be returned back to the process
        try:
            w.addstr(row, col, "[" + str(y) + str(z))
            CellList.append(str(col) + "-" + str(row))
        except curses.error:
            row += 1
            col = 0

        # Add the neccessary amount of characters to skip over.
        col += tmp

        # If col has reached its limit then we move on to the next line
        if col > lib.collimit * 2:
            row += 1
            col = 0
            
    # We are all done
    # Return CellList
    return CellList
    
if __name__ == "__main__":
    sys.exit(1) # This program is not intended to be run directly.


# And we all *shut* down...
