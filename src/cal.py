#!/bin/python3
# © abdul karim kikar 2022
# licenseret under GNU GPL version 3 og nyere versioner.
#
# the purpose of this file is to parse calendars and provide
# easy, safe and fast functions for manipulating osocomp calendars.


calfile = ""
# This function must be ran first
# before running any other
# calendar related function
def parse(file):
    file = str(file)
    # Check if this is actual valid input
    if file == "" or file == NULL:
        return -1

