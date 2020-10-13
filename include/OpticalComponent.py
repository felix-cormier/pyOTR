import numpy as np
import CoordTrans


class OpticalComponent:
    def __init__(self, name=None):
        self.name = name

    def SetName(self, name):
        self.name = name

    def GetName(self):
        return self.name

    def GetPosition(self):
        return self.X

    def GetOrientation(self):
        return self.angles

    def Place(self, X=np.zeros((1, 3)), angles=np.zeros(3), yrot=False):
        print('Placing component:' + self.name)
        self.X = X
        print('X = ' + str(self.X))
        self.angles = angles
        print('angles = ' + str(self.angles) + ' and yrot = ' + str(yrot))
        print(' ')
        self.transform_coord = CoordTrans.CoordTrans(
            X=self.X, angles=self.angles, yrot=yrot)
