import requests
import json
import time
import sqlite3
import xlrd
from pathlib import Path
from apitest import check_database, create_input

def read_spreadsheet_input():
    # This function requests user input of a file of upc numbers.
    # For each value, it checks if the value is already in the database.
    # If it isn't, it calls a function to add it

#    inp = Path(input('select input file: '))

    # Check if the user input is a file. Moving forward, will be expanded to
    # check if it's a file of the wrong type.
#    if not inp.is_file():
#        print(inp, 'is not a file.')
#        return

    #data = open(inp, 'r')

    try:
        wb = xlrd.open_workbook('Sample List and Format.xlsx')
#        wb = xlrd.open_workbook(inp)
    except:
        print(inp, 'is not a workbook.')
        return


    ws = wb.sheet_by_index(0)
    row = 1
    col = 2


    # Connect to the database and create a cursor to do operations
    # Note that this is Global so that I don't have to reopen the SS every time
    # or pass things back and forth constantly.
    global con, cur
    con = sqlite3.connect("UPCData.db")
    cur = con.cursor()

    while ws.cell(row, col).value != xlrd.empty_cell.value:
        upc = int(ws.cell(row, col).value)
        print(upc)
        is_in = check_database(upc)

        if is_in:
            print("UPC Number", upc, "already in database")
        else:
            create_input(upc)
        row += 1

read_spreadsheet_input()
