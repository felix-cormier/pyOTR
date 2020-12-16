import numpy as np
import Config as cf
from OpticalComponent import OpticalComponent


class Reflector(OpticalComponent):
    def __init__(self, name=None):
        OpticalComponent.__init__(self, name=name)
        self.diam = 50.

    def PlaneTransport(self, X, V):
        X, V = self.PlaneIntersect(X, V)
        return X, self.PlaneReflect(V)


class PerfectReflector(Reflector):
    def __init__(self, normal=np.array([[0., 1., 0.]]), R=20., name='PerfectReflector'):
        Reflector.__init__(self, name=name)
        self.normal = normal
        self.R = R

    def PlaneReflect(self, V):
        return V - 2 * V.dot(self.normal.T) * self.normal

    def PlaneIntersect(self, X, V):
        y = X[:, 1]     # selects the y component of all rays
        Vy = V[:, 1]    # selects the Vz component of all rays
        eps = 10e-5  # tolerance
        Xy = 0.       # Position of reflection plane in reflector ref. system
        AtPlane = np.abs(y - Xy) > eps
        HasV = np.abs(Vy) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        y = y[GoodRays]
        Vy = Vy[GoodRays]
        X = X[GoodRays]
        V = V[GoodRays]
        #Only keep rays that are pointing at the reflector:
        #Final y - initial should be negative, like the velocity
        ToPlane = Vy/np.abs(Vy) == (Xy - y) / np.abs(Xy - y)
        y = y[ToPlane]
        Vy = Vy[ToPlane]
        X = X[ToPlane]
        V = V[ToPlane]
        #Interaction at y = 0, by construction:
        t = (Xy - y)/Vy
        assert (t > 0).all()
        t.resize(t.shape[0], 1)
        # Propagate the rays to the interaction point:
        X = X + V * t
        assert (np.abs(X[:, 1] - Xy) < eps).all()
        # Only keep rays that cross the (currently circular) reflector:
        keepX = np.abs(X[:,0]) < 55
        keepZ = np.abs(X[:,2]) < 25
        keep = keepX & keepZ
        X = X[keep]
        V = V[keep]
        assert X.shape == V.shape
        return X, V
    
    def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get the interaction points X and the V reflected:
        X, V = self.PlaneTransport(X, V)
        # Transform back to the global coords:
        X = self.transform_coord.TransfrmPoint(X, inv=True)
        V = self.transform_coord.TransfrmVec(V, inv=True)
        return X, V

