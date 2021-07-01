import numpy as np
import matplotlib.pyplot as plt



def plotting(X,Y,Z):
    # ax1.scatter(X,Z)
    # ax2.scatter(Y,Z)
    # ax.scatter3D(X,Y,Z)
    ax1.plot(X,Y)
    ax2.plot(Z,Y)
    ax.plot3D(X,Y,Z)

    ax1.set_xlabel('x [mm]')
    ax1.set_ylabel('y [mm]')
    ax2.set_xlabel('z [mm]')
    ax2.set_ylabel('y [mm]')
    ax.set_xlim3d(-np.max([X,Y,Z])-50,np.max([X,Y,Z])+50)
    ax.set_ylim3d(-np.max([X,Y,Z])-50,np.max([X,Y,Z])+50)
    ax.set_xlabel('x [mm]')
    ax.set_ylabel('y [mm]')
    ax.set_zlabel('z [mm]')
    # fig3.colorbar(h3[3])
    # fig4.colorbar(h4[3])
    # ax.set_zlim3d(np.min([X,Y,Z])-50,np.max([X,Y,Z])+50)

for i in range(500):
    # locals()['ray%d' % (i)]  = np.loadtxt("output/bottom/ray%d.txt"%(i)).T
    # locals()['ray%d' % (i)]  = np.loadtxt("output/diff_scatter/ray%d.txt"%(i)).T
    # locals()['ray%d' % (i)]  = np.loadtxt("output/diffuse/ray%d.txt"%(i)).T
    # locals()['ray%d' % (i)]  = np.loadtxt("output/plane/ray%d.txt"%(i)).T
    # locals()['ray%d' % (i)]  = np.loadtxt("output/plane_many/ray%d.txt"%(i)).T
    locals()['ray%d' % (i)]  = np.loadtxt("output/diffuse_many/ray%d.txt"%(i)).T

# ray1=np.vstack((O[0],M1[0],M2[0],M3[0],M4[0],Cam[0])).T
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()
fig = plt.figure()
ax = plt.axes(projection='3d')
# ax.plot3D(ray1[0],ray1[1],ray1[2])
# for i in range(1):
x=[]
y=[]
z=[]
for i in range(500):
    plotting(locals()['ray%d' % (i)] [0],locals()['ray%d' % (i)] [1],locals()['ray%d' % (i)] [2])
    x=np.append(x,locals()['ray%d' % (i)] [0])
    y=np.append(y,locals()['ray%d' % (i)] [1])
    z=np.append(z,locals()['ray%d' % (i)] [2])
    print(x)



    # plotting(locals()['ray%d' % (i)] [0][:6],locals()['ray%d' % (i)] [1][:6],locals()['ray%d' % (i)] [2][:6])
    # plotting(locals()['ray%d' % (i)] [0][5:],locals()['ray%d' % (i)] [1][5:],locals()['ray%d' % (i)] [2][5:])

    # plotting(locals()['ray%d' % (i)] [0][:40],locals()['ray%d' % (i)] [1][:40],locals()['ray%d' % (i)] [2][:40])

h3=ax3.hist2d(x,y,bins=70)
h4=ax4.hist2d(z,y,bins=70)
ax3.set_xlabel('x [mm]')
ax3.set_ylabel('y [mm]')
ax4.set_xlabel('z [mm]')
ax4.set_ylabel('y [mm]')
fig3.colorbar(h3[3], ax=ax3)
fig4.colorbar(h4[3], ax=ax4)
plt.show()
