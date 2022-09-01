import logging
import datetime
import time
import numpy as np


def Conv(deg):
    return (np.pi * deg) / 180.


VERBOSE = 1  # Set to 1 for debugging info

save = True
inputs = 'data/otr_filament_2_{}.npy'
name = 'output/otr_filament_2_final'  # name prefix used to create all outputs
logfile = name + '.log'  # log output will be directed to this file and to screen

chunck = 1_000

def options_for_propagation(generator_options):

    light = {
        0: 'OTR',
        1: 'F1',
        2: 'F2',
        3: 'F3',
        4: 'Laser'
    }

    light_source = 1

    foils = {
        0: 'Blank',
        1: 'Fluorescent',
        2: 'Calibration',
        3: 'Ti1',
        4: 'Ti2',
        5: 'Ti3',
        6: 'Ti4',
        7: 'Cross'
    }

    generator_options.foil = {
        'X': np.zeros((1, 3)),
        'angles': np.array([0., Conv(90), Conv(45)]),
        'normal': np.array([[0, -1, 0]]),
        'D': 50.,
        'name': foils[3],
        'tht_range': 0.3
    }

    generator_options.M0 = {
        'normal': np.array([[0., 0., -1.]]),
        'R': 100.,
        'X': np.zeros((1, 3)),
        'angles': np.array([0., Conv(45), 0.]),
        'yrot': True,
        'name': 'PlaneMirror'
    }

    generator_options.M1 = {
        'X': np.array([[1100., 0., 0.]]),
        'angles': np.array([0., 0., 0.]),
        'f': 550.,
        'H': 120.,
        'D': 120.,
    # 'H': 100_000.,
    # 'D': 100_000.,
        'rough': False,
        'name': 'ParaMirror1',
        'refl': 1,
        'trans': 2,
        'dir_comp': 1
    }

    generator_options.M2 = {
        'X': np.array([[1100., 3850., 0.]]),
        'angles': np.array([0., Conv(180), 0.]),
        'f': 550.,
        'H': 120.,
        'D': 120.,
    # 'H': 100_000.,
    # 'D': 100_000.,
        'rough': False,
        'name': 'ParaMirror2',
        'refl': -2,
        'trans': -1,
        'dir_comp': 0
    }

    generator_options.M3 = {
        'X': np.array([[-1100., 3850., 0.]]),
        'angles': np.array([Conv(90), Conv(180), Conv(-90)]),
        'f': 550.,
        'H': 120.,
        'D': 120.,
    # 'H': 100_000.,
    # 'D': 100_000.,
        'rough': False,
        'name': 'ParaMirror3',
        'refl': -1,
        'trans': 2,
        'dir_comp': 1
    }

    M4 = {
        'X': np.array([[-1100., 6522., 0.]]),
        'angles': np.array([Conv(180.), 0., 0.]),
        'f': 300.,
        'H': 120.,
        'D': 120.,
    # 'H': 100_000.,
    # 'D': 100_000.,
        'rough': False,
        'name': 'ParaMirror4',
        'refl': -1,
        'trans': 1,
        'dir_comp': 0
    }

    generator_options.M4 = M4

    generator_options.camera = {
        'npxlX': 484,
        'npxlY': 704,
        'focal distance': 300.,
        'R': 11.,
        'L': 7.9376,
        'H': 12.672,
        'name': 'ImagePlane',
        'refl': -3,
        'trans': 3,
        'X': np.array([[-1100. + 2*M4['f'], 6522., 0.]]),
        'angles': np.array([Conv(90), Conv(90), -Conv(90)])
        
        #At foil
        #'X': np.array([[0., 0., 0.]]),
        #Angles for pointed at bg dist
        #  'angles': np.array([Conv(90), Conv(90), Conv(90)]),
        #Angles for pointed at beam
        #'angles': np.array([0., 0., 0.]),
        
        #At M1
        #'X': np.array([[1100., 0., 0.]]),
        #'angles': np.array([Conv(90), Conv(90), Conv(90)]),
        
        #For background
        #'X': np.array([[20., 0., 0.]]),#produced odd results
        #'angles': np.array([Conv(90), Conv(90), Conv(90)]),
        
        #camera at M2 position
        #'X': np.array([[1100., 3850., 0.]]),
        #'angles': np.array([0., Conv(90), 0.])

        #camera at M3 position
        #'X': np.array([[-1100., 3850., 0.]]),
        #'angles': np.array([Conv(90), Conv(90), 0.])

        #camera at M4 position
        #'X': np.array([[-1100., 6522., 0.]]),
        #'angles': np.array([0., Conv(90), 0.])

        #camera at M4 focal point
    }

