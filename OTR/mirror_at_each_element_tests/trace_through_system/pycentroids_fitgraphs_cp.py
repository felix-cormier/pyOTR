import numpy as np

def GetLatexPMSet(p1=0, p2=0, p3=0):
    from ROOT import TLatex
    t1 = TLatex(0.1,0.8,"a = " + str(p3))
    t1.SetTextFont(23)
    t1.SetTextSize(18)
    t2 = TLatex(0.1,0.6,"b = " + str(p2))
    t2.SetTextFont(23)
    t2.SetTextSize(18)
    t3 = TLatex(0.1,0.4,"c = " + str(p1))
    t3.SetTextFont(23)
    t3.SetTextSize(18)
    return t1, t2, t3

def ComputePMSet(n):
    from ROOT import TGraph, Double, TF1, TCanvas, TPad, TLatex, TEllipse
    files = 'F{}_centroids.txt'
    g = TGraph(files.format(n), '%lg %lg')
    ver = TGraph(0)
    hor = TGraph(0)
   
    vmin, vmax = 0, 0
    hmin, hmax = 0, 0

    for i in range(g.GetN()):
        x, y = Double(0), Double(0)
        g.GetPoint(i, x, y)
        if (i < 3) or (i > 8): 
            hor.SetPoint(hor.GetN(), x, y)
            if(x < hmin): hmin = x
            if(x > hmax): hmax = x
        else: 
            ver.SetPoint(ver.GetN(), x, y)
            if(x < vmin): vmin = x
            if(x > vmax): vmax = x
    
    hor.GetXaxis().SetLimits(-484,484*2)
    hor.GetYaxis().SetRangeUser(0,780*2)
    #Fit to polynomials
    fver = TF1("fver", "pol1", vmin, vmax)
    ver.Fit(fver, 'Q')
    fhor = TF1("fhor","pol2",hmin, hmax)
    hor.Fit(fhor, 'Q')
    vp0 = fver.GetParameter("p0")
    vp1 = fver.GetParameter("p1")
    hp0 = fhor.GetParameter("p0")
    hp1 = fhor.GetParameter("p1")
    hp2 = fhor.GetParameter("p2")
    
    #Get intersection and ver/hor points closest to intersection
    f1 = TF1("f1", "pol2", vmin, vmax)
    f1.SetParameter(0, vp0 - hp0)
    f1.SetParameter(1, vp1 - hp1)
    f1.SetParameter(2, 0 - hp2)
    x1C = f1.GetX(0)
    y1C = fver.Eval(x1C)
    
    #Compute magnification
    inX = np.array([[-1000.,0.],[1000.,0.]])
    inY = np.array([[0.,-1000.],[0.,1000.]])
    for i in range(ver.GetN()):
        xver, yver = Double(0), Double(0)
        xhor, yhor = Double(0), Double(0)
        ver.GetPoint(i,xver,yver)
        hor.GetPoint(i,xhor,yhor)
        dx = x1C - xhor
        dy = y1C - yver
        if(0 > dx and dx > inX[0][0]): inX[0][0] = xhor; inX[0][1] = yhor
        if(0 < dx and dx < inX[1][0]): inX[1][0] = xhor; inX[1][1] = yhor
        if(0 > dy and dy > inY[0][1]): inY[0][1] = yver; inY[0][0] = xver
        if(0 < dy and dy < inY[1][1]): inY[1][1] = yver; inY[1][0] = xver 
    dHor = inX[1] - inX[0]
    deltHor = np.sqrt(dHor[0]*dHor[0] + dHor[1]*dHor[1])
    dVer = inY[1] - inY[0]
    deltVer = np.sqrt(dVer[0]*dVer[0] + dVer[1]*dVer[1])
    magF = open('mag_std.txt', 'r') 
    magCmp = magF.readlines()
    split = magCmp[n-1].split()
    stdHor = float(split[0])
    stdVer = float(split[1])
    magHor = deltHor/stdHor
    magVer = deltVer/stdVer
    magF.close()
    
    #Curvature and slope
    slope = vp1
    c = hp0 
    b = hp1
    a = hp2
    k = 2*a/np.sqrt((1+(2*a*x1C +b)**2)**(3))

    #Write number data to files
    files = 'F{}_fits.txt'
    f = open(files.format(n), 'w')
    f.write("slope = " + f"{vp1}\n")
    f.write("k = " + f"{k}\n")
    f.write("mag = " + f"({magHor},{magVer})\n")
    f.write("cross = " + f"({x1C},{y1C})\n")
    f.write("vp0 = " + f"{vp0}\n")
    f.write("vp1 = " + f"{vp1}\n")
    f.write("hp0 = " + f"{hp0}\n")
    f.write("hp1 = " + f"{hp1}\n")
    f.write("hp2 = " + f"{hp2}\n")
    f.close()
    #Slope plot
    files = 'F{}_slope.txt'
    f = open(files.format(n), 'a')
    parameters = open('files_npy/f3_4_pm.txt','r')
    pms = parameters.readlines()
    pms_split = pms[0].split()
    tht = pms_split[2]
    parameters.close()
    f.write(f"{tht} {slope}\n")
    f.close()
   
    draw = False
    if(draw == True):
        #Draw and save for reference
        c = TCanvas('c1', 'c1', 1000, 800)
        c.Divide(2,1);
        c.cd(1).SetGrid(1,1);
        #...
        #Vertical
        ver.GetXaxis().SetLimits(0,484)
        ver.GetYaxis().SetRangeUser(0,780)
        ver.SetMarkerColor(4)
        ver.SetTitle(f"F{n} - Vertical")
        ver.Draw('AP*')
        #Vertical parameter pad
        pad1 = TPad("pad1","pad1",0.1,0.9,0.5,0.7);
        pad1.SetFillColor(11);
        pad1.Draw(); 
        pad1.cd()
        p1 = round(vp0,3)
        p2 = round(vp1,3)
        t1, t2, t3 = GetLatexPMSet(p1, p2)
        t1.Draw(), t2.Draw(), t3.Draw()
        #Horizontal
        c.cd(2).SetGrid(1,1)
        hor.SetMarkerColor(4)
        hor.SetTitle(f"F{n} - Horizontal")
       
       #Draw ellipse to verify curvature
        r = 1/k
        x_new = fhor.GetMinimumX()
        y_new = fhor.GetMinimum() + r
        region = TEllipse(x_new,y_new,r,r);
        region.SetFillStyle(0);
        region.SetLineColorAlpha(3, 0.5);
        region.SetLineWidth(3);
        hor.Draw('AP*')
        region.Draw('same');
    
        #Horizontal parameter pad
        pad2 = TPad("pad2","pad2",0.1,0.9,0.5,0.7);
        pad2.SetFillColor(11);
        pad2.Draw(); 
        pad2.cd()
        p1 = round(hp0,3)
        p2 = round(hp1,3)
        p3 = round(hp2,3)
        t4, t5, t6 = GetLatexPMSet(p1, p2, p3) 
        t4.Draw(), t5.Draw(), t6.Draw()
        td = TLatex(0.1,0.2,"k = " + str(round(k,6)))
        td.SetTextFont(23)
        td.SetTextSize(18)
        td.Draw()
        c.SaveAs(f'fit_{n}.png')

ComputePMSet(1)
ComputePMSet(2)
ComputePMSet(3)
