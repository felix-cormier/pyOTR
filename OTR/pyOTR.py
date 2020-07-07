import concurrent.futures
import numpy as np
import sys
sys.path.append('Modules/')
sys.path.append('../Beam/Modules/')
import Config as cf
import Beam
import Geometry


@cf.timer
def SimulateOTR(X, V, system):

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(system.TraceRay, X, V)
        for i, result in enumerate(results):
            if i % 100 == 0:
                cf.logger.debug(f'Running data chunck: {i}')
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

    #Testing out saving arrays
    foilfile='data/foil_image.npy'

    cf.GetTime()

    # Get details about the beam:
    beam = Beam.Beam()
    X, V = beam.GenerateBeam()
    if cf.save:
        np.save(f'{cf.name}_Xinitial', X)
        np.save(f'{cf.name}_Vinitial', V)
    if beam.chunck > 0:
        X, V = beam.PrepareData(X, V)

    # Get the optical components to be simulated:
    system = Geometry.GetGeometry()

    # Run simulation:
    X, V = SimulateOTR(X, V, system)
    print(X[:10])
    print(V[:10])

    if cf.save:
        np.save(f'{cf.name}_Xfinal', X)
        np.save(f'{cf.name}_Vfinal', V)

    cf.GetTime(start=False)
