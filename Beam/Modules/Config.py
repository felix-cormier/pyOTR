import logging
import datetime
import time
import numpy as np
from enum import Enum

def Conv(deg):
    return (np.pi * deg) / 180.

class Source(Enum):
    filament=0
    filament_v2=1
    protons=2
    laser=3

class generatorConfig():
    def __init__(self, verbose=1, save=False, name='test', not_parallel=True, nrays=1000, chunck=0, source=Source.filament_v2) -> None:
        self.verbose=verbose #1 for debuggiing info
        self.save=save
        self.name=name
        self.not_parallel=not_parallel
        self.nrays=nrays
        self.chunck=chunck
        self.source=source
        self.logfile = name + '.log'  # log output will be directed to this file and to screen

        self.filament = {
            'Vtype': 'parallel',
            'spread': 0.02,
            'F1': True, #true for on, false for off
            'F2': True,
            'F3': True
        }

        self.background = {
            'length':25., 
            'cfoil':0, #0,1,2 -> normal, cross, diamond
            #'spread':0.0,
            #'spread':0.025,
            'spread':0.075,
            #'spread':0.001,
            'style': 'cross',#cross or square
            'Vtype': 'divergent'  #parallel or divergent
            #potentially add cross parameter
        }

        self.M0 = {
            'normal': np.array([[0., 0., -1.]]),
            'R': 100.,
            'X': np.zeros((1, 3)),
            #'angles': np.array([0., Conv(90), -Conv(135)]),
            'angles': np.array([-Conv(45), Conv(90), Conv(0)]),
            'yrot': False,
            'name': 'PlaneMirror'
        }

        self.plane = {
            'normal': np.array([[1., 0., 0.]]),
            'R': 1000.,
            'X': np.array([-377.,0.,0.]),
            #First and last angle elements should remain the same, middle rot. matches y-rot.
            #'angles': np.array([Conv(-90), Conv(90), Conv(90)]),
            #'angles': np.array([Conv(90), Conv(90), Conv(-90)]),
            #'angles': np.array([Conv(-45), Conv(-90), 0.]),
            'angles': np.array([0., 0., Conv(70.18)]),
            'yrot': False,
            'name': 'PerfectPlane'
        }

        self.reflector = {
            'normal': np.array([[0., 1., 0.]]),
            'R': 1000.,
            'X': np.array([-371.166,0.,0.]),
            #'angles': np.array([0., 0., Conv(70.18)]), #x=oriented
            'angles': np.array([0., 0., Conv(-51.066/2.)]),
            'yrot': False,
            'name': 'PerfectReflector'
        }

        self.foils = {
            0: 'Blank',
            1: 'Fluorescent',
            2: 'Calibration',
            3: 'Ti1',
            4: 'Ti2',
            5: 'Ti3',
            6: 'Ti4',
            7: 'Cross'
        }

        self.foil = {
            'X': np.zeros((1, 3)),
            'angles': np.array([0., Conv(90), Conv(45)]),
        # 'angles': np.array([0., Conv(90), 0.]),
            'normal': np.array([[0, -1, 0]]),
            'eps':1.0,
            'D': 50.,
            'name': 'Calibration',
            'tht_range': 0.3
        }

        self.camera = {
            'npxlX': 484,
            'npxlY': 704,
            'focal distance': 60.,
            'yrot': True,
            #At foil
            #'X': np.array([[10., 0., 0.]]),
            #Trying to test no tilt
            #'X': np.array([[0., 0., -20.]]),
            #Imaging filament
            #'X': np.array([[0.,0.,0.]]),
            #'angles': np.array([0., Conv(90), Conv(45)]),
            #Angles for pointed at bg dist
            #'angles': np.array([0., -Conv(90), 0.]),
            #Angles for pointed at beam
            #'angles': np.array([0., 0., 0.]),
            #At M1
            'X': np.array([[1100., 3850., 0.]]),
            'angles': np.array([0., Conv(180), 0.]),
            #For background
            #'X': np.array([[20., 0., 0.]]),#produced odd results
            #'angles': np.array([Conv(90), Conv(90), Conv(90)]),
            'R': 10_000.,
            'name': 'ImagePlane'
        }

        self.M1 = {
            'X': np.array([[1100., 0., 0.]]),
            'angles': np.array([0., 0., 0.]),
            'f': 550.,
            'H': 120.,
            'D': 120.,
        # 'H': 100_000.,
        # 'D': 100_000.,
            'rough': False,
            'name': 'ParaMirror1'
        }

        self.M2 = {
            'X': np.array([[1100., 3850., 0.]]),
            'angles': np.array([0., Conv(180), 0.]),
            'f': 550.,
            'H': 120.,
            'D': 120.,
        # 'H': 100_000.,
        # 'D': 100_000.,
            'rough': False,
            'name': 'ParaMirror2'
        }



        self.beam = {
            'x': -1000., #for filament backlight
            #'x': 0.,
            'y': 0.,
            #'z': 0.,
            'z': -100.,
            #'gamma':21., #E = 20 GeV
            'gamma':32., #E = 30 GeV
        #    'gamma':53.5, #E = 50 GeV
            'cov': np.diag([9., 9., 0.]),
            'Vtype': 'parallel',  # need to implement divergent beam also
            'vcov': np.diag([0.05, 0.05, 1.]),  # not yet used, vz needs to be constrained by vx/vy

        }

    def init_logger(self):
        level = logging.DEBUG if self.verbose else logging.INFO
        message = '%(message)s\n'
        logging.basicConfig(filename=self.logfile, filemode='w', format=message)
        logger = logging.getLogger('generate_pbeam')
        logger.setLevel(level)
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.logfile)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    def GetTime(start=True):
        now = datetime.datetime.now()
        now = now.strftime('%Y, %b %d %H:%M:%S')
        if start:
            message = f'{now}\nStarting beam generation:'
        else:
            message = f'Ending beam generation, bye!!\n{now}'
        logger.info(message)









# Decorator to measure the time each function takes to run:
def timer(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        dt = time.time() - t0
        logger.info(f'{func.__name__} ran in {dt:.2f} s')
        return result
    return wrapper
