}

background = {
    'length':25., 
    'cfoil':1, #0,1,2 -> normal, cross, diamond
    #'spread':0.0,
    #'spread':0.025,
    'spread':0.075,
    #'spread':0.001,
    'style': 'cross',#cross or square
    'Vtype': 'divergent'  #parallel or divergent
    #potentially add cross parameter
}

M0 = {
    'normal': np.array([[0., 0., -1.]]),
    'R': 100.,
    'X': np.zeros((1, 3)),
    #'angles': np.array([0., Conv(90), -Conv(135)]),
    'angles': np.array([-Conv(45), Conv(90), Conv(0)]),
    'yrot': False,
    'name': 'PlaneMirror'
}

plane = {
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

reflector = {
    'normal': np.array([[0., 1., 0.]]),
    'R': 1000.,
    'X': np.array([-529.309,0.,0.]),
    'Xl': np.array([-529.309,0.,2.]), #Where on reflector laser should land
    'Xf': np.array([0.,0.,0.]), #Where on foil laser should land
    #'angles': np.array([Conv(-50.813/2.), Conv(0.), Conv(0.)]), #no offset
    #'angles': np.array([Conv(-50.9/2.), Conv(3.511), Conv(-0.04)]),
    #'angles': np.array([Conv(-50.9/2.), Conv(-3.), Conv(-0.04)]),
    'angles': np.array([Conv(-51.5/2.), Conv(6.99), Conv(0.015)]),
    'yrot': False,
    'name': 'ConnectedReflector'
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
   # 'angles': np.array([0., Conv(90), 0.]),
    'normal': np.array([[0, -1, 0]]),
    'eps':1.0,
    'D': 50.,
    'name': 'Calibration',
    'tht_range': 0.3
}

camera = {
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
    #'angles': np.array([0., -Conv(90), 0.]),
    #Angles for pointed at bg dist
    #'angles': np.array([0., -Conv(90), 0.]),
    #Angles for pointed at beam
    #'angles': np.array([0., 0., 0.]),
    #At M1
    'X': np.array([[0., 0., 0.]]),
    'angles': np.array([0., -Conv(90), 0.]),
    #For background
    #'X': np.array([[20., 0., 0.]]),#produced odd results
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
