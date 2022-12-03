t#!/bin/python3

import sys,curses
w = curses.initscr()
w.keypad(True)

debug=True

def leave():
    curses.echo()
    w.keypad(False)
    curses.nocbreak()
    curses.endwin()
    sys.exit(1)

cal = ""

def calOpenPrompt():
    try:
        w.clear()
        w.addstr("Specify which calendar file you want open")
        w.addstr("\nOr press Enter for the default (cal.txt)")
        w.refresh()
        w.keypad(False)
        while 1:
            w.addstr("\n> ")
            cmd = w.getstr()
            if debug == True:
                print(str(str(cmd) + "\n"))
            if cmd == "quit":
                leave()
            
    except KeyboardInterrupt:
        w.addstr("\nAborting...\n")
        leave()
        sys.exit(1)
    

def main():
    try:
        w.clear()
        # Calendar view mechanism
        if cal == "":
            w.addstr("\n- - - - - - - -")
            w.addstr("\nNo calendar file open")
            w.addstr("\nPress \"o\" and specify")
            w.addstr("\nWhich file to open")
            w.addstr("\n- - - - - - - -\n")
        w.addstr("Type ? for help\n")    
        w.refresh()
        while 1:
            w.addstr("> ")
            cmd = w.getch()
            if debug == True:
                w.addstr(str("\n" + str(cmd)))
            w.addstr("\n");
            if cmd == 113:
                leave()
            if cmd == 111:
                calOpenPrompt()
            w.refresh()            
        
    except KeyboardInterrupt:
        w.addstr("\nAborting...\n")
        leave()
        sys.exit(1)

if __name__ == "__main__":
    main()
    
else:
    print("Do not import this program")
    sys.exit(1)
