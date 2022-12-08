#!/bin/python3
# A library for handling dates
# To be used in cal.py, term.py
# and maybe cell.py

# To see if a year is a leap year We do the following:
# 1. If year is divisible by 400 then it's a leap year.
# 2. If year is divisible by 100 then it's a non-leap year.
# 3. If year is divisible by 4 then it's a leap year.
# 3.1. else it's a non-leap year.
# This was taken from Wikipedia's leap year algorithm but
# it was modified to work in Python and to be a bit better.
def isLeapYear(year):
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
def getDaysInMonth(monthNum, year = lib.year):
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

if ___name__ == "__main__":
    sys.exit(1) # Not intended to be ran directly.
