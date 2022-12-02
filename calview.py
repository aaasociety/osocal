#!/bin/python3

import sys,curses
w = curses.initscr()
w.keypad(True)

def leave():
    curses.echo()
    w.keypad(False)
    curses.nocbreak()
    curses.endwin()
    sys.exit(1)

def main():
    try:
        w.clear()
        w.addstr("? for help\n")
        w.refresh()
        while 1:
            w.addstr("> ")
            cmd = w.getch()
            w.addstr("\n");
            if cmd == 113:
                leave()
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
