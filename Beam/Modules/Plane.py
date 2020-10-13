import numpy as np
from OpticalComponent import OpticalComponent


class Plane(OpticalComponent):
    def __init__(self, name=None):
        OpticalComponent.__init__(self, name=name)
        self.diam = 50.

    def PlaneTransport(self, X, V):
        self.PrintAxes()
        X, V = self.PlaneIntersect(X, V)
        return X, self.PlaneReflect(V)


class PerfectPlane(Plane):
    def __init__(self, normal=np.array([[1., 0., 0.]]), R=20., name='PerfectPlane'):
        Plane.__init__(self, name=name)
        self.normal = normal
        self.R = R
        print("Created:" + name + " with normal = " + str(self.normal))

    def PrintAxes(self):
        axes = np.array([[1,0,0],[0,1,0],[0,0,1]])
        print('X-Y-Z axes in global coordinates')
        print(axes)
        print(' ')
        axes = self.transform_coord.TransfrmVec(axes)
        print('Global X-Y-Z axes in reflector coordinates')
        print(axes)
        print(' ')
        print('X-Y-Z rotated back into global coordinates')
        axes = self.transform_coord.TransfrmVec(axes,inv=True)
        print(axes)
        print(' ')
        vec_x = np.array([1,0,0.])
        print('+X-directed vector:')
        print(vec_x)
        neg_vec_x = np.array([-1.,0,0.])
        print('... reflected')
        print(self.PlaneReflect(vec_x))
        print(' ')
        print('-X-directed vector:')
        print(neg_vec_x)
        print('... reflected')
        print(self.PlaneReflect(neg_vec_x))

        return 0


    def PlaneReflect(self, V):
        refl_vec = V - 2 * V.dot(self.normal.T) * self.normal
        return V - 2 * V.dot(self.normal.T) * self.normal

    def PlaneIntersect(self, X, V):
        x = X[:, 0]     # selects the x component of all rays
        Vx = V[:, 0]    # selects the Vx component of all rays
        eps = 10e-5  # tolerance
        Xx = 0.       # Position of reflection plane in reflector ref. system
        AtPlane = np.abs(x - Xx) > eps
        HasV = np.abs(Vx) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        x = x[GoodRays]
        Vx = Vx[GoodRays]
        X = X[GoodRays]
        V = V[GoodRays]
        #Only keep rays that are pointing at the reflector:
        #Final y - initial should be negative, like the velocity
        ToPlane = Vx/np.abs(Vx) == (Xx - x) / np.abs(Xx - x)
        x = x[ToPlane]
        Vx = Vx[ToPlane]
        X = X[ToPlane]
        V = V[ToPlane]
        #Interaction at y = 0, by construction:
        t = (Xx - x)/Vx
        assert (t > 0).all()
        t.resize(t.shape[0], 1)
        # Propagate the rays to the interaction point:
        X = X + V * t
        assert (np.abs(X[:, 0] - Xx) < eps).all()
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
        print(' ')
        print('Laser position at Plane (reflector coords):')
        print(X)
        print('Laser velocity at Plane (reflector coords):')
        print(V)
        print(' ')
        # Transform back to the global coords:
        X = self.transform_coord.TransfrmPoint(X, inv=True)
        V = self.transform_coord.TransfrmVec(V, inv=True)
        print(' ')
        print('Laser position at Plane (global coords):')
        print(X)
        print('Laser velocity at Plane (global coords):')
        print(V)
        print(' ')
        return X, V


