import numpy as np
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F
from ROOT import gROOT

data = np.load('../sources/pencil_Vfinal.npy')
f1 = TFile("hf.root",'recreate', 'my first histogram test')
finalX = TH2F("hxhy", "x vs y", 50, -0.2, 0.2, 50,-0.2,0.2)

print(data[:10])

for i in range (0,data.shape[0]):
    y = data[i][1]
    z = data[i][2]
    finalX.Fill(y,z)

finalX.Draw()
finalX.Write()
#f1.Close()
