import random
import numpy as np
import matplotlib.pyplot as plt

### trianglular pattern ###
def point_on_triangle(pt1, pt2, pt3):
    s, t = sorted([random.random(), random.random()])
    return (s * pt1[0] + (t-s)*pt2[0] + (1-t)*pt3[0],
            s * pt1[1] + (t-s)*pt2[1] + (1-t)*pt3[1])

#vertices' coordinates
pt1 = (-0.3, 2.5)
pt2 = (-0.7, 1.3)
pt3 = (0.7, 1.3)
points = [point_on_triangle(pt1, pt2, pt3) for _ in range(1000)]
x0, y0 = zip(*points)

### elliptical pattern ###
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

x1,y1=get_random_ellipse(1000,0.7, 0.7)

### rectangular pattern ###
x2 = np.random.uniform(1.3,2.5,1000)
y2 = np.random.uniform(1.3,2.5,1000)


x=np.hstack((x0,x1,x2))
y=np.hstack((y0,y1,y2))
X=np.vstack((x,y))
