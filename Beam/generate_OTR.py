

import concurrent.futures
import numpy as np
from Beam.Modules.Config import generatorConfig, Conv
import Beam.Modules.Beam as Beam
import Beam.Modules.Laser as Laser
import Beam.Modules.Filament as Filament
import Beam.Modules.Geometry as Geometry
import time
from include.PrepareData import PrepareData

def SimulateBeam(X, V, system, generator_options):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        if generator_options.not_parallel:
            Xf,Vf = system.TraceRays(X,V)
        else:
            results = executor.map(system.TraceRays, X, V)
            for i, result in enumerate(results):
                if i % 100 == 0:
                    generator_options.logger.debug(f'Running data piece: {i}')
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



def generate_OTR():

    generator_options = generatorConfig()
    generator_options.GetTime()
    # Get details about the beam:
    beam = Beam.Beam(generator_options)
   # laser = Laser.Laser(rad=0.1, nrays=10_000)
   # laser.Place(-1062.438, 855.654, 0., np.array([0.,0.,generator_options.Conv(51.066)]))
    
    filament = Filament.Filament( generator_options, factor=0.5)
    filament.Place(-1062.438, 855.654, 0., np.array([0.,0.,Conv(51.066)]))
   # filament.Place(0., 0., 0., np.array([0.,0.,0.]))
    
    if(generator_options.source.name == 'protons'):
        X, V = beam.GenerateBeam()
    elif(generator_options.source.name == 'filament'):
        start = time.time()
       # X, V = beam.GenerateFilamentBacklight_v1()
        X, V = beam.GenerateFilament()
        end = time.time()
        print(f"Filament backlight generation time: {end - start}")
    elif(generator_options.source.name == 'filament_v2'):
        start = time.time()
        X,V = filament.GenerateRays()
        end = time.time()
        print(f"Filament backlight generation time: {end - start}")
    elif(generator_options.source.name == 'laser'):
        start = time.time()
        X, V = laser.GenerateRays()
        end = time.time()
        #print(f"Filament backlight generation time: {end - start}")
    else:
        print('Not a valid source')
    
    #Save initial distribution
    if generator_options.save:
        if(generator_options.source.name == 'protons'):
            np.save(f'{generator_options.name}_protonsX', X)
            np.save(f'{generator_options.name}_protonsV', V)
        elif(generator_options.source == 'filament'):
            np.save(f'{generator_options.name}_filamentX', X)
            np.save(f'{generator_options.name}_filamentV', V)

    if generator_options.chunck > 0 and not generator_options.not_parallel:
        X, V  = PrepareData(X, V, chunck=generator_options.chunck)

    # Get the Foil Geometry: 
    system = Geometry.GetGeometry(generator_options)
    # Run simulation:
    X, V = SimulateBeam(X, V, system, generator_options)
    print('end')
    print(X[:10])
    print(V[:10])
    print(X.shape)
    if generator_options.save:
        np.save(f'{generator_options.name}_X', X)
        np.save(f'{generator_options.name}_V', V)
    
    generator_options.GetTime(start=False)

if __name__ == '__main__':
    generate_OTR()
