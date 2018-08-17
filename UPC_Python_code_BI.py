for line in data:
        
        sett = line.rstrip()
        #Calculating the 12th digit for each of the 11 UPC number completes the complete UPC number 
        # The 12 upc number helps to find the details of each UPC.
        #Note: the code will only calculate for 11 digit upcs otherwise the number is considered as invalid
        
        totall = 0 #total is the sum of all even number digits
        total=0 #totall is the sum of all add number digits
        if len(sett) == 11:
            for i in range(len(sett)):
                  
           #if len(sett) == 11:
                if i % 2 == 0:
                    temp = 3*(int(sett[i]))
                    totall +=temp
                else:
                    temp = int(sett[i])
                    total +=temp 
                #Sum is the sum of total and totall numbers
                Sum = totall+total 
        
            
        # n is the last digit number add to the UPC. 
            if Sum %10 > 0:
                n = 10-(Sum%10)
            else:
                n = 0
            ere = ''.join((sett, str(n)))   
            print(ere)
        elif len(sett) == 12:
            len(sett)== sett
        else:
            print("UPC number is invalid")
            continue
       
