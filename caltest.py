#!/bin/python3
#
# This tests the cal module
# But it also acts a useful debugging tool
# to print out event data if it looks wrong
# on calview.py

import src.cal as cal
import src.date as date

events = cal.parse("cal.txt")

for i,x in enumerate(events):
    print("--")
    print("Id: " + str(x))
    print("Name: " + cal.getName(x,events))
    print("Location: " + cal.getLocation(x,events))
    print("Starts at: " + cal.getStartDate(x,events))
    print("Ends at: " + cal.getEndDate(x,events))
    print("Notes: " + cal.getNotes(x,events))

