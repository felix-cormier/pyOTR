import numpy as np
from OpticalComponent import OpticalComponent


class Mirror(OpticalComponent):
    def __init__(self, name=None):
        OpticalComponent.__init__(self, name=name)

    def PlaneTransport(self, X, V):
        X, V = self.PlaneIntersect(X, V)
        return X, self.PlaneReflect(V)

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


class PlaneMirror(Mirror):
    def __init__(self, normal=np.array([[0., 0., -1.]]), R=20., name='PlaneMirror'):
        Mirror.__init__(self, name=name)
        self.normal = normal
        self.R = R

    def PlaneReflect(self, V):
        return V - 2 * V.dot(self.normal.T) * self.normal

    def PlaneIntersect(self, X, V):
        z = X[:, 2]     # selects the z component of all rays
        Vz = V[:, 2]    # selects the Vz component of all rays
        eps = 10e-5  # tolerance
        Z = 0.       # Position of Mirror Plane in Mirror Reference System
        AtPlane = np.abs(z - Z) > eps
        HasV = np.abs(Vz) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        z = z[GoodRays]
        Vz = Vz[GoodRays]
        X = X[GoodRays]
        V = V[GoodRays]
        # Only keep rays that are pointing at the mirror:
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
        # Only keep rays that cross the Spherical Mirror:
        keep = np.diag(X.dot(X.T)) < (self.R**2)
        X = X[keep]
        V = V[keep]
        assert X.shape == V.shape
        return X, V


class ParaMirror(Mirror):
    def __init__(self, f=550., H=120., D=120., rough=False, name=None):
        Mirror.__init__(self, name=name)
        self.f = f  # focal length
        self.f2 = 2. * self.f  # double the focal length
        self.H = H  # Height
        self.R = D / 2.  # Diameter
        self.rough = rough  # simulate roughness?
        self.shift = np.array([[2. * self.f, self.f, 0]])
        self.acc = 1.e-3
        self.niter = 100

    def GetIncrement(self, t, X, V):
        Xr = X + self.shift + (V * t)
        Maux = np.array([-Xr[:, 0], [4. * self.f] * Xr.shape[0], -Xr[:, 2]])
        f = np.diag(Xr.dot(Maux))
        Maux *= 2.
        Maux[1] = Maux[1] / 2
        fprime = np.diag(V.dot(Maux))
        assert f.shape == fprime.shape
        return f, fprime

    def GetNormal(self, X):
        normal = np.array([-(X[:, 0] + self.f2),
                           [self.f2] * X.shape[0],
                           -X[:, 2]]).T
        normal = normal / self.f2
        if self.rough:
            normal = normal + \
                np.random.normal(0., 0.00019, normal.shape[0])
        mag = np.sqrt(np.diag(normal.dot(normal.T)).reshape(normal.shape[0], 1))
        return normal / mag

    def PlaneReflect(self, V):
        return V - 2 * np.diag(V.dot(self.normal.T)).reshape(V.shape[0], 1) * self.normal

    def PlaneIntersect(self, X, V):
        # Initial guess:
        X0 = X
        V0 = V
        t = np.fabs(X0[:, 0]).reshape(X0.shape[0], 1)
        f, fprime = self.GetIncrement(t, X, V)
        i = 0
        while (np.fabs(f) > self.acc).all():
            f, fprime = self.GetIncrement(t, X, V)
            mask = np.fabs(fprime) > self.acc
            f = f[mask]
            fprime = fprime[mask]
            X0 = X0[mask]
            V0 = V0[mask]
            t = t - (f / fprime).reshape(f.shape[0], 1)
            i += 1
            if i > self.niter:
                print(f'Failure to converge in {self.niter} iterations')
                break
        # intersection Point:
        X0 = X0 + (V0 * t)
        # Only keep rays that hit the ParaMirror:
        vertical = np.fabs(X0[:, 1]) < self.H / 2
        circle = np.square(X0[:, 0]) + np.square(X0[:, 2]) < self.R**2
        keep = np.logical_and(vertical, circle)
        X0 = X0[keep]
        V0 = V0[keep]
        self.normal = self.GetNormal(X0)
        return X0, V0
