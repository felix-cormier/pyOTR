import numpy as np
from sklearn.cluster import KMeans as km

#This program writes centroids to text files
def BeamToPixels(X):
    npxl = np.array([484, 704, 0])
    pxl_scale = np.array([1./(18.0e-3),1./(16.4e-3),0])
    pxl_center = npxl/2
    tpr_scale = 18./40.
    X = X*tpr_scale*pxl_scale + pxl_center
    return X

invert = True
f1 = np.load('../../mirror_at_each_element_tests/trace_through_system/files_npy/f1_4_Xfinal.npy')
f2 = np.load('../../mirror_at_each_element_tests/trace_through_system/files_npy/f2_4_Xfinal.npy')
f3 = np.load('../../mirror_at_each_element_tests/trace_through_system/files_npy/f3_4_Xfinal.npy')
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

files = 'output/F{}_centroids.txt'
for i, centers in enumerate(centroids):
    with open(files.format(i+1), 'w') as f:
        for center in centers:
            f.write(f'{center[0]} {center[1]}\n')
