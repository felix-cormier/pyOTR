import numpy as np
from numpy import cos, sin, sqrt, pi, exp
from scipy.stats import truncnorm
import Config as cf
from LightSource import LightSource


class Filament(LightSource):
    def __init__(self, nrays=1_000_000, name=None):
        LightSource.__init__(self, nrays, name=name)
        self.nrays = nrays
        self.rad = 35.0/2 #reflector radius
        self.sep = 40.0 #dist between filament centers 
        self.l_wire =  8.5 #length of filament wire
        self.wire = cf.filament['wire'] #true if wire is simulated
        self.reflector = cf.filament['reflector'] #true if reflected light is simulated
        if(self.reflector):
            if cf.filament['Vtype'] == 'parallel':
                cf.logger.info(f'Selected filament light source with parallel rays')
            elif cf.filament['Vtype'] == 'divergent': #bivariate normal divergence
                cf.logger.info(f'Selected filament light source light source with div=' + str(cf.filament['spread']))

    def GenerateWireRaysV(self):
        #Method to generate isotropic light from each point on wire, with cutoff at ang
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
            #Truncated normal cutoff at 3 sigma, centered at 0
            V[:,1] = truncnorm.rvs(-3,3,loc=0,scale=spread,size=V.shape[0])
            V[:,2] = truncnorm.rvs(-3,3,loc=0,scale=spread,size=V.shape[0])
            V[:,0] = np.sqrt(1. - V[:,1]*V[:,1] - V[:,2]*V[:,2])
        elif Vtype == 'divergent_v2':
            #Bivariate normal with elvelocity elements that can't be normalized removed
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
        #Same as DirectRays in laser class, see additional comments there
        v = np.array([1,0,0])
        R = cf.reflector['X']-cf.filament['X']
        R = R/np.sqrt(R[0]**2 + R[1]**2 + R[2]**2) #normalize
        r = np.cross(R,v) 
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
        #Generate isotropic light along the length of the filament wire
        shape = (self.nrays, 3)
        V = self.GenerateWireRaysV()
        self.nrays, shape = V.shape[0], V.shape
        l = self.l_wire
        X = np.zeros(shape)
        X[:,1] = np.random.uniform(-l/2,l/2,self.nrays)
        X = X + shift
        X = self.OrientRaysX(X)
        V = self.OrientRaysV(V)
        return X,V
    
    def GenerateWire_v2(self, tht = 0., shift=np.array([0.,0.,0.])):
        #Generate isotropic light along the length of the filament wire
        shape = (self.nrays, 3)
        V = self.GenerateWireRaysV()
        self.nrays, shape = V.shape[0], V.shape
        l = self.l_wire
        X = np.zeros(shape)
        #Added to rotate wires, but never implemented
        L = np.random.uniform(-l/2,l/2,self.nrays)
        X[:,1] = L*np.sin(tht)
        X[:,2] = L*np.cos(tht)
        X = X + shift
        V = self.GenerateWireRaysV()
        X, V = self.DirectRays(X,V)
        X = self.TranslateRaysX(X)
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
    
    def GenerateReflFilament_v2(self, shift=np.array([0.,0.,0.])):
        shape = (self.nrays, 3)
        X = np.zeros(shape)
        if(self.rad != 0):
            theta = np.random.uniform(0, 2*pi, self.nrays)
            r = sqrt(np.random.uniform(0, self.rad**2, self.nrays))
            X[:,2] = r*cos(theta)
            X[:,1] = r*sin(theta)
        X = X + shift
        V = self.GenerateWireRaysV()
        X, V = self.DirectRays(X,V)
        X = self.TranslateRaysX(X)
        return X,V
    
    def GenerateFilament(self,tht=np.pi/2, shift=np.array([0.,0.,0.])):
        #Generate wire rays, reflector rays, or both
        if(self.wire):
            X, V = self.GenerateWire_v2(tht,shift)
            #X, V = self.GenerateWire(shift)
        if(self.reflector):
            Xf,Vf = self.GenerateReflFilament_v2(shift)
            if(self.wire):
                X = np.concatenate((X,Xf),axis=0)
                V = np.concatenate((V,Vf),axis=0)
            else:
                X,V = Xf,Vf
        return X,V

    def GenerateRays(self):
        #Can generate light from any filament (or combination)
        if(cf.filament['F1']):
            X,V = self.GenerateFilament(shift=np.array([0.,-self.sep/2, self.sep/2]))
            cf.logger.info(f'F1:Added')
        if(cf.filament['F2']):
            cf.logger.info(f'F2:Added')
            if(cf.filament['F1'] == False):
                X,V = self.GenerateFilament(shift=np.array([0.,self.sep/2, self.sep/2]))
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
