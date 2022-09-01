from codecs import namereplace_errors
import logging
import datetime
import time
import os
import numpy as np
from enum import Enum
from generics_python.make_plots import generic_2D_plot  
import cv2

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def Conv(deg):
    return (np.pi * deg) / 180.

class Source(Enum):
    filament=0
    filament_v2=1
    protons=2
    laser=3

class generatorConfig():
    def __init__(self, verbose=1, save=False, name='test', not_parallel=False, nrays=20000, chunck=0, source=Source.laser, output_path='output/') -> None:
        self.verbose=verbose #1 for debuggiing info
        self.save=save
        self.name=name
        self.not_parallel=not_parallel
        self.nrays=nrays
        self.chunck=chunck
        self.source=source
        self.logfile = name + '.log'  # log output will be directed to this file and to screen
        self.logger = self.init_logger()
        self.output_path = output_path

        self.filament = {
            'Vtype': 'parallel',
            'spread': 0.02,
            'name': 'Filament',
            'refl': 2,
            'trans': -2,
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
            'refl': 2,
            'trans': -1,
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
            'name': 'Foil',
            'refl': 3,
            'trans': 2,
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
            'refl': 2,
            'trans': -2,
            #'x': 0., #FOR PROTONS
            'y': 0.,
            'z': 0., #FOR FILAMENTS
            #'z': -100., #FOR PROTONS
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
        return logger

    def diagnosticImage_parallel(self, hh_container, hh_f_container, hh_r_container, xedges_container, yedges_container, xedges_f_container, yedges_f_container, xedges_r_container, yedges_r_container, name, extra_name):

        unit = 'mm'

        if 'Image' in name:
            print(hh_container)
            print(xedges_container)
            print(yedges_container)

        plt.imshow(hh_container, cmap='jet', interpolation='nearest', origin='lower',extent=[xedges_container[0], xedges_container[-1], yedges_container[0], yedges_container[-1]])
        plt.xlabel(f"X [{unit}]")
        plt.ylabel(f"Y [{unit}]")
        plt.title(name)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Num. Photons', rotation=90)
        plt.savefig(self.output_path+'/'+name+'_X.png', format='png', transparent=False)
        if 'Image' in name:
            norm = np.amax(hh_container)/256
            temp_hh_container = cv2.flip(hh_container, 0)
            cv2.imwrite(self.output_path+'/'+name+'_X_'+extra_name+'.pgm', temp_hh_container*(1./norm))
        plt.close()
        plt.clf()

        plt.imshow(hh_f_container, cmap='jet', interpolation='nearest', origin='lower',extent=[xedges_f_container[0], xedges_f_container[-1], yedges_f_container[0], yedges_f_container[-1]])
        plt.xlabel(f"Transmitted X [{unit}]")
        plt.ylabel(f"Transmitted Y [{unit}]")
        plt.title(name)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Num. Photons', rotation=90)
        #plt.savefig(self.output_path+'/'+name+'_Xf.png', format='png', transparent=False)
        plt.close()
        plt.clf()

        plt.imshow(hh_r_container, cmap='jet', interpolation='nearest', origin='lower',extent=[xedges_r_container[0], xedges_r_container[-1], yedges_r_container[0], yedges_r_container[-1]])
        plt.xlabel(f"Reflected X [{unit}]")
        plt.ylabel(f"Reflected Y [{unit}]")
        plt.title(name)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Num. Photons', rotation=90)
        #plt.savefig(self.output_path+'/'+name+'_Xr.png', format='png', transparent=False)
        plt.close()
        plt.clf()

    def diagnosticImage(self, X,V, name, dim = None, isGenerator = False, parallel = False, dir_comp=2, ref_dir=3, trans_dir=3, generator_options=None):
        Xf, Xr = [], []
        print(ref_dir)
        print(trans_dir)
        sign_ref = ref_dir/abs(ref_dir)
        print(sign_ref)
        sign_trans = trans_dir/abs(trans_dir)
        print(sign_trans)
        ref_dir = abs(ref_dir) - 1
        trans_dir = abs(trans_dir) - 1
        print(ref_dir)
        print(trans_dir)

        #To find out which dimensions to plot
        x_0_min = np.amin(X[:,0])
        x_0_max = np.amax(X[:,0])
        x_1_min = np.amin(X[:,1])
        x_1_max = np.amax(X[:,1])
        x_2_min = np.amin(X[:,2])
        x_2_max = np.amax(X[:,2])

        print(dim)

        print(f'x0 min : {x_0_min}, x0 max: {x_0_max}; x1 min: {x_1_min}, x1 max: {x_1_max}; x2 min: {x_2_min}, x2 max: {x_2_max}')

        num_bins=50
        num_bins_x=num_bins
        num_bins_y=num_bins
        if "Image" in name and generator_options is not None:
            num_bins_x = generator_options.camera['npxlX'] 
            num_bins_y = generator_options.camera['npxlY'] 

        dim_0 = 0
        dim_1 = 1

        if 0 > x_0_min and 0 < x_0_max:
            dim_0 = 0
            if 0 > x_1_min and 0 < x_1_max: 
                dim_1=1
            else:
                dim_1=2
        else:
            dim_0 = 1
            dim_1 = 2
        if "Image" in name:
            dim_0 = 0
            dim_1 = 1
            num_bins=100
        if "ParaMirror1" in name:
            dim_0=2
            dim_1=1
        if "ParaMirror2" in name:
            dim_0=1
            dim_1=2
        if "ParaMirror3" in name:
            dim_0=2
            dim_1=0
        if "Foil" in name or "Reflector" in name:
            dim_0=2
            dim_1=1
            print("FOIL X:")

        print(f'dim 0: {dim_0}, dim 1: {dim_1}')

        for x, v in zip(X, V):
            if sign_trans*v[trans_dir] > 0:
                Xf.append((x[0], x[1], x[2]))
            if sign_ref*v[ref_dir] > 0:
                Xr.append((x[0], x[1], x[2]))
        Xf = np.array(Xf).T
        print(f"generated Xf shape: {Xf.shape}")
        Xr = np.array(Xr).T
        print(f"generated Xr shape: {Xr.shape}")
        try:
            os.makedirs(self.output_path)
        except FileExistsError:
            pass

        if dim is not None:
            x_min_X = dim[0]
            x_max_X = dim[1]
            y_min_X = dim[2]
            y_max_X = dim[3]

            x_min_Xrf = dim[0]
            x_max_Xrf = dim[1]
            y_min_Xrf = dim[2]
            y_max_Xrf = dim[3]
        else:
            x_min_X = np.amin(X[:,dim_0])-10
            x_max_X = np.amax(X[:,dim_0])+10
            y_min_X = np.amin(X[:,dim_1])-10
            y_max_X = np.amax(X[:,dim_1])+10 

            x_min_Xrf = np.amin(X[dim_0,:])-10
            x_max_Xrf = np.amax(X[dim_0,:])+10
            y_min_Xrf = np.amin(X[dim_1,:])-10 
            y_max_Xrf = np.amax(X[dim_1,:])+10 


        hh=None
        xedges = None
        yedges = None
        hh_f = None
        xedges_f = None
        yedges_f = None
        hh_r = None
        xedges_r = None
        yedges_r = None


        if len(X.shape) > 1 and X.shape[1] > 0:
            if parallel:
                hh, xedges, yedges = generic_2D_plot(X[:,dim_0], X[:,dim_1], [ x_min_X, x_max_X], num_bins_x, "Transmitted X", [y_min_X, y_max_X], num_bins_y, 
                                "Transmitted Y", "Position", self.output_path, name+"_all", return_hist = True, save_plot = False)
            else:
                generic_2D_plot(X[:,dim_0], X[:,dim_1], [ x_min_X, x_max_X], num_bins_x, "Transmitted X", [y_min_X, y_max_X], num_bins_y, 
                                "Transmitted Y", "Position", self.output_path, name+"_all")
        if len(Xf.shape) > 1 and Xf.shape[1] > 0:
            if parallel:
                hh_f, xedges_f, yedges_f = generic_2D_plot(Xf[dim_0,:], Xf[dim_1,:], [x_min_Xrf, x_max_Xrf], num_bins_x, "Transmitted X", [y_min_Xrf, y_max_Xrf], num_bins_y, 
                                    "Transmitted Y", "Position", self.output_path, name+"_transmitted", return_hist = True, save_plot=False)
            else:
                generic_2D_plot(Xf[dim_0,:], Xf[dim_1,:], [x_min_Xrf, x_max_Xrf], num_bins_x, "Transmitted X", [y_min_Xrf, y_max_Xrf], num_bins_y, 
                                    "Transmitted Y", "Position", self.output_path, name+"_transmitted")
        if len(Xr.shape) > 1 and Xr.shape[1] > 0:
            if parallel:
                hh_r, xedges_r, yedges_r = generic_2D_plot(Xr[dim_0,:], Xr[dim_1,:], [x_min_Xrf, x_max_Xrf], num_bins_x, "Reflected X", [y_min_Xrf, y_max_Xrf], num_bins_y, 
                                    "Reflected Y", "Position", self.output_path, name+"_reflected", return_hist = True, save_plot = False)
            else:
                generic_2D_plot(Xr[dim_0,:], Xr[dim_1,:], [x_min_Xrf, x_max_Xrf], num_bins_x, "Reflected X", [y_min_Xrf, y_max_Xrf], num_bins_y, 
                                    "Reflected Y", "Position", self.output_path, name+"_reflected")

        if parallel:
            if hh is None:
                hh = np.zeros([num_bins, num_bins])
                print(f'{name}, init')
            if hh_f is None:
                hh_f = np.zeros([num_bins, num_bins])
                xedges_f = xedges
                yedges_f = yedges
                print(f'{name}, f')
            if hh_r is None:
                hh_r = np.zeros([num_bins, num_bins])
                xedges_r = xedges
                yedges_r = yedges
                print(f'{name}, r')

            return hh, xedges, yedges, hh_f, xedges_f, yedges_f, hh_r, xedges_r, yedges_r
        if "Mirror" in name:
            print(f'hh min {np.amin(hh)}, max {np.amax(hh)}')
            print(f'hh X {np.amin(X[:,0])}, max {np.amax(X[:,0])}')
            print(f'hh X {np.amin(X[:,dim_0])}, max {np.amax(X[:,dim_0])}')
            print(f'hh X {np.amin(X[:,dim_1])}, max {np.amax(X[:,dim_1])}')
            print(dim_0)
            print(dim_1)
            print(dim)

    def GetTime(self, start=True):
        now = datetime.datetime.now()
        now = now.strftime('%Y, %b %d %H:%M:%S')
        if start:
            message = f'{now}\nStarting beam generation:'
        else:
            message = f'Ending beam generation, bye!!\n{now}'
        self.logger.info(message)

    # Decorator to measure the time each function takes to run:
    def timer(self,func):
        def wrapper(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            dt = time.time() - t0
            logger.info(f'{func.__name__} ran in {dt:.2f} s')
            return result
        return wrapper










