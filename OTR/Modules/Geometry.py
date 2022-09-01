import OTR.Modules.Mirror as Mirror
import OTR.include.ImagePlane as ImagePlane
import OTR.include.OpticalSystem as OpticalSystem
import numpy as np


def GetGeometry(generator_options):

    M0 = Mirror.PlaneMirror(
        normal=generator_options.M0['normal'], R=generator_options.M0['R'], name=generator_options.M0['name'])

    M1 = Mirror.ParaMirror(f=generator_options.M1['f'], H=generator_options.M1['H'], D=generator_options.M1['D'],
                           rough=generator_options.M1['rough'], name=generator_options.M1['name'])

    M2 = Mirror.ParaMirror(f=generator_options.M2['f'], H=generator_options.M2['H'], D=generator_options.M2['D'],
                           rough=generator_options.M2['rough'], name=generator_options.M2['name'])

    M3 = Mirror.ParaMirror(f=generator_options.M3['f'], H=generator_options.M3['H'], D=generator_options.M3['D'],
                           rough=generator_options.M3['rough'], name=generator_options.M3['name'])

    M4 = Mirror.ParaMirror(f=generator_options.M4['f'], H=generator_options.M4['H'], D=generator_options.M4['D'],
                           rough=generator_options.M4['rough'], name=generator_options.M4['name'])

    image = ImagePlane.ImagePlane(R=generator_options.camera['R'], name=generator_options.camera['name'], generator_options=generator_options)

    #M0.Place(X=generator_options.M0['X'], angles=generator_options.M0['angles'], yrot=generator_options.M0['yrot'])
    M1.Place(X=generator_options.M1['X'], angles=generator_options.M1['angles'])
    M2.Place(X=generator_options.M2['X'], angles=generator_options.M2['angles'])
    M3.Place(X=generator_options.M3['X'], angles=generator_options.M3['angles'])
    M4.Place(X=generator_options.M4['X'], angles=generator_options.M4['angles'])
    image.Place(X=generator_options.camera['X'], angles=generator_options.camera['angles'])

    system = OpticalSystem.OpticalSystem()
    #system.AddComponent(M0)
    system.AddComponent(M1)
    system.AddComponent(M2)
    system.AddComponent(M3)
    system.AddComponent(M4)
    system.AddComponent(image)

    return system
