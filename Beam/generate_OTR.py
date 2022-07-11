from itertools import repeat

import concurrent.futures
import numpy as np
from Beam.Modules.Config import generatorConfig, Conv
import Beam.Modules.Beam as Beam
import Beam.Modules.Laser as Laser
import Beam.Modules.Filament as Filament
import Beam.Modules.Geometry as Geometry
import time
from OTR.include.PrepareData import PrepareData

def SimulateBeam(X, V, system, generator_options, isGenerator):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        if generator_options.not_parallel:
            Xf,Vf = system.TraceRays(X,V, generator_options, isGenerator)
        else:
            results = executor.map(system.TraceRays, X, V, repeat(generator_options), repeat(isGenerator))
            for i, result in enumerate(results):
                if i % 100 == 0:
                    generator_options.logger.debug(f'Running data piece: {i}')
                x, v, hh_container, xedges_container, yedges_container, hh_f_container, xedges_f_container, yedges_f_container, hh_r_container, xedges_r_container, yedges_r_container, name_container, dim_container = result
                assert x.shape == v.shape
                if i == 0:
                    Xf = np.array(x)
                    Vf = np.array(v)
                    hh = np.array(hh_container)
                    hh_f = np.array(hh_f_container)
                    hh_r = np.array(hh_r_container)
                    xedges = xedges_container
                    yedges = yedges_container
                    xedges_f = xedges_f_container
                    yedges_f = yedges_f_container
                    xedges_r = xedges_r_container
                    yedges_r = yedges_r_container
                    name = name_container
                    dim = dim_container
                else:
                    Xf = np.concatenate((Xf, x), axis=0)
                    Vf = np.concatenate((Vf, v), axis=0)
                    if hh is not None and hh_container is not None:
                        hh = np.add(hh, hh_container)
                    if hh_f is not None and hh_f_container is not None:
                        hh_f = np.add(hh_f, hh_f_container)
                    if hh_r is not None and hh_r_container is not None:
                        hh_r = np.add(hh_r, hh_r_container)
                        

    if not generator_options.not_parallel:
        for temp_hh, temp_hh_f, temp_hh_r, temp_xedges, temp_yedges, temp_xedges_f, temp_yedges_f, temp_xedges_r, temp_yedges_r, temp_name, temp_dim in zip(hh, hh_f, hh_r, xedges, yedges, xedges_f, yedges_f, xedges_r, yedges_r, name, dim):
            generator_options.diagnosticImage_parallel(temp_hh, temp_hh_f, temp_hh_r, temp_xedges, temp_yedges, temp_xedges_f, temp_yedges_f, temp_xedges_r, temp_yedges_r, temp_name)

    Xf = np.array(Xf)
    Vf = np.array(Vf)
    return Xf, Vf



def generate_OTR():

    generator_options = generatorConfig()
    generator_options.output_path = '/scratch/fcormier/t2k/otr/output/test_jul11_2'
    generator_options.nrays = 5000
    generator_options.chunck = 2500
    generator_options.not_parallel=False
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
        generator_options.diagnosticImage(X,V, 'Generator')
        end = time.time()
        print(f"Filament v2 backlight generation time: {end - start}")
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
    X, V = SimulateBeam(X, V, system, generator_options, isGenerator=True)
    print('end')
    print(X[:10])
    print(V[:10])
    print(X.shape)
    if generator_options.save:
        np.save(f'{generator_options.name}_X', X)
        np.save(f'{generator_options.name}_V', V)

    generator_options.GetTime(start=False)

    return X,V, generator_options

    

if __name__ == '__main__':
    generate_OTR()
