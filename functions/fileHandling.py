import urllib.request
import json
import csv
import os

import datetime
#
#
#
def csvParsing(filename,cols):

    data = {}
    for col in cols:
        data[col] = []
    
    with open(filename) as f:
        csv_read = csv.reader(f,delimiter=',')        
        col_head = True
        
        for rows in csv_read:
            if col_head:
                col_head = False                
            else:
                for i in range(0,len(cols)):
                    try:
                        if (rows[i].isnumeric()):
                            data[cols[i]].append(int(rows[i]))
                        else:
                            data[cols[i]].append(rows[i])
                    except:
                        print(rows)
                        pass
        return data 
                            
            
#
# fileretrieval function
#
def fileretrieval(file,url,expectedUpdate):
    fileExsist = os.path.isfile(file)
    if (fileExsist):
        fileStats  = os.stat(file)
        lastMod    = datetime.datetime.fromtimestamp(fileStats.st_mtime)
        print("File last Modified:",lastMod.date())
    
        timeToUpdate  =  datetime.datetime.today().combine(datetime.datetime.today(),expectedUpdate)
        timeLastUpdate=  timeToUpdate - datetime.timedelta(days=1)
    
        retrieveAfterUpdate    =  (lastMod < timeToUpdate and datetime.datetime.today()>timeToUpdate)
        retrieveAfterOutofDate =  lastMod < timeLastUpdate
        
        retrieveFile= retrieveAfterOutofDate or retrieveAfterUpdate    
    else:
        print("File not present in path")
        retrieveFile = True
    # Retrieve file
    if retrieveFile:
        print("Retrieving File")
        print("")
        urllib.request.urlretrieve(url, file)
    else:
        print("Using exsisting file.")
        print("")
    # Read file
    with open(file) as f:
        data = json.load(f)    
        
    return data

#
#    printFileStats function
#
def printFileStats(data):
    ##############################################################################
    ##                           file statistics                                ##
    ##############################################################################

    firstDataDate = datetime.date.fromisoformat(data[0]["Date_of_statistics"])
    lastDataDate = datetime.date.fromisoformat(data[-1]["Date_of_statistics"])
    
    print("First date of data: ",firstDataDate)
    print("Last date of data: ",lastDataDate)
    print("   ")

    ##############################################################################
    ##                     Repeat most recent statistics                        ##
    ##############################################################################

    Tested    = 0
    TestedPos = 0
    
    for i in range(0,len(data),1):
        date_i = datetime.date.fromisoformat(data[i]["Date_of_statistics"])
       
        if(date_i == lastDataDate):
            Tested    += data[i]["Tested_with_result"]
            TestedPos += data[i]["Tested_positive"]
    
    print("Tested: ", Tested)
    print("Positive: ", TestedPos)
    print("Percentage: ", round((TestedPos/Tested)*100,2),'%')