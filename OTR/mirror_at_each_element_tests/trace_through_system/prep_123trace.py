import sys
import numpy as np
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F
from ROOT import gROOT

inv = int(sys.argv[1])
print(int(inv))

f = TFile("trace123.root",'recreate', 'multi_h')
for i in [1,2,3]:
    #for j in [0,4]:
    for j in [4]:
        #Load file
        X = np.load('files_npy/f' + str(i) + '_' + str(j) + '_Xfinal.npy')
        title = 'f' + str(i) + '_' + str(j)
        print(title)
    #Declare histogram
        if(j == 0):
            finalX = TH2F("f" + str(i) + "_h" +str(j), title, 250, -30., 30., 250,-30.,30.)
        else:
            finalX = TH2F("f" + str(i) + "_h" +str(j), title, 250, -50., 50., 250,-50.,50.)
        #Fill histogram
        for k in range (0,X.shape[0]):
            if(inv == 1):
                x = X[k][0]
                y = -X[k][1]
            else:
                x = X[k][0]
                y = X[k][1]
            finalX.Fill(x,y)
        #Write
        finalX.Write()
