#!/bin/python3
import sys,curses
import curses.ascii as ascii
import src.lib as lib

w = lib.w
row = lib.row
ERR = lib.ErrType
# Print function with the
# ability to print entire
# arrays.
#
# The brute function tells the function to
# try and forcefully print, discarding any other
# text or messages.
def leave():
    curses.echo()
    w.keypad(False)
    curses.nocbreak()
    curses.endwin()
    sys.exit(1)


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
    if prompt is None or not isinstance(prompt,list) or not isinstance(prompt,str):
        return -1

    if prompt is None or not isinstance(userprompt,list) or not isinstance(userprompt,str):
        return -1
    
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

if __name__ == "__main__":
    sys.exit(1) # This program is not intended to be run directly.
