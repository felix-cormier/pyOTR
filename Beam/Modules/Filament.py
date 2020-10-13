import numpy as np
from numpy import cos, sin, sqrt, pi, exp
from scipy.stats import truncnorm
import Config as cf
from LightSource import LightSource


class Filament(LightSource):
    def __init__(self, rad=21., sep=48.6, nrays=1_000_000, name=None):
        LightSource.__init__(self, nrays, name=name)
        self.rad = rad
        self.sep=sep
        if cf.filament['Vtype'] == 'parallel':
            cf.logger.info(f'Selected filament light source with parallel rays')
        elif cf.filament['Vtype'] == 'divergent':
            cf.logger.info(f'Selected filament light source light source with div=' + str(cf.filament['spread']))

    def GenerateRaysV(self, shape):
        V = np.zeros(shape)
        Vtype = cf.filament['Vtype']
        spread = cf.filament['spread']
        if Vtype == 'parallel':
            V[:,0] = 1.
            return V
        elif Vtype == 'divergent':
            V[:,1] = truncnorm.rvs(-3*spread,3*spread,loc=0,scale=spread,size=V.shape[0])
            V[:,2] = truncnorm.rvs(-3*spread,3*spread,loc=0,scale=spread,size=V.shape[0])
            V[:,0] = np.sqrt(1 - V[:,1]*V[:,1] - V[:,2]*V[:,2])
            return V
        else:
            cf.logger.info('Unknown velocity distribution...exiting')
            sys.exit()
        return V

    def GenerateFilament(self, shift=np.array([0.,0.,0.])):
        shape = (self.nrays, 3)
        X = np.zeros(shape)
        if(self.rad != 0):
            theta = np.random.uniform(0, 2*pi, self.nrays)
            r = sqrt(np.random.uniform(0, self.rad**2, self.nrays))
            X[:,2] = r*cos(theta)
            X[:,1] = r*sin(theta)
        X = X + shift
        X = self.OrientRaysX(X)
        V = self.GenerateRaysV(X.shape)
        V = self.OrientRaysV(V)
        return X,V

    def GenerateRays(self):
        if(cf.filament['F1']):
            X,V = self.GenerateFilament(np.array([0.,self.sep/2, -self.sep/2]))
            cf.logger.info(f'F1:Added')
        if(cf.filament['F2']):
            cf.logger.info(f'F2:Added')
            if(cf.filament['F1'] == False):
                X,V = self.GenerateFilament(np.array([0.,self.sep/2, self.sep/2]))
            else:
                X2,V2 = self.GenerateFilament(np.array([0.,self.sep/2, self.sep/2]))
                X = np.concatenate((X,X2),axis=0)
                V = np.concatenate((V,V2),axis=0)
        if(cf.filament['F3']):
            cf.logger.info(f'F3:Added')
            if(cf.filament['F1'] == False and cf.filament['F2'] == False):
                X,V = self.GenerateFilament(np.array([0.,-self.sep/2, self.sep/2]))
            else:
                X3,V3 = self.GenerateFilament(np.array([0.,-self.sep/2, self.sep/2]))
                X = np.concatenate((X,X3),axis=0)
                V = np.concatenate((V,V3),axis=0)
        #X,V = self.GenerateFilament()
        #X = np.concatenate((X1, X2, X3), axis=0)
        #V = np.concatenate((V1, V2, V3), axis=0)
        return X,V
