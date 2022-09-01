import numpy as np

def GetFitPMS(n, h = 0.775):
    from ROOT import TLatex
    f = open(f'output/F{n}_fits.txt','r')
#    f = open(f'output/F{n}_data.txt','r')
    fits = f.readlines()
    title = TLatex(0.05,0.8,"F" + str(n) + ":")
    title.SetTextFont(23)
    title.SetTextSize(30)
    s = TLatex(0.05,0.65,f"slope = {round(float(fits[0]),3)}")
    s.SetTextFont(23)
    s.SetTextSize(20)
    k = TLatex(0.05,0.45,f"k = {round(float(fits[1]),6)} / r = {round(float(fits[2]),3)}")
    k.SetTextFont(23)
    k.SetTextSize(20)
    x = TLatex(0.05,0.25,f"cross = ({round(float(fits[5]),3)} , {round(float(fits[6]),3)})")
    x.SetTextFont(23)
    x.SetTextSize(20)
    mag = TLatex(0.05,0.05,f"mag = ({round(float(fits[3]),3)} , {round(float(fits[4]),3)})")
    mag.SetTextFont(23)
    mag.SetTextSize(20)
    return title, s, k, x, mag

#Get centroids, parameters
centroids = 'output/F{}_centroids.txt'
#centroids = 'data/f{}.txt'
parameters = open('../../mirror_at_each_element_tests/trace_through_system/files_npy/f3_4_pm.txt','r')
pms = parameters.readlines()
parameters.close()


root = True
if root:
    from ROOT import Double, TEllipse, TMath, TLatex, TPad, TFile, TF1, TGraph, TCanvas, TLegend

    #Create canvas
    c1 = TCanvas('c1', 'c1', 1000, 800)
    c1.Divide(2,1);
    c1.cd(1).SetGrid(1,1);
    outf = TFile('centers.root', 'recreate')
    
    #Load and set graphs
    g1 = TGraph(centroids.format(1), '%lg %lg')
    g2 = TGraph(centroids.format(2), '%lg %lg')
    g3 = TGraph(centroids.format(3), '%lg %lg')
    g1.SetMarkerColor(1);
    g1.SetTitle("Centroids")
    g1.Draw('AP*')
    g2.SetMarkerColor(2);
    g2.Draw('P*same')
    g3.SetMarkerColor(4);
    g3.Draw('P*same')

    #Add legend
    leg = TLegend(0.7, 0.6, .9, 0.9)
    leg.AddEntry(g1, 'F1', 'p')
    leg.AddEntry(g2, 'F2', 'p')
    leg.AddEntry(g3, 'F3', 'p')
    leg.Draw('same')
    
    #Draw parameters pad
    c1.cd(2)
    pad1 = TPad("pad1","Sim parameters pad",0.0,0.72,1.,1.0);
    pad1.SetFillColor(11);
    pad1.Draw(); 
    pad1.cd()
    title1 = TLatex(0.05,0.85,"Simulation parameters")
    title1.SetTextFont(23)
    title1.SetTextSize(30)
    ta = TLatex(0.05,0.65,pms[0])
    ta.SetTextFont(23)
    ta.SetTextSize(25)
    tb = TLatex(0.05,0.45,pms[1])
    tb.SetTextFont(23)
    tb.SetTextSize(25)
    tc = TLatex(0.05,0.25,pms[2])
    tc.SetTextFont(23)
    tc.SetTextSize(25)
    td = TLatex(0.05,0.05,pms[3])
    td.SetTextFont(23)
    td.SetTextSize(25)
    title1.Draw()
    ta.Draw()
    tb.Draw()
    tc.Draw()
    td.Draw()
    c1.cd(2)
    #Draw fit pads
    f1pad = TPad("f1","f1",0.,0.48,1.,0.7);
    f1pad.SetFillColor(11);
    f1pad.Draw(); 
    f2pad = TPad("f2","f2",0.,0.24,1.,0.46);
    f2pad.SetFillColor(11);
    f2pad.Draw(); 
    f3pad = TPad("f3","f3",0.,0., 1., 0.22);
    f3pad.SetFillColor(11);
    f3pad.Draw(); 
    f1pad.cd()
    #F1
    tf1, s1, k1, x1, mag1 = GetFitPMS(1)
    tf1.Draw()
    s1.Draw(), k1.Draw(), x1.Draw(), mag1.Draw()
    #F2
    f2pad.cd()
    tf2, s2, k2, x2, mag2 = GetFitPMS(2)
    tf2.Draw()
    s2.Draw(), k2.Draw(), x2.Draw(), mag2.Draw()
    #F3
    f3pad.cd()
    tf3, s3, k3, x3, mag3 = GetFitPMS(3)
    tf3.Draw()
    s3.Draw(), k3.Draw(), x3.Draw(), mag3.Draw()
    #Save graphs and picture
    c1.SaveAs('output/centers.png')
    g1.SetName('g1')
    g1.Write()
    g2.SetName('g2')
    g2.Write()
    g3.SetName('g3')
    g3.Write()
    outf.Close()
