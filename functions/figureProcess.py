import matplotlib
import datetime

def has_twinx(ax):
    s = ax.get_shared_x_axes().get_siblings(ax)
    if len(s) > 1:
        for ax1 in [ax1 for ax1 in s if ax1 is not ax]:
            if ax1.bbox.bounds == ax.bbox.bounds:
                return True
    return False

def syncAxes(axVector):
    
    ymin = 0
    ymax = 0    
    
    ymin_title = 0
    ymax_title = 0  
        
    for axes in axVector:        
        try:                          
            if axes.get_ylim()[0]<ymin and axes.get_title() != '':
                ymin = axes.get_ylim()[0]
            if axes.get_ylim()[1]>ymax and axes.get_title() != '':
                ymax = axes.get_ylim()[1]
                
            if axes.get_ylim()[0]<ymin_title and axes.get_title() == '':
                ymin_title = axes.get_ylim()[0]
            if axes.get_ylim()[1]>ymax_title and axes.get_title() == '':
                ymax_title = axes.get_ylim()[1]
        except AttributeError:
            pass

    for axes in axVector: 
        try:
            if axes.get_title() != '':
                axes.set_ylim([ymin,ymax])
            else:
                axes.set_ylim([ymin_title,ymax_title])
        except AttributeError:
            pass
    
    formatAxes(axVector)
        
def zoomFigure(axVector,N=100):
    for axes in axVector: 
        try:
            xmin = datetime.datetime.today() - datetime.timedelta(days = N)
            xmax = datetime.datetime.today()
            lims = [xmin,xmax]
            
            frmt = "%d/%m"
            ticks = [lims[0].strftime(frmt),lims[1].strftime(frmt)]
            axes.set_xticks(lims)
            axes.set_xticklabels(ticks)     
            axes.set_xlim(lims)            
            
        except AttributeError:
            pass
        
    formatAxes(axVector)
    formatYLimits(axVector)

def formatAxes(axVector):
    BotRow   = findBottomRow(axVector)
    leftCol  = findLeftCol(axVector)
    rightCol = findRightCol(axVector)
    
    for i in range(0,len(rightCol)):
        isRightCol= rightCol[i]
        isLeftCol = leftCol[i]
        isBotRow  = BotRow[i]
        
        if(not isBotRow):
            ticks = []
            axVector[i].set_xticks(ticks)
            axVector[i].set_xticklabels(ticks)             
            axVector[i].set_xlabel('')
            
        if  (isLeftCol and axVector[i].get_title()!=''):
            pass
        elif (isRightCol and axVector[i].get_title()==''):
            pass
        else:
            ticks = [''] * len(axVector[i].get_yticks())            
            axVector[i].set_yticklabels(ticks)
            axVector[i].set_ylabel('')
            
def formatYLimits(axVector,N=100):
    
    minY = 1e6
    maxY = 0
    
    minYTitle = 1e6
    maxYTitle = 0
    
    for axes in axVector:
        line_ax  = axes.lines[0].get_ydata()
        lineData = line_ax[-N:]        
        
        ## Minimums 
        if min(lineData) < minY and axes.get_title() != '': 
            minY = min(lineData)
        if min(lineData) < minYTitle and axes.get_title() == '':
            minYTitle = min(lineData)           
        ## Maximums    
        if max(lineData) > maxY and axes.get_title() != '':
            maxY = max(lineData)
        if max(lineData) > maxYTitle and axes.get_title() == '':
            maxYTitle = max(lineData)
            
    maxYTitle = 1.1 * maxYTitle
    maxY = 1.1* maxY
    
    if minY < 0:
        minY = 1.1*minY
    else:            
        minY      = 1/1.1*minY
        
    if minYTitle < 0:
        minYTitle = 1.1*minYTitle
    else:
        minYTitle = 1/1.1*minYTitle

    for axes in axVector:
        if axes.get_title() != '':
            axes.set_ylim([minY,maxY])
        if axes.get_title() == '':
            axes.set_ylim([minYTitle,maxYTitle])  
    
def findRightCol(axVector):
    xmax = 0 
    isRightCol = []
    
    for axes in axVector:
        pos = axes.get_position()        
        if pos.x0 > xmax:
            xmax = pos.x0
            
    for axes in axVector:
        pos = axes.get_position()
        if pos.x0 == xmax:
            isRightCol.append(True)
        else:
            isRightCol.append(False)
            
    return isRightCol

def findLeftCol(axVector):
    xmin = axVector[0].get_position().x0   
    isLeftCol = []
    
    for axes in axVector:
        pos = axes.get_position()        
        if pos.x0 < xmin:
            xmin = pos.x0
            
    for axes in axVector:
        pos = axes.get_position()
        if pos.x0 == xmin:
            isLeftCol.append(True)
        else:
            isLeftCol.append(False)
            
    return isLeftCol
            
def findBottomRow(axVector):
    ymax = axVector[0].get_position().y0   
    isBotRow = []
    
    for axes in axVector:
        pos = axes.get_position()        
        if pos.y0 < ymax:
            ymax = pos.y0
            
    for axes in axVector:
        pos = axes.get_position()
        if pos.y0 == ymax:
            isBotRow.append(True)
        else:
            isBotRow.append(False)
            
    return isBotRow

        
        
        