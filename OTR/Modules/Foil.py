import numpy as np
import LightDist
from OpticalComponent import OpticalComponent



# Generic Foil class, common among all Foils:
class Foil(OpticalComponent):
    def __init__(self, normal=np.array([[0, 1, 0]]), diam=50., name=None):
        OpticalComponent.__init__(self, name=name)
        self.diam = diam
        self.normal = normal

    def GetDiameter(self):
        return self.diam

    def PlaneIntersect(self, X, V):
        y = X[:, 1]     # selects the y component of all rays
        Vy = V[:, 1]    # selects the vy component of all rays
        eps = 10e-5  # tolerance
        Y = 0.       # Position of Foil Plane in Foil Reference System
        AtPlane = np.abs(y - Y) > eps
        HasV = np.abs(Vy) > eps # why would either of these things NOT be true?
        GoodRays = np.logical_and(AtPlane, HasV)
        y = y[GoodRays] #removes all array elements that don't satisfy conditions above
        Vy = Vy[GoodRays]
        X = X[GoodRays]
        V = V[GoodRays]
        # Only keep rays that are pointing at the foil:
        ToPlane = Vy / np.abs(Vy) == (Y - y) / np.abs(Y - y) #final - initial makes more sense
        y = y[ToPlane]
        Vy = Vy[ToPlane]
        X = X[ToPlane]
        V = V[ToPlane]
        # interaction at y = 0, by construction:
        t = (Y - y) / Vy
        assert (t > 0).all() #both asserts just checks
        t.resize(t.shape[0], 1) #turns out weird results without this format
        Xint = X + V * t
        assert (np.abs(Xint[:, 1] - Y) < eps).all()
        # Only keep rays that cross the Foil:
        #1) To get a vector dot product we need a transpose array (Xint.dot(Xint.T))
        #2) Diagonal holds the dot product and all y coordinates at zero by construction
        #3) In foil coordinates, so it's enough to make sure that rays fall within foil circle
        #4) Would Xint[:,0]*Xint[:,0] + ... reduce or increase computations?
        passed = np.diag(Xint.dot(Xint.T)) < (self.diam**2) / 4.
        # Xint, V --> Only those rays that cross the foil
        Xint = Xint[passed]
        V = V[passed]
        assert Xint.shape == V.shape
        return Xint, V
    
    #if PlaneIntersect then PlaneReflect
    def PlaneReflect(self, V):
        #1) V.dot(self.normal.T) = the component of V in the direction normal to the foil plane
        #2) -2*Vdot... etc. --- flip normal to plane component over the plane
        #3) Multiplying again by normal isolates x,y,z components
        return V - 2 * V.dot(self.normal.T) * self.normal

    def PlaneTransport(self, X, V):
        X, V = self.PlaneIntersect(X, V)
        return X, self.PlaneReflect(V)


# Calibration Foil class, inherits from Generic Foil class:
# class CalibrationFoil(OpticalComponent, Foil):
class CalibrationFoil(Foil):
    def __init__(self, normal=np.array([[0., 1., 0.]]), diam=50.,
                 hole_dist=7., hole_diam=1.2, name=None):
        Foil.__init__(self, normal=normal, diam=diam)
        self.hole_dist = hole_dist
        self.hole_diam = hole_diam
        self.holes = self.GetHoles()

    def GetHoles(self):
        import os
        from MakeCalibHoles import MakeHoles
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
        for ihole in self.holes: #in __init__ for Calib Foil
            diff = X - ihole[:-1].reshape(1, 3) #how far particle is from hole
            #diagonal holds vector dotproducts
            #ihole[-1] is the hole diameter
            mask = np.diag(diff.dot(diff.T)) < (ihole[-1]**2) / 4.#? why this specific inequality
            masks.append(mask)#set of true or false
        #Makes a an array of length = number of elements in masks
        passed = np.array([False] * len(masks[0]))
        for mask in masks:
            #why this?
            #shouldn't masks print true whenever passed or masks prints true
            #since passed is always false
            passed = np.logical_or(passed, mask)
        return passed

    def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get X interaction points and V reflected:
        Xint, Vr = self.PlaneTransport(X, V) #but PlaneTransport still removes
        passed = self.PassHole(Xint)
        #remains V if P because goes through, otherwise bounces back as Vr

        Vr = np.array([v if p else vr
                       for p, v, vr in zip(passed, V, Vr)])
        # Transform back to the global coords:
        # Why not just remove rays that don't pass calibration foil here?
        Xint = self.transform_coord.TransfrmPoint(Xint, inv=True)
        Vr = self.transform_coord.TransfrmVec(Vr, inv=True)
        return Xint, Vr
# Metal Foil class, inherits from Generic Foil class:
# class MetalFoil(OpticalComponent, Foil):
class MetalFoil(Foil):
    def __init__(self, normal=np.array([[0., 1., 0.]]), diam=50.,
                 hole_dist=7., hole_diam=1.2, name=None):
        Foil.__init__(self, normal=normal, diam=diam) #child init overrides parent init
        self.reflect=1 #should set in config
        self.dffs=0 #do we need this? should set in config
        self.light = LightDist.LightDist() 

    def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get X interaction points and V reflected:
        Xint, Vr = self.PlaneTransport(X, V) #but PlaneTransport still removes
        Vr = self.light.GetOTRRays(Vr) #should be before, but does this make changes?
        # Transform back to the global coords:
        # Why not just remove rays that don't pass foil here?
        Xint = self.transform_coord.TransfrmPoint(Xint, inv=True)
        Vr = self.transform_coord.TransfrmVec(Vr, inv=True)

        return Xint, Vr
