import numpy as np
from sklearn.cluster import KMeans as km

def BeamToPixels(X):
    npxl = np.array([484, 704, 0])
    pxl_scale = np.array([1./(18.0e-3),1./(16.4e-3),0])
    pxl_center = npxl/2
    tpr_scale = 18./40.
    X = X*tpr_scale*pxl_scale + pxl_center
    return X

def GetParameterSet(p1=0, p2=0, p3=0):
    t1 = TLatex(0.1,0.8,"p1 = " + str(p1))
    t1.SetTextFont(23)
    t1.SetTextSize(18)
    t2 = TLatex(0.1,0.6,"p2 = " + str(p2))
    t2.SetTextFont(23)
    t2.SetTextSize(18)
    t3 = TLatex(0.1,0.4,"p3 = " + str(p3))
    t3.SetTextFont(23)
    t3.SetTextSize(18)
    return t1, t2, t3

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

c1 = model1.cluster_centers_[np.argsort(model1.cluster_centers_[:, 0])]
c2 = model2.cluster_centers_[np.argsort(model2.cluster_centers_[:, 0])]
c3 = model3.cluster_centers_[np.argsort(model3.cluster_centers_[:, 0])]

centroids = [c1, c2, c3]

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
    from ROOT import Double, TEllipse, TMath, TLatex, TPad, TFile, TF1, TGraph, TCanvas, TLegend

    c = TCanvas('c1', 'c1', 1000, 800)
    c.Divide(2,1);
    c.cd(1).SetGrid(1,1);
    outf = TFile('centers.root', 'recreate')
    g1 = TGraph(files.format(1), '%lg %lg')
    
    g1ver = TGraph(0)
    g1hor = TGraph(0)
   
    v1min, v1max = 0, 0
    h1min, h1max = 0, 0

    for i in range(g1.GetN()):
        x, y = Double(0), Double(0)
        g1.GetPoint(i, x, y)
        if (i < 3) or (i > 8): 
            g1hor.SetPoint(g1hor.GetN(), x, y)
            if(x < h1min): h1min = x
            if(x > h1max): h1max = x
        else: 
            g1ver.SetPoint(g1ver.GetN(), x, y)
            if(x < v1min): v1min = x
            if(x > v1max): v1max = x

    g1ver.GetXaxis().SetLimits(0,484)
    g1ver.GetYaxis().SetRangeUser(0,780)
    g1hor.GetXaxis().SetLimits(0,484*3)
    g1hor.GetYaxis().SetRangeUser(0,780*3)
    g1ver.SetMarkerColor(4)
    g1hor.SetMarkerColor(4)
    g1ver.SetTitle("Vertical")
    g1ver.Draw('AP*')
    f1ver = TF1("f1ver", "pol1", v1min, v1max)
    g1ver.Fit(f1ver, 'Q')
    f1hor = TF1("f1hor","pol2",h1min, h1max)
   # g1hor.Fit(f1hor, 'Q')
   # g1hor.Draw('P*same')
   # g1hor.Draw('AP*')
   # c.cd(1)
    pad1 = TPad("pad1","This is pad1",0.1,0.9,0.5,0.7);
    pad1.SetFillColor(11);
    pad1.Draw(); 
    pad1.cd()
    p1 = round(f1ver.GetParameter("p0"),3)
    p2 = round(f1ver.GetParameter("p1"),3)
    t1, t2, t3 = GetParameterSet(p1, p2)
    t1.Draw(), t2.Draw(), t3.Draw()
    c.cd(2).SetGrid(1,1)
    g1hor.Fit(f1hor, 'Q')
    g1hor.SetTitle("Horizontal")
    g1hor.Draw('AP*')
   
    r = 780.
    x_new = 253.8
    y_new = 334.65 + r
    region = TEllipse(x_new,y_new,r,r);
    region.SetFillStyle(0);
    region.SetLineColor(3);
    region.SetLineWidth(3);
    region.Draw('same');
    
    pad2 = TPad("pad1","This is pad1",0.1,0.9,0.5,0.7);
    pad2.SetFillColor(11);
    pad2.Draw(); 
    pad2.cd()
    p1 = round(f1hor.GetParameter("p0"),3)
    p2 = round(f1hor.GetParameter("p1"),3)
    p3 = round(f1hor.GetParameter("p2"),3)
    t4, t5, t6 = GetParameterSet(p1, p2, p3) 
    t4.Draw(), t5.Draw(), t6.Draw()
    td = TLatex(0.1,0.2,"k = 0.001282")
    td.SetTextFont(23)
    td.SetTextSize(18)
    td.Draw()
    c.Draw()

    c.SaveAs('sort.png')
    g2 = TGraph(files.format(2), '%lg %lg')
    g3 = TGraph(files.format(3), '%lg %lg')
#    
    c1 = TCanvas('c1', 'c1', 1000, 800)
    c1.Divide(2,1);
    c1.cd(1).SetGrid(1,1);
    g1.SetMarkerColor(1);
    g1.SetTitle("Centroids")
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
#    
    #Draw parameters pad
    c1.cd(2)
    pad1 = TPad("pad1","This is pad1",0.0,0.25,0.75,0.75);
    pad1.SetFillColor(11);
    pad1.Draw(); 
    pad1.cd()
    ta = TLatex(0.1,0.8,lines[0])
    ta.SetTextFont(23)
    ta.SetTextSize(35)
    tb = TLatex(0.1,0.6,lines[1])
    tb.SetTextFont(23)
    tb.SetTextSize(35)
    tc = TLatex(0.1,0.4,lines[2])
    tc.SetTextFont(23)
    tc.SetTextSize(35)
    #td = TLatex(0.1,0.2,"k = 0.001282")
    #td.SetTextFont(23)
    #td.SetTextSize(35)
    ta.Draw()
    tb.Draw()
    tc.Draw()
    #td.Draw()
    
    c1.SaveAs('centers.png')
    g1.SetName('g1')
    g1.Write()
    g2.SetName('g2')
    g2.Write()
    g3.SetName('g3')
    g3.Write()
    outf.Close()

