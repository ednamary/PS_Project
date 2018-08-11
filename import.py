import sqlite3
import xlrd
#from pathlib import Path
import work_with_database

def get_input():
    # This function requests user input of a file of upc numbers.
    # For each value, it checks if the value is already in the database.
    # If it isn't, it calls a function to add it

    inp = input('select input file: ')
    print(inp)

    try:
        data = xlrd.open_workbook(inp)
        type(data)
        excel_input(data)
    except:
        print(inp, 'is not a workbook.')
        try:
            data = open(inp, 'r')
            text_input(data)
        except:
            print(inp, 'is not a usable file.')
            return

def text_input(data):
    con = sqlite3.connect("UPCData.db")
    cur = con.cursor()

    for line in data:
        upc = line.rstrip()
        check_input(upc, con, cur)

def excel_input(wb):

    # Hardcoded assuming it begins where it does in the basic spreadsheet
    # Needs to be updated

    ws = wb.sheet_by_index(0)
    row = 1
    col = 2

    # Connect to the database and create a cursor to do operations
    # Note that this is Global so that I don't have to reopen the SS every time
    # or pass things back and forth constantly.
    con = sqlite3.connect("UPCData.db")
    cur = con.cursor()

    while ws.cell(row, col).value != xlrd.empty_cell.value:
        upc = int(ws.cell(row, col).value)
        check_input(upc, con, cur)
        row += 1

def check_input(upc, con, cur):
    print(upc)
    is_in = work_with_database.check_database(upc, con, cur)

    if is_in:
        print("UPC Number", upc, "already in database")
    else:
        work_with_database.create_input(upc, con, cur)


get_input()
