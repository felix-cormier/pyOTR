import random
import numpy as np

def get_random_ellipse(n, x0, y0):
    xout = np.zeros(n)
    yout = np.zeros(n)
    nkeep=0
    while nkeep < n:
        x=2*x0*(np.random.random(n-nkeep) - 0.5)
        y=2*y0*(np.random.random(n-nkeep) - 0.5)
        w,=np.where( ( ((x)/x0)**2 + ((y)/y0)**2 ) < 1 )
        if w.size > 0:
            xout[nkeep:nkeep+w.size] = x[w]
            yout[nkeep:nkeep+w.size] = y[w]
            nkeep += w.size
    return xout,yout

xc,yc=get_random_ellipse(1_000_000,2.5,2.5)
