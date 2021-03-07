import numpy as np

def movmean(data,N):
    
    datalength = len(data)
    
    if (type(N) == int):
        kb = N
        kf = 0
    else :
        kb = N(0)
        kf = N(1)
        
    summeddata = np.cumsum(data)
        
    forwardsum  = summeddata[kf:] 
    backwardsum = summeddata[:-kb]    
    
    prependbackward = datalength - len(backwardsum) 
    prepender       = [0] * prependbackward
    backwardsum      = np.hstack([prepender,backwardsum])

    
    appendforward   = datalength - len(forwardsum)
    appender        = [summeddata[-1]] * appendforward
    forwardsum      = np.hstack([forwardsum,appender])
    
    mean = (forwardsum - backwardsum) / (kb+kf+1)    
    
    return mean