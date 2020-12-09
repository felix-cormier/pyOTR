import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans as km

f1 = 'f1_4_Xfinal.npy'
f2 = 'f2_4_Xfinal.npy'
f3 = 'f3_4_Xfinal.npy'
f1 = np.load(f1)
f2 = np.load(f2)
f3 = np.load(f3)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(16, 6))

ax1.scatter(f1[:,0], f1[:,1], marker='.', s=2, color='g')
ax1.set_title('F1')
ax2.scatter(f2[:,0], f2[:,1], marker='.', s=2, color='r')
ax2.set_title('F2')
ax3.scatter(f3[:,0], f3[:,1], marker='.', s=2, color='b')
ax3.set_title('F3')
plt.show()


nholes = 12
model1 = km(n_clusters=nholes)
model2 = km(n_clusters=nholes)
model3 = km(n_clusters=nholes)
model1.fit(f1[:, 0:2])
model2.fit(f2[:, 0:2])
model3.fit(f3[:, 0:2])
km(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
       n_clusters=12, n_init=10, n_jobs=None, precompute_distances='auto',
       random_state=None, tol=0.0001, verbose=0)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(16, 6))

ax1.scatter(f1[:,0], f1[:,1], marker='.', s=2, color='k')
ax1.scatter(model1.cluster_centers_[:,0], model1.cluster_centers_[:,1], marker='*', s=10, color='r')
ax1.set_title('F1')

ax2.scatter(f2[:,0], f2[:,1], marker='.', s=2, color='r')
ax2.scatter(model2.cluster_centers_[:,0], model2.cluster_centers_[:,1], marker='*', s=10, color='k')
ax2.set_title('F2')

ax3.scatter(f3[:,0], f3[:,1], marker='.', s=2, color='b')
ax3.scatter(model3.cluster_centers_[:,0], model3.cluster_centers_[:,1], marker='*', s=10, color='y')
ax3.set_title('F3')

plt.show()
