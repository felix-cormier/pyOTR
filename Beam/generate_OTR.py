

import concurrent.futures
import numpy as np
import Config as cf
import Beam
import Laser
import Filament
import Geometry
import time
from PrepareData import PrepareData

@cf.timer
def SimulateBeam(X, V, system, not_parallel):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        if not_parallel:
            Xf,Vf = system.TraceRays(X,V)
        else:
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
    beam = Beam.Beam()
   # laser = Laser.Laser(rad=0.1, nrays=10_000)
   # laser.Place(-1062.438, 855.654, 0., np.array([0.,0.,cf.Conv(51.066)]))
    
    filament = Filament.Filament(factor=0.5, nrays = cf.nrays)
    filament.Place(-1062.438, 855.654, 0., np.array([0.,0.,cf.Conv(51.066)]))
   # filament.Place(0., 0., 0., np.array([0.,0.,0.]))
    
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
        end = time.time()
        print(f"Filament backlight generation time: {end - start}")
    elif(cf.source == 'laser'):
        start = time.time()
        X, V = laser.GenerateRays()
        end = time.time()
        #print(f"Filament backlight generation time: {end - start}")
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

    if cf.chunck > 0 and not cf.not_parallel:
        X, V  = PrepareData(X, V, chunck=cf.chunck)

    # Get the Foil Geometry: 
    system = Geometry.GetGeometry()
    # Run simulation:
    X, V = SimulateBeam(X, V, system, cf.not_parallel)
    print('end')
    print(X[:10])
    print(V[:10])
    print(X.shape)
    if cf.save:
        np.save(f'{cf.name}_X', X)
        np.save(f'{cf.name}_V', V)
    
    cf.GetTime(start=False)


