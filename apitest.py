
rrrrr


import requests
import json
import time
import sqlite3
from pathlib import Path

class datum():
    def __init__(self,  json_dict):
        self.missing = False
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


# FILE TO INPUT: C:\\Users\\User\\Desktop\\upc_test2.txt

def save_to_database(new):

    # Check if data already in
    cur.execute('SELECT UPCnum from UPC WHERE UPCnum = ?', (new.upc, ))
    row = cur.fetchone()

    if row is not None: # Data is already in the database
        print("UPC Number", new.upc, "already in database")
        return

    if new.missing == True: # There is missing information
        print("Missing information from UPC", new.upc + ".")

    cur.execute('INSERT INTO UPC (UPCnum, Title, Description, Brand, Weight, Image)'
                'VALUES (?, ?, ?, ?, ?, ?)',
                (new.upc, new.title, new.description, new.brand, new.weight, new.image)
                )
    con.commit()
    return

def create_input():
    inp = Path(input('select input file: '))

#    f = open(inp, 'r')
#    print(f)
    if not inp.is_file():
        print(inp, 'is not a file.')
        return

    prev = 'C:\\Users\\User\\Desktop\\database.txt'
    prev = open(prev, 'a')

    data = open(inp, 'r')
    global con, cur
    con = sqlite3.connect("C:\\Users\\User\\Documents\\Python Practice\\API Spreadsheet\\UPCData.db")
    cur = con.cursor()

    for line in data:
        parameters = {'upc': line.rstrip()}

        while True:
            response = requests.get('https://api.upcitemdb.com/prod/trial/lookup', params=parameters)
            # Print the content of the response (the data the server returned)
            dat = response.json()
#            print(response)
            print(dat)
#            print(dat['code'])

            if dat['code'] == 'TOO_FAST': # rerun loop iteration
                time.sleep(60)
                continue
            elif dat['code'] == 'EXCEED_LIMIT': # Done more than 100
                print('\n\n\n Reached API limit for the day')
                return
            if dat['total'] == 0:
                # Item not in Database accessed by API
                # Add to database so we know for the future
                # Also warn user
                dat['items'] = []
                dat['items'].append({'upc': parameters['upc'], 'title': '', 'description': '',
                                    'brand': '', 'weight': '', 'images': ''})

            save_to_database(datum(dat))
#            try:
#                prev.write('upc: ' + line + '\ntitle: ' + dat['items'][0]['title'] + '\ndescription: '
#                + dat['items'][0]['description'] + '\nbrand: '
#                + dat['items'][0]['brand'] + '\nweight: ' + dat['items'][0]['weight']
#                + '\nImage URL: ' + dat['items'][0]['images'][0])
#            except:
#                print("Problem with UPC Number ", line)

            break


        #print(dat['items'][0]['title'], dat['items'][0]['description'], dat['items'][0]['brand'], dat['items'][0]['weight'])
#        print(dat)
#        print(dat['X-RateLimit-Remaining'])

create_input()

#parameters = {'upc': '0012511405007'}

#response = requests.get('https://api.upcitemdb.com/prod/trial/lookup', params=parameters)

        # Print the content of the response (the data the server returned)
#data = response.json()

#print(data['items'][0]['title'], '\n', data['items'][0]['description'], '\n', data['items'][0]['brand'], '\n', data['items'][0]['weight'], '\n\n\n')
#print(response.url)
