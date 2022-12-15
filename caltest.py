#!/bin/python3
#
# This tests the cal module
# But it also acts a useful debugging tool
# to print out event data if it looks wrong
# on calview.py

import src.cal as cal
import src.date as date

events = cal.parse("cal.txt")

print("Getting data about events manually")
for i,x in enumerate(events):
    print("--")
    print("Id: " + str(x))
    print("Name: " + str(events[x][1]))
    print("Location: " + str(events[x][2]))
    print("Starts at: " + str(events[x][3]))
    print("Ends at:" + str(events[x][4]))
    print("Notes: " + str(events[x][5]))
    
print("--")
print("\n\n")

print("Getting data about events using the cal get functions")
for i,x in enumerate(events):
    print("--")
    print("Id: " + str(x))
    print("Name: " + cal.getName(x,events))
    print("Location: " + cal.getLocation(x,events))
    print("Starts at: " + cal.getStartDate(x,events))
    print("Ends at: " + cal.getEndDate(x,events))
    print("Notes: " + cal.getNotes(x,events))


print("--")
