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
    print("File last Modified:")
    print(lastMod.date())
# Retrieve file
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
print("First date of retrieved file: ")
firstDataDate = date.fromisoformat(data[0]["Date_of_statistics"])
print(firstDataDate)
print("Last date of retrieved file: ")
lastDataDate = date.fromisoformat(data[-1]["Date_of_statistics"])
print(lastDataDate)
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

print("Tested")
print(Tested)
print("Tested Positive")
print(TestedPos)
print("Percentage")
print(round((TestedPos/Tested)*100,2))