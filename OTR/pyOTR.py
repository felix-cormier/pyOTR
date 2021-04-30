import concurrent.futures
import Modules.Config as cf
import Modules.Geometry as Geometry
from include.PrepareData import PrepareData
import DataGen
import Plotter
import numpy as np
# import Modules.Filament as Filament
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
    X,V = DataGen.asy_patt_bottom()
    # X,V = DataGen.MC_top()
    # X,V = DataGen.MC_bottom()

    ### Plot the Generated Pattern ###
    # file name
    Plotter.ring = 2
    Plotter.test = 6
    size_gen=3
    # h0 = Plotter.plot_gen_top(X)
    h0=Plotter.plot_gen_bottom(X)



    # Get details about the beam:
    #beam = Beam.Beam()
   # laser = Laser.Laser(rad=0.1, nrays=10_000)
   # laser.Place(-1062.438, 855.654, 0., np.array([0.,0.,cf.Conv(51.066)]))

   #  filament = Filament.Filament(factor=0.5, nrays = 1_000_000)
   #  filament.Place(-1062.438, 855.654, 0., np.array([0.,0.,cf.Conv(51.066)]))
   # # filament.Place(0., 0., 0., np.array([0.,0.,0.]))
   #
   #
   #  if(cf.light[cf.light_source] == 'F1'):
   #      start = time.time()
   #     # X, V = beam.GenerateFilamentBacklight_v1()
   #      X, V = beam.GenerateFilament()
   #      end = time.time()
   #      print(f"Filament backlight generation time: {end - start}")
   #  # elif(cf.source == 'filament_v2'):
   #  #     start = time.time()
   #  #     X,V = filament.GenerateRays()
   #  #     end = time.time()
   #  #     print(f"Filament backlight generation time: {end - start}")
   #  # elif(cf.source == 'laser'):
   #  #     start = time.time()
   #  #     X, V = laser.GenerateRays()
   #  #     end = time.time()
   #      #print(f"Filament backlight generation time: {end - start}")
   #  else:
   #      print('Not a valid source')
   #
   #  #Save initial distribution
   #  if cf.save:
   #      # if(cf.source == 'protons'):
   #      #     np.save(f'{cf.name}_protonsX', X)
   #      #     np.save(f'{cf.name}_protonsV', V)
   #      if(cf.light[cf.light_source] == 'F1'):
   #          np.save(f'{cf.name}_filamentX', X)
   #          np.save(f'{cf.name}_filamentV', V)

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
    size_obs=3
    h = Plotter.plot_obs(X)

    ### Plot the Pattern Difference ###
    Plotter.plot_dist(X, h, h0)

    plt.show()
