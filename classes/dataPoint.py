# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:23:07 2021

@author: KoendeVos
"""
import datetime
from functions import dataManipulation

######################################
class dataPoint:    
    def __init__(self, date ,data = (0,0), region="not_specified"):
        self.date = date
        self.data = data
        self.region = region
        
    def getDate(self):
        return self.date
        
    def getPositive(self) :
        return self.data[1]

    def getTests(self) :
        return self.data[0]
    
    def getRegion(self):
        return self.region
    
    def getPercentage(self):
        return self.data[1]/self.data[0]
    
    def __repr__(self):
        printstr = "Data: " + str(self.date) + " Region: " + self.region
        
        return printstr
    
    def  __str__(self):
        printstr = "Data from: " + str(self.date) + "\n Tests performed: " + \
                   str(self.data[0]) + "\n Tested Positive: " + str(self.data[1])
        return printstr
######################################    
class dataDay:
    def __init__(self, date):
        self.date       = date
        self.dataPoints = []
        
        self.totals     = None
        self.positive   = None
        self.percentage = None
        
        self.needsUpdate = True
        
    def __repr__(self):
         self.updateData()
         printstr  = "Data from: " + str(self.date) + " Entries: " + str(len(self.dataPoints)) + " Totals: "+ str(self.totals) + \
                     " Positive: " + str(self.positive) + " Percentage: " + str(round(self.percentage,0))
         return printstr
        
    def appendDataPoint(self,item):
        self.dataPoints.append(item)
        self.needsUpdate = True
        
    def updateData(self):               
        self.positive = 0
        for items in self.dataPoints:
            self.positive += items.data[1]       
            
        self.totals = 0
        for items in self.dataPoints:
            self.totals += items.data[0]        
            
        self.percentage = (self.positive/self.totals)*100
            
        self.needsUpdate = False
        
    def getTotals(self):        
        if(self.needsUpdate):
           self.updateData()
           
        return self.totals
    
    def getPositive(self):        
        if(self.needsUpdate):
            self.updateData()

        return self.positive
    
    def getPercentage(self):
         if(self.needsUpdate):
             self.updateData()

         return self.percentage
######################################       
class dataSet:
    def __init__(self):
        self.dates = []
        self.dataDays = []
        
    def addRecord(self,dataPoint):
        if(dataPoint.getDate() in self.dates):
            idx = self.dates.index(dataPoint.getDate())
            self.dataDays[idx].appendDataPoint(dataPoint)
        else:
            self.dates.append(dataPoint.getDate())
            
            itemDate = dataDay(dataPoint.getDate())
            itemDate.appendDataPoint(dataPoint)            
            self.dataDays.append(itemDate)
            
    def getDayTotals(self):
        dayTotals    = [None] * len(self.dates)
        dayPositives = [None] * len(self.dates)
        dayPercentage= [None] * len(self.dates)
        
        for i in range(0,len(self.dates)):
            dayTotals[i]     = self.dataDays[i].getTotals()
            dayPositives[i]  = self.dataDays[i].getPositive()
            dayPercentage[i] = dayPositives[i]/dayTotals[i]
            
        smoothTotals = dataManipulation.movmean(dayTotals, 7)  
        smoothPos    = dataManipulation.movmean(dayPositives, 7)  
        smoothPercent= smoothPos/smoothTotals
            
        result = {"Date"             : self.dates,
                  "Total"            : dayTotals,
                  "smoothTotal"      : smoothTotals,
                  "Positive"         : dayPositives,
                  "smoothPositive"   : smoothPos,
                  "Percentage"       : dayPercentage,
                  "smoothPercentage" : smoothPercent}
            
        return result
######################################            