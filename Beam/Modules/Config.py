import logging
import datetime
import time
import os
import numpy as np
from enum import Enum
import configparser
import json
import cv2
from codecs import namereplace_errors
import itertools



import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from generics_python.make_plots import generic_2D_plot, generic_histogram, multi_scatter_with_fit 

def Conv(deg):
    return (np.pi * deg) / 180.

class Source(Enum):
    filament=0
    filament_v2=1
    protons=2
    laser=3

class generatorConfig():
    def __init__(self, parser_file='util_config.ini'): 
    #def __init__(self, verbose=1, save=False, name='test', not_parallel=False, nrays=5000, chunck=0, source=Source.laser, outputPath='output/') -> None:
        """Sets up generatorConfig class to make light for pyOTR

        Args:
            verbose (int, optional): Whether to show debugging info. Defaults to 1.
            save (bool, optional): DEPRECATED. Defaults to False.
            name (str, optional): DEPRECATED. Defaults to 'test'.
            not_parallel (bool, optional): If we are using multi CPU parallelization. Do not set, should be set based on nrays and chunck Defaults to False.
            nrays (int, optional): How many total photons to generate. Defaults to 5000.
            chunck (int, optional): How many photons per CPU. Put 0 to run in non-parallel mode. Defaults to 0.
            source (_type_, optional): Source of photons. Defaults to Source.laser.
            outputPath (str, optional): Where to store output plots and files. Defaults to 'output/'.
        """
        config = configparser.ConfigParser()
        config.read(parser_file)
        self.onAxis=False
        source = config['DEFAULT']['Source']
        self.parser_string(config, source)
        #self.logger = self.init_logger()
        self.not_parallel=False
        if self.chunck == 0 or self.chunck==self.nrays: 
            self.not_parallel=True

        self.initialize_generator_components()
        self.initialize_source()

    def parser_string(self, config, source):
        json_dict = {}
        for key in config[source]:
            if 'Source'.lower() in key.lower():
                self.source = config[source][key]
            if 'OutputPath'.lower() in key.lower():
                self.outputPath = config[source][key]
            if 'NRays'.lower() in key.lower():
                self.nrays = config[source].getint(key)
            if 'Chunck'.lower() in key.lower():
                self.chunck = config[source].getint(key)
            if 'Order'.lower() in key.lower():
                self.order = self.parse_order(config[source][key])
            if 'Foil'.lower() in key.lower():
                self.foil = config[source][key]
            if 'GeneratorHole'.lower() in key.lower():
                self.generatorHole = config[source][key]
            if 'DoGeneration'.lower() in key.lower():
                self.doGeneration = config[source].getboolean(key)
            if 'GenerationPath'.lower() in key.lower():
                self.generationPath = config[source][key]
            if 'DoPropagation'.lower() in key.lower():
                self.doPropagation = config[source].getboolean(key)
            if 'PropagationPath'.lower() in key.lower():
                self.propagationPath = config[source][key]
            if 'Verbose'.lower() in key.lower():
                self.verbose = config[source].getint(key)
            if 'saveGeneration'.lower() in key.lower():
                self.saveGeneration = config[source].getboolean(key)
            if 'savePropagation'.lower() in key.lower():
                self.savePropagation = config[source].getboolean(key)
            if 'F1On'.lower() in key.lower():
                self.f1On = config[source].getboolean(key)
            if 'F2On'.lower() in key.lower():
                self.f2On = config[source].getboolean(key)
            if 'F3On'.lower() in key.lower():
                self.f3On = config[source].getboolean(key)
            if 'DoHoleFinding'.lower() in key.lower():
                self.doHoleFinding = config[source].getboolean(key)
            if 'HoleFindingPath'.lower() in key.lower():
                self.holeFindingPath = config[source][key]
            if 'HoleDirectory'.lower() in key.lower():
                self.holeDirectory = config[source][key]
            if 'LaserPosition'.lower() in key.lower():
                self.laserPosition = json.loads(config.get(source, 'LaserPosition'))
            if 'LaserAngle'.lower() in key.lower():
                self.laserAngle = json.loads(config.get(source, 'LaserAngle'))
            if 'LaserRadius'.lower() in key.lower():
                self.laserRadius = config[source].getfloat(key)
            if 'FilamentPosition'.lower() in key.lower():
                print(source)
                self.filamentPosition = json.loads(config.get(source, 'FilamentPosition'))
            if 'FilamentAngle'.lower() in key.lower():
                self.filamentAngle = json.loads(config.get(source, 'FilamentAngle'))
            if 'LogFile'.lower() in key.lower():
                self.logfile = config[source][key]
            if 'doShift'.lower() in key.lower():
                self.doShift = config[source].getboolean(key)
                json_dict['doShift'] = self.doShift
            if 'doOnAxisComparison'.lower() in key.lower():
                self.doOnAxisComparison = config[source].getboolean(key)
            if 'doOnAxisFitting'.lower() in key.lower():
                self.doOnAxisFitting = config[source].getboolean(key)
            if 'OnAxisFittingPlottingFile'.lower() in key.lower():
                self.OnAxisFittingPlottingFile = config[source][key]
        if self.doShift:
            for key in config['Shift']:
                if 'simultaneousShift'.lower() in key.lower():
                    self.simultaneousShift = config['Shift'].getboolean(key)
                    json_dict['simultaneousShift'] = self.simultaneousShift
                if 'Mirror1PosShift'.lower() in key.lower():
                    self.mirror1PosShift = json.loads(config.get('Shift', 'Mirror1PosShift'))
                    json_dict['Mirror1PosShift'] = self.mirror1PosShift
                if 'Mirror2PosShift'.lower() in key.lower():
                    self.mirror2PosShift = json.loads(config.get('Shift', 'Mirror2PosShift'))
                    json_dict['Mirror2PosShift'] = self.mirror2PosShift
                if 'Mirror3PosShift'.lower() in key.lower():
                    self.mirror3PosShift = json.loads(config.get('Shift', 'Mirror3PosShift'))
                    json_dict['Mirror3PosShift'] = self.mirror3PosShift
                if 'Mirror4PosShift'.lower() in key.lower():
                    self.mirror4PosShift = json.loads(config.get('Shift', 'Mirror4PosShift'))
                    json_dict['Mirror4PosShift'] = self.mirror4PosShift
                if 'Mirror1OrShift'.lower() in key.lower():
                    self.mirror1OrShift = json.loads(config.get('Shift', 'Mirror1OrShift'))
                    json_dict['Mirror1OrShift'] = self.mirror1OrShift
                if 'Mirror2OrShift'.lower() in key.lower():
                    self.mirror2OrShift = json.loads(config.get('Shift', 'Mirror2OrShift'))
                    json_dict['Mirror2OrShift'] = self.mirror2OrShift
                if 'Mirror3OrShift'.lower() in key.lower():
                    self.mirror3OrShift = json.loads(config.get('Shift', 'Mirror3OrShift'))
                    json_dict['Mirror3OrShift'] = self.mirror3OrShift
                if 'Mirror4OrShift'.lower() in key.lower():
                    self.mirror4OrShift = json.loads(config.get('Shift', 'Mirror4OrShift'))
                    json_dict['Mirror4OrShift'] = self.mirror4OrShift
        if self.doPropagation:
            self.save_json_dict(json_dict, "shift_dictionary")

    def save_json_dict(self, json_dict, name):
        try:
            os.makedirs(self.outputPath)
        except FileExistsError:
            pass
        with open(self.outputPath+name+'.json', 'w') as outfile:
            json.dump(json_dict, outfile)


    def parse_order(self, order_string):
        return list(order_string.split(","))
        
    def initialize_generator_components(self):
        if self.source.lower() == 'filament':
            self.filament = {
                'Vtype': 'parallel',
                'spread': 0.02,
                'name': 'Filament',
                'refl': 2,
                'trans': -2,
                'F1': self.f1On, #true for on, false for off
                'F2': self.f2On,
                'F3': self.f3On
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



        if self.source.lower() == 'filament':
            self.beam = {
                'x': -1000., #for filament backlight
                'refl': 2,
                'trans': -2,
                'y': 0.,
                'z': 0., #FOR FILAMENTS
                #'gamma':21., #E = 20 GeV
                'gamma':32., #E = 30 GeV
            #    'gamma':53.5, #E = 50 GeV
                'cov': np.diag([9., 9., 0.]),
                'Vtype': 'parallel',  # need to implement divergent beam also
                'vcov': np.diag([0.05, 0.05, 1.]),  # not yet used, vz needs to be constrained by vx/vy
            }
        elif self.source.lower() == 'protons':
            self.beam = {
                'refl': 2,
                'trans': -2,
                'x': 0., #FOR PROTONS
                'y': 0.,
                'z': -100., #FOR PROTONS
                #'gamma':21., #E = 20 GeV
                'gamma':32., #E = 30 GeV
            #    'gamma':53.5, #E = 50 GeV
                'cov': np.diag([9., 9., 0.]),
                'Vtype': 'parallel',  # need to implement divergent beam also
                'vcov': np.diag([0.05, 0.05, 1.]),  # not yet used, vz needs to be constrained by vx/vy
            }

        self.M0 = {
            'normal': np.array([[0., 0., -1.]]),
            'R': 100.,
            'X': np.zeros((1, 3)),
            'angles': np.array([0., Conv(45), 0.]),
            'yrot': True,
            'name': 'PlaneMirror'
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
            'name': 'ParaMirror1',
            'refl': 1,
            'trans': 2,
            'dir_comp': 1
        }

        self.M2 = {
            'X': np.array([[1100., 3850., 0.]]),
            'angles': np.array([0., Conv(180), 0.]),
            'f': 550.,
            'H': 120.,
            'D': 120.,
            'rough': False,
            'name': 'ParaMirror2',
            'refl': -2,
            'trans': -1,
            'dir_comp': 0
        }

        self.M3 = {
            'X': np.array([[-1100., 3850., 0.]]),
            'angles': np.array([Conv(90), Conv(180), Conv(-90)]),
            'f': 550.,
            'H': 120.,
            'D': 120.,
            'rough': False,
            'name': 'ParaMirror3',
            'refl': -1,
            'trans': 2,
            'dir_comp': 1
        }

        self.M4 = {
            'X': np.array([[-1100., 6522., 0.]]),
            'angles': np.array([Conv(180.), 0., 0.]),
            'f': 300.,
            'H': 120.,
            'D': 120.,
            'rough': False,
            'name': 'ParaMirror4',
            'refl': -1,
            'trans': 1,
            'dir_comp': 0
        }


        self.camera = {
            'npxlX': 484,
            'npxlY': 704,
            'focal distance': 300.,
            'R': 40.,
            'L': 7.9376,
            'H': 12.672,
            'name': 'ImagePlane',
            'refl': -3,
            'trans': 3,
            'X': np.array([[-1100. + 2*self.M4['f'], 6522., 0.]]),
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

    def onAxisAnalysis(self):
        onAxis_file = open(self.OnAxisFittingPlottingFile, mode='r')
        lines = onAxis_file.readlines()
        onAxis_file.close()

        xMax = []
        yMax = []
        mirrorShift = []

        indices_in=None
        for path in lines:
            #Check indices
            path = path.strip('\n')
            shift_file = open(path+'/shift_dictionary.json','r')
            shift_data = json.loads(shift_file.read())
            for i,shift in enumerate(shift_data['Mirror1PosShift']):
                sim = np.load(path+'/'+'shift_'+str(i)+'/sim_hole_locator.npy')
                hole_names=[]
                for name in self.hole_names:
                    if 'h' in name:
                        hole_names.append(int(name.split("h",2)[1]))

                if indices_in is not None:
                    indices_in = np.logical_and(np.isin(hole_names,sim[:,2]),indices_in)
                else:
                    indices_in = np.isin(hole_names,sim[:,2]) 

        for path in lines:
            path = path.strip('\n')
            print(path)
            shift_file = open(path+'/shift_dictionary.json','r')
            shift_data = json.loads(shift_file.read())
            temp_xmax = []
            temp_ymax = []
            temp_mirrorShift = []



            for i, (m1shift, m2shift, m3shift, m4shift) in enumerate(zip(shift_data['Mirror1PosShift'],shift_data['Mirror2PosShift'],shift_data['Mirror3PosShift'], shift_data['Mirror4PosShift'])):
                sim = np.load(path+'/'+'shift_'+str(i)+'/sim_hole_locator.npy')
                if i==0:
                    sim_ref = sim
                    hole_names=[]
                    for name in self.hole_names:
                        if 'h' in name:
                            hole_names.append(int(name.split("h",2)[1]))

                    if indices_in is not None:
                        indices_in = np.logical_and(np.isin(hole_names,sim[:,2]),indices_in)
                    else:
                        indices_in = np.isin(hole_names,sim[:,2]) 
                    temp_sim_ref = sim_ref[indices_in[np.isin(hole_names,sim[:,2])]] 
                else:
                    temp_mirrorShift.append(np.array(np.concatenate((np.array(m1shift), np.array(m2shift), np.array(m3shift), np.array(m4shift)))))
                    hole_names=[]
                    for name in self.hole_names:
                        if 'h' in name:
                            hole_names.append(int(name.split("h",2)[1]))

                    if indices_in is not None:
                        indices_in = np.logical_and(np.isin(hole_names,sim[:,2]),indices_in)
                    else:
                        indices_in = np.isin(hole_names,sim[:,2]) 
                    temp_sim = sim[indices_in[np.isin(hole_names,sim[:,2])]] 
                    temp_xmax.append(np.array(temp_sim[:,0] - temp_sim_ref[:,0]))
                    temp_ymax.append(np.array(temp_sim[:,1] - temp_sim_ref[:,1]))
            mirrorShift.append(np.array(temp_mirrorShift))
            xMax.append(np.array(temp_xmax))
            yMax.append(np.array(temp_ymax))

        #First index is the FILE
        #Second index is the SHIFT
        addition_index=[]


        #Gross
        print(f'length: {len(mirrorShift)}')
        for i,shifts_1 in enumerate(mirrorShift):
            print(i)
            for j,shifts_2 in enumerate(mirrorShift):
                for k,shifts_3 in enumerate(mirrorShift):
                    if np.allclose(shifts_1+shifts_2,shifts_3):
                        if (j,i,k) not in addition_index:
                            addition_index.append((i,j,k))
                    for l,shifts_4 in enumerate(mirrorShift):
                        if np.allclose(shifts_1+shifts_2+shifts_3,shifts_4):
                            if (i,k,j,l) not in addition_index and (j,k,i,l) not in addition_index and (j,i,k,l) not in addition_index and (k,i,j,l) not in addition_index and (k,j,i,l) not in addition_index:
                                addition_index.append((i,j,k,l))
                        for m, shifts_5 in enumerate(mirrorShift):
                            if np.allclose(shifts_1+shifts_2+shifts_3+shifts_4,shifts_5):
                                add=True
                                for item in list(itertools.permutations((i,j,k,l,m), 5)):
                                    if item in addition_index:
                                        add=False
                                if add==True:
                                    addition_index.append((i,j,k,l,m))

        n=1
        x_differences = []
        y_differences = []
        x_differences_norm = []
        y_differences_norm = []
        linear_plot_x_1 = []
        linear_plot_y_1 = []
        linear_plot_x_2 = []
        linear_plot_y_2 = []
        linear_plot_x_3 = []
        linear_plot_y_3 = []
        for index_combo in addition_index:
            print(index_combo[:-n or None])
            print(index_combo[-n])
            temp_linear_plot_x_1 = []
            temp_linear_plot_y_1 = []
            temp_linear_plot_x_2 = []
            temp_linear_plot_y_2 = []
            temp_linear_plot_x_3 = []
            temp_linear_plot_y_3 = []
            for i, add_index in enumerate(index_combo[:-n or None]):
                if i==0:
                    add_result_y = yMax[add_index]
                    add_result_x = xMax[add_index]
                    if len(index_combo) == 3 and index_combo[1]==index_combo[0]+1 and index_combo[2] == index_combo[1]+1:
                        print(yMax[add_index])
                        temp_linear_plot_x_1.append(xMax[add_index][0])
                        temp_linear_plot_y_1.append(yMax[add_index][0])
                        temp_linear_plot_x_2.append(xMax[add_index][1])
                        temp_linear_plot_y_2.append(yMax[add_index][1])
                        temp_linear_plot_x_3.append(xMax[add_index][2])
                        temp_linear_plot_y_3.append(yMax[add_index][2])
                else:
                    add_result_y = np.add(add_result_y,yMax[add_index])
                    add_result_x = np.add(add_result_x,xMax[add_index])
                    if len(index_combo) == 3 and index_combo[1]==index_combo[0]+1 and index_combo[2] == index_combo[1]+1:
                        temp_linear_plot_x_1.append(xMax[add_index][0])
                        temp_linear_plot_y_1.append(yMax[add_index][0])
                        temp_linear_plot_x_2.append(xMax[add_index][1])
                        temp_linear_plot_y_2.append(yMax[add_index][1])
                        temp_linear_plot_x_3.append(xMax[add_index][2])
                        temp_linear_plot_y_3.append(yMax[add_index][2])

            if len(index_combo) == 3 and index_combo[1]==index_combo[0]+1 and index_combo[2] == index_combo[1]+1:
                temp_linear_plot_x_1.append(xMax[index_combo[-n]][0])
                temp_linear_plot_y_1.append(yMax[index_combo[-n]][0])
                temp_linear_plot_x_2.append(xMax[index_combo[-n]][1])
                temp_linear_plot_y_2.append(yMax[index_combo[-n]][1])
                temp_linear_plot_x_3.append(xMax[index_combo[-n]][2])
                temp_linear_plot_y_3.append(yMax[index_combo[-n]][2])
                linear_plot_x_1.append(temp_linear_plot_x_1)
                linear_plot_y_1.append(temp_linear_plot_y_1)
                linear_plot_x_2.append(temp_linear_plot_x_2)
                linear_plot_y_2.append(temp_linear_plot_y_2)
                linear_plot_x_3.append(temp_linear_plot_x_3)
                linear_plot_y_3.append(temp_linear_plot_y_3)
            
            temp_x_differences = xMax[index_combo[-n]]-add_result_x
            temp_x_differences = temp_x_differences[np.isnan(temp_x_differences) == False]
            x_differences.append(temp_x_differences)
            temp_y_differences = yMax[index_combo[-n]]-add_result_y
            temp_y_differences = temp_y_differences[np.isnan(temp_y_differences) == False]
            y_differences.append(temp_y_differences)
            temp_x_differences_norm = (xMax[index_combo[-n]]-add_result_x)/xMax[index_combo[-n]] 
            temp_x_differences_norm = temp_x_differences_norm[np.isnan(temp_x_differences_norm) == False]
            temp_x_differences_norm = temp_x_differences_norm[np.isinf(temp_x_differences_norm) == False]
            x_differences_norm.append(temp_x_differences_norm)
            temp_y_differences_norm = (yMax[index_combo[-n]]-add_result_y)/yMax[index_combo[-n]] 
            temp_y_differences_norm = temp_y_differences_norm[np.isnan(temp_y_differences_norm) == False]
            temp_y_differences_norm = temp_y_differences_norm[np.isinf(temp_y_differences_norm) == False]
            y_differences_norm.append(temp_y_differences_norm)

            if len(index_combo) == 3 and index_combo[1]==index_combo[0]+1 and index_combo[2] == index_combo[1]+1:
                print(index_combo)
                print(temp_linear_plot_y_3)
                print(temp_linear_plot_y_3[0][1])
                print(temp_linear_plot_y_3[0][2])
                print(temp_linear_plot_y_3[0][6])
                print(temp_linear_plot_y_3[1][1])
                print(temp_linear_plot_y_3[1][2])
                print(temp_linear_plot_y_3[1][6])
                print(temp_linear_plot_y_3[2][1])
                print(temp_linear_plot_y_3[2][2])
                print(temp_linear_plot_y_3[2][6])

                y_sequence_dim0_hole0 = [temp_linear_plot_y_1[0][1], temp_linear_plot_y_1[1][1], temp_linear_plot_y_1[2][1]]
                y_sequence_dim1_hole0 = [temp_linear_plot_y_2[0][1], temp_linear_plot_y_2[1][1], temp_linear_plot_y_2[2][1]]
                y_sequence_dim2_hole0 = [temp_linear_plot_y_3[0][1], temp_linear_plot_y_3[1][1], temp_linear_plot_y_3[2][1]]

                y_sequence_dim0_hole1 = [temp_linear_plot_y_1[0][2], temp_linear_plot_y_1[1][2], temp_linear_plot_y_1[2][2]]
                y_sequence_dim1_hole1 = [temp_linear_plot_y_2[0][2], temp_linear_plot_y_2[1][2], temp_linear_plot_y_2[2][2]]
                y_sequence_dim2_hole1 = [temp_linear_plot_y_3[0][2], temp_linear_plot_y_3[1][2], temp_linear_plot_y_3[2][2]]

                y_sequence_dim0_hole2 = [temp_linear_plot_y_1[0][6], temp_linear_plot_y_1[1][6], temp_linear_plot_y_1[2][6]]
                y_sequence_dim1_hole2 = [temp_linear_plot_y_2[0][6], temp_linear_plot_y_2[1][6], temp_linear_plot_y_2[2][6]]
                y_sequence_dim2_hole2 = [temp_linear_plot_y_3[0][6], temp_linear_plot_y_3[1][6], temp_linear_plot_y_3[2][6]]

                #labels = ['X Dim., Hole 0', 'Z Dim., Hole 0', 'X Dim., Hole 1', 'Z Dim., Hole 1', 'X Dim., Hole 2', 'Z Dim., Hole 2']
                labels = ['Y Dim., Hole 0', 'Y Dim., Hole 1', 'Y Dim., Hole 2']

                multi_scatter_with_fit([0.05, 0.1, 0.15], [y_sequence_dim1_hole0, y_sequence_dim1_hole1, 
                                            y_sequence_dim1_hole2], labels, '/home/fcormier/t2k/otr/pyOTR/output/', 'translate'+str(index_combo), 'Simulation Translated [mm]', 'Y Pixels Diff. from Data')

        generic_histogram(temp_x_differences, 'Difference in X [Pixels]', '/home/fcormier/t2k/otr/pyOTR/output/', 'x_diff_pos_single',y_name='Counts',label='pos')
        generic_histogram(temp_y_differences, 'Difference in Y [Pixels]', '/home/fcormier/t2k/otr/pyOTR/output/', 'y_diff_pos_single',y_name='Counts',label='pos')
        generic_histogram(temp_x_differences_norm, '(Added X - Original X)/Original X [Pixels]', '/home/fcormier/t2k/otr/pyOTR/output/', 'x_diff_norm_pos_single',y_name='Counts',label='pos')
        generic_histogram(temp_y_differences_norm, '(Added Y - Original X)/Original Y [Pixels]', '/home/fcormier/t2k/otr/pyOTR/output/', 'y_diff_norm_pos_single',y_name='Counts',label='pos')




    def loadGeneration(self, extra_string=''):
        try:
            return np.load(self.generationPath+'/'+extra_string+'/generated_X.npy'), np.load(self.generationPath+'/'+extra_string+'/generated_V.npy') 
        except FileNotFoundError:
            print(f'Did not find expected directory {extra_string}')
            return None, None

    def initialize_onAxisLaser(self):
        self.holes = np.load('Beam/data/calib_holes.npy')
        self.hole_names = ['h19', 'h15', 'h21', 'h22', 'h23', 'h16', 'h10', 'h9', 'h8', 'h14', 'h25', 'h26', 'h27', 'h28', 'h29', 'h20', 'h13', 'h11', 'h6', 'h5', 'h4', 'h3', 'h2', 'h7', 'h17', 'h18', 'none_1', 'none_2', 'none_3', 'none_4']
        self.onAxis=True
        if 'All'.lower() not in self.generatorHole.lower():
            self.holes = [self.holes[self.hole_names.index(self.generatorHole)]]
            self.hole_names = [self.generatorHole]
            print("test")

    def initialize_source(self):
        if 'Laser'.lower() in self.source.lower():
            if 'OnAxis'.lower() in self.source.lower():
                self.initialize_onAxisLaser()
            self.source = Source.laser
        elif 'Filament'.lower() in self.source.lower():
            self.source = Source.filament_v2
        elif 'Protons'.lower() in self.source.lower():
            self.source = Source.protons

    def makeShift(self, mirror1shift, mirror2shift, mirror3shift, mirror4shift, mirror1rot, mirror2rot, mirror3rot, mirror4rot):
        self.M1['X'][0,0] = self.M1['X'][0,0] + mirror1shift[0]
        self.M1['X'][0,1] = self.M1['X'][0,1] + mirror1shift[1]
        self.M1['X'][0,2] = self.M1['X'][0,2] + mirror1shift[2]

        self.M2['X'][0,0] = self.M2['X'][0,0] + mirror2shift[0]
        self.M2['X'][0,1] = self.M2['X'][0,1] + mirror2shift[1]
        self.M2['X'][0,2] = self.M2['X'][0,2] + mirror2shift[2]

        self.M3['X'][0,0] = self.M3['X'][0,0] + mirror3shift[0]
        self.M3['X'][0,1] = self.M3['X'][0,1] + mirror3shift[1]
        self.M3['X'][0,2] = self.M3['X'][0,2] + mirror3shift[2]

        self.M4['X'][0,0] = self.M4['X'][0,0] + mirror4shift[0]
        self.M4['X'][0,1] = self.M4['X'][0,1] + mirror4shift[1]
        self.M4['X'][0,2] = self.M4['X'][0,2] + mirror4shift[2]

        self.M1['angles'][0] = self.M1['angles'][0] + Conv(mirror1rot[0])
        self.M1['angles'][1] = self.M1['angles'][1] + Conv(mirror1rot[1])
        self.M1['angles'][2] = self.M1['angles'][2] + Conv(mirror1rot[2])

        self.M2['angles'][0] = self.M2['angles'][0] + Conv(mirror2rot[0])
        self.M2['angles'][1] = self.M2['angles'][1] + Conv(mirror2rot[1])
        self.M2['angles'][2] = self.M2['angles'][2] + Conv(mirror2rot[2])

        self.M3['angles'][0] = self.M3['angles'][0] + Conv(mirror3rot[0])
        self.M3['angles'][1] = self.M3['angles'][1] + Conv(mirror3rot[1])
        self.M3['angles'][2] = self.M3['angles'][2] + Conv(mirror3rot[2])

        self.M4['angles'][0] = self.M4['angles'][0] + Conv(mirror4rot[0])
        self.M4['angles'][1] = self.M4['angles'][1] + Conv(mirror4rot[1])
        self.M4['angles'][2] = self.M4['angles'][2] + Conv(mirror4rot[2])

    def resetShift(self, mirror1shift, mirror2shift, mirror3shift, mirror4shift, mirror1rot, mirror2rot, mirror3rot, mirror4rot):
        self.M1['X'][0,0] = self.M1['X'][0,0] - mirror1shift[0]
        self.M1['X'][0,1] = self.M1['X'][0,1] - mirror1shift[1]
        self.M1['X'][0,2] = self.M1['X'][0,2] - mirror1shift[2]

        self.M2['X'][0,0] = self.M2['X'][0,0] - mirror2shift[0]
        self.M2['X'][0,1] = self.M2['X'][0,1] - mirror2shift[1]
        self.M2['X'][0,2] = self.M2['X'][0,2] - mirror2shift[2]

        self.M3['X'][0,0] = self.M3['X'][0,0] - mirror3shift[0]
        self.M3['X'][0,1] = self.M3['X'][0,1] - mirror3shift[1]
        self.M3['X'][0,2] = self.M3['X'][0,2] - mirror3shift[2]

        self.M4['X'][0,0] = self.M4['X'][0,0] - mirror4shift[0]
        self.M4['X'][0,1] = self.M4['X'][0,1] - mirror4shift[1]
        self.M4['X'][0,2] = self.M4['X'][0,2] - mirror4shift[2]

        self.M1['angles'][0] = self.M1['angles'][0] - Conv(mirror1rot[0])
        self.M1['angles'][1] = self.M1['angles'][1] - Conv(mirror1rot[1])
        self.M1['angles'][2] = self.M1['angles'][2] - Conv(mirror1rot[2])

        self.M2['angles'][0] = self.M2['angles'][0] - Conv(mirror2rot[0])
        self.M2['angles'][1] = self.M2['angles'][1] - Conv(mirror2rot[1])
        self.M2['angles'][2] = self.M2['angles'][2] - Conv(mirror2rot[2])

        self.M3['angles'][0] = self.M3['angles'][0] - Conv(mirror3rot[0])
        self.M3['angles'][1] = self.M3['angles'][1] - Conv(mirror3rot[1])
        self.M3['angles'][2] = self.M3['angles'][2] - Conv(mirror3rot[2])

        self.M4['angles'][0] = self.M4['angles'][0] - Conv(mirror4rot[0])
        self.M4['angles'][1] = self.M4['angles'][1] - Conv(mirror4rot[1])
        self.M4['angles'][2] = self.M4['angles'][2] - Conv(mirror4rot[2])


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
        plt.savefig(self.outputPath+'/images/'+'/'+name+'_X.png', format='png', transparent=False)
        if 'Image' in name:
            norm = np.amax(hh_container)/256
            temp_hh_container = cv2.flip(hh_container, 0)
            cv2.imwrite(self.outputPath+'/images/'+'/'+name+'_X_'+extra_name+'.pgm', temp_hh_container*(1./norm))
        plt.close()
        plt.clf()

        plt.imshow(hh_f_container, cmap='jet', interpolation='nearest', origin='lower',extent=[xedges_f_container[0], xedges_f_container[-1], yedges_f_container[0], yedges_f_container[-1]])
        plt.xlabel(f"Transmitted X [{unit}]")
        plt.ylabel(f"Transmitted Y [{unit}]")
        plt.title(name)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Num. Photons', rotation=90)
        #plt.savefig(self.outputPath+'/'+name+'_Xf.png', format='png', transparent=False)
        plt.close()
        plt.clf()

        plt.imshow(hh_r_container, cmap='jet', interpolation='nearest', origin='lower',extent=[xedges_r_container[0], xedges_r_container[-1], yedges_r_container[0], yedges_r_container[-1]])
        plt.xlabel(f"Reflected X [{unit}]")
        plt.ylabel(f"Reflected Y [{unit}]")
        plt.title(name)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Num. Photons', rotation=90)
        #plt.savefig(self.outputPath+'/'+name+'_Xr.png', format='png', transparent=False)
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
        print(f'diagnostic X: {X}')
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
            os.makedirs(self.outputPath+'/images/')
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
                                "Transmitted Y", "Position", self.outputPath+'/images/', name+"_all", return_hist = True, save_plot = False)
            else:
                generic_2D_plot(X[:,dim_0], X[:,dim_1], [ x_min_X, x_max_X], num_bins_x, "Transmitted X", [y_min_X, y_max_X], num_bins_y, 
                                "Transmitted Y", "Position", self.outputPath+'/images/', name+"_all")
        if len(Xf.shape) > 1 and Xf.shape[1] > 0:
            if parallel:
                hh_f, xedges_f, yedges_f = generic_2D_plot(Xf[dim_0,:], Xf[dim_1,:], [x_min_Xrf, x_max_Xrf], num_bins_x, "Transmitted X", [y_min_Xrf, y_max_Xrf], num_bins_y, 
                                    "Transmitted Y", "Position", self.outputPath+'/images/', name+"_transmitted", return_hist = True, save_plot=False)
            else:
                generic_2D_plot(Xf[dim_0,:], Xf[dim_1,:], [x_min_Xrf, x_max_Xrf], num_bins_x, "Transmitted X", [y_min_Xrf, y_max_Xrf], num_bins_y, 
                                    "Transmitted Y", "Position", self.outputPath+'/images/', name+"_transmitted")
        if len(Xr.shape) > 1 and Xr.shape[1] > 0:
            if parallel:
                hh_r, xedges_r, yedges_r = generic_2D_plot(Xr[dim_0,:], Xr[dim_1,:], [x_min_Xrf, x_max_Xrf], num_bins_x, "Reflected X", [y_min_Xrf, y_max_Xrf], num_bins_y, 
                                    "Reflected Y", "Position", self.outputPath+'/images/', name+"_reflected", return_hist = True, save_plot = False)
            else:
                generic_2D_plot(Xr[dim_0,:], Xr[dim_1,:], [x_min_Xrf, x_max_Xrf], num_bins_x, "Reflected X", [y_min_Xrf, y_max_Xrf], num_bins_y, 
                                    "Reflected Y", "Position", self.outputPath+'/images/', name+"_reflected")

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
        #self.logger.info(message)

    # Decorator to measure the time each function takes to run:
    def timer(self,func):
        def wrapper(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            dt = time.time() - t0
            logger.info(f'{func.__name__} ran in {dt:.2f} s')
            return result
        return wrapper










