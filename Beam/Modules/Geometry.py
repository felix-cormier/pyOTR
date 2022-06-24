from Beam.Modules.Config import generatorConfig
import Beam.Modules.Foil
import Beam.Modules.Mirror
import include.ImagePlane
import include.OpticalSystem
import Beam.Modules.Reflector
import Beam.Modules.Plane
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

    M1 = Mirror.ParaMirror(f=cf.M1['f'], H=cf.M1['H'], D=cf.M1['D'],
                           rough=cf.M1['rough'], name=cf.M1['name'])

    M2 = Mirror.ParaMirror(f=cf.M2['f'], H=cf.M2['H'], D=cf.M2['D'],
                           rough=cf.M2['rough'], name=cf.M2['name'])

    foil = Foil.CalibrationFoil(normal=np.array([[0., 1., 0.]]), diam=50.,
                hole_dist=7., hole_diam=1.2, name=cf.foil['name'], cross=cf.background['cfoil'])
    
  #  M0 = Mirror.PlaneMirror(
  #      normal=cf.M0['normal'], R=cf.M0['R'], name=cf.M0['name'])
    
    image = ImagePlane.ImagePlane(R=cf.camera['R'], name=cf.camera['name'])


    
 #   M0.Place(X=cf.M0['X'], angles=cf.M0['angles'], yrot=cf.M0['yrot'])
   
    reflector.Place(X=cf.reflector['X'], angles=cf.reflector['angles'], yrot=cf.reflector['yrot'])
    
 #   plane.Place(X=cf.plane['X'], angles=cf.plane['angles'], yrot=cf.plane['yrot'])
  
    foil.Place(X=cf.foil['X'], angles=cf.foil['angles'])

    M1.Place(X=cf.M1['X'], angles=cf.M1['angles'])
    M2.Place(X=cf.M2['X'], angles=cf.M2['angles'])
   
    image.Place(X=cf.camera['X'], angles=cf.camera['angles'], yrot=cf.camera['yrot'])

    system = OpticalSystem.OpticalSystem()
  #  system.AddComponent(plane)
    system.AddComponent(reflector)
    system.AddComponent(foil)
    system.AddComponent(M1)
    system.AddComponent(M2)
    system.AddComponent(image)
    return system
