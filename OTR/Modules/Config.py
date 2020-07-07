import logging
import datetime
import time
import numpy as np


def Conv(deg):
    return (np.pi * deg) / 180.


VERBOSE = 1  # Set to 1 for debugging info

save = True
name = 'output/pencil'  # name prefix used to create all outputs
logfile = name + '.log'  # log output will be directed to this file and to screen

beam = {
    'PID': 22,  # PDG PID: 22 for photons and 2212 for proton beam
    'Xtype': 'pencil',  # Create square grid, pencil beam or use testimage
    'nrays': 1_000_000,
    'chunck': 1_000,  # 0 if no division is to be made
    'size': 25.,
    'Vtype': 'parallel',
    'x': 0.,
    'y': 0.,
    'z': -100.,
    'cov': np.diag([10., 10., 0.])
}

light = {
    0: 'OTR',
    1: 'F1',
    2: 'F2',
    3: 'F3',
    4: 'Laser'
}

light_source = 0

foils = {
    0: 'Blank',#does this do anything?
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
    'angles': np.array([0., Conv(90), Conv(45)]),# original had 0 for third rotation
    'normal': np.array([[0, 1, 0]]),
    'D': 50.,  # diameter - 55.0, original C++ code, not sure why
    'name': foils[0]
}

M0 = {
    'normal': np.array([[0., 0., -1.]]),
    'R': 100.,
    'X': np.zeros((1, 3)),
    'angles': np.array([0., Conv(45), 0.]),
    'yrot': True,
    'name': 'PlaneMirror'
}

M1 = {
    'X': np.array([[1100., 0., 0.]]),
    'angles': np.array([0., 0., 0.]),
    'f': 550.,
    'H': 120.,
    'D': 120.,
    'rough': False,
    'name': 'ParaMirror1'
}

M2 = {
    'X': np.array([[1100., 3850., 0.]]),
    'angles': np.array([0., Conv(180), 0.]),
    'f': 550.,
    'H': 120.,
    'D': 120.,
    'rough': False,
    'name': 'ParaMirror2'
}

M3 = {
    'X': np.array([[-1100., 3850., 0.]]),
    'angles': np.array([Conv(90), Conv(180), Conv(-90)]),
    'f': 550.,
    'H': 120.,
    'D': 120.,
    'rough': False,
    'name': 'ParaMirror3'
}

M4 = {
    'X': np.array([[-1100., 6522., 0.]]),
    'angles': np.array([Conv(180.), 0., 0.]),
    'f': 300.,
    'H': 120.,
    'D': 120.,
    'rough': False,
    'name': 'ParaMirror4'
}

camera = {
    'npxlX': 484,
    'npxlY': 704,
    'focal distance': 60.,
    'X': np.array([[10., 0., 0.]]),#originally set to y = -10
    'angles': np.array([0., 0., 0.]), #originally set y to Conv(90)
    'R': 100.,
    'name': 'ImagePlane'
}

level = logging.DEBUG if VERBOSE else logging.INFO
message = '%(message)s\n'
logging.basicConfig(filename=logfile, filemode='w', format=message)
logger = logging.getLogger('pyOTR')
logger.setLevel(level)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(logfile)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def GetTime(start=True):
    now = datetime.datetime.now()
    now = now.strftime('%Y, %b %d %H:%M:%S')
    if start:
        message = f'{now}\nStarting pyOTR:'
    else:
        message = f'Ending pyOTR, bye!!\n{now}'
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
