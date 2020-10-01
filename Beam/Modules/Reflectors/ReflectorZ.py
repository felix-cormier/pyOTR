import numpy as np
from OpticalComponent import OpticalComponent


class Reflector(OpticalComponent):
    def __init__(self, name=None):
        OpticalComponent.__init__(self, name=name)
        self.diam = 50.

    def PlaneTransport(self, X, V):
        X, V = self.PlaneIntersect(X, V)
        return X, self.PlaneReflect(V)


class PerfectReflector(Reflector):
    def __init__(self, normal=np.array([[0., 0., 1.]]), R=20., name='PerfectReflector'):
        Reflector.__init__(self, name=name)
        self.normal = normal
        self.R = R

    def PlaneReflect(self, V):
        return V - 2 * V.dot(self.normal.T) * self.normal

    def PlaneIntersect(self, X, V):
        z = X[:, 2]     # selects the y component of all rays
        V2 = V[:, 2]    # selects the Vz component of all rays
        eps = 10e-5  # tolerance
        Z = 0.       # Position of reflection plane in reflector ref. system
        AtPlane = np.abs(z - Z) > eps
        HasV = np.abs(Vz) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        z = z[GoodRays]
        Vz = Vz[GoodRays]
        X = X[GoodRays]
        V = V[GoodRays]
        #Only keep rays that are pointing at the reflector:
        #Final y - initial should be negative, like the velocity
        ToPlane = Vz/np.abs(Vz) == (Z - z) / np.abs(Z - z)
        z = z[ToPlane]
        Vz = Vz[ToPlane]
        X = X[ToPlane]
        V = V[ToPlane]
        #Interaction at y = 0, by construction:
        t = (Z - z)/Vz
        assert (t > 0).all()
        t.resize(t.shape[0], 1)
        # Propagate the rays to the interaction point:
        X = X + V * t
        assert (np.abs(X[:, 2] - Z) < eps).all()
        # Only keep rays that cross the (currently circular) reflector:
        keep = np.diag(X.dot(X.T)) < (self.R**2)
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
        print('after reflector v')
        print(V[:10])
        return X, V


