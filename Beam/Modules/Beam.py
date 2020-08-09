import numpy as np
import Config as cf


class Beam():
    def __init__(self):
        self.nrays = cf.nrays
        self.x = cf.beam['x']
        self.y = cf.beam['y']
        self.z = cf.beam['z']
        self.cov = cf.beam['cov']
        
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
        O = np.zeros(self.nrays)
        return X, V, O
