# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Imports
from functions import fileHandling
from classes.dataPoint import *

import datetime 

import matplotlib.pyplot as plt
from matplotlib import ticker

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
# Compile list of daytotals

dataPoints = dataSet()

for item in data:
   itemDate    = datetime.date.fromisoformat(item["Date_of_statistics"])
   itemTotal   = item["Tested_with_result"]
   itemPositive= item["Tested_positive"]
   itemRegion  = item["Security_region_name"]

   itemPoint = dataPoint(itemDate,(itemTotal,itemPositive),itemRegion)   
   dataPoints.addRecord(dataPoint= itemPoint)

dayData = dataPoints.getDayTotals()

##############################################################################
#     Plotting 
##############################################################################
fig1, ax1 = plt.subplots()
ax1.grid('minor')
## Positive cases plot
ax1.plot(dayData["Date"],dayData["smoothPositive"],2, color= 'red')
ax1.scatter(dayData["Date"],dayData["Positive"],2, color= 'red')

plt.xlabel("Date")
plt.ylabel("Positive Tests")

ax1.set_xlim(left = dayData["Date"][0] ,right = dayData["Date"][-1])
ax1.set_ylim(bottom = 0, top = max(dayData["Positive"]))

## Percentage plot
ax3 = ax1.twinx()
ax3.plot(dayData["Date"],dayData["smoothPercentage"],2, color= 'black')
ax3.scatter(dayData["Date"],dayData["Percentage"],2, color= 'black')

ax3.set_xlim(left = dayData["Date"][0] ,right = dayData["Date"][-1])
ax3.set_ylim(bottom = 0, top = max(dayData["Percentage"]))

plt.ylabel("Percentage of Pos. Tests")

ax1.xaxis.set_major_locator(ticker.MaxNLocator(5))
fig1.savefig("Percentage_vs_Cases.pdf")

N_zoom = 100
ax1.set_xlim(left = datetime.datetime.today()-datetime.timedelta(days=100) ,right = datetime.datetime.today())
ax1.set_ylim(bottom = 0.8*min(dayData["smoothPositive"][-100:]), top = 1.2*max(dayData["smoothPositive"][-100:]))
ax3.set_ylim(bottom = 0.8*min(dayData["smoothPercentage"][-100:]), top = 1.2*max(dayData["smoothPercentage"][-100:]))

fig1.savefig("Percentage_vs_Cases_recentzoom.pdf")