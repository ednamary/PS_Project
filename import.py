import sqlite3
import xlrd
import xlsxwriter
#from pathlib import Path
import work_with_database


# Bereket's code t ocheck for validity
def check_validity(upc):
    upc = str(upc)
    # Return 12 digit UPC number
    if len(upc) == 12:
        return upc
    elif len(upc) == 11:
        # Convert 11 digit UPC to 12 digit and return that
        sum = 0
        for i in range(upc):
                if i % 2 == 0:
                    temp = 3*(int(sett[i]))
                    sum +=temp
                else:
                    temp = int(sett[i])
                    sum +=temp
        if Sum %10 > 0:
            n = 10-(Sum%10)
        else:
            n = 0
        ere = ''.join((sett, str(n)))
        return ere
    # Return 0 if not 11 or 12 digit UPC
    else:
        return 0

def get_input():
    # This function requests user input of a file of upc numbers.
    # For each value, it checks if the value is already in the database.
    # If it isn't, it calls a function to add it

    # File with initial spreadsheet, currently can take xls, xlsx, or txt
    inp = input('select input file: ')

    # if input is Excel spreadsheet, use xlrd
    if inp.lower().endswith(('.xls', '.xlsx')):
        data = xlrd.open_workbook(inp)
#        excel_input(data, output, sheet)
        excel_input(data)

    # Check if text list of UPCs
    elif inp.lower().endswith(('.txt', )):
        print(inp, 'is not a workbook.')
        text_input(inp)
    # No current plans for other extensions
    else:
        print('invalid file extension')


# The code that processes inputs that are *.txt in the format
# UPC1
# UPC2
# UPC3, etc
def text_input(inp):
    rate_limit = False
    data = open(inp, 'r')

    # Connect to the database and create a cursor to do operations
    con = sqlite3.connect("UPCData.db")
    cur = con.cursor()

    to_export = []

    # Loop over data
    for line in data:
        upc = line.rstrip()
        check = check_validity(upc)
        if len(str(check)) == 12:
            upc = check
        else:
            temp = [0, upc]
            to_export.append(temp)
            continue
        # Recieve tuple to pass into new spreadsheet
        # If r is an int instead then passing status
        r=check_input(upc, con, cur, rate_limit)
        if r == 1:
            # r = 1 when rate limited
            rate_limit = True
            continue
        try:
            # Try to insert r's tuple
            temp = list(r)
            temp.insert(0, 0)
            to_export.append(temp)
        except:
            pass
    close(data)
    export(to_export)
    return

# The code that processes these inputs
def excel_input(wb):

    # Hardcoded assuming it begins where it does in Product with UPC.xlsx
    # Needs to be updated
    ws = wb.sheet_by_index(0)
    row = 0
    col = 0
    item_found = False
    upc_found = False
    rate_limit = False

    while ws.cell(row, col).value != xlrd.empty_cell.value:
        v = str(ws.cell(row, col).value.strip())
        if v.lower().startswith('upc'):
            if upc_found == True:
                # Add something else here in future
                print("Two columns of UPCs found in Spreadsheet")
            upc_col = col
            upc_found = True
        elif v.lower().startswith('item'):
            if item_found == True:
                print("Two item number columns found in spreadsheet")
            item_col = col
            item_found = True

        if item_found and upc_found:
            break
        col+=1
    if not upc_found:
        print("No UPC column")
        return
    row = 1
    # Connect to the database and create a cursor to do operations
    con = sqlite3.connect("UPCData.db")
    cur = con.cursor()

    # This is for passing to new spreadsheet, keeps track of row
    # Extremely inelegant, want to come up with better method
    to_export = []

    # iterate through the column of UPCs
    while ws.cell(row, upc_col).value != xlrd.empty_cell.value:
        # Get value of UPC
        upc = int(ws.cell(row, upc_col).value.strip())

        check = check_validity(upc)
        if len(str(check)) == 12:
            upc = check
        else:
            temp = [0, upc]
            to_export.append(temp)
            continue
        # Go to next row of input spreadsheet
        row += 1
        # Recieve tuple to pass into new spreadsheet
        r=check_input(upc, con, cur, rate_limit)
        # Pass to new spreadsheet
        # col-3 is a magic number for the item_no column of initial spreadsheet
        if item_found == False:
            item_no = 0
        if r == 1:
            rate_limit = True
            temp = [item_no, upc]
            to_export.append(temp)
            continue
        if r == 0:
            # Pass to new spreadsheet
            # Item_no set to 0 because it's not included in txt inputs
            temp = [item_no, upc]
            to_export.append(temp)
            continue

        # IF r is just a return code
        try:
            temp = list(r)
            temp.insert(0, item_no)
            to_export.append(temp)
        except:
            pass

    export(to_export)
    return


# Check the input and return based on result
def check_input(upc, con, cur, rate_limit):

    # Find out if element is already in db
    r=work_with_database.check_database(upc, con, cur)

    if r is not None:
        # Is not in db, so create new input
        print("UPC Number", upc, "already in database")
    elif rate_limit == False:
        r=work_with_database.create_input(upc, con, cur)
    else:
        r = 0
        print("new element but rate capped")
        # Already in

    return r

# Send to database
def export(upcs):
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
    line = 1
    for upc in upcs:
        #write row to spreadsheet
        sheet.write_row(line, 0, li)
        line += 1
        # to write in next available row
    output.close()
    return


get_input()
