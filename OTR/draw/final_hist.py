import numpy as np
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F
from ROOT import gROOT




X = np.load('../output/pencil_Xfinal.npy')
V = np.load('../output/pencil_Vfinal.npy')

Xx = X[:,0]
Vx = V[:,0]
x = 1100.
t = (x - Xx)/Vx
t.resize(t.shape[0],1)
X = X + V*t

f1 = TFile("hf.root",'recreate', 'my first histogram test')
finalX = TH2F("hxhy", "y vs z", 150, -500, 500, 150,-500,500)

print(X[:10])

for i in range (0,X.shape[0]):
    y = X[i][1]
    z = X[i][2]
    finalX.Fill(y,z)

finalX.Draw()
finalX.Write()
#f1.Close()
