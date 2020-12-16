import numpy as np
from numpy import cos, sin, sqrt, pi, exp
import Config as cf
from LightSource import LightSource


class Laser(LightSource):
    def __init__(self, rad=1.0, nrays=1_000_000, name=None):
        LightSource.__init__(self, nrays, name=name)
        self.rad = rad
        self.xorient = False
        self.yorient = False

    def GenerateRaysV(self, shape):
        V = np.zeros(shape)
        V[:,0] = 1.0
#        V = self.DirectRaysV(V)
        return V

    def DirectRays(self, X, V):
        R = cf.reflector['Xl']-cf.laser['X']
        R = R/np.sqrt(R[0]**2 + R[1]**2 + R[2]**2) #normalize
        print(R)
        r = np.cross(R,V[0]) #should be unit b/c cross of units
        r = r/np.sqrt(r[0]**2 + r[1]**2 + r[2]**2)
        C = np.dot(R,V[0])
        t = 1-C
        tht = np.arccos(C)
        S = np.sin(tht)
        M = np.array([[(t*r[0]*r[0] + C), (t*r[0]*r[1] - S*r[2]), (t*r[0]*r[2] + S*r[1])],
                  [t*r[0]*r[1] + S*r[2], t*r[1]*r[1] + C, t*r[1]*r[2] - S*r[0]],
                  [t*r[0]*r[2]-S*r[1], t*r[1]*r[2] + S*r[0], t*r[2]*r[2] + C]])
        return X.dot(M), V.dot(M)


    def GenerateRays(self):
        shape = (self.nrays, 3)
        X = np.zeros(shape)
        if(self.rad != 0):
            theta = np.random.uniform(0, 2*pi, self.nrays)
            r = sqrt(np.random.uniform(0, self.rad**2, self.nrays))
            X[:,2] = r*cos(theta)
            X[:,1] = r*sin(theta)
            if(self.xorient):
                Xmark = self.GenerateXMarker()
                X = np.concatenate((X, Xmark), axis=0)
            if(self.yorient):
                Ymark = self.GenerateYMarker()
                X = np.concatenate((X, Ymark), axis=0)

        V = self.GenerateRaysV(X.shape)
        X = self.OrientRaysX(X)
        V = self.OrientRaysV(V)
        print(' ')
        print('Starting laser velocity')
        print(V)
        print('Starting laser position')
        print(X)
        print(' ')
        return X,V
    
    def GenerateRays_v2(self):
        shape = (self.nrays, 3)
        X = np.zeros(shape)
        if(self.rad != 0):
            theta = np.random.uniform(0, 2*pi, self.nrays)
            r = sqrt(np.random.uniform(0, self.rad**2, self.nrays))
            X[:,2] = r*cos(theta)
            X[:,1] = r*sin(theta)
            if(self.xorient):
                Xmark = self.GenerateXMarker()
                X = np.concatenate((X, Xmark), axis=0)
            if(self.yorient):
                Ymark = self.GenerateYMarker()
                X = np.concatenate((X, Ymark), axis=0)

        V = self.GenerateRaysV(X.shape)
        X, V = self.DirectRays(X,V)
        X = self.TranslateRaysX(X)
        #print(' ')
        #print('Starting laser velocity')
        #print(V)
        #print('Starting laser position')
        #print(X)
        #print(' ')
        return X,V

    def GenerateXMarker(self):
        div = 2
        shape = (int(self.nrays/div),3)
        X = np.zeros(shape)
        theta = np.random.uniform(0, 2*pi, int(self.nrays/div))
        r = sqrt(np.random.uniform(0, (self.rad/4)**2, int(self.nrays/div)))
        X[:,2] = r*cos(theta) + self.rad*2/3
        X[:,1] = r*sin(theta)
        return X
    
    def GenerateYMarker(self):
        div = 5
        shape = (int(self.nrays/div),3)
        X = np.zeros(shape)
        theta = np.random.uniform(0, 2*pi, int(self.nrays/div))
        r = sqrt(np.random.uniform(0, (self.rad/4)**2, int(self.nrays/div)))
        X[:,2] = r*cos(theta) 
        X[:,1] = r*sin(theta) + self.rad*2/3
        return X
