from itertools import repeat
import math
import time
import concurrent.futures

import numpy as np

from Beam.Modules.Config import generatorConfig, Conv, Source
import Beam.Modules.Beam as Beam
import Beam.Modules.Laser as Laser
import Beam.Modules.Laser_v2 as Laser_v2
import Beam.Modules.Filament as Filament
import Beam.Modules.Geometry as Geometry
from OTR.include.PrepareData import PrepareData

def SimulateBeam(X, V, system, generator_options, isGenerator, extra_name = ''):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        if generator_options.not_parallel:
            Xf,Vf = system.TraceRays(X,V, generator_options, isGenerator)
        else:
            print(f'X before trace rays: {X}')
            results = executor.map(system.TraceRays, X, V, repeat(generator_options), repeat(isGenerator))
            for i, result in enumerate(results):
                if i % 100 == 0:
                    #generator_options.logger.debug(f'Running data piece: {i}')
                    pass
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
            generator_options.diagnosticImage_parallel(temp_hh.T, temp_hh_f.T, temp_hh_r.T, temp_xedges, temp_yedges, temp_xedges_f, temp_yedges_f, temp_xedges_r, temp_yedges_r, temp_name, extra_name)

    Xf = np.array(Xf)
    Vf = np.array(Vf)
    return Xf, Vf



def generate_OTR(generator_options=None, extra_name=None):


    if generator_options.onAxis:
        output_path = generator_options.outputPath
        for i, (hole_pos, hole_name) in enumerate(zip(generator_options.holes,generator_options.hole_names)):
            print(f'HOLE NAME: {hole_name}')
            if 'none' in hole_name:
                continue
            generator_options.outputPath = output_path
            laser = Laser.Laser(generator_options, rad=hole_pos[3]*2, name='Laser')
            #laser.Place(np.array([-1000, 0., 0.]), np.array([0.,0.,0.]))
            laser.Place(-10., -hole_pos[2], math.cos(0.785398)*hole_pos[0], np.array([0.,0.,0.]))
            generator_options.outputPath=generator_options.outputPath+str(hole_name)
            start = time.time()
            X, V = laser.GenerateRays()
            generator_options.diagnosticImage(X,V, 'Generator')
            print(X)
            end = time.time()
            print(f"Laser generation time: {end - start}")
            if generator_options.chunck > 0 and not generator_options.not_parallel:
                X, V  = PrepareData(X, V, chunck=generator_options.chunck)

            # Get the Foil Geometry: 
            system = Geometry.GetGeometry(generator_options)
            # Run simulation:
            X, V = SimulateBeam(X, V, system, generator_options, isGenerator=True, extra_name = extra_name)
            print('end')
            if generator_options.saveGeneration:
                np.save(f'{generator_options.outputPath}/generated_X', X)
                np.save(f'{generator_options.outputPath}/generated_V', V)

            generator_options.GetTime(start=False)


    else:
        beam = Beam.Beam(generator_options)
        
        # filament.Place(0., 0., 0., np.array([0.,0.,0.]))
        
    if(generator_options.source.name == 'protons'):
        X, V = beam.GenerateBeam()
    elif(generator_options.source.name == 'filament'):
        filament = Filament.Filament( generator_options, factor=0.5)
        filament.Place(generator_options.filamentPosition[0], generator_options.filamentPosition[1], 
                        generator_options.filamentPosition[2], 
                        np.array([Conv(generator_options.filamentAngle[0]),
                        Conv(generator_options.filamentAngle[1]),Conv(generator_options.filamentAngle[2])]))
        start = time.time()
       # X, V = beam.GenerateFilamentBacklight_v1()
        X, V = beam.GenerateFilament()
        end = time.time()
        print(f"Filament backlight generation time: {end - start}")
    elif(generator_options.source.name == 'filament_v2'):
        start = time.time()
        filament = Filament.Filament( generator_options, factor=0.5)
        filament.Place(generator_options.filamentPosition[0], generator_options.filamentPosition[1], 
                        generator_options.filamentPosition[2], 
                        np.array([Conv(generator_options.filamentAngle[0]),
                        Conv(generator_options.filamentAngle[1]),Conv(generator_options.filamentAngle[2])]))
        start = time.time()
        X,V = filament.GenerateRays()
        generator_options.diagnosticImage(X,V, 'Generator')
        end = time.time()
        print(f"Filament v2 backlight generation time: {end - start}")
    elif(generator_options.source.name == 'laser'):
        start = time.time()
        laser = Laser.Laser(generator_options, rad=generator_options.laserRadius, name='Laser')
        #laser.Place(np.array([-1000, 0., 0.]), np.array([0.,0.,0.]))
        laser.Place(generator_options.laserPosition[0], generator_options.laserPosition[1], 
                        generator_options.laserPosition[2], 
                        np.array([Conv(generator_options.laserAngle[0]),
                        Conv(generator_options.laserAngle[1]),Conv(generator_options.laserAngle[2])]))
        X, V = laser.GenerateRays()
        generator_options.diagnosticImage(X,V, 'Generator')
        print(X)
        end = time.time()
        print(f"Laser generation time: {end - start}")
    else:
        print('Not a valid source')
    

    if generator_options.chunck > 0 and not generator_options.not_parallel:
        print(f'Prepare Data X: {X}')
        X, V  = PrepareData(X, V, chunck=generator_options.chunck)

    # Get the Foil Geometry: 
    system = Geometry.GetGeometry(generator_options)
    # Run simulation:
    X, V = SimulateBeam(X, V, system, generator_options, isGenerator=True, extra_name = extra_name)
    print('end')
    if generator_options.saveGeneration:
        np.save(f'{generator_options.outputPath}/generated_X', X)
        np.save(f'{generator_options.outputPath}/generated_V', V)

    generator_options.GetTime(start=False)

    return X,V, generator_options

    

if __name__ == '__main__':
    generate_OTR()
