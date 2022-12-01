import numpy as np
from numpy import cos, sin, sqrt, pi, exp
from scipy.stats import truncnorm
from Beam.Modules.Config import generatorConfig
from OTR.include.LightSource import LightSource


class Filament(LightSource):
    def __init__(self, generator_options, factor=0.5, name=None):
        LightSource.__init__(self, generator_options, name=name)
        self.settings = generator_options
        self.nrays = self.settings.nrays
        self.conversion = factor
        self.rad = 55.0/2

        self.sep = 40.0
        self.l_wire = 10.5*self.conversion
        self.wire = False #true = on
        self.reflector = True #true = on
        '''
        if(self.reflector):
            if self.settings.filament['Vtype'] == 'parallel':
                self.settings.logger.info(f'Selected filament light source with parallel rays')
            elif self.settings.filament['Vtype'] == 'divergent':
                self.settings.logger.info(f'Selected filament light source light source with div=' + str(self.settings.filament['spread']))
        '''

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
        Vtype = self.settings.filament['Vtype']
        spread = self.settings.filament['spread']
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
            self.settings.logger.info('Unknown velocity distribution...exiting')
            sys.exit()
        return V
    
    def GenerateWire(self, shift=np.array([0.,0.,0.])):
        shape = (self.nrays, 3)
        V = self.GenerateWireRaysV_v2()
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

    def GenerateReflFilament(self, shift=np.array([0.,0.,0.])):
        shape = (self.nrays, 3)
        print(f"nrays: {self.nrays}")
        X = np.zeros(shape)
        if(self.rad != 0):
            theta = np.random.uniform(0, 2*pi, self.nrays)
            r = sqrt(np.random.uniform(0, self.rad**2, self.nrays))
            X[:,2] = r*cos(theta)
            X[:,1] = r*sin(theta)
            
        dummy_V=np.ones(X.shape)
        self.settings.diagnosticImage(X,dummy_V, 'Gen_1')

        X = X + shift
        dummy_V=np.ones(X.shape)
        self.settings.diagnosticImage(X,dummy_V, 'Gen_2')
        X = self.OrientRaysX(X)
        dummy_V=np.ones(X.shape)
        self.settings.diagnosticImage(X,dummy_V, 'Gen_3')
        V = self.GenerateReflRaysV(X.shape)
        V = self.OrientRaysV(V)
        return X,V
    
    def GenerateFilament(self, shift=np.array([0.,0.,0.])):
        if(self.wire):
            X, V = self.GenerateWire(shift)
        if(self.reflector):
            Xf,Vf = self.GenerateReflFilament(shift)
            if(self.wire):
                X = np.concatenate((X,Xf),axis=0)
                V = np.concatenate((V,Vf),axis=0)
            else:
                X,V = Xf,Vf
        return X,V

    def GenerateRays(self):
        if(self.settings.filament['F1']):
            X,V = self.GenerateFilament(shift=np.array([0.,self.sep/2, -self.sep/2]))
            self.settings.diagnosticImage(X,V, 'F1', isGenerator = True)
            #X,V = self.GenerateFilament()
            #self.settings.logger.info(f'F1:Added')
        if(self.settings.filament['F2']):
            #self.settings.logger.info(f'F2:Added')
            if(self.settings.filament['F1'] == False):
                X,V = self.GenerateFilament(shift=np.array([0.,self.sep/2, self.sep/2]))
                #X,V = self.GenerateFilament(shift=np.array([0.,0., 0.]))
            else:
                X2,V2 = self.GenerateFilament(shift=np.array([0.,self.sep/2, self.sep/2]))
                self.settings.diagnosticImage(X2,V2, 'F2', isGenerator = True)
                X = np.concatenate((X,X2),axis=0)
                V = np.concatenate((V,V2),axis=0)
        if(self.settings.filament['F3']):
            #self.settings.logger.info(f'F3:Added')
            if(self.settings.filament['F1'] == False and self.settings.filament['F2'] == False):
                X,V = self.GenerateFilament(shift=np.array([0.,-self.sep/2, self.sep/2]))
            else:
                X3,V3 = self.GenerateFilament(np.array([0.,-self.sep/2, self.sep/2]))
                self.settings.diagnosticImage(X3,V3, 'F3', isGenerator = True)
                X = np.concatenate((X,X3),axis=0)
                V = np.concatenate((V,V3),axis=0)
        return X,V
