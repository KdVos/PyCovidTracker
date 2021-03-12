# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:23:07 2021

@author: KoendeVos
"""
import datetime
import matplotlib.pyplot as plt

from matplotlib import ticker
import numpy    as np

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
        self.dataRegion = ""
        
    def __repr__(self):
         self.updateData()
         printstr  = "Data from: " + str(self.date) + \
                     " Entries: " + str(len(self.dataPoints)) + " Totals: "+ str(self.totals) + \
                     " Positive: " + str(self.positive) + " Percentage: " + str(round(self.percentage,0))
         return printstr
        
    def appendDataPoint(self,item):
        self.dataPoints.append(item)
        self.needsUpdate = True
        
    def updateData(self,regionFilter=""):               
        self.positive = 0
        for items in self.dataPoints:
            if regionFilter in items.getRegion():
                self.positive += items.data[1]       
            
        self.totals = 0
        for items in self.dataPoints:
            if regionFilter in items.getRegion():
                self.totals += items.data[0]        
            
        try:
            self.percentage = (self.positive/self.totals)*100
        except ZeroDivisionError:
            self.percentage = 0
            
        self.needsUpdate = False
        self.dataRegion = regionFilter
        
    def getTotals(self,regionFilter=""):        
        if(self.needsUpdate) or (regionFilter != self.dataRegion):
           self.updateData(regionFilter)
           
        return self.totals
    
    def getPositive(self,regionFilter=""):        
        if(self.needsUpdate) or (regionFilter != self.dataRegion):
            self.updateData(regionFilter)

        return self.positive
    
    def getPercentage(self,regionFilter=""):
         if(self.needsUpdate) or (regionFilter != self.dataRegion):
             self.updateData(regionFilter)

         return self.percentage
######################################       
class dataSet:
    def __init__(self):
        self.dates = []
        self.dataDays = []
        
        self.dayTotals    = []
        self.dayPositives = []
        self.dayPercentage= []
        
        self.smoothTotals = []
        self.smoothPos    = []
        self.smoothPercent= []
        
    def __repr__(self):
        return "Dataset containing " + str(len(self.dates)) + " entries. From " \
            + str(self.dates[0]) + " till " + str(self.dates[-1])
        
    def addRecord(self,dataPoint):
        if(dataPoint.getDate() in self.dates):
            idx = self.dates.index(dataPoint.getDate())
            self.dataDays[idx].appendDataPoint(dataPoint)
        else:
            self.dates.append(dataPoint.getDate())
            
            itemDate = dataDay(dataPoint.getDate())
            itemDate.appendDataPoint(dataPoint)            
            self.dataDays.append(itemDate)
            
    def getSecurityRegions(self):
        securityRegions = []
        for items in self.dataDays[0].dataPoints:
            securityRegions.append(items.region)
        return securityRegions
            
    def getDayTotals(self,regionFilter=""):
        self.dayTotals    = [None] * len(self.dates)
        self.dayPositives = [None] * len(self.dates)
        self.dayPercentage= [None] * len(self.dates)
        
        for i in range(0,len(self.dates)):
            self.dayTotals[i]     = self.dataDays[i].getTotals(regionFilter)
            self.dayPositives[i]  = self.dataDays[i].getPositive(regionFilter)
            
            try:
                self.dayPercentage[i] = self.dayPositives[i]/self.dayTotals[i]*100
            except ZeroDivisionError:
                self.dayPercentage[i] = 0
            
        self.smoothTotals = dataManipulation.movmean(self.dayTotals, 6)  
        self.smoothPos    = dataManipulation.movmean(self.dayPositives, 6)  
        self.smoothPercent= self.smoothPos/self.smoothTotals*100
            
        self.dayData = {"Date"             : self.dates,
                        "Total"            : self.dayTotals,
                        "smoothTotal"      : self.smoothTotals,
                        "Positive"         : self.dayPositives,
                        "smoothPositive"   : self.smoothPos,
                        "Percentage"       : self.dayPercentage,
                        "smoothPercentage" : self.smoothPercent}
            
        return self.dayData 
    
    def getDayTotalsDiff(self,regionFilter=""):
        self.getDayTotals(regionFilter)         
        diffsmoothTotals  = dataManipulation.diff(self.smoothTotals)
        diffsmoothPositive= dataManipulation.diff(self.smoothPos)
        
        diffsmoothTotalsS  = dataManipulation.movmean(diffsmoothTotals,6)
        diffsmoothPositiveS= dataManipulation.movmean(diffsmoothPositive,6)
        
        self.diffData = {"Date"              : self.dates,
                         "DiffTotal"         : diffsmoothTotals,
                         "DiffTotalSmooth"   : diffsmoothTotalsS,
                         "DiffPositive"      : diffsmoothPositive,
                         "DiffPositiveSmooth": diffsmoothPositiveS}
        
        return self.diffData
        ##############################################################################
        #     Plotting  1 
        ##############################################################################
    def getPlots1(self,fileFolder,regionFilter="",ax1 = "", title = '',inhabitants = 1):
        ##Find data
        self.getDayTotalsDiff(regionFilter)
        
        red  = (0.753,0.224,0.169)
        black= (0.173,0.243,0.314)
        
        #######
        #Plots#
        #######
        ## Positive cases plot
        ax1.plot(self.dayData["Date"],np.array(self.dayData["smoothPositive"])/inhabitants,2, color= red)  #red
        ax1.scatter(self.dayData["Date"],np.array(self.dayData["Positive"])/inhabitants,2, color= red)  #red
        
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Positive Tests" , color = red)
        ax1.set_title(regionFilter + title)                

        
        ax1.set_xlim(left = self.dayData["Date"][0] ,right = datetime.datetime.today())
        ax1.set_ylim(bottom = 0, top = max(self.dayData["Positive"]))
        
        ## Percentage plot
        ax2 = ax1.twinx()
        ax2.grid(axis = 'y', ls = 'dotted')
        ax2.plot(self.dayData["Date"],np.array(self.dayData["smoothPercentage"]),2, color= black) #black
        ax2.scatter(self.dayData["Date"],np.array(self.dayData["Percentage"]),2, color= black) #black
        
        ax2.set_xlim(left = self.dayData["Date"][0] ,right = self.dayData["Date"][-1])
        ax2.set_ylim(bottom = 0, top = max(self.dayData["Percentage"]))
        
        ax2.set_ylabel("Percentage + " , color = black)
        
        ax1.xaxis.set_major_locator(ticker.MaxNLocator(5))
        
        frmt = "%d/%m"
        
        xticks = [self.dayData["Date"][0],self.dayData["Date"][-1]]
        ticks  = [xticks[0].strftime(frmt),xticks[-1].strftime(frmt)]
        
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(ticks)    
        
        ax1.set_ylim([0.9*min(self.dayData["smoothPositive"])/inhabitants,1.1*max(self.dayData["smoothPositive"])/inhabitants])        
        ax2.set_ylim([0.9*min(self.dayData["smoothPercentage"]),1.1*max(self.dayData["smoothPercentage"])])     
        
        ax1.set_frame_on(False)
        ax2.set_frame_on(False)
        ##############################################################################
        #     Plotting  2 
        ##############################################################################
    def getPlots2(self,fileFolder,regionFilter="",ax3 = "", title = "",inhabitants = 1):
        self.getDayTotalsDiff(regionFilter)
        ax3.grid(axis = 'y', ls = 'dotted')
        
        blue = (0.161, 0.502, 0.725)
        red  = (0.753,0.224,0.169)
        
        ax3.plot(self.dayData["Date"],np.array(self.dayData["smoothPositive"])/inhabitants,2, color= red) #red
        ax3.scatter(self.dayData["Date"],np.array(self.dayData["Positive"])/inhabitants,2, color= red) #red
        ax3.set_ylabel("Pos. Tests", color = red)
        ax3.set_xlabel("Date")
        
        
        ax3.set_xlim(left = self.dayData["Date"][0] ,right = datetime.datetime.today())
        ax3.set_ylim(bottom = 0, top = max(self.dayData["Positive"]))
        
        ax4 = ax3.twinx()
        ax4.plot(self.dayData["Date"],np.array(self.dayData["smoothTotal"])/inhabitants,2, color= blue) # blue
        ax4.scatter(self.dayData["Date"],np.array(self.dayData["Total"])/inhabitants,2, color= blue) # blue
        ax4.set_ylabel("Total Tests", color = blue)
        
        frmt = "%d/%m"
        
        xticks = [self.dayData["Date"][0],self.dayData["Date"][-1]]
        ticks  = [xticks[0].strftime(frmt),xticks[-1].strftime(frmt)]
        
        ax3.set_xticks(xticks)
        ax3.set_xticklabels(ticks)        
        ax3.set_title(regionFilter + title)     

        ax3.set_ylim([0.9*min(self.dayData["smoothPositive"])/inhabitants,1.1*max(self.dayData["smoothPositive"])/inhabitants])        
        ax4.set_ylim([0.9*min(self.dayData["smoothTotal"])/inhabitants,1.1*max(self.dayData["smoothTotal"])/inhabitants])       
        
        ax3.set_frame_on(False)
        ax4.set_frame_on(False)
        ##############################################################################
        #     Plotting  3 
        ##############################################################################
    def getPlots3(self,fileFolder,regionFilter="",ax5 = "", title = "",inhabitants = 1):
        self.getDayTotalsDiff(regionFilter)
        ax5.grid(axis = 'y', ls = 'dotted')
        
        green = (0.152, 0.682, 0.376)
        
        ax5.plot(self.diffData["Date"],np.array(self.diffData["DiffPositiveSmooth"])/inhabitants,color= green) #green
        ax5.scatter(self.diffData["Date"],np.array(self.diffData["DiffPositive"])/inhabitants,2,color= green) #green
        
        ax5.set_ylim(bottom = 1.1*min(self.diffData["DiffPositiveSmooth"])/inhabitants, \
                     top    = 1.1*max(self.diffData["DiffPositiveSmooth"])/inhabitants)
                    
        ax5.set_ylabel("Diff", color= green)
        ax5.set_xlabel("Date")
        ax5.set_title(regionFilter + title)           
        
        frmt = "%d/%m"
        
        xticks = [self.dayData["Date"][0],self.dayData["Date"][-1]]
        ticks  = [xticks[0].strftime(frmt),xticks[-1].strftime(frmt)]
        
        ax5.set_xticks(xticks)
        ax5.set_xticklabels(ticks)        
                
        ax5.set_frame_on(False)