import sqlite3
inp = input('select input file: ')
inp=open(inp, "r")
#foo = fun.rstrip()
#sett = foo.readlines()

for line in inp:
    sett = line.rstrip()
    
    
#sett= '07341640153'
#ele = int(sett)
    totall = 0
    total=0
    for i in range(len(sett)):
        if len(sett) == 11:
            
            if i % 2 == 0:
                temp = 3*(int(sett[i]))
                totall +=temp
            else:
                temp = int(sett[i])
                total +=temp
            Sum = totall+total
        else:
            print("UPC number is invalid")
        

        if Sum %10 > 0:
            n = 10-(Sum%10)
        else:
            n = 0
        ere = ''.join((sett, str(n)))   
        print(ere)
        
        
        conn = sqlite3.connect('bere_DB.db')



        try:
            conn.execute('''CREATE TABLE bereket
                   (UPC_s INTEGER NOT NULL)''')
                    #conn = sqlite3.connect("test.db")
            cur = conn.cursor()
            conn.execute("INSERT INTO bereket (UPC_ss) \
                      VALUES (?)", [ere])
            conn.commit()
            conn.close();
        except:
            pass
