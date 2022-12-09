#!/bin/python3
# A library for handling dates
# To be used in cal.py, term.py
# and maybe cell.py
import src.lib as lib
import datetime

# To see if a year is a leap year We do the following:
# 1. If year is divisible by 400 then it's a leap year.
# 2. If year is divisible by 100 then it's a non-leap year.
# 3. If year is divisible by 4 then it's a leap year.
# 3.1. else it's a non-leap year.
# This was taken from Wikipedia's leap year algorithm but
# it was modified to work in Python and to be a bit better.
def isLeapYear(year):
    year = int(year)
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False
        
# Returns the precise number of days
# in a month. monthNum is just the number
# of the month, 1 is January, 12 is December!
# We could instead move this whole function
# to an array of numbers but that would not
# account for leap years.

# Also use lib.year if no year is provided.
def getDays(monthNum, year = lib.year):
    year = int(year)
    monthNum = int(monthNum)
    if isLeapYear(year) == True:
        febDays = 29
    else:
        febDays = 28
    days = {
        1: 31, # January
        2: febDays, # February
        3: 31, # March
        4: 30, # April
        5: 31, # May
        6: 30, # June
        7: 31, # July
        8: 31, # August
        9: 30, # September
        10: 31, # October
        11: 30, # November
        12: 31 # December
    }
    return days.get(monthNum)

def getMonth(monthNum):
    monthNum = int(monthNum)
    months = {
        1: "Januar",
        2: "Februar",
        3: "Marts",
        4: "April",
        5: "Maj",
        6: "Juni",
        7: "Juli",
        8: "August",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "December"
    }
    return months.get(monthNum) 

def getStartingDate():
    curtime = datetime.datetime.now()
    month = curtime.month
    year = curtime.year
    return str(month) + "-" + str(year)

if __name__ == "__main__":
    sys.exit(1) # Not intended to be ran directly.
