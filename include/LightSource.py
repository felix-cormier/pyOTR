import numpy as np
from numpy import sin, cos, pi
#Class implementation for...
    #Beam
    #Filament backlights
    #Lasers
#Sources are generated at the origin and then rotated and repositioned 
#Multipled sources can be used at once, generate multiple then concatenate

class LightSource:
    def __init__(self, nrays=1_000_000, name=None):
        self.name = name
        self.nrays = nrays
        self.angles= np.zeros(3)
        self.M = self.GetM()
        self.x = 0.
        self.y = 0.
        self.z = 0.

    def SetName(self, name):
        self.name = name

    def GetName(self):
        return self.name

    def GetPosition(self):
        return self.X

    def GetOrientation(self):
        return self.angles
    
    def SetOrientation(self, angles):
        self.angles = angles
        self.M = self.GetM()

    def GetM(self):
        #yaw, pitch and roll - easier for placement
        xrot, yrot, zrot = self.angles
        # Rotation around the x axis
        R1 = np.array([[1, 0, 0],
                       [0, cos(xrot), -sin(xrot)],
                       [0, sin(xrot), cos(xrot)]])
        # Rotation around the y axis
        R2 = np.array([[cos(yrot), 0, sin(yrot)],
                       [0, 1, 0],
                       [-sin(yrot), 0, cos(yrot)]])
        # Rotation around the z axis
        R3 = np.array([[cos(zrot), -sin(zrot), 0],
                       [sin(zrot), cos(zrot), 0],
                       [0, 0, 1]])
        return R3.dot(R2.dot(R1))
        #return R1.dot(R2.dot(R3))


    def Place(self, xcent, ycent, zcent, angles=np.zeros(3)):
        self.x = xcent
        self.y = ycent
        self.z = zcent
        self.SetOrientation(angles)
    
    def OrientRaysV(self, Vorig):
        return Vorig.dot(self.M)   
    
    def OrientRaysX(self,Xorig):
        X = Xorig.dot(self.M)
        return X + np.array([self.x,self.y,self.z])
    
    def TranslateRaysX(self,Xorig):
        return Xorig + np.array([self.x,self.y,self.z])
