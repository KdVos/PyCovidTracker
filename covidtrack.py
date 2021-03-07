# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Imports
from functions import fileHandling, dataManipulation
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

days      = []
daytotals = []
dayposit  = []
percent   = []

for item in data:
   itemDate    = datetime.date.fromisoformat(item["Date_of_statistics"])
   itemTotal   = item["Tested_with_result"]
   itemPositive= item["Tested_positive"]
   if(itemDate in days): 
      idx             = days.index(itemDate)
      daytotals[idx] += itemTotal
      dayposit[idx]  += itemPositive
      percent[idx]    = dayposit[idx]/daytotals[idx]
      pass
   else:
       days.append(itemDate)
       daytotals.append(itemTotal)
       dayposit.append(itemPositive)
       percent.append(itemPositive/itemTotal)
       

movpositive = dataManipulation.movmean(dayposit, 7)
movtotal    = dataManipulation.movmean(daytotals, 7)  
movpercent  = movpositive/movtotal
  
fig1, ax1 = plt.subplots()
ax1.scatter(days,dayposit,2, color= 'red')
ax1.plot(days,movpositive,color='red')

ax3 = ax1.twinx()
ax3.scatter(days,percent,2, color= 'black')
ax3.plot(days,movpercent,color='black')

ax1.xaxis.set_major_locator(ticker.MaxNLocator(6))
fig1.savefig("Percentage_vs_Cases.pdf")

ax1.set_xlim(left = datetime.datetime.today()-datetime.timedelta(days=50) ,right = datetime.datetime.today())
ax1.set_ylim(bottom = 0.8*min(movpositive[-50:]), top = 1.2*max(movpositive[-50:]))
ax3.set_ylim(bottom = 0.8*min(movpercent[-50:]), top = 1.2*max(movpercent[-50:]))

fig1.savefig("Percentage_vs_Cases_recentzoom.pdf")