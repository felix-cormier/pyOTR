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
        # keep = np.diag(X.dot(X.T)) < (self.R**2)
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


