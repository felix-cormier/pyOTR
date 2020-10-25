import logging
import datetime
import time
import numpy as np


def Conv(deg):
    return (np.pi * deg) / 180.

VERBOSE = 1  # Set to 1 for debugging info

save = True
inputs = 'data/square_20mm_Xfinal.npy'

# Set data to false if you would like to use simulated camera control points instead of a data file
data = False
control_points_foil = 'data/calib_holes_foil.npy'
control_points_cam = 'data/calib_holes_cam.npy'

name = 'output/undistort'  # name prefix used to create all outputs
logfile = name + '.log'  # log output will be directed to this file and to screen

chunck = 1  # 0 if no division is to be made

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
    'taperX': 40/18,
    'taperY': 40/18,
    'pxlsize_X': 18.0e-3,
    'pxlsize_Y': 16.4e-3,
    'xbeamOffset': 0,
    'ybeamOffset': 0,
    'focal distance': 60.,
    'X': np.array([[-500., 6522., 0.]]),
    'angles': np.array([0., Conv(90), 0.]),
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
