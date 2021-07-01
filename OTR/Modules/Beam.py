import numpy as np
from numpy import sin, cos, pi
import Modules.Config as cf
from scipy.stats import truncnorm


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
        return X, V

    def GenerateBackgroundLightV(self,n):
        Vtype = cf.background['Vtype']
        spread = cf.background['spread']
        if Vtype == 'parallel':
            V = np.zeros(n)
            V[:,0] = 1.
            cf.logger.info(f'Selected parallel background light source')
            return V
        elif Vtype == 'divergent':
            V = np.zeros(n)
            V[:,1] = truncnorm.rvs(-3*spread,3*spread,loc=0,scale=spread,size=V.shape[0])
            V[:,2] = truncnorm.rvs(-3*spread,3*spread,loc=0,scale=spread,size=V.shape[0])
            V[:,0] = np.sqrt(1 - V[:,1]*V[:,1] - V[:,2]*V[:,2])
            cf.logger.info(f'Selected diffuse background light source')
            return V
        else:
            cf.logger.info('Unknown velocity distribution...exiting')
            sys.exit()

    def GenerateFilamentBacklight_v1(self):
        side = cf.background['length']
        nrays = self.nrays
        X=np.zeros(nrays*3).reshape(nrays,3)
        X[:,0] = self.x

        if cf.background['style'] == 'square':
            X[:,1] = np.random.uniform(-side,side,nrays)
            X[:,2] = np.random.uniform(-side,side,nrays)
        elif cf.background['style'] == 'cross':
            w = 2.8 #hole width + 0.4
            i = 0
            while i < nrays:
                y = np.random.uniform(-side,side)
                z = np.random.uniform(-side,side)
                if np.abs(y) <= w/2 or np.abs(z) <= w/2:
                    X[i,1] = y
                    X[i,2] = z
                    i+=1

        V = self.GenerateBackgroundLightV(X.shape)
        return X, V

    def GenerateFilamentBacklight_v2(self):
        side = cf.background['length']
        nrays = self.nrays
        X=np.zeros(nrays*3).reshape(nrays,3)
        X[:,0] = self.x

        if cf.background['style'] == 'square':
            X[:,1] = np.random.uniform(-side,side,nrays)
            X[:,2] = np.random.uniform(-side,side,nrays)
        elif cf.background['style'] == 'cross':
            w = 2.8 #hole width + 0.4
            y1 = np.random.uniform(-side,side,int(nrays/2))
            y2 = np.random.uniform(-w/2,w/2,int(nrays/2))
            X[:,1] = np.concatenate((y1,y2))
            z1 = np.random.uniform(-w/2,w/2,int(nrays/2))
            z2 = np.random.uniform(-side,side,int(nrays/2))
            X[:,2] = np.concatenate((z1,z2))
            #Remove doubles at center using masks
            a = np.abs(X[:,1]) < w/2
            b = np.abs(X[:,2]) < w/2
            c = np.random.choice([True,False],nrays)
            d = ~(a & b)
            e = c | d
            X = X[e]

        V = self.GenerateBackgroundLightV(X.shape)
        return X, V

    def GenerateFilamentBacklightCross(self):
        cf.logger.info(f'Selected diffuse background light source')
        side = cf.background['length']
        w = 2.8 #hole width + 0.4
        nrays = self.nrays
        X=np.zeros(nrays*3).reshape(nrays,3)
        X[:,0] = self.x
        #Loop for y/z
        i = 0
        while i < nrays:
            y = np.random.uniform(-side,side)
            z = np.random.uniform(-side,side)
            if np.abs(y) <= w/2 or np.abs(z) <= w/2:
                X[i,1] = y
                X[i,2] = z
                i+=1

        V = self.GenerateBackgroundLightV(X.shape)
        return X, V

    def GenerateFilamentV(self, tilt):
        phi = np.random.uniform(0,2*pi,self.nrays)
        theta = np.random.uniform(0,pi,self.nrays)
        vx=sin(theta)*cos(phi)
        vy=sin(theta)*sin(phi)
        vz=cos(theta)
        V=np.array([vx,vy,vz]).T
        return V

    def GenerateFilament(self):
        h = 10.0
        tilt = pi/4
        xpos = -10.0
        zpos = 10.0
        r = np.random.uniform(-h/2,h/2,self.nrays)
        x = r*cos(tilt) + xpos
        y = r*sin(tilt)
        z = np.zeros(self.nrays) + zpos
        X = np.array([x,y,z]).T
        V = self.GenerateFilamentV(tilt)
        return X, V
