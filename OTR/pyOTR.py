import concurrent.futures
import Modules.Config as cf
import Modules.Geometry as Geometry
from include.PrepareData import PrepareData
import DataGen
import Plotter
import numpy as np
import matplotlib.pyplot as plt


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

    ### Get details about the beam ###
    # X,V = DataGen.test_top()
    # X,V = DataGen.test_bottom()
    # X,V = DataGen.asy_patt_top()
    # X,V = DataGen.asy_patt_bottom()
    X,V = DataGen.MC_top()
    # X,V = DataGen.MC_bottom()
    
    ### Plot the Generated Pattern ###
    Plotter.ring = 2
    Plotter.test = 6
    h0 = Plotter.plot_gen_top(X)
    # h0=Plotter.plot_gen_bottom(X)

    ### Start the simulation ###
    if cf.chunck > 0:
        X, V = PrepareData(X, V, chunck=cf.chunck)

    # Get the optical components to be simulated:
    system = Geometry.GetGeometry()

    # Run simulation:
    X, V = SimulateOTR(X, V, system)

    if cf.save:
        np.save(f'{cf.name}_Xfinal', X)
        np.save(f'{cf.name}_Vfinal', V)

    cf.GetTime(start=False)

    ### Plot the Observed Pattern ###
    h = Plotter.plot_obs(X)

    ### Plot the Pattern Difference ###
    Plotter.plot_dist(X, h, h0)

    plt.show()
