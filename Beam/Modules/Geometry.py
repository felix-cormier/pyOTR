from Beam.Modules.Config import generatorConfig
import Beam.Modules.Foil as Foil
import Beam.Modules.Mirror as Mirror
import OTR.include.ImagePlane as ImagePlane
import OTR.include.OpticalSystem as OpticalSystem
import Beam.Modules.Reflector as Reflector
import Beam.Modules.Plane as Plane
import numpy as np


def GetGeometry(generator_options):

    print(generator_options.foil['name'])
    #foil = Foil.MetalFoil(generator_options, normal=generator_options.foil['normal'], diam=generator_options.foil['D'],
    #                            name=generator_options.foil['name'])
    
    foil = Foil.DimpledFoil(generator_options, normal=generator_options.foil['normal'], diam=generator_options.foil['D'],eps=generator_options.foil['eps'],
                                 name=generator_options.foil['name'])
    
    #plane = Plane.PerfectPlane(
    #   normal=generator_options.plane['normal'], R=generator_options.plane['R'], name=generator_options.plane['name'])

    reflector = Reflector.PerfectReflector( isGenerator=True,
        normal=generator_options.reflector['normal'], R=generator_options.reflector['R'], name=generator_options.reflector['name'])

    M1 = Mirror.ParaMirror(f=generator_options.M1['f'], H=generator_options.M1['H'], D=generator_options.M1['D'],
                           rough=generator_options.M1['rough'], name=generator_options.M1['name'])

    M2 = Mirror.ParaMirror(f=generator_options.M2['f'], H=generator_options.M2['H'], D=generator_options.M2['D'],
                           rough=generator_options.M2['rough'], name=generator_options.M2['name'])

    #foil = Foil.CalibrationFoil(normal=generator_options.foil['normal'], diam=50., isGenerator=True,
    #            hole_dist=7., hole_diam=1.2, name=generator_options.foil['name'], cross=generator_options.background['cfoil'])
    
  #  M0 = Mirror.PlaneMirror(
  #      normal=generator_options.M0['normal'], R=generator_options.M0['R'], name=generator_options.M0['name'])
    
    image = ImagePlane.ImagePlane(R=generator_options.camera['R'], name=generator_options.camera['name'])


    
 #   M0.Place(X=generator_options.M0['X'], angles=generator_options.M0['angles'], yrot=generator_options.M0['yrot'])
   
    reflector.Place(X=generator_options.reflector['X'], angles=generator_options.reflector['angles'], yrot=generator_options.reflector['yrot'])
    
 #   plane.Place(X=generator_options.plane['X'], angles=generator_options.plane['angles'], yrot=generator_options.plane['yrot'])
  
    foil.Place(X=generator_options.foil['X'], angles=generator_options.foil['angles'])

    #M1.Place(X=generator_options.M1['X'], angles=generator_options.M1['angles'])
    #M2.Place(X=generator_options.M2['X'], angles=generator_options.M2['angles'])
   
    #image.Place(X=generator_options.camera['X'], angles=generator_options.camera['angles'], yrot=generator_options.camera['yrot'])

    system = OpticalSystem.OpticalSystem()
    #system.AddComponent(plane)
    #system.AddComponent(reflector)
    system.AddComponent(foil)
    return system
