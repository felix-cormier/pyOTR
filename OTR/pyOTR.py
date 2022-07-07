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
