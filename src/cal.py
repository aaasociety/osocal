#!/bin/python3
# © abdul karim kikar 2022
# licenseret under GNU GPL version 3 og nyere versioner.
#
# the purpose of this file is to parse calendars and provide
# easy, safe and fast functions for manipulating osocomp calendars.
#import src.lib as lib

ERR = None
calfile = ""

# The "events" dictionary follows this format:
# Numbers/Integers: EVENT_ID
# Dates/Special data types: EVENT_STARTS, EVENT_ENDS
# Strings: NAME, LOCATION
# dict = {
#    EVENT_ID: [NAME,LOCATION,EVENT_STARTS,EVENT_ENDS]
#}
# Dates follow this format:
# YYYY-MM-DD-HH-MM
def parse(file):
    f = open("cal.txt")
    # The calendar format is thus:
    # Every event starts with { and ends with }
    lines = f.readlines()
    count = 0
    # This array contains numerous flags
    # Individual ints are too hard to keep
    # track of
    flags = [
        False, # Event flag ("{")
        False, # Quotation mark flag ("\"")
        False, # Backslash flag ("\\")
        False, # Event ID var
        0, # What thing are we currently processing variable
    ]
    events = {}
    event = [
        0,
        "",
        "",
        "",
        "",
        ""
    ]
    for line in lines:
        line = line.rstrip()
        for ch in line:
            print(ch + " || " + str(flags))
            if ch == '{' and flags[1] == False:
                flags[0] == True 
            
            if flags[0] == False:
                continue # If we haven't detected a "{" yet
                         # then it's probably worth it to skip. 

            # Check for quote character
            if ch == '"':
                # if we are currently processing a string
                # then: check if the backslash flag is enabled
                #   if the backslash flag is enabled
                #   then: add it to whatever we are parsing
                #   else: end the string and add it 
                # else: start processing a string
                if flags[1] == True:
                    if flags[2] == True:
                        # TODO: add it to whatever we are parsing
                        event[flags[4]] += ch
                        continue
                    else:
                        flags[4] += 1 
                        flags[1] == False
                        continue
                else:
                    flags[1] == True
                    continue

            # Check for backslash characters
            if "\\" in ch:
                if flags[1] == False:
                    continue
                else:
                    event[flags[4]] += ch
                    flags[2] = True

            # Check if character is number
            if ch.isdigit() == True and flags[1] == False:
                flags[3] = int(ch)
                flags[4] += 1
                continue 

            # If we have reached this point then We are probably
            # parsing a string
            if flags[1] == True:
                event[flags[4]] += ch
                continue





def dayHasEvent(day, month):
    if day % 2 == 0:
        return True
    else:
        return False


# A function extract col value from CellList
def extractCol(CellList,num = 0):
    if not isinstance(CellList,list):
        return ERR
    return int(CellList[num].split("-")[0])

# A function extract row value from CellList
def extractRow(CellList,num = 0):
    if not isinstance(CellList,list):
        return ERR
    return int(CellList[num].split("-")[1])
