import numpy as np
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2D
from ROOT import gROOT,gRandom, gSystem

ring=3
test=1
X = np.loadtxt("output/camera_light_ray_ring%d_test%d.txt"%(ring,test))

# Create a new canvas, and customize it.
# c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200, 10, 700, 500 )
# Create some histograms, a profile histogram and an ntuple
# hpxpy  = TH2D( 'hpxpy', 'py vs px', 1000, -8, 8, 1000,-8,8)
hpxpy = TH2D( 'hpxpy', 'py vs px', 100, -8,-33,100,5,1)
for i in range(len(X[:,0])):
    hpxpy.Fill(X[i,0], X[i,1])
print(hpxpy.GetXaxis().GetXmin())
hpxpy.GetXaxis().SetRangeUser(hpxpy.GetXaxis().GetXmin(),hpxpy.GetXaxis().GetXmin()-0.25*hpxpy.GetXaxis().GetXmin());
print(hpxpy.GetMean(1));
print(hpxpy.GetMean(2));
centre = np.array([hpxpy.GetMean(1),hpxpy.GetMean(2)])
with open('output/Holecentre.txt','a') as f:
    for item in centre:
        f.write("%.7f "%(item))
    f.write("\n")
# hpxpy.Draw("colz")

# c1.Update()

# input()
