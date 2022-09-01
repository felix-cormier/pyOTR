import numpy as np
from numpy import sqrt, pi, exp
import Beam.Modules.LightDist as LightDist
import Beam.Modules.Config as cf
from OTR.include.OpticalComponent import OpticalComponent


# Generic Foil class, common among all Foils:
class Foil(OpticalComponent):
    def __init__(self, isGenerator=False, normal=np.array([[0, 1, 0]]), diam=50., name=None):
        OpticalComponent.__init__(self, isGenerator, name=name)
        self.diam = diam
        self.normal = normal

    def GetDiameter(self):
        return self.diam

    def PlaneIntersect(self, X, V):
        y = X[:, 1]     # selects the y component of all rays, changed from 1
        Vy = V[:, 1]    # selects the vy component of all rays
        eps = 10e-5  # tolerance
        Y = 0.       # Position of Foil Plane in Foil Reference System
        AtPlane = np.abs(y - Y) > eps
        HasV = np.abs(Vy) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        y = y[GoodRays]
        Vy = Vy[GoodRays]
        X = X[GoodRays]
        print("X diagnostics")
        print(np.amin(X[:,0]))
        print(np.amin(X[:,1]))
        print(np.amin(X[:,2]))
        V = V[GoodRays]
        # Only keep rays that are pointing at the foil:
        ToPlane = Vy / np.abs(Vy) != (y - Y) / np.abs(y - Y)
        y = y[ToPlane]
        Vy = Vy[ToPlane]
        X = X[ToPlane]
        print(np.amin(X[:,0]))
        print(np.amin(X[:,1]))
        print(np.amin(X[:,2]))
        V = V[ToPlane]
        # interaction at y = 0, by construction:
        t = (Y - y) / Vy
        #assert (t > 0).all()
        t.resize(t.shape[0], 1)
        Xint = X + V * t
        print(np.amin(Xint[:,0]))
        print(np.amin(Xint[:,1]))
        print(np.amin(Xint[:,2]))
        assert (np.abs(Xint[:, 1] - Y) < eps).all()
        # Only keep rays that cross the Foil:
        passed = np.diag(Xint.dot(Xint.T)) < (self.diam**2) / 4.
        Xint = Xint[passed]
        V = V[passed]
        assert Xint.shape == V.shape
        print(np.amin(Xint[:,0]))
        print(np.amin(Xint[:,1]))
        print(np.amin(Xint[:,2]))
        return Xint, V

    def PlaneReflect(self, V):
        return V - 2 * V.dot(self.normal.T) * self.normal

    def PlaneTransport(self, X, V):
        X, V = self.PlaneIntersect(X, V)
        return X, self.PlaneReflect(V)


# Calibration Foil class, inherits from Generic Foil class:
# class CalibrationFoil(OpticalComponent, Foil):
class CalibrationFoil(Foil):
    def __init__(self, isGenerator=False, normal=np.array([[0., 1., 0.]]), diam=50.,
                 hole_dist=7., hole_diam=1.2, name=None, cross=0):
        Foil.__init__(self, isGenerator, normal=normal, diam=diam, name=name)
        self.hole_dist = hole_dist
        self.hole_diam = hole_diam
        self.holes = self.GetHoles(cross)
        print("holes")

    def GetHoles(self, cross=0):
        if cross == 1 or cross ==2:
            from Beam.Modules.MakeCalibHoles import MakeCross
            return MakeCross(5.657, 4., 1.2, cross)
        import os
        from Beam.Modules.MakeCalibHoles import MakeHoles
        calibfile = 'data/calib_holes.npy'
        if os.path.isfile(calibfile):
            return np.load(calibfile)
        return MakeHoles(fHdist=self.hole_dist, fHdmtr=self.hole_diam)

    def PrintHolePos(self, screen=False):
        print('Using Calibration Holes:')
        for i, ihole in enumerate(self.holes):
            print('{0} {1} {2}'.format(i, ihole[0], ihole[2]))

    def PassHole(self, X):
        masks = []
        for ihole in self.holes:
            test_hole = ihole[:-1].reshape(1, 3) 
            diff = X - ihole[:-1].reshape(1, 3)
            test_1 = diff.dot(diff.T) 
            test_2 = (ihole[-1]**2) / 4. 
            mask = np.diag(diff.dot(diff.T)) < (ihole[-1]**2) / 4.
            masks.append(mask)
        passed = np.array([False] * len(masks[0]))
        for mask in masks:
            passed = np.logical_or(passed, mask)
        return passed

    def diffraction(self, V):

        print("DIFFRACTION")
        print(f'ORIGINAL V: {V.shape}')
        print(V)
        print(np.amin(V[:,0]))
        print(np.amin(V[:,1]))
        print(np.amin(V[:,2]))
        print(np.amax(V[:,0]))
        print(np.amax(V[:,1]))
        print(np.amax(V[:,2]))
        print(V.dtype)

        V_same = V

        change_indices = V[:,0] > 0.99

        mu, sigma = 0., 0.05
        angles_x = np.random.normal(mu, sigma, V.shape[0])
        angles_y = np.random.normal(mu, sigma, V.shape[0])

        prop_z = np.sin(angles_x)
        prop_y = np.sin(angles_y)
        prop_x = 1 - np.sqrt( np.add( np.square(prop_z), np.square(prop_y)))

        V_temp = np.concatenate((prop_x.reshape(prop_x.shape[0],1), prop_y.reshape(prop_y.shape[0],1), prop_z.reshape(prop_z.shape[0],1)), axis=1)
        V[change_indices] = V_temp[change_indices]
        print(f'NEW V: {V.shape}')
        print(V)
        print(V.dtype)

        return V

    def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get X interaction points and V reflected:
        Xint, Vr = self.PlaneTransport(X, V)

        passed = self.PassHole(Xint)
        Vr = np.array([v if p else vr
                       for p, v, vr in zip(passed, V, Vr)])
        # Transform back to the global coords:
        Xint = self.transform_coord.TransfrmPoint(Xint, inv=True)
        Vr = self.transform_coord.TransfrmVec(Vr, inv=True)
        #Vr = self.diffraction(Vr)
        return Xint, Vr

