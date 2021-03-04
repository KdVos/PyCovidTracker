# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Imports
from functions import fileHandling
import datetime 

# Path to dataset, local file, and expected update time stamp
url                         = "https://data.rivm.nl/covid-19/COVID-19_uitgevoerde_testen.json"
file                        = "./COVID-19_uitgevoerde_testen.json"
expectedUpdate              = datetime.time.fromisoformat('15:15:00')

##############################################################################
# Check whether file needs to be retrieved, 
# or whether old file is still the most up-to date one
##############################################################################
# Retrieve file
data = fileHandling.fileretrieval(file,url,expectedUpdate)
# Print Stats from file
fileHandling.printFileStats(data)
##############################################################################