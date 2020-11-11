import numpy as np
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F
from ROOT import gROOT

f1 = TFile("trace.root",'recreate', 'multi_h')
for i in range (0,5):
    #Load file
    title = str(i)
    X = np.load('files_npy/f1_' + str(i) + '_Xfinal.npy')
    #Declare histogram
    if(i < 4):
        finalX = TH2F("h"+str(i), title, 250, -30., 30., 250,-30.,30.)
        if(i == 0):
            finalX2 = TH2F("hx"+str(i), title, 250, -500., 500., 250,-500.,500.)
    else:
        finalX = TH2F("h"+str(i), title, 250, -10., 10., 250,-10.,10.)
    #Fill histogram
    for j in range (0,X.shape[0]):
        x = X[j][0]
        y = X[j][1]
        finalX.Fill(x,y)
        if(i == 0):
            finalX2.Fill(x,y)
    #Write
    finalX.Write()
    if(i == 0):
        finalX2.Write()
