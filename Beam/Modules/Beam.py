import numpy as np
import Config as cf


class Beam():
    def __init__(self):
        self.nrays = cf.nrays
        self.x = cf.beam['x']
        self.y = cf.beam['y']
        self.z = cf.beam['z']
        self.cov = cf.beam['cov']
        print("(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")")
        
    def GenerateRaysV(self, n):
        Vtype = cf.beam['Vtype']
        if Vtype == 'parallel':
            V = np.zeros(n)
            V[:, 2] = 1.
            return V
        elif Vtype == 'divergent':
            vx = 0.05 * np.random.uniform(0., 1.)
            vy = 0.05 * np.random.uniform(0., 1.)
            vz = np.sqrt(1 - vx*vx - vy*vy)            
            V = np.random.multivariate_normal(mean, self.cov, n)
            cf.logger.info('Not yet implemented...exiting')
        else:
            cf.logger.info('Unknown velocity distribution...exiting')
        sys.exit()

    def GenerateBeam(self):
        cf.logger.info(f'Selected Proton Beam')
        mean = [self.x, self.y, self.z]
        X = np.random.multivariate_normal(mean, self.cov, self.nrays)
        V = self.GenerateRaysV(X.shape)
        return X, V
    
    def GenerateBackgroundLightV(self,n):
        Vtype = cf.background['Vtype']
        spread = cf.background['spread']
        if Vtype == 'parallel':
            V = np.zeros(n)
            V[:,0] = 1.
            return V
        elif Vtype == 'divergent':
            V = np.zeros(n)
            V[:,1] = np.random.uniform(-spread,spread,V.shape[0])
            V[:,2] = np.random.uniform(-spread,spread,V.shape[0])
            V[:,0] = 1 - V[:,1]*V[:,1] - V[:,2]*V[:,2]
            return V
        else:
            cf.logger.info('Unknown velocity distribution...exiting')
            sys.exit()

    def GenerateBackgroundLight(self):
        cf.logger.info(f'Selected diffuse background light source')
        side = cf.background['length']
        nrays = self.nrays
        X=np.zeros(nrays*3).reshape(nrays,3)
        X[:,1] = np.random.uniform(-side,side,nrays)
        X[:,2] = np.random.uniform(-side,side,nrays)
        X[:,0] = self.x
        V = self.GenerateBackgroundLightV(X.shape)
        print(X[:10])
        print(V[:10])
        return X, V
