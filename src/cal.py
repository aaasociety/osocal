#!/bin/python3
# © abdul karim kikar 2022
# licenseret under GNU GPL version 3 og nyere versioner.
#
# the purpose of this file is to parse calendars and provide
# easy, safe and fast functions for manipulating osocomp calendars.
import src.lib as lib

calfile = ""
# This function must be ran first
# before running any other
# calendar related function
def parse(file):
    file = str(file)
    # Check if this is actual valid input
    if file == "" or file == NULL:
        return -1

def dayHasEvent(day, month):
    if day % 2 == 0:
        return True
    else:
        return False


ERR = lib.ErrType
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