# Metal Foil class, inherits from Generic Foil class:
# class MetalFoil(OpticalComponent, Foil):
class MetalFoil(Foil):
    def __init__(self, generator_options, normal=np.array([[0., 1., 0.]]), diam=50.,
                 hole_dist=7., hole_diam=1.2, name="Metal Foil"):
        Foil.__init__(self, normal=normal, diam=diam, name=name) #child init overrides parent init
        self.reflect=1 #should set in config
        self.dffs=0 #do we need this? should set in config
        self.light = LightDist.LightDist(generator_options) 
        self.settings = generator_options

    def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get X interaction points and V reflected:
        Xint, Vr = self.PlaneTransport(X, V) #but PlaneTransport still removes
        #Vr = self.light.MoyalScatter(Vr)
        Vr = self.light.GetOTRRays4(Vr) #should be before, but does this make changes?
        # Transform back to the global coords:
        # Why not just remove rays that don't pass foil here?
        Xint = self.transform_coord.TransfrmPoint(Xint, inv=True)
        Vr = self.transform_coord.TransfrmVec(Vr, inv=True)

        return Xint, Vr

class DimpledFoil(Foil):
    def __init__(self, generator_options, isGenerator=False, normal=np.array([[0., 1., 0.]]), diam=50.,
                 hole_dist=7., hole_diam=1.2, eps=0., name='Dimpled Foil'):
        Foil.__init__(self, isGenerator, normal=normal, diam=diam, name=name) #child init overrides parent init
        self.reflect=1 #should set in config
        self.dffs=0 #do we need this? should set in config
        self.eps = eps #should set in configuration
        self.light = LightDist.LightDist(generator_options)
        self.settings = generator_options

    def norm_xy(self, X):
        sig = sqrt(self.settings.beam['cov'][0][0])
        xsq = X[:,0]*X[:,0]
        ysq = X[:,1]*X[:,1]
        var = (-1/(2*sig*sig))*(xsq+ysq)
        const = 1/(2*pi*sig*sig)
        g = self.eps*exp(var)
        return g

    def dzbydx(self, X):
        sig = sqrt(self.settings.beam['cov'][0][0])
        dzbydx = 1.- X[:,0]*self.norm_xy(X)/(sig**2)
        #dzbydx = -X[:,0]*self.eps*self.norm_xy(X)/(sig**2)
        return dzbydx


    def dzbydy(self, X):
        sig = sqrt(self.settings.beam['cov'][0][0])
        dzbydy = -X[:,1]*self.norm_xy(X)/(sig**2)
        return dzbydy

    def GetN(self, X):
        #Get the normal vector corresponding to dimpled foil at the locations where the beam crosses the foil
        dzdx = self.dzbydx(X)
        dzdy = self.dzbydy(X)
        A = sqrt(dzdx**2 + dzdy**2 +1)
        nx = -dzdx/A 
        ny = -dzdy/A
        nz = np.ones(X.shape[0])/A
        N = np.array([nx,ny,nz]).T
        N.reshape(X.shape[0],3)
        return N

    def DimpleReflect(self,N,V):
        scale = (V*N).sum(1)
        scale.resize(scale.shape[0], 1)
        return V - 2*(scale)*N

    def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get X interaction points and V reflected:
        Xint, V = self.PlaneIntersect(X, V)
        Xint_global = self.transform_coord.TransfrmPoint(Xint, inv=True)
        #Use Xint positions to define normals
        N = self.GetN(Xint_global)
        N = self.transform_coord.TransfrmVec(N)
        Vr = self.DimpleReflect(N,V)
        Vr = self.light.GetOTRRays4(Vr) 
        # Transform back to the global coords:
        Xint = self.transform_coord.TransfrmPoint(Xint, inv=True)
        Vr = self.transform_coord.TransfrmVec(Vr, inv=True)

        return Xint, Vr
