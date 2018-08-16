import sqlite3
import xlrd
import xlsxwriter
#from pathlib import Path
import work_with_database

def get_input():
    # This function requests user input of a file of upc numbers.
    # For each value, it checks if the value is already in the database.
    # If it isn't, it calls a function to add it

    # Create initial worksheet. Note that xlsxwriter requires the worksheet
    # to not exist when you run the code so another library should probably be used.
    output = xlsxwriter.Workbook('output.xlsx')
    sheet = output.add_worksheet()
    sheet.write('A1', 'Item ID')
    sheet.write('B1', 'UPC code')
    sheet.write('C1', 'Product Name')
    sheet.write('D1', 'Product Brand')
    sheet.write('E1', 'Product Description')
    sheet.write('F1', 'Weight')
    sheet.write('G1', 'Image')

    # File with initial spreadsheet, currently can take xls, xlsx, or txt
    inp = input('select input file: ')

    # if input is Excel spreadsheet, use xlrd
    if inp.lower().endswith(('.xls', '.xlsx')):
        data = xlrd.open_workbook(inp)
#        excel_input(data, output, sheet)
        excel_input(data, output, sheet)

    # Check if text list of UPCs
    elif inp.lower().endswith(('.txt', )):
        print(inp, 'is not a workbook.')
        text_input(inp, output, sheet)
    # No current plans for other extensions
    else:
        print('invalid file extension')


# The code that processes inputs that are *.txt in the format
# UPC1
# UPC2
# UPC3, etc
def text_input(inp, output, sheet):
    data = open(inp, 'r')

    # Connect to the database and create a cursor to do operations
    con = sqlite3.connect("UPCData.db")
    cur = con.cursor()

    # This is for passing to new spreadsheet, keeps track of row
    # Extremely inelegant, want to come up with better method
    row_num = 1

    # Loop over data
    for line in data:
        print(line)
        upc = line.rstrip()
        print(upc)
        # Recieve tuple to pass into new spreadsheet
        r=check_input(upc, con, cur)
        if r == 0:
            # Input is invalid for some reason, skip to next element
            # probably needs to add in some way
            continue
        # Pass to new spreadsheet
        # Item_no set to 0 because it's not included in txt inputs
        row_num = export(r, 0, output, sheet, row_num)
    close(data)
    output.close()
    return

# The code that processes these inputs
def excel_input(wb, output, sheet):

    # Hardcoded assuming it begins where it does in Product with UPC.xlsx
    # Needs to be updated
    ws = wb.sheet_by_index(1)
    row = 1
    col = 4

    # Connect to the database and create a cursor to do operations
    con = sqlite3.connect("UPCData.db")
    cur = con.cursor()

    # This is for passing to new spreadsheet, keeps track of row
    # Extremely inelegant, want to come up with better method
    row_num = 1

    print(ws.cell(row, col).value)
    # iterate through the column of UPCs
    while ws.cell(row, col).value != xlrd.empty_cell.value:
        # Get value of UPC
        upc = int(ws.cell(row, col).value.strip())

        print(upc, type(upc))
        # Go to next row of input spreadsheet
        row += 1
        # Recieve tuple to pass into new spreadsheet
        r=check_input(upc, con, cur)
        if r == 0:
            # Pass to new spreadsheet
            # Item_no set to 0 because it's not included in txt inputs
            continue
        # Pass to new spreadsheet
        # col-3 is a magic number for the item_no column of initial spreadsheet
        row_num = export(r, ws.cell(row, col-3).value, output, sheet, row_num)
    output.close()
    return 0


# Check the input and return based on result
def check_input(upc, con, cur):

    # Find out if element is already in db
    r=work_with_database.check_database(upc, con, cur)

    if r is None:
        # Is not in db, so create new input
        r=work_with_database.create_input(upc, con, cur)
    else:
        # Already in
        print("UPC Number", upc, "already in database")
    return r

# Send to database
def export(tup, item_no, output, sheet, row_num):
    # write_row requires a list, so convert tuple to list and and item_no
    li = list(tup)
    li.insert(0, item_no)

    #write row to spreadsheet
    sheet.write_row(row_num, 0, li)
    # to write in next available row
    return(row_num + 1)


get_input()
