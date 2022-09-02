import argparse
from Beam.generate_OTR import generate_OTR
from hole_finder import hole_finder
from OTR.pyOTR import pyOTR
from Beam.Modules.Config import generatorConfig, Source
import Beam.Modules.Laser as Laser

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import numpy as np
import math

parser = argparse.ArgumentParser()
parser.add_argument("--doGeneration", help="generate photons", action="store_true")
parser.add_argument("--doPropagation", help="propagate photons to camera", action="store_true")
parser.add_argument("--doHoleFinding", help="find bright spots in file", action="store_true")
parser.add_argument("--doOnAxis", help="find bright spots in file", action="store_true")
parser.add_argument("--doOnAxisComparison", help="Compares data and simulated on-axis measurements", action="store_true")
parser.add_argument("--holeDirectory", help="directory over in doHoleFinding")
args = parser.parse_args()

if args.doGeneration and args.doPropagation:
    print("Generating and Propagating Photons")
    X,V, generator_options = generate_OTR()
    pyOTR(X, V, generator_options)

elif args.doGeneration:
    print("Generating Photons")
    generate_OTR()

elif args.doPropagation:
    print("Propagating photons to camera")

elif args.doHoleFinding:
    hole_finder(args.holeDirectory, 'sim')

elif args.doOnAxis:

    holes = np.load('Beam/data/calib_holes.npy')
    hole_names = ['h19', 'h15', 'h21', 'h22', 'h23', 'h16', 'h10', 'h9', 'h8', 'h14', 'h25', 'h26', 'h27', 'h28', 'h29', 'h20', 'h13', 'h11', 'h6', 'h5', 'h4', 'h3', 'h2', 'h7', 'h13', 'h20', 'none_1', 'none_2', 'none_3', 'none_4']
    for i, hole_pos in enumerate(holes):
        generator_options = generatorConfig()
        generator_options.output_path = '/scratch/fcormier/t2k/otr/output/test_aug22_laser_3'
        generator_options.nrays = 20000
        generator_options.chunck = 2000
        generator_options.source = Source.laser
        generator_options.not_parallel=False
        if generator_options.chunck == 0: 
            generator_options.not_parallel=True
        laser = Laser.Laser(generator_options, rad=hole_pos[3]*2, name='Laser')
        #laser.Place(np.array([-1000, 0., 0.]), np.array([0.,0.,0.]))
        laser.Place(-10., -hole_pos[2], math.cos(0.785398)*hole_pos[0], np.array([0.,0.,0.]))
        X,V, generator_options = generate_OTR(generator_options, laser, hole_names[i])
        pyOTR(X, V, generator_options, hole_names[i])

elif args.doOnAxisComparison:
    data = np.load('output/data_hole_locator.npy')
    sim = np.load('output/sim_hole_locator.npy')
    plt.scatter(data[:,0], data[:,1], color='r', label='Data')
    plt.scatter(sim[:,0], sim[:,1], color='b', label='Sim')
    plt.xlim(0,484)
    plt.ylim(0,704)
    plt.legend()
    plt.savefig('output/comparison_onAxis.png')