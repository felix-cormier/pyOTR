import numpy as np

root = True
if root:
    from ROOT import TFile, TGraph, TCanvas, TLegend, TLatex, TPad, TAttMarker
    #Create canvas
    c1 = TCanvas('c1', 'c1', 800, 800)
    c1.SetGrid(1,1)
    outf = TFile('slopes.root', 'recreate')
    
    slopes = 'F{}_slope.txt'
    #Load and set graphs
    g1 = TGraph(slopes.format(1), '%lg %lg')
    g2 = TGraph(slopes.format(2), '%lg %lg')
    g3 = TGraph(slopes.format(3), '%lg %lg')
    g1.GetXaxis().SetLimits(-4,4)
    g1.GetXaxis().SetTitle("#theta")
    g1.GetYaxis().SetRangeUser(-200,200)
    g1.GetYaxis().SetTitle("slope")
    g1.SetMarkerStyle(1)
    g1.SetMarkerSize(2)
    g1.SetMarkerColor(1);
    g1.SetTitle("Slope")
    g1.Draw('AP*')
    g2.SetMarkerStyle(2)
    g2.SetMarkerSize(2)
    g2.SetMarkerColor(2);
    g2.Draw('P*same')
    g3.SetMarkerSize(2)
    g3.SetMarkerStyle(3)
    g3.SetMarkerColor(4);
    g3.Draw('P*same')
    
    #Add legend
    leg = TLegend(0.7, 0.6, .9, 0.9)
    leg.AddEntry(g1, 'F1', 'p')
    leg.AddEntry(g2, 'F2', 'p')
    leg.AddEntry(g3, 'F3', 'p')
    leg.Draw('same')
    
    
    
    c1.SaveAs('slopes.png')
    g1.SetName('g1')
    g1.Write()
    g2.SetName('g2')
    g2.Write()
    g3.SetName('g3')
    g3.Write()
    outf.Close()
