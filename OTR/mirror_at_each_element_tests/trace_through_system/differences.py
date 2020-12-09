import numpy as np
from sklearn.cluster import KMeans as km

f1_std = np.load('files_npy/f1_4_std.npy')
f2_std = np.load('files_npy/f2_4_std.npy')
f3_std = np.load('files_npy/f3_4_std.npy')

f1_test = np.load('files_npy/f1_4_Xfinal.npy')
f2_test = np.load('files_npy/f2_4_Xfinal.npy')
f3_test = np.load('files_npy/f3_4_Xfinal.npy')


diff_f1 = f1_std - f1_test
diff_f2 = f2_std - f2_test
diff_f3 = f3_std - f3_test

f1 = np.sqrt(diff_f1[:,0]**2 + diff_f1[:,1]**2)
f2 = np.sqrt(diff_f2[:,0]**2 + diff_f2[:,1]**2)
f3 = np.sqrt(diff_f3[:,0]**2 + diff_f3[:,1]**2)
print(f1)
print(f2)
print(f3)
print(f1.shape[0])
root = True
if root:
    from ROOT import TFile, TGraph, TH1F, TCanvas, TLegend

    outf = TFile('differences.root', 'recreate')
    h1 = TH1F('h1', 'This is f1 dist', 50, 20, 22)
    h2 = TH1F('h2', 'This is f2 dist', 50, 20, 22)
    h3 = TH1F('h3', 'This is f3 dist', 50, 20, 22)
    
    for i in range (0,f1.shape[0]):
        h1.Fill(f1[i])
        h2.Fill(f2[i])
        h3.Fill(f3[i])

    h1.Write()
    h2.Write()
    h3.Write()
    outf.Close()
