import numpy as np
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F
from ROOT import gROOT




X = np.load('../output/pencil_Xfinal.npy')
V = np.load('../output/pencil_Vfinal.npy')

f1 = TFile("hf.root",'recreate', 'my first histogram test')
finalX = TH2F("hxhy", "x vs y", 150, -80, 80, 150,-80,80)

print(X[:10])

for i in range (0,X.shape[0]):
    x = X[i][0]
    y = X[i][1]
    finalX.Fill(x,y)

finalX.Draw()
finalX.Write()
#f1.Close()
