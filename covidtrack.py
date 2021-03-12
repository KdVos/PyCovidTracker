# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Imports
from functions import fileHandling, dataManipulation, figureProcess
from classes.dataPoint import *

import os

import datetime 
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import ticker

# Path to dataset, local file, and expected update time stamp
url                         = "https://data.rivm.nl/covid-19/COVID-19_uitgevoerde_testen.json"
file                        = "./data/COVID-19_uitgevoerde_testen.json"
fileVeiligheid              = "./data/veiligheidsregios.csv"
expectedUpdate              = datetime.time.fromisoformat('15:15:00')
fileFolder                  = "./figures/"
fileExtension               = ".png"

veiligheidCols              = ["Gemeente","CBS","VeiligheidsRegio","Inwoners"]
veiligheidsRegios           = fileHandling.csvParsing(fileVeiligheid,veiligheidCols)
veiligheidsRegios           = dataManipulation.regionSummation(veiligheidsRegios)
try:
    os.mkdir(fileFolder)
except:
    pass

##############################################################################
# Check whether file needs to be retrieved, 
# or whether old file is still the most up-to date one
##############################################################################
# Retrieve file
data = fileHandling.fileretrieval(file,url,expectedUpdate)
fileHandling.printFileStats(data)
##############################################################################
# Compile list of daytotals
##############################################################################
dataPoints = dataSet()

for item in data:
   itemDate    = datetime.date.fromisoformat(item["Date_of_statistics"])
   itemTotal   = item["Tested_with_result"]
   itemPositive= item["Tested_positive"]
   itemRegion  = item["Security_region_name"]

   itemPoint = dataPoint(itemDate,(itemTotal,itemPositive),itemRegion)   
   dataPoints.addRecord(dataPoint= itemPoint)
   
securityRegions = dataPoints.getSecurityRegions()

##############################################################################
if True:    
    ## Plot 1
    f1, ax1 = plt.subplots(nrows = 5, ncols = 5)
    f1.set_size_inches(15, 10, forward=True)
    f1.set_dpi(500)
    f1.patch.set_facecolor((0.925,0.941,0.945))
    ax1 = np.hstack(ax1)
    ## Plot 2
    f2 , ax2 = plt.subplots(nrows = 5, ncols = 5)
    f2.set_size_inches(15, 10, forward=True)
    f2.set_dpi(500)
    f2.patch.set_facecolor((0.925,0.941,0.945))
    ax2 = np.hstack(ax2)
    ## Plot 3
    f3, ax3 = plt.subplots(nrows = 5, ncols = 5)
    f3.set_size_inches(15, 10, forward=True)
    f3.set_dpi(500)
    f3.patch.set_facecolor((0.925,0.941,0.945))
    ax3 = np.hstack(ax3)
    
    for i in range(0,len(securityRegions)-1):        
        region    = securityRegions[i]
        idx       = veiligheidsRegios["VeiligheidsRegio"].index(region)
        inhabs    = veiligheidsRegios["Inwoners"][idx] / 1e4
        
        ax_region = ax1[i]
        dataPoints.getPlots1(fileFolder,region,ax_region,inhabitants = inhabs)
        
        ax_region = ax2[i]
        region    = securityRegions[i]
        dataPoints.getPlots2(fileFolder,region,ax_region,inhabitants = inhabs)
    
        ax_region = ax3[i]
        region    = securityRegions[i]
        dataPoints.getPlots3(fileFolder,region,ax_region,inhabitants = inhabs)
        
    figureProcess.syncAxes(f1.axes)
    figureProcess.syncAxes(f2.axes)
    figureProcess.syncAxes(f3.axes)   
    
    f1.tight_layout() 
    f2.tight_layout()
    f3.tight_layout()
    
    f1.savefig(fileFolder + '1_0_Regions_Percentage_vs_Positive' + fileExtension)
    f2.savefig(fileFolder + '1_0_Regions_Tests_vs_Positive' + fileExtension)
    f3.savefig(fileFolder + '1_0_Regions_Diff_Positive' + fileExtension)
    
    figureProcess.zoomFigure(f1.axes)
    figureProcess.zoomFigure(f2.axes)
    figureProcess.zoomFigure(f3.axes)
    
    f1.savefig(fileFolder + '1_1_Regions_Percentage_vs_Positive_zoom' + fileExtension)
    f2.savefig(fileFolder + '1_1_Regions_Tests_vs_Positive_zoom' + fileExtension)
    f3.savefig(fileFolder + '1_1_Regions_Diff_Positive_zoom' + fileExtension)


# ###############################################
if True:
    f1, ax1 = plt.subplots()
    f1.set_size_inches(6, 4, forward=True)
    f1.set_dpi(500)
    f1.patch.set_facecolor((0.925,0.941,0.945))
    
    f2, ax2 = plt.subplots()
    f2.set_size_inches(6, 4, forward=True)
    f2.set_dpi(500)
    f2.patch.set_facecolor((0.925,0.941,0.945))
    
    f3, ax3 = plt.subplots()
    f3.set_size_inches(6, 4, forward=True)
    f3.set_dpi(500)
    f3.patch.set_facecolor((0.925,0.941,0.945))
    
    dataPoints.getPlots1(fileFolder,'',ax1,'Nederland')
    dataPoints.getPlots2(fileFolder,'',ax2,'Nederland')
    dataPoints.getPlots3(fileFolder,'',ax3,'Nederland')
    
    f1.tight_layout() 
    f2.tight_layout()
    f3.tight_layout()
    
    f1.savefig(fileFolder + '0_0_Percentage_vs_Positive' + fileExtension)
    f2.savefig(fileFolder + '0_0_Tests_vs_Positive' + fileExtension)
    f3.savefig(fileFolder + '0_0_Diff_Positive' + fileExtension)
    
    figureProcess.zoomFigure(f1.axes)
    figureProcess.zoomFigure(f2.axes)
    figureProcess.zoomFigure(f3.axes)
    
    f1.savefig(fileFolder + '0_1_Percentage_vs_Positive_zoom' + fileExtension)
    f2.savefig(fileFolder + '0_1_Tests_vs_Positive_zoom' + fileExtension)
    f3.savefig(fileFolder + '0_1_Diff_Positive_zoom' + fileExtension)
