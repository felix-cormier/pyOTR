import Config as cf
import Foil
import ImagePlane
import OpticalSystem


def GetGeometry():

    foil = Foil.MetalFoil(normal=cf.foil['normal'], diam=cf.foil['D'],
                                 name=cf.foil['name'])
    image = ImagePlane.ImagePlane(R=cf.camera['R'], name=cf.camera['name'])


    foil.Place(X=cf.foil['X'], angles=cf.foil['angles'])
    image.Place(X=cf.camera['X'], angles=cf.camera['angles'])

    system = OpticalSystem.OpticalSystem()
    system.AddComponent(foil)
   # system.AddComponent(image)
    return system
