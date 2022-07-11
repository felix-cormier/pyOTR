import concurrent.futures
import numpy as np
from   OTR.Modules.Config import options_for_propagation
import OTR.Modules.Geometry as Geometry
from OTR.include.PrepareData import PrepareData

from itertools import repeat


def SimulateOTR(X, V, system, generator_options, isGenerator):

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

def pyOTR(X,V, generator_options):
    if generator_options.chunck > 0:
        X, V = PrepareData(X, V, chunck=generator_options.chunck)

    options_for_propagation(generator_options) 
    # Get the optical components to be simulated:
    system = Geometry.GetGeometry(generator_options)

    # Run simulation:
    X, V = SimulateOTR(X, V, system, generator_options, isGenerator=False)

    if generator_options.save:
        np.save(f'{generator_options.name}_Xfinal_2', X)
        np.save(f'{generator_options.name}_Vfinal_2', V)

    generator_options.GetTime(start=False)


if __name__ == '__main__':

    generator_options.GetTime()
    # Get details about the beam:
    X = np.load(generator_options.inputs.format('X'))
    V =	np.load(generator_options.inputs.format('V'))

    if generator_options.chunck > 0:
        X, V = PrepareData(X, V, chunck=generator_options.chunck)
    
    # Get the optical components to be simulated:
    system = Geometry.GetGeometry()

    # Run simulation:
    X, V = SimulateOTR(X, V, system, isGenerator=False)

    if generator_options.save:
        np.save(f'{generator_options.name}_Xfinal_2', X)
        np.save(f'{generator_options.name}_Vfinal_2', V)

    generator_options.GetTime(start=False)
