import numpy as np
from sklearn.cluster import KMeans as km


def BeamToPixels(X):
    npxl = np.array([484, 704, 0])
    pxl_scale = np.array([1./(18.0e-3),1./(16.4e-3),0])
    pxl_center = npxl/2
    tpr_scale = 18./40.
    X = X*tpr_scale*pxl_scale + pxl_center
    return X

invert = True
f1 = np.load('files_npy/f1_4_Xfinal.npy')
f2 = np.load('files_npy/f2_4_Xfinal.npy')
f3 = np.load('files_npy/f3_4_Xfinal.npy')
if(invert):
    f1[:,1] = -f1[:,1]
    f2[:,1] = -f2[:,1]
    f3[:,1] = -f3[:,1]

f = np.concatenate((f1,f2,f3),axis=0)
min_f = np.array([np.amin(f[:,0]),np.amin(f[:,1]), 0.])
max_f = np.array([np.amax(f[:,0]),np.amax(f[:,1]), 0.])
shift = 0.5*(min_f+max_f)

f1 = BeamToPixels(f1 - shift)
f2 = BeamToPixels(f2 - shift)
f3 = BeamToPixels(f3 - shift)

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


parameters = open('files_npy/f3_4_pm.txt','r')
lines = parameters.readlines()
parameters.close()


root = True
if root:
    from ROOT import TFile, TGraph, TCanvas, TLegend, TLatex, TPad

    outf = TFile('centers.root', 'recreate')
    g1 = TGraph(files.format(1), '%lg %lg')
    g2 = TGraph(files.format(2), '%lg %lg')
    g3 = TGraph(files.format(3), '%lg %lg')
    
    c1 = TCanvas('c1', 'c1', 1000, 800)
    c1.Divide(2,1);
    c1.cd(1).SetGrid(1,1);
    g1.SetMarkerColor(1);
    g2.SetMarkerColor(2);
    g3.SetMarkerColor(4);

    g1.GetXaxis().SetLimits(0,484)
    g1.GetYaxis().SetRangeUser(0,780)
    g1.Draw('AP*')
    g2.Draw('P*same')
    g3.Draw('P*same')

    leg = TLegend(0.7, 0.6, .9, 0.9)
    leg.AddEntry(g1, 'F1', 'p')
    leg.AddEntry(g2, 'F2', 'p')
    leg.AddEntry(g3, 'F3', 'p')
    leg.Draw('same')

    #Draw parameters pad
    c1.cd(2)
    pad1 = TPad("pad1","This is pad1",0.0,0.25,0.75,0.75);
    pad1.SetFillColor(11);
    pad1.Draw(); 
    pad1.cd()
    t1 = TLatex(0.1,0.8,lines[0])
    t1.SetTextFont(23)
    t1.SetTextSize(35)
    t2 = TLatex(0.1,0.6,lines[1])
    t2.SetTextFont(23)
    t2.SetTextSize(35)
    t3 = TLatex(0.1,0.4,lines[2])
    t3.SetTextFont(23)
    t3.SetTextSize(35)
    t1.Draw()
    t2.Draw()
    t3.Draw()
    
    c1.SaveAs('centers.png')
    g1.SetName('g1')
    g1.Write()
    g2.SetName('g2')
    g2.Write()
    g3.SetName('g3')
    g3.Write()

    outf.Close()
