import numpy as np

def movmean(data,N):
    
    datalength = len(data)
    
    if (type(N) == int):
        kb = N
        kf = 0
    else :
        kb = N[0]
        kf = N[1]
        
    summeddata = np.cumsum(data)
        
    forwardsum  = summeddata[kf:] 
    backwardsum = summeddata[:-(kb+1)]    
    
    prependbackward = datalength - len(backwardsum) 
    prepender       = [0] * prependbackward
    backwardsum      = np.hstack([prepender,backwardsum])

    
    appendforward   = datalength - len(forwardsum)
    appender        = [summeddata[-1]] * appendforward
    forwardsum      = np.hstack([forwardsum,appender])     
    
    mean = (forwardsum - backwardsum) / (kb+kf+1)    
    
    # Correct edges
    for i in range (0,kb):        
        lft_bnd         =   0
        rgh_bnd         =   i + kf
        range_mean      =   data[lft_bnd:rgh_bnd+1]
        mean[i]         =   sum(range_mean)/len(range_mean)
        
    for i in range (0,kf):        
        lft_bnd                   =   (len(data)-1) - (i + kb)
        rgh_bnd                   =   (len(data)-1)
        range_mean                =   data[lft_bnd:rgh_bnd+1]
        mean[(len(data)-1)-i]     =   sum(range_mean)/len(range_mean)
        
    return mean