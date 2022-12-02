# Terminal handling
# This is a cross-platform API/library
# for rendering stuff for osocomp.

# A pseudo-function for
# initializing term.py
import sys,os

# For concurrency
from threading import Thread
printables = [""]

# Mode 0 means continue as is, keep clearing and printing
# Mode 1 means stop. This could be for processing input or the like
# Mode 2 means break. Maybe the user is leaving.
mode = 0

# Here we enter a 0.01 loop
# and print everything in printables
def loop():
    while 1:
        print(str(mode))
        print(str(printables))
#        clear()
        if mode == 1:
            continue
        if mode == 2:
            break

        for x in printables:
            print(x)

p = Thread(target=loop)
            
def init():
    p.start()
    
def refresh():
    clear()

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    return 0;

def print(text,attr = "",breakline = True):
    extra = ""
    if breakline == True:
        extra += "\n"
    printables.append(str(text + extra))
    return 0;

def setmode(newmode):
    if int(newmode) > 1:
        return 1;
    else:
        mode = int(newmode)

def destroy():
    p.join()
    setmode(2)
    mode = 2
    p.terminate()
    return 0;

def debug():
    return str(mode + "\n" + printables)
