import logging
import datetime
import time
import numpy as np


def Conv(deg):
    return (np.pi * deg) / 180.

VERBOSE = 1  # Set to 1 for debugging info

save = True
name = 'output/scat'
#name = '../OTR/data/otr'  # name prefix used to create all outputs
logfile = name + '.log'  # log output will be directed to this file and to screen

nrays = 1_000_000
chunck = 1000  # 0 if no division is to be made

beam = {
    'x': 0.,
    'y': 0.,
    'z': -100.,
    'cov': np.diag([9., 9., 0.]),
    'Vtype': 'parallel',  # need to implement divergent beam also
    'vcov': np.diag([0.05, 0.05, 1.])  # not yet used, vz needs to be constrained by vx/vy
}

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

foil = {
    'X': np.zeros((1, 3)),
    'angles': np.array([0., Conv(90), Conv(45)]),
    'normal': np.array([[0, -1, 0]]),
    'D': 50.,
    'name': foils[3]
}

camera = {
    'npxlX': 484,
    'npxlY': 704,
    'focal distance': 60.,
    #At CalibFoil
    'X': np.array([[0., 0., 1.]]),
    'angles': np.array([0.,0.,0.]),
    #At foil
    #'X': np.array([[0., 0., 0.]]),
    #'angles': np.array([0.,0.,0.]),
    #At M1
    #'X': np.array([[1100., 0., 0.]]),
    #'angles': np.array([Conv(90), Conv(90), Conv(90)]),
    'R': 10_000.,
    'name': 'ImagePlane'
}

level = logging.DEBUG if VERBOSE else logging.INFO
message = '%(message)s\n'
logging.basicConfig(filename=logfile, filemode='w', format=message)
logger = logging.getLogger('generate_pbeam')
logger.setLevel(level)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(logfile)
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
