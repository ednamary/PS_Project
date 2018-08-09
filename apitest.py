import requests
import json
import time
import sqlite3
from pathlib import Path

# This class is to have an easily portable data structure to add things to
# the database or whatever else is necessary
class datum():
    def __init__(self,  json_dict):
        # Missing is a flag to check if there is any data Missing
        # The idea is to inform the user so they can figure out what to do
        self.missing = False
        # All of these elements have checks except for upc because upc is
        # absolutely necessary; if it doesn't exist we can't write to the DB.
        # If there is no upc at this point I want to error out because something
        # very wrong has happened.
        self.upc = json_dict['items'][0]['upc']
        self.title = json_dict['items'][0]['title']
        if self.title == '':
            self.missing = True
        self.description = json_dict['items'][0]['description']
        if self.description == '':
            self.missing = True
        self.brand = json_dict['items'][0]['brand']
        if self.brand == '':
            self.missing = True
        self.weight = json_dict['items'][0]['weight']
        if self.weight == '':
            self.missing = True
        try:
            self.image = json_dict['items'][0]['images'][0]
        except:
            self.image = ''
            self.missing = True


    def __repr__(self):
        print("UPC Number", self.upc)
        print("Title", self.title)
        print("Description", self.description)
        print("Brand", self.brand)
        print("Weight", self.weight)
        print("Image URL", self.image)


def check_database(upc):
    # Check if data is already in the database
    cur.execute('SELECT UPCnum from UPC WHERE UPCnum = ?', (upc, ))
    row = cur.fetchone()

    if row is not None: # Data is already in the database, just return
        # In future this will probably pass that database element to the SS
        # or CSV or whatever
        return True
    return False

def save_to_database(new):
    # This function takes a datum element and saves it to the database.

    # Insert into the database
    cur.execute('INSERT INTO UPC (UPCnum, Title, Description, Brand, Weight, Image)'
                'VALUES (?, ?, ?, ?, ?, ?)',
                (new.upc, new.title, new.description, new.brand, new.weight, new.image)
                )
    con.commit()
    return

def find_input():
    # This function requests user input of a file of upc numbers.
    # For each value, it checks if the value is already in the database.
    # If it isn't, it calls a function to add it

    inp = Path(input('select input file: '))

    # Check if the user input is a file. Moving forward, will be expanded to
    # check if it's a file of the wrong type.
    if not inp.is_file():
        print(inp, 'is not a file.')
        return

    data = open(inp, 'r')

    # Connect to the spreadsheet and create a cursor to do operations
    # Note that this is Global so that I don't have to reopen the SS every time
    # or pass things back and forth constantly.
    global con, cur
    con = sqlite3.connect("C:\\Users\\User\\Documents\\Python Practice\\API Spreadsheet\\UPCData.db")
    cur = con.cursor()

    for line in data:
        upc = line.rstrip()
        is_in = check_database(upc)

        if is_in:
            print("UPC Number", upc, "already in database")
        else:
            create_input(upc)


def create_input(upc):
    # This function currently takes a upc number not already in the DB
    # and passes it to the upcitemdb. It creates an object from
    # the relevant data and passes it to the save_to_database function.


    # Create a new mini dictionary to use with the Requests syntax
    # To do: find out if it's possible to make one large dictionary and do
    # one large API call instead of a bunch of tiny ones
    parameters = {'upc': upc}


    while True:
        response = requests.get('https://api.upcitemdb.com/prod/trial/lookup', params=parameters)
        # Print the content of the response (the data the server returned)
        # The thing that actually gets sent is
        # https://api.upcitemdb.com/prod/trial/lookup?upc=<line>

        dat = response.json()
        # Convert to json

        if dat['code'] == 'TOO_FAST':
            # Throtted because we sent more than 6 requests per minutes
            # rerun loop iteration after waiting a minute
            time.sleep(60)
            continue
        elif dat['code'] == 'EXCEED_LIMIT':
            # Done more than 100, the limit on upcitemdb for trial version
            print('\n\n\n Reached API limit for the day')
            return
        if dat['total'] == 0:
            # Item not in Database accessed by API
            # Add to our database so we know for the future
            # We create dummy values for everything but upc itself
            dat['items'] = []
            dat['items'].append({'upc': parameters['upc'], 'title': '', 'description': '',
                                'brand': '', 'weight': '', 'images': ''})

        save_to_database(datum(dat))
        # Exit while(true) loop
        break


find_input()
