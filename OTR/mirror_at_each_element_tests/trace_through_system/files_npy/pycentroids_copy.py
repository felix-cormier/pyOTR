import numpy as np
from sklearn.cluster import KMeans as km


f1_std = np.load('f1_4_std.npy')
f2_std = np.load('f2_4_std.npy')
f3_std = np.load('f3_4_std.npy')

invert = False
#f1 = np.load('f1_4_Xfinal.npy')
f1 = f1_std
if(invert):
    f1[:,1] = -f1[:,1] 
#f2 = np.load('f2_4_Xfinal.npy')
f2 = f2_std
if(invert):
    f2[:,1] = -f2[:,1] 
#f3 = np.load('f3_4_Xfinal.npy')
f3 = f3_std
if(invert):
    f3[:,1] = -f3[:,1] 
f = np.concatenate((f1,f2,f3),axis=0)

x_min = np.amin(f[:,0])
y_min = np.amin(f[:,1])
shift = np.array([x_min,y_min,0.])
scale = np.array([13.77,15.12,0.])
taper = np.array([40./18.,40./18.,0.])

f1 = (f1 - shift)*scale
f2 = (f2 - shift)*scale
f3 = (f3 - shift)*scale

nholes = 12
model1 = km(n_clusters=nholes)
model2 = km(n_clusters=nholes)
model3 = km(n_clusters=nholes)

model1.fit(f1[:, 0:2])
model2.fit(f2[:, 0:2])
model3.fit(f3[:, 0:2])

centroids = [model1.cluster_centers_,
            model2.cluster_centers_,
            model3.cluster_centers_]

files = 'F{}_centroids.txt'
for i, centers in enumerate(centroids):
    with open(files.format(i+1), 'w') as f:
        for center in centers:
            f.write(f'{center[0]} {center[1]}\n')


root = True
if root:
    from ROOT import TFile, TGraph, TCanvas, TLegend

    outf = TFile('centers.root', 'recreate')
    g1 = TGraph(files.format(1), '%lg %lg')
    g2 = TGraph(files.format(2), '%lg %lg')
    g3 = TGraph(files.format(3), '%lg %lg')
    
    c1 = TCanvas('c1', 'c1', 500, 800)
    c1.SetGrid(1,1);
    g1.SetMarkerColor(1);
    g1.Draw('AP*')
    g2.SetMarkerColor(2);
    g2.Draw('P*same')
    g3.SetMarkerColor(4);
    g3.Draw('P*same')

    leg = TLegend(0.7, 0.6, .9, 0.9)
    leg.AddEntry(g1, 'F1', 'p')
    leg.AddEntry(g2, 'F2', 'p')
    leg.AddEntry(g3, 'F3', 'p')
    leg.Draw('same')
    
    c1.SaveAs('centers.png')
    g1.SetName('g1')
    g1.Write()
    g2.SetName('g2')
    g2.Write()
    g3.SetName('g3')
    g3.Write()
    outf.Close()
