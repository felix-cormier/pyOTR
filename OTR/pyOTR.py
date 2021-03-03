import concurrent.futures
import numpy as np
import Modules.Config as cf
import Modules.Geometry as Geometry
from include.PrepareData import PrepareData


@cf.timer
def SimulateOTR(X, V, system):

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(system.TraceRays, X, V)
        for i, result in enumerate(results):

            if i % 100 == 0:
                cf.logger.debug(f'Running data piece: {i}')
            x, v = result
            print(result)
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
    N = 1000000
    # Get details about the beam:
    #X = np.load(cf.inputs.format('X'))
    #V = np.load(cf.inputs.format('V'))
    theta = np.random.uniform(0,2*np.pi,N)
    r = np.random.uniform(0,2,N)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    zero = np.zeros(N)
    one = np.ones(N)
    X = np.transpose(np.array([x,y,zero]))
    V = np.transpose(np.array([-1*one,zero,zero]))


    if cf.chunck > 0:
        X, V = PrepareData(X, V, chunck=cf.chunck)
        # print(X)
    # Get the optical components to be simulated:
    system = Geometry.GetGeometry()

    # Run simulation:
    X, V = SimulateOTR(X, V, system)

    if cf.save:
        np.save(f'{cf.name}_Xfinal', X)
        np.save(f'{cf.name}_Vfinal', V)

    cf.GetTime(start=False)
