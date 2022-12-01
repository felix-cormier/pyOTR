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
import json

parser = argparse.ArgumentParser()
parser.add_argument("--doGeneration", help="generate photons", action="store_true")
parser.add_argument("--doPropagation", help="propagate photons to camera", action="store_true")
parser.add_argument("--doHoleFinding", help="find bright spots in file", action="store_true")
parser.add_argument("--doOnAxis", help="find bright spots in file", action="store_true")
parser.add_argument("--doOnAxisComparison", help="Compares data and simulated on-axis measurements", action="store_true")
parser.add_argument("--holeDirectory", help="directory over in doHoleFinding")
args = parser.parse_args()

settings = generatorConfig('util_config.ini')

def make_shift_label(mirror1shift, mirror2shift, mirror3shift, mirror4shift, mirror1rot, mirror2rot, mirror3rot, mirror4rot):
    label_string = ""
    spacer=0
    if np.sum(np.abs(np.array(mirror1shift))) > 0:
        label_string = label_string + "M1:"+str(mirror1shift) 
        spacer+=1
    if np.sum(np.abs(np.array(mirror2shift))) > 0:
        label_string = label_string + "\nM2:"+str(mirror2shift) 
        spacer+=1
    if np.sum(np.abs(np.array(mirror3shift))) > 0:
        label_string = label_string + "\nM3:"+str(mirror3shift) 
        spacer+=1
    if np.sum(np.abs(np.array(mirror4shift))) > 0:
        label_string = label_string + "\nM4:"+str(mirror4shift) 
        spacer+=1
    if np.sum(np.abs(np.array(mirror1rot))) > 0:
        label_string = label_string + "M1:"+str(mirror1rot) 
        spacer+=1
    if np.sum(np.abs(np.array(mirror2rot))) > 0:
        label_string = label_string + "\nM2:"+str(mirror2rot) 
        spacer+=1
    if np.sum(np.abs(np.array(mirror3rot))) > 0:
        label_string = label_string + "\nM3:"+str(mirror3rot) 
        spacer+=1
    if np.sum(np.abs(np.array(mirror4rot))) > 0:
        label_string = label_string + "\nM4:"+str(mirror4rot) 
        spacer+=1
    return label_string, spacer

