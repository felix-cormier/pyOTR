import concurrent.futures
import Modules.Config as cf
import Modules.Geometry as Geometry
from include.PrepareData import PrepareData
import DataGen
import Plotter
import numpy as np
import Modules.Filament as Filament
import matplotlib.pyplot as plt
import time
import Modules.Beam as Beam
import sys

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


def main(program,shift0):
    cf.GetTime()
    # Geometry.shift = shift0

    # ### Get details about the beam ###
    # X,V = DataGen.test_top()
    # X,V = DataGen.test_bottom()
    # X,V = DataGen.asy_patt_top()
    # X,V = DataGen.asy_patt_bottom()
    # X,V = DataGen.filled_circ_top()
    # X,V = DataGen.filled_circ_bottom()
    X,V = DataGen.MC_top()
    # X,V = DataGen.MC_bottom()

    # for i in range (500):
    #     with open('output/ray%d.txt'%(i),'a') as f:
    #         for item in X[i]:
    #             f.write("%.7f "%(item))
    #         f.write("\n")



    # Get details about the beam:
   #  beam = Beam.Beam()
   #  # laser = Laser.Laser(rad=0.1, nrays=10_000)
   #  # laser.Place(-1062.438, 855.654, 0., np.array([0.,0.,cf.Conv(51.066)]))
   #
   #  filament = Filament.Filament(factor=0.5, nrays = 1_000_000)
   #  # filament.Place(-1062.438, 855.654, 0., np.array([0.,0.,cf.Conv(51.066)]))
   #  # filament.Place(-1100, -20.,20., np.array([cf.Conv(0),cf.Conv(0),cf.Conv(0)]))
   #  filament.Place(-1100, -20.,20., np.array([cf.Conv(0),cf.Conv(0),cf.Conv(0)]))
   #
   #  # filament.Place(-1100, 0.,20., np.array([cf.Conv(0),cf.Conv(0),cf.Conv(0)]))
   #  # filament.Place(-1100, -20+6522.,20., np.array([cf.Conv(180),cf.Conv(0),cf.Conv(0)]))
   # #x,y,z
   # #z,y,x
   # # filament.Place(0., 0., 0., np.array([0.,0.,0.]))
   #
   #
   #  if(cf.source == 'filament'):
   #      start = time.time()
   #      # X, V = beam.GenerateFilamentBacklight_v2()
   #      X, V = beam.GenerateFilamentBacklightCross()
   #      # X, V = beam.GenerateFilament()
   #      end = time.time()
   #      print(f"Filament backlight generation time: {end - start}")
   #  elif(cf.source == 'filament_v2'):
   #      start = time.time()
   #      X,V = filament.GenerateRays()
   #      end = time.time()
   #      print(f"Filament backlight generation time: {end - start}")
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
   #      if(cf.source == 'filament'):
   #          np.save(f'{cf.name}_filamentX', X)
   #          np.save(f'{cf.name}_filamentV', V)
   #

    # ### Plot the Generated Pattern ###
    # file name


    Plotter.ring = 3
    Plotter.test = 1
    size_gen     = 3
    h0 = Plotter.plot_gen_top(X)
    # h0 = Plotter.plot_gen_bottom(X)

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
    np.savetxt("output/camera_light_ray_ring%d_test%d.txt"%(Plotter.ring,Plotter.test),X)
    h = Plotter.plot_obs(X)

    ### Plot the Pattern Difference ###
    Plotter.plot_dist(X, h, h0)

    # plt.show()
if __name__ == '__main__':
    PROGRAME = sys.argv[0]
    SHIFT    = float(sys.argv[1])
    main(PROGRAME,SHIFT)
