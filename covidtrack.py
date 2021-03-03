# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Imports
import urllib.request
import json
import os

from datetime import datetime
from datetime import timedelta
from datetime import date
from datetime import time
# Path to dataset, local file, and expected update time stamp
url                         = "https://data.rivm.nl/covid-19/COVID-19_uitgevoerde_testen.json"
file                        = "./COVID-19_uitgevoerde_testen.json"
expectedUpdate              = time.fromisoformat('15:15:00')

##############################################################################
# Check whether file needs to be retrieved, 
# or whether old file is still the most up-to date one
##############################################################################

fileExsist = os.path.isfile(file)
if (fileExsist):
    fileStats  = os.stat(file)
    lastMod    = datetime.fromtimestamp(fileStats.st_mtime)
    print("File last Modified:",lastMod.date())

    timeToUpdate  =  datetime.today().combine(datetime.today(),expectedUpdate)
    timeLastUpdate=  timeToUpdate - timedelta(days=1)

    retrieveAfterUpdate    =  (lastMod < timeToUpdate and datetime.today()>timeToUpdate)
    retrieveAfterOutofDate =  lastMod < timeLastUpdate
    
    retrieveFile= retrieveAfterOutofDate or retrieveAfterUpdate    
else:
    print("File not present in path")
    retrieveFile = True
# Retrieve file
if retrieveFile:
    print("Retrieving File")
    urllib.request.urlretrieve(url, file)
# Read file
with open(file) as f:
    data = json.load(f)        
    
##############################################################################
##                           file statistics                                ##
##############################################################################

firstDataDate = date.fromisoformat(data[0]["Date_of_statistics"])
lastDataDate = date.fromisoformat(data[-1]["Date_of_statistics"])

print("First date of data: ",firstDataDate)
print("Last date of data: ",lastDataDate)

##############################################################################
##                     Repeat most recent statistics                        ##
##############################################################################

Tested    = 0
TestedPos = 0

for i in range(0,len(data),1):
    date_i = date.fromisoformat(data[i]["Date_of_statistics"])
   
    if(date_i == lastDataDate):
        Tested    += data[i]["Tested_with_result"]
        TestedPos += data[i]["Tested_positive"]

print("Tested: ", Tested)
print("Positive: ", TestedPos)
print("Percentage: ", round((TestedPos/Tested)*100,2),'%')