class ConnectedReflector(Reflector):
    def __init__(self, normal=np.array([[0., 1., 0.]]), R=20., name='ConnectedReflector'):
        Reflector.__init__(self, name=name)
        self.normal = normal
        self.R = R

    def GetGlobalNormal(self, vi, vf):
        #After a couple tests, seems to be working!
        #Note: keeping vf doesn't matter for this function because we've 
        #selected the y-axis -- a general version should be written
        N = np.zeros(3)
        
        if(vi[1] != 0):
            N[1] = np.sqrt(1./(1. + (vi[2]/vi[1])**2 + ((vi[0]-1.)/vi[1])**2))
            N[0] = (vi[0]-1)*N[1]/vi[1]
            N[2] = vi[2]*N[1]/vi[1]
            return N
        
        elif(vi[2] != 0):
            N[2] = np.sqrt(1./(1. + (vi[1]/vi[2])**2 + ((vi[0]-1.)/vi[2])**2))
            N[0] = (vi[0]-1)*N[2]/vi[2]
            N[1] = vi[1]*N[2]/vi[2]
            return N
        
        N = np.array([1,0,0])
        return N
    
    def GetGlobalNormal_v2(self, vi, vf):
        Dx = vi[0] - vf[0]
        Dy = vi[1] - vf[1]
        Dz = vi[2] - vf[2]

        N = np.zeros(3)
        if(Dx != 0):
            N[0] = np.sqrt(1./(1. + (Dy/Dx)**2 + (Dz/Dx)**2))
            N[1] = N[0]*Dy/Dx
            N[2] = N[0]*Dz/Dx
            print("N = ")
            print(N)
            return N
        elif(Dy != 0):
            N[1] = np.sqrt(1./(1. + (Dx/Dy)**2 + (Dz/Dy)**2))
            N[0] = N[1]*Dx/Dy
            N[2] = N[1]*Dz/Dy
            print("N = ")
            print(N)
            return N
        elif(Dz != 0):
            N[2] = np.sqrt(1./(1. + (Dx/Dz)**2 + (Dy/Dz)**2))
            N[0] = N[2]*Dx/Dz
            N[1] = N[2]*Dy/Dz
            print("N = ")
            print(N)
            return N
            
        print('There has been an error')
        return N

    def CalcSetM(self):
        dXi = cf.reflector['Xl']-cf.laser['X']
        dXf = cf.reflector['Xf']-cf.reflector['Xl']
        Vi = dXi/np.sqrt(dXi[0]**2 + dXi[1]**2 + dXi[2]**2) #normalize
        Vf = dXf*(1/np.sqrt(dXf[0]**2 + dXf[1]**2 + dXf[2]**2)) #normalize
        
        n = self.GetGlobalNormal_v2(Vi,Vf)
        y = np.array([0.,1.,0.])
        r = np.cross(y,n) #axis of rotation
        r = r/np.sqrt(r[0]**2 + r[1]**2 + r[2]**2)
        
        C = np.dot(y,n)
        t = 1-C
        tht = np.arccos(C)
        S = np.sin(tht)
        M = np.array([[(t*r[0]*r[0] + C), (t*r[0]*r[1] - S*r[2]), (t*r[0]*r[2] + S*r[1])],
                  [t*r[0]*r[1] + S*r[2], t*r[1]*r[1] + C, t*r[1]*r[2] - S*r[0]],
                  [t*r[0]*r[2]-S*r[1], t*r[1]*r[2] + S*r[0], t*r[2]*r[2] + C]])
    
        self.transform_coord.M = M.T
        return M.T

    def PlaneReflect(self, V):
        return V - 2 * V.dot(self.normal.T) * self.normal

    def PlaneIntersect(self, X, V):
        y = X[:, 1]     # selects the y component of all rays
        Vy = V[:, 1]    # selects the Vz component of all rays
        eps = 10e-5  # tolerance
        Xy = 0.       # Position of reflection plane in reflector ref. system
        AtPlane = np.abs(y - Xy) > eps
        HasV = np.abs(Vy) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        y = y[GoodRays]
        Vy = Vy[GoodRays]
        X = X[GoodRays]
        V = V[GoodRays]
        #Only keep rays that are pointing at the reflector:
        #Final y - initial should be negative, like the velocity
        ToPlane = Vy/np.abs(Vy) == (Xy - y) / np.abs(Xy - y)
        y = y[ToPlane]
        Vy = Vy[ToPlane]
        X = X[ToPlane]
        V = V[ToPlane]
        #Interaction at y = 0, by construction:
        t = (Xy - y)/Vy
        assert (t > 0).all()
        t.resize(t.shape[0], 1)
        # Propagate the rays to the interaction point:
        X = X + V * t
        assert (np.abs(X[:, 1] - Xy) < eps).all()
        # Only keep rays that cross the (currently circular) reflector:
        keepX = np.abs(X[:,0]) < 55
        keepZ = np.abs(X[:,2]) < 25
        keep = keepX & keepZ
        X = X[keep]
        V = V[keep]
        assert X.shape == V.shape
        return X, V
    
    def RaysTransport(self, X, V):
        # Go to local coords:
        m = self.CalcSetM()
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get the interaction points X and the V reflected:
        X, V = self.PlaneTransport(X, V)
        # Transform back to the global coords:
        X = self.transform_coord.TransfrmPoint(X, inv=True)
        V = self.transform_coord.TransfrmVec(V, inv=True)
        return X, V

