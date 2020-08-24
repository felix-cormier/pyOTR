import Config as cf
import Foil
import ImagePlane
import OpticalSystem
import numpy as np


def GetGeometry():

   # foil = Foil.MetalFoil(normal=cf.foil['normal'], diam=cf.foil['D'],
    #                             name=cf.foil['name'])

    foil = Foil.CalibrationFoil(normal=np.array([[0., 1., 0.]]), diam=50.,
                hole_dist=7., hole_diam=1.2, name=None, cross=cf.background['cfoil'])

    image = ImagePlane.ImagePlane(R=cf.camera['R'], name=cf.camera['name'])


    foil.Place(X=cf.foil['X'], angles=cf.foil['angles'])
    image.Place(X=cf.camera['X'], angles=cf.camera['angles'])

    system = OpticalSystem.OpticalSystem()
    system.AddComponent(foil)
   # system.AddComponent(image)
    return system
