import numpy as np
import Modules.Config as cf

import Pattern

### Monte-Carlo data ###
N = 500000
# r = 2.5 * np.random.uniform(0,1,N) # light rays in Gaussian
r = 2.5                              # light rays in Circular Ring

zero  = np.zeros(N)
one   = np.ones(N)
theta = np.random.uniform(0,2*np.pi,N)
x     = r*np.cos(theta)
y     = r*np.sin(theta)

x_p = Pattern.X[0]
y_p = Pattern.X[1]
zero_p  = np.zeros(len(x_p))
one_p   = np.ones(len(x_p))

### Get details about the beam ###

# def read():
#     X = np.load(cf.inputs.format('X'))
#     V = np.load(cf.inputs.format('V'))
#    return X,V

def test_top():
    X = np.array([[-1100. + 2*cf.M4['f'],6522+2,1],[-1100. + 2*cf.M4['f'],6522+1.5,0.5],[-1100. + 2*cf.M4['f'],6522+1.5,0.5],[-1100. + 2*cf.M4['f'],6522+0,2.5],[-1100. + 2*cf.M4['f'],6522+1,2]])
    V = np.array([[-1,0,0,],[-1,0,0],[-1,0,0],[-1,0,0],[-1,0,0]])
    return X,V

def test_bottom():
    X = np.array([[0,2,1],[0,1.5,0.5],[0,1.5,0.5],[0,0,2.5],[0,1,2]])
    V = np.array([[1,0,0,],[1,0,0],[1,0,0],[1,0,0],[1,0,0]])
    return X,V

def asy_patt_top():
    X = np.stack(((-1100. + 2*cf.M4['f'])*one_p,6522+y_p,x_p),axis=-1)
    V = np.stack((-1*one_p,zero_p,zero_p),axis=-1)
    return X,V

def asy_patt_bottom():
    X = np.stack((zero_p,y_p,x_p),axis=-1)
    V = np.stack((1*one_p,zero_p,zero_p),axis=-1)
    return X,V

def MC_top():
    X = np.stack(((-1100. + 2*cf.M4['f'])*one,6522+y,x),axis=-1)
    V = np.stack((-1*one,zero,zero),axis=-1)
    return X,V

def MC_bottom():
    X = np.stack((zero,y,x),axis=-1)
    V = np.stack((1*one,zero,zero),axis=-1)
    # h_p = np.histogram2d(-X[:,2]*300/550,X[:,1]*300/550, bins=100)
    return X,V
