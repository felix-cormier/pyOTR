import Config as cf
import Mirror
import ImagePlane
import OpticalSystem
import numpy as np


def GetGeometry():

    system = OpticalSystem.OpticalSystem()
    
    M0 = Mirror.PlaneMirror(
        normal=cf.M0['normal'], R=cf.M0['R'], name=cf.M0['name'])

    M1 = Mirror.ParaMirror(f=cf.M1['f'], H=cf.M1['H'], D=cf.M1['D'],
                           rough=cf.M1['rough'], name=cf.M1['name'])

    M2 = Mirror.ParaMirror(f=cf.M2['f'], H=cf.M2['H'], D=cf.M2['D'],
                           rough=cf.M1['rough'], name=cf.M2['name'])

    M3 = Mirror.ParaMirror(f=cf.M3['f'], H=cf.M3['H'], D=cf.M3['D'],
                           rough=cf.M1['rough'], name=cf.M3['name'])

    M4 = Mirror.ParaMirror(f=cf.M4['f'], H=cf.M4['H'], D=cf.M4['D'],
                           rough=cf.M1['rough'], name=cf.M4['name'])

    image = ImagePlane.ImagePlane(R=cf.camera['R'], name=cf.camera['name'])

    M0.Place(X=cf.M0['X'], angles=cf.M0['angles'], yrot=cf.M0['yrot'])
    M1.Place(X=cf.M1['X'], angles=cf.M1['angles'])
    M2.Place(X=cf.M2['X'], angles=cf.M2['angles'])
    M3.Place(X=cf.M3['X'], angles=cf.M3['angles'])
    M4.Place(X=cf.M4['X'], angles=cf.M4['angles'])

    if(cf.image_loc == 0):
        image.Place(X=cf.image_foil['X'], angles=cf.image_foil['angles'], yrot = cf.image_foil['yrot'])
        system.AddComponent(image)
    elif(cf.image_loc == 1):
        image.Place(X=cf.image_m1['X'], angles=cf.image_m1['angles'], yrot = cf.image_m1['yrot'])
        system.AddComponent(M1)
        system.AddComponent(image)
    elif(cf.image_loc == 2):
        image.Place(X=cf.image_m2f['X'], angles=cf.image_m2f['angles'], yrot = cf.image_m2f['yrot'])
        system.AddComponent(M1)
        system.AddComponent(M2)
        system.AddComponent(image)
    elif(cf.image_loc == 3):
        image.Place(X=cf.image_m3['X'], angles=cf.image_m3['angles'], yrot = cf.image_m3['yrot'])
        system.AddComponent(M1)
        system.AddComponent(M2)
        system.AddComponent(M3)
        system.AddComponent(image)
    elif(cf.image_loc == 4):
        image.Place(X=cf.image_m4f['X'], angles=cf.image_m4f['angles'], yrot=cf.image_m4f['yrot'])
        system.AddComponent(M1)
        system.AddComponent(M2)
        system.AddComponent(M3)
        system.AddComponent(M4)
        system.AddComponent(image)
    else:
        image.Place(X=cf.camera['X'], angles=cf.camera['angles'], yrot = cf.camera['yrot'])
        system.AddComponent(M1)
        system.AddComponent(M2)
        system.AddComponent(M3)
        system.AddComponent(M4)
        system.AddComponent(image)

    return system
