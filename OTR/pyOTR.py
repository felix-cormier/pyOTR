import concurrent.futures
import numpy as np
import Config as cf
import Geometry
from PrepareData import PrepareData


@cf.timer
def SimulateOTR(X, V, O, system):
    Xf, Vf, Of = system.TraceRays(X, V, O)
    return Xf, Vf, Of


if __name__ == '__main__':

    cf.GetTime()

    # Get details about the beam:
    X = np.load(cf.inputs.format('X'))
    V =	np.load(cf.inputs.format('V'))
    O =	np.load(cf.inputs.format('O'))
    print(O[:10])

    # Get the optical components to be simulated:
    system = Geometry.GetGeometry()

    # Run simulation:
    X, V, O = SimulateOTR(X, V, O, system)
    print(X.shape)
    print(O.shape)
    print(O[:10])

    if cf.save:
        np.save(f'{cf.name}_Xfinal', X)
        np.save(f'{cf.name}_Vfinal', V)
        np.save(f'{cf.name}_Ofinal', O)

    cf.GetTime(start=False)
