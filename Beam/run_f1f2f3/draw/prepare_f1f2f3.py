import numpy as np
import sys
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F
from ROOT import gROOT


rng = sys.argv[1]
print(rng)
f1 = TFile("f1f2f3.root",'recreate', 'multi_h')
for i in range (1,4):
    #Load file
    title = str(i)
    X = np.load('../sim_output/f' + str(i) + '_X.npy')
    #Declare histogram
    finalX = TH2F("h"+str(i), title, 250, -75., 75., 250,-75.,75.)
    for j in range (0,X.shape[0]):
        x = X[j][0]
        y = X[j][1]
        z = X[j][2]
        finalX.Fill(x,y)
    finalX.Write()
