import concurrent.futures
import numpy as np
import Config as cf
import Beam
import Geometry
from PrepareData import PrepareData

@cf.timer
def SimulateBeam(X, V, O, system):
    Xf, Vf, Of = system.TraceRays(X, V, O)
    print(Xf.shape)
    return Xf, Vf, Of

if __name__ == '__main__':

    cf.GetTime()
    # Get details about the beam:
    beam = Beam.Beam()
    X, V, O = beam.GenerateBeam()
    if cf.save:
        np.save(f'{cf.name}_protonsX', X)
        np.save(f'{cf.name}_protonsV', V)
        np.save(f'{cf.name}_protonsO', O)

    # Get the Foil Geometry: 
    system = Geometry.GetGeometry()
    # Run simulation:
    X, V, O = SimulateBeam(X, V, O, system)
    print(O.shape)
    print(O[:10])
    print(X.shape)
    if cf.save:
        np.save(f'{cf.name}_X', X)
        np.save(f'{cf.name}_V', V)
        np.save(f'{cf.name}_O', O)
    
    cf.GetTime(start=False)


