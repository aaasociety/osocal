#!/bin/python3
# © abdul karim kikar 2022
# licenseret under GNU GPL version 3 og nyere versioner.
#
# the purpose of this file is to parse calendars and provide
# easy, safe and fast functions for manipulating osocomp calendars.
import src.lib as lib
import os as os
ERR = lib.ErrType
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
    countlines = 0
    # This array contains numerous flags
    # Individual ints are too hard to keep
    # track of
    flags = [
        False, # Event flag ("{"), This triggers if the code detects "{" or "}" (The event start and stop symbols)
        False, # Quotation mark flag ("\""), this triggers if the code detects a quotation mark (Double quotes)
        False, # Backslash flag ("\\"), this triggers if the code detects a backslash.
        False, # Event ID var, this stores the event id
        0, # An integer to store what string we are currently processing.
        False, # Previous number flag, this is used to check if there are double digit or triple digit numbers. It increases by one when it finds a number so we can use it a context clue to how many events exist.
    ]
    events = {}
    event = [
        0,  # Event id
        "", # Name of event
        "", # Location of event
        "", # Start date (YYYY-MM-DD-HH-MM)
        "", # End date (YYYY-MM-DD-HH-MM)
        ""  # Notes
    ]
    for line in lines:
        countlines += 1
        line = line.rstrip()
        for ch in line:
            count += 1
            if flags[4] > 7:
                flags[4] = 0
            # Here we detect if we found a open event symbol
            # And we then tell the program that we are in
            # an event so it can finish it when it detects a closing.
            if ch == '{' and flags[1] == False:
                flags[0] = True 
            
            if flags[0] == False:
                continue # If we haven't detected a "{" yet
                         # then it's probably worth it to skip. 

            # If we detect a closing
            # Then we first make sure this isn't a part
            # of the string and then we clear up everything
            # And add the "event" array to the events dict.
            if ch == '}' and flags[1] == False:
                if flags[0] == False:
                    # Somehow we have entered a condition in which
                    # We have detected a closing before an opening
                    # So we skip the character and pray to god
                    # everything is fine.
                    continue
                
                flags[0] = False # Set event flag to False so that the above code
                                 # can process it if there are even more events.
                                
                events[flags[3]] = event # Add the event array to the events dict
                
                # Clear out the event id
                flags[3] = False
                # Then clear out the actual event array.
                event = [
                    0,
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
                continue
                    
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
                        event[flags[4]] += ch
                        continue
                    else:
                        flags[4] += 1 
                        flags[1] = False
                        continue
                else:
                    flags[1] = True
                    continue

            # Check for backslash characters
            if "\\" in ch:
                if flags[1] == False:
                    continue
                else:
                    event[flags[4]] += ch
                    flags[2] = True

            # Check if the event id had finished processing
            if ch == ',' and flags[3] == False:
                # Set the "event id" flag to the event id we have processed now
                event[0]  = int(event[0])
                flags[3] = int(event[0])
                
                # Increase "Current processing" flag by one to let
                # the program know we are done
                flags[4] = 1
                continue
                    
            # Check if character is number
            if ch.isdigit() == True and flags[1] == False:
                # Check if the event id is set.
                if flags[3] == False:
                    # Add the event id to the array as a string so we can check if a comma exists later.
                    if event[0] == 0:
                        event[0] = str(ch)
                    else:
                        event[0] += str(ch)
                continue 

            # If we have reached this point then We are probably
            # parsing a string, so check and if we are then
            # add it to whatever we are parsing currently.
            if flags[1] == True:
                event[flags[4]] += ch
                continue

    # Set global events list to the now-decoded events list
    lib.events = events
    # Return the events list
    return events


# A funcion to check if a specific day has any events
def dayHasEvent(day, month, year = lib.year, events = lib.events):
    for i,x in enumerate(events):
        eventyear = str(events[x][3]).split("-")[0]  #*2022*-12-19-15-00
        eventmonth = str(events[x][3]).split("-")[1] # 2022-*12*19-15-00 
        eventday  =  str(events[x][3]).split("-")[2] # 2022-12-*19*15-00
        
        if lib.debug == True:
            os.system(str("echo \"\n--\neventday:" + str(eventday) + "\nday: " + str(day) + "\neventmonth: " + str(eventmonth) + "\nmonth: " + str(month) + "\neventyear: " + str(eventyear) + "\nyear: " + str(year) + "\" >> logit.txt"))
        # Now we compare it to the day and month provided by the process
        # calling. Yes this is slow but it's the only approach I can think off.
        if str(year) == eventyear and str(month) == eventmonth and str(day) == eventday:
            if lib.debug == True:
                os.system("echo \"Result: true\" >> logit.txt")
            return True
        else:
            if lib.debug == True:
                os.system("echo \"Result: false\" >> logit.txt")
        
    # Nothing returned true, return false.
    return False


# A function to get the name of an event
# from its event id.
def getName(id,events):
    # Return the int of id just in case
    id = int(id)

    # Check if events is a valid dictionary
    if not isinstance(events,dict):
        return ERR
    
    # Return false because we know the id is not the events dict
    if not id in events:
        return False

    # Return the name
    return events[id][1]

# A function get the location of an event
# from its id
def getLocation(id,events):
    # Return the int of id just in case
    id = int(id)

    # Check if events is a valid dictionary
    if not isinstance(events,dict):
        return ERR
    
    # Return false because we know the id is not the events dict
    if not id in events:
        return False

    # Return the location
    return events[id][2]

# A function to get the starting date of an event
# from its id
def getStartDate(id,events):
    # Return the int of id just in case
    id = int(id)

    # Check if events is a valid dictionary
    if not isinstance(events,dict):
        return ERR
    
    # Return false because we know the id is not the events dict
    if not id in events:
        return False
    
    # Return the start date
    return events[id][3]

# A function to get the ending date of an event
# from its id
def getEndDate(id,events):
    # Return the int of id just in case
    id = int(id)

    # Check if events is a valid dictionary
    if not isinstance(events,dict):
        return ERR
    
    # Return false because we know the id is not the events dict
    if not id in events:
        return False

    # Return the end date
    return events[id][4]

# A function to get notes and other info from an event
# using its id.
def getNotes(id,events):
    # Return the int of id just in case
    id = int(id)

    # Check if events is a valid dictionary
    if not isinstance(events,dict):
        return ERR
    
    # Return false because we know the id is not the events dict
    if not id in events:
        return False

    # Return the notes
    return events[id][5]

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
