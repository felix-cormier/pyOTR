import numpy as np
from OTR.include.OpticalComponent import OpticalComponent


class ImagePlane(OpticalComponent):
    def __init__(self, R=20., name='ImagePlane'):
        OpticalComponent.__init__(self, name=name)
        self.name = 'ImagePlane'
        self.R = R

    def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get the interaction points X and the V reflected:
        X, V = self.PlaneIntersect(X, V)
        # Here we actually do not transform back to Global Coords, since it makes more sense to plot things
        # with respect to the Image Plane.
        #X = self.transform_coord.TransfrmPoint(X, inv=True)
        #V = self.transform_coord.TransfrmVec(V, inv=True)
        return X, V

    def PlaneIntersect(self, X, V):
        z = X[:, 2]     # selects the z component of all rays
        Vz = V[:, 2]    # selects the Vz component of all rays
        eps = 10e-5  # tolerance
        Z = 0.       # Position of Plane in Plane Reference System
        AtPlane = np.abs(z - Z) > eps
        HasV = np.abs(Vz) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        z = z[GoodRays]
        Vz = Vz[GoodRays]
        X = X[GoodRays]
        V = V[GoodRays]
        # Only keep rays that are pointing at the Plane:
        ToPlane = Vz / np.abs(Vz) != (z - Z) / np.abs(z - Z)
        z = z[ToPlane]
        Vz = Vz[ToPlane]
        X = X[ToPlane]
        V = V[ToPlane]
        # interaction at z = 0, by construction:
        t = (Z - z) / Vz
        assert (t > 0).all()
        t.resize(t.shape[0], 1)
        # Propagate the rays to the interaction point:
        X = X + V * t
        assert (np.abs(X[:, 2] - Z) < eps).all()
        # Only keep rays that cross the Plane:
        keep = np.diag(X.dot(X.T)) < (self.R**2)
        X = X[keep]
        V = V[keep]
        assert X.shape == V.shape
        return X, V
