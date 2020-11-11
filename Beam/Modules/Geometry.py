import Config as cf
import Foil
import Mirror
import ImagePlane
import OpticalSystem
import Reflector
import Plane
import numpy as np


def GetGeometry():

    #foil = Foil.MetalFoil(normal=cf.foil['normal'], diam=cf.foil['D'],
     #                            name=cf.foil['name'])
    
    #foil = Foil.DimpledFoil(normal=cf.foil['normal'], diam=cf.foil['D'],eps=cf.foil['eps'],
    #                             name=cf.foil['name'])
    
    #plane = Plane.PerfectPlane(
     #   normal=cf.plane['normal'], R=cf.plane['R'], name=cf.plane['name'])

    reflector = Reflector.PerfectReflector(
        normal=cf.reflector['normal'], R=cf.reflector['R'], name=cf.reflector['name'])
    
    foil = Foil.CalibrationFoil(normal=np.array([[0., 1., 0.]]), diam=50.,
                hole_dist=7., hole_diam=1.2, name=cf.foil['name'], cross=cf.background['cfoil'])
    
  #  M0 = Mirror.PlaneMirror(
  #      normal=cf.M0['normal'], R=cf.M0['R'], name=cf.M0['name'])
    
    image = ImagePlane.ImagePlane(R=cf.camera['R'], name=cf.camera['name'])


    
 #   M0.Place(X=cf.M0['X'], angles=cf.M0['angles'], yrot=cf.M0['yrot'])
   
    reflector.Place(X=cf.reflector['X'], angles=cf.reflector['angles'], yrot=cf.reflector['yrot'])
    
 #   plane.Place(X=cf.plane['X'], angles=cf.plane['angles'], yrot=cf.plane['yrot'])
  
    foil.Place(X=cf.foil['X'], angles=cf.foil['angles'])
   
    image.Place(X=cf.camera['X'], angles=cf.camera['angles'], yrot=cf.camera['yrot'])

    system = OpticalSystem.OpticalSystem()
  #  system.AddComponent(plane)
    system.AddComponent(reflector)
  #  system.AddComponent(foil)
    system.AddComponent(image)
    return system
