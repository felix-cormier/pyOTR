import numpy as np
from numpy import cos, sin, sqrt, pi, exp
from scipy.stats import truncnorm
import Config as cf
from LightSource import LightSource


class Filament(LightSource):
    def __init__(self, nrays=1_000_000, name=None):
        LightSource.__init__(self, nrays, name=name)
        self.nrays = nrays
        #self.n = np.array([500_000,1_000_000,1_500_000])
        self.rad = 35.0/2
        self.sep = 40.0
        self.l_wire =  8.5
        self.wire = cf.filament['wire']
        self.reflector = cf.filament['reflector']
        if(self.reflector):
            if cf.filament['Vtype'] == 'parallel':
                cf.logger.info(f'Selected filament light source with parallel rays')
            elif cf.filament['Vtype'] == 'divergent':
                cf.logger.info(f'Selected filament light source light source with div=' + str(cf.filament['spread']))

    def GenerateWireRaysV(self,shape):
        V = np.zeros(shape)
        ang = pi/34
        #phi = np.random.uniform(-(pi/2-delt),(pi/2-delt), self.nrays)
        #theta = np.random.uniform(delt,(pi-delt), self.nrays)
        phi = np.random.uniform(0., 2*pi, self.nrays)
        theta = np.random.uniform(0.,ang, self.nrays)
        V[:,1] = sin(theta)*cos(phi)
        V[:,2] = sin(theta)*sin(phi)
        V[:,0] = cos(theta)
        return V
    
    def GenerateWireRaysV_v2(self):
        ang = 36./1100.
        scale = 1
        u = np.random.uniform(0., 1., scale*self.nrays)
        h_min = cos(ang)
        v = np.random.uniform(h_min,1.,scale*self.nrays)
        theta = np.arccos(v)
        phi = 2*pi*u
        keep = theta < ang
        phi = phi[keep]
        theta = theta[keep]
        V = np.zeros((phi.size,3))
        V[:,1] = sin(theta)*cos(phi)
        V[:,2] = sin(theta)*sin(phi)
        V[:,0] = cos(theta)
        return V

    def GenerateReflRaysV(self, shape):
        V = np.zeros(shape)
        Vtype = cf.filament['Vtype']
        spread = cf.filament['spread']
        if Vtype == 'parallel':
            V[:,0] = 1.
            return V
        elif Vtype == 'divergent':
            V[:,1] = truncnorm.rvs(-3,3,loc=0,scale=spread,size=V.shape[0])
            V[:,2] = truncnorm.rvs(-3,3,loc=0,scale=spread,size=V.shape[0])
            V[:,0] = np.sqrt(1. - V[:,1]*V[:,1] - V[:,2]*V[:,2])
        elif Vtype == 'divergent_v2':
            mean = [0.,0.]
            cov = np.diag([spread**2,spread**2])
            VyVz = np.random.multivariate_normal(mean,cov,self.nrays)
            KeepElements = (1. - VyVz[:,0]*VyVz[:,0] - VyVz[:,1]*VyVz[:,1]) > 0.
            VyVz = VyVz[KeepElements]
            V[:,1] = VyVz[:,0]
            V[:,2] = VyVz[:,1]
            V[:,0] = np.sqrt(1. - V[:,1]*V[:,1] - V[:,2]*V[:,2])
            return V
        else:
            cf.logger.info('Unknown velocity distribution...exiting')
            sys.exit()
        return V
    
    def DirectRays(self, X, V):
        v = np.array([1,0,0])
        R = cf.reflector['X']-cf.filament['X']
        R = R/np.sqrt(R[0]**2 + R[1]**2 + R[2]**2) #normalize
        print(R)
        r = np.cross(R,v) #should be unit b/c cross of units
        r = r/np.sqrt(r[0]**2 + r[1]**2 + r[2]**2)
        C = np.dot(R,v)
        t = 1-C
        tht = np.arccos(C)
        S = np.sin(tht)
        M = np.array([[(t*r[0]*r[0] + C), (t*r[0]*r[1] - S*r[2]), (t*r[0]*r[2] + S*r[1])],
                  [t*r[0]*r[1] + S*r[2], t*r[1]*r[1] + C, t*r[1]*r[2] - S*r[0]],
                  [t*r[0]*r[2]-S*r[1], t*r[1]*r[2] + S*r[0], t*r[2]*r[2] + C]])
        return X.dot(M), V.dot(M)
    
    def GenerateWire(self, shift=np.array([0.,0.,0.])):
        shape = (self.nrays, 3)
        V = self.GenerateWireRaysV_v2()
        #V = self.DirectRaysV(V)
        #V = self.GenerateWireRaysV(shape)
        self.nrays, shape = V.shape[0], V.shape
        #l = self.rad*(10/21)
        l = self.l_wire
        X = np.zeros(shape)
        X[:,1] = np.random.uniform(-l/2,l/2,self.nrays)
        X = X + shift
        X = self.OrientRaysX(X)
        V = self.OrientRaysV(V)
        print('Wire velocity')
        print(V[:10])
        return X,V
    
    def GenerateWire_v2(self, tht = 0., shift=np.array([0.,0.,0.])):
        shape = (self.nrays, 3)
        V = self.GenerateWireRaysV_v2()
        self.nrays, shape = V.shape[0], V.shape
        l = self.l_wire
        X = np.zeros(shape)
        L = np.random.uniform(-l/2,l/2,self.nrays)
        X[:,1] = L*np.sin(tht)
        X[:,2] = L*np.cos(tht)
        X = X + shift
        V = self.GenerateWireRaysV_v2()
        X, V = self.DirectRays(X,V)
        X = self.TranslateRaysX(X)
        print(' ')
        print('Starting laser velocity')
        print(V)
        print('Starting laser position')
        print(X)
        print(' ')
        return X,V

    def GenerateReflFilament(self, shift=np.array([0.,0.,0.])):
        shape = (self.nrays, 3)
        X = np.zeros(shape)
        if(self.rad != 0):
            theta = np.random.uniform(0, 2*pi, self.nrays)
            r = sqrt(np.random.uniform(0, self.rad**2, self.nrays))
            X[:,2] = r*cos(theta)
            X[:,1] = r*sin(theta)
        X = X + shift
        X = self.OrientRaysX(X)
        V = self.GenerateReflRaysV(X.shape)
        V = self.OrientRaysV(V)
        return X,V
    
    def GenerateFilament(self,tht=np.pi/2, shift=np.array([0.,0.,0.])):
        if(self.wire):
            X, V = self.GenerateWire_v2(tht,shift)
        if(self.reflector):
            Xf,Vf = self.GenerateReflFilament(shift)
            if(self.wire):
                X = np.concatenate((X,Xf),axis=0)
                V = np.concatenate((V,Vf),axis=0)
            else:
                X,V = Xf,Vf
        return X,V

    def GenerateRays(self):
        if(cf.filament['F1']):
            X,V = self.GenerateFilament(shift=np.array([0.,-self.sep/2, self.sep/2]))
            #X,V = self.GenerateFilament()
            cf.logger.info(f'F1:Added')
        if(cf.filament['F2']):
            cf.logger.info(f'F2:Added')
            if(cf.filament['F1'] == False):
                X,V = self.GenerateFilament(shift=np.array([0.,self.sep/2, self.sep/2]))
                #X,V = self.GenerateFilament(shift=np.array([0.,0., 0.]))
            else:
                X2,V2 = self.GenerateFilament(shift=np.array([0.,self.sep/2, self.sep/2]))
                X = np.concatenate((X,X2),axis=0)
                V = np.concatenate((V,V2),axis=0)
        if(cf.filament['F3']):
            cf.logger.info(f'F3:Added')
            if(cf.filament['F1'] == False and cf.filament['F2'] == False):
                X,V = self.GenerateFilament(shift=np.array([0.,self.sep/2, -self.sep/2]))
            else:
                X3,V3 = self.GenerateFilament(shift = np.array([0.,self.sep/2, -self.sep/2]))
                X = np.concatenate((X,X3),axis=0)
                V = np.concatenate((V,V3),axis=0)
        return X,V
