import concurrent.futures
import numpy as np
import Config as cf
import Geometry
from PrepareData import PrepareData


@cf.timer
def SimulateOTR(X, V, system):

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
    X = np.load(cf.inputs.format('X'))
    V =	np.load(cf.inputs.format('V'))

    if cf.chunck > 0:
        X, V = PrepareData(X, V, chunck=cf.chunck)
    
    # Get the optical components to be simulated:
    system = Geometry.GetGeometry()

    # Run simulation:
    X, V = SimulateOTR(X, V, system)

    if cf.save:
        np.save(f'{cf.name}_Xfinal_2', X)
        np.save(f'{cf.name}_Vfinal_2', V)

    cf.GetTime(start=False)
