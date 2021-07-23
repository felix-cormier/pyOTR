import importlib
importlib.invalidate_caches()
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
    print('end')
    print(X[:1])
    print(V[:1])
    print(X.shape)
    if cf.save:
        np.save(f'{cf.name}_Xfinal', X)
        np.save(f'{cf.name}_Vfinal', V)
        pms = open(cf.name + '_pm.txt', 'w')
        pms.write("#theta = " + str(cf.pm['tht']) + "\n")
        pms.write("#hat{#sigma} = " + str(cf.pm['sig']) + "\n")
        pms.write("#hat{#epsilon} = " + str(cf.pm['eps']) + "\n")
        beam_pm = open('mirror_at_each_element_tests/trace_through_system/files_npy/f_shift_pm.txt')
        psi = (beam_pm.readlines())[0]
        pms.write(psi + "\n")

    cf.GetTime(start=False)
