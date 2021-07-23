#import importlib
#importlib.invalidate_caches()
import concurrent.futures
import numpy as np
import Config as cf
import Beam
import Laser
import Laser_v2
import Filament
import Geometry
import time
from PrepareData import PrepareData

@cf.timer
def SimulateBeam(X, V, system):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(system.TraceRays, X, V)
        for i, result in enumerate(results):
            if i % 100 == 0:
                cf.logger.debug(f'Running data piece: {i}')
            x, v = result
            assert x.shape == v.shape
            if i == 0:
                Xf = np.array(x)
                Vf = np.array(v)
            else:
                Xf = np.concatenate((Xf, x), axis=0)
                Vf = np.concatenate((Vf, v), axis=0)

    Xf = np.array(Xf)
    Vf = np.array(Vf)
    return Xf, Vf

if __name__ == '__main__':

    cf.GetTime()
    # Get details about the beam:
    #beam = Beam.Beam()
    #laser = Laser.Laser(rad=cf.laser['rad'], nrays=1_000)
    #laser.Place(cf.laser['X'][0], cf.laser['X'][1], cf.laser['X'][2], cf.laser['angles'])
    
    filament = Filament.Filament(nrays = 1_000_000)
    filament.Place(cf.filament['X'][0],cf.filament['X'][1], cf.filament['X'][2], cf.filament['angles'])

    if(cf.source == 'protons'):
        X, V = beam.GenerateBeam()
    elif(cf.source == 'filament'):
        start = time.time()
       # X, V = beam.GenerateFilamentBacklight_v1()
        X, V = beam.GenerateFilament()
        end = time.time()
        print(f"Filament backlight generation time: {end - start}")
    elif(cf.source == 'filament_v2'):
        start = time.time()
        X,V = filament.GenerateRays()
        print(X[:10])
        print(V[:10])
        end = time.time()
        print(f"Filament backlight generation time: {end - start}")
    elif(cf.source == 'laser'):
        start = time.time()
        X, V = laser.GenerateRays_v2()
        #X, V = laser.GenerateRays()
        end = time.time()
        #print(f"Laser generation time: {end - start}")
    else:
        print('Not a valid source')
    
    #Save initial distribution
    if cf.save:
        if(cf.source == 'protons'):
            np.save(f'{cf.name}_protonsX', X)
            np.save(f'{cf.name}_protonsV', V)
        elif(cf.source == 'filament'):
            np.save(f'{cf.name}_filamentX', X)
            np.save(f'{cf.name}_filamentV', V)

    if cf.chunck > 0:
        X, V  = PrepareData(X, V, chunck=cf.chunck)


    # Get the Foil Geometry: 
    system = Geometry.GetGeometry()
    # Run simulation:
    X, V = SimulateBeam(X, V, system)
    print(X[:10])
    print(V[:10])

    if cf.save:
        np.save(f'{cf.name}_X', X)
        np.save(f'{cf.name}_V', V)
        pms = open(cf.pm_name + '_pm.txt', 'w')   
        pms.write("#hat{#psi} = " + str(cf.pm['psi']))
    cf.GetTime(start=False)


