#!/bin/python3
# © abdul karim kikar 2022
# licenseret under GNU GPL version 3 og nyere versioner.

import sys,curses
import curses.ascii as ascii
w = curses.initscr()
w.keypad(True)

helpArray=["osocomp -- Abdul's tredje OSO produkt\n","\n\tHvad er dette?","\nDet her er abdul\'s tredje OSO produkt. Det er en kalendar program som","\ntjekker ens kalendar og beregner vejret når man skal udenfor, så hvis","\nman skal til en fest så beregner den vejret for når man tager til feste","\nog indtil man gårer hjem. Den siger så om hvis man skal tage jakke på","\neller andre tøje på.","\n","\n\tHvorfor er denne program tekst-baseret?","\nDet er umuligt at lave en kalendar program med alt disse funktioner på","\net uge når man arbejder med grafisk programmer. Også det er vigtigt","\nat denne program burde virke på alle systemer, forskellige systemer","\nhar forskellige \"grafisk værktøjsset\" (De programmer som gører det","\nmuligt for programmer til at lave grafiske vinduer), Windows har deres","\negen som kaldes for \"WinUI\", MacOS har \"UIKit\", HaikuOS har","\n\"Interface Kit\", og Linux har \"xlib\" men de fleste bruger \"GTK\"","\neller \"Qt\". Det er ikke umuligt at lave en grafiske program som","\nvirker på alle disse systemer men det er virkelig svært og det tager","\nmere end en uge.","\n","\n\tHvem har skrevet denne program?","\nDet har Abdul Karim Kikar, jeg begyndte at skrive denne program I","\nDecember 2022, Lidt tidligere før OSO ugen fordi jeg vidste at det vil","\nvære lidt svær at lave 3 produkter på kun et uge og gører alt de andre","\nting (Fremlæggelse, interview etc.) Også denne program er licenseret","\nunder GNU GPL version 3 eller nyere versioner. Du kan få kildekoden","\nved at spørge Abdul selv."]


debug=True

def leave():
    curses.echo()
    w.keypad(False)
    curses.nocbreak()
    curses.endwin()
    sys.exit(1)

cal = ""

row = 5
col = 5

def continueArray(arr):
    for i,x in enumerate(arr):
        try:
            w.addstr(x)
        except curses.error:
            return i

def helpPrompt():
    w.clear()
    w.refresh()
    y = 0
    erri = 0
    for i,prompt in enumerate(helpArray):
        try:
            w.addstr(prompt)
        except curses.error:
            erri = i
# 25
    while True:                
        cmd = w.getch()
        if cmd == curses.KEY_DOWN or cmd == 258: # Down arrow key
            w.clear()
            if erri - 1 < 0:
                y = erri
            else:
                y = len(helpArray) - erri + 1
            for num in range(y,len(helpArray)):
                text = helpArray[num]
                if num == y:
                    text = text[1:]
                w.addstr(text)
            w.addstr("\n: ")
        if cmd == curses.KEY_UP or cmd == 259: # Up arrow key
            if y == 0:
                pass
            else:
                w.clear()
                if y - 1 > len(helpArray):
                    pass
                else:
                    y = y - 1
                    for num in range(y,len(helpArray)):
                        text = helpArray[num]
                        if num == y:
                            text = text[1:]
                        try:
                            w.addstr(text)
                        except curses.error:
                            pass
        if cmd == curses.KEY_ENTER or cmd == 10:
            w.clear()
            main()


def calOpenPrompt():
    try:
        curses.cbreak()
        w.refresh()
        w.keypad(True)
        assembledstring = ""
        curses.noecho()
        while True:
            w.clear()
            w.addstr("Specify which calendar file you want open")
            w.addstr("\nOr press Enter for the default (cal.txt)")
            w.addstr("\nOr type \"quit\" to quit!")
            w.addstr("\n> " + assembledstring)
            w.refresh()
            cmd = w.getch()
            if cmd == curses.KEY_ENTER or cmd == 10: # Enter
                break
            elif cmd == curses.KEY_BACKSPACE or cmd == 127: # Backspace
                l = len(assembledstring)
                assembledstring = assembledstring[:l-1]
            else:
                # Here we convert the int provided by
                # getch() and add it assembledstring.
                # Enter is not properly parsed.
                if len(ascii.unctrl(cmd)) > 1:
                    continue # Other invalid key detected
                assembledstring += ascii.unctrl(cmd)

        w.addstr("\n")
        if assembledstring == "quit":
            w.addstr("Aborting...")
            leave()
            
    except KeyboardInterrupt:
        w.addstr("\nAborting...\n")
        leave()
        sys.exit(1)
    

def main():
    try:
        clear = True
        while 1:
            if clear == True and debug == False:
                w.clear()
            if cal == "":
                w.addstr("\n- - - - - - - -")
                w.addstr("\nNo calendar file open")
                w.addstr("\nPress \"o\" and specify")
                w.addstr("\nWhich file to open")
                w.addstr("\n- - - - - - - -\n")
            w.addstr("Type ? for help\n")    
            w.refresh()
            w.addstr("> ")
            cmd = w.getch()
            # Clear "clear" var if it is set
            if clear == False:
                clear = True
            w.addstr("\n");
            truecmd = ascii.unctrl(cmd).lower()
            if truecmd == 'q':
                leave()
            elif truecmd == 'o':
                calOpenPrompt()
            elif truecmd == '?':
                helpPrompt()
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
        leave()
        sys.exit(1)

if __name__ == "__main__":
    main()
#    curses.wrapper(calOpenPrompt)
    
else:
    print("Do not import this program")
    sys.exit(1)

