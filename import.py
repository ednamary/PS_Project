import sqlite3
import xlrd
import xlsxwriter
#from pathlib import Path
import work_with_database

def get_input():
    # This function requests user input of a file of upc numbers.
    # For each value, it checks if the value is already in the database.
    # If it isn't, it calls a function to add it
    output = xlsxwriter.Workbook('output.xlsx')
    sheet = output.add_worksheet()
    sheet.write('A1', 'Item ID')
    sheet.write('B1', 'UPC code')
    sheet.write('C1', 'Product Name')
    sheet.write('D1', 'Product Brand')
    sheet.write('E1', 'Product Description')
    sheet.write('F1', 'Weight')
    sheet.write('G1', 'Image')

    inp = input('select input file: ')

    if inp.lower().endswith(('.xls', '.xlsx', '.ods')):
        data = xlrd.open_workbook(inp)
#        excel_input(data, output, sheet)
        excel_input(data, output, sheet)
    elif inp.lower().endswith(('.txt', '.csv')):
        print(inp, 'is not a workbook.')
        text_input(inp, output, sheet)
    else:
        print('invalid file extension')

def text_input(inp, output, sheet):
    data = open(inp, 'r')
    con = sqlite3.connect("UPCData.db")
    cur = con.cursor()
    row_num = 1

    for line in data:
        print(line)
        upc = line.rstrip()
        print(upc)
        r=check_input(upc, con, cur)
        if r == 0:
            continue
        row_num = export(r, 0, output, sheet, row_num)
    close(data)
    output.close()
    return 0

def excel_input(wb, output, sheet):

    # Hardcoded assuming it begins where it does in the basic spreadsheet
    # Needs to be updated
    print("test")

    ws = wb.sheet_by_index(1)
    row = 1
    col = 4

    # Connect to the database and create a cursor to do operations
    # Note that this is Global so that I don't have to reopen the SS every time
    # or pass things back and forth constantly.
    con = sqlite3.connect("UPCData.db")
    cur = con.cursor()
    row_num = 1
    print(ws.cell(row, col).value)
    while ws.cell(row, col).value != xlrd.empty_cell.value:
        upc = int(ws.cell(row, col).value.strip())
        print(upc, type(upc))
        row += 1
        print(row)
        r=check_input(upc, con, cur)
        if r == 0:
            continue
        row_num = export(r, ws.cell(row, col-3).value, output, sheet, row_num)
    output.close()
    return 0


def check_input(upc, con, cur):

    r=work_with_database.check_database(upc, con, cur)

    if r is None:
        r=work_with_database.create_input(upc, con, cur)
    else:
        print("UPC Number", upc, "already in database")
    return r

def export(tup, item_no, output, sheet, row_num):
    print(tup)
    li = list(tup)
    li.insert(0, item_no)
    print(li)
    sheet.write_row(row_num, 0, li)
    return(row_num + 1)


get_input()