def sim_data_onAxisComparison():
    shift_file = open(settings.holeFindingPath+'shift_dictionary.json','r')
    shift_data = json.loads(shift_file.read())
    for line in shift_data:
        print(line)

    sim_ref = []
    X=[]
    Y=[]
    U=[]
    V=[]
    Color=[]
    Name=[]
    labels=[]

    for i, (m1shift, m2shift, m3shift, m4shift, m1rot, m2rot, m3rot, m4rot) in enumerate(zip(shift_data['Mirror1PosShift'],shift_data['Mirror2PosShift'],shift_data['Mirror3PosShift'], shift_data['Mirror4PosShift'],shift_data['Mirror1OrShift'],shift_data['Mirror2OrShift'],shift_data['Mirror3OrShift'], shift_data['Mirror4OrShift'])):
        print(i)
        data = np.load('output/data_hole_locator.npy')
        sim = np.load(settings.holeFindingPath+'/'+'shift_'+str(i)+'/sim_hole_locator.npy')
        if i==0:
            sim_ref = sim
            xmin = np.ones(len(sim[:,0]))*9999
            xmax = np.ones(len(sim[:,0]))*-9999
            ymin = np.ones(len(sim[:,1]))*9999
            ymax = np.ones(len(sim[:,1]))*-9999
        else:
            hole_names = []
            for name in settings.hole_names:
                if 'h' in name:
                    hole_names.append(int(name.split("h",2)[1]))

            indices_in = np.isin(hole_names,sim[:,2])
            temp_sim_ref = sim_ref[indices_in] 
            print(hole_names)
            print(sim[:,2])
            print(indices_in)
            label_string, spacer = make_shift_label(m1shift, m2shift, m3shift, m4shift, m1rot, m2rot, m3rot, m4rot)
            labels.append(label_string)
            print(label_string)
            temp_xmin = temp_sim_ref[:,0] - sim[:,0]
            temp_xmax = sim[:,0] - temp_sim_ref[:,0]
            X.append(temp_sim_ref[:,0])
            U.append(temp_xmax)
            print(temp_xmax)
            temp_ymin = temp_sim_ref[:,1] - sim[:,1]
            temp_ymax = sim[:,1] - temp_sim_ref[:,1]
            Y.append(temp_sim_ref[:,1])
            V.append(temp_ymax)
            print(temp_ymax)
            '''
            xmin[ temp_xmin < xmin] = temp_xmin[ temp_xmin < xmin]
            xmax[ temp_xmax > xmax] = temp_xmax[ temp_xmax > xmax]
            ymin[ temp_ymin < ymin] = temp_ymin[ temp_ymin < ymin]
            ymax[ temp_ymax > ymax] = temp_ymax[ temp_ymax > ymax]
            '''
            Color.append(i*np.ones(len(temp_ymax)))
            Name.append(str(i))

        plt.scatter(data[:,0], data[:,1], color='r', label='Data')
        '''
        if i > 0:
            plt.quiver(temp_sim_ref[:,0], temp_sim_ref[:,1], temp_xmax, temp_ymax, angles='uv', scale_units='xy', scale=1)
        '''
        plt.scatter(sim[:,0], sim[:,1], color='b', label='Sim')
        plt.xlim(0,484)
        plt.ylim(0,704)
        plt.xlabel('Camera X [Pixels]')
        plt.ylabel('Camera Y [Pixels]')
        plt.legend()
        plt.savefig(settings.holeFindingPath+'/'+'shift_'+str(i)+'/data_sim_comp.png')
        plt.clf
        plt.clf
        plt.close()

    plt.scatter(data[:,0], data[:,1], color='r', label='Data')
    plt.scatter(sim_ref[:,0], sim_ref[:,1], color='b', label='Sim')
    #quiver = plt.quiver(X,Y,U,V, Color, angles='xy', scale_units='xy', scale=1)
    #plt.quiverkey(quiver, 0.8,0.8, 0.3, coordinates='axes', label=Name)
    colors=["m","g","b","y","k","c"]
    for i,(x,y,u,v,color) in enumerate(zip(X,Y,U,V,Color)):
        continue
        quiver = plt.quiver(x,y,u,v, angles='xy', scale_units='xy', scale=1, color=colors[i], width = 0.005, headwidth=3./1., headlength=5./1., headaxislength=4.5/1.)
        plt.quiverkey(quiver,0.89,0.89-(i*spacer)*0.05,20,label=labels[i], labelpos='E', labelcolor=colors[i])
    #plt.errorbar(sim_ref[:,0], sim_ref[:,1], xerr=[abs(xmin),xmax], yerr=[abs(ymin), ymax], color='b', fmt='.', label='Sim w/ shift')
    plt.xlim(0,484)
    plt.ylim(0,704)
    plt.xlabel("Camera X [Pixels]")
    plt.ylabel("Camera Y [Pixels]")
    plt.legend(frameon=False)
    plt.savefig(settings.holeFindingPath+'/data_sim_comp.png')
    plt.clf
    plt.clf
    plt.close()

if settings.doGeneration and settings.doPropagation:
    print("Generating and Propagating Photons")
    X,V, settings = generate_OTR(settings)
    print(f'In between X: {X}')
    pyOTR(settings, X=X, V=V)

elif settings.doGeneration:
    print("Generating Photons")
    generate_OTR(settings)

elif settings.doPropagation:
    print("Propagating photons to camera")
    pyOTR(settings)

elif settings.doOnAxisFitting:
    settings.onAxisAnalysis()

if settings.doHoleFinding:
    hole_finder(settings, 'sim')


if settings.doOnAxisComparison:
    sim_data_onAxisComparison()