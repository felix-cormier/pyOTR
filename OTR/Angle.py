import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

name_phi = 'phi'
name_theta = 'theta'
name_boo_M1 = 'boo_M1'

with open('output/%s.txt'%(name_phi)) as f:
    phi = [ [float(item) for item in lines.split()] for lines in f]

with open('output/%s.txt'%(name_theta)) as f:
    theta = [ [float(item) for item in lines.split()] for lines in f]

with open('output/%s.txt'%(name_boo_M1)) as f:
    keep = [ [bool(int(item)) for item in lines.split()] for lines in f]

list_phi0=[]
list_theta0=[]

for i in range (len(phi)):
    phi0 = np.array(phi[i])
    theta0 = np.array(theta[i])

    phi0 = phi0[keep[i]]
    theta0 = theta0[keep[i]]
    
    if any(keep):
        list_phi0 = np.append(list_phi0,phi0,axis=0)
        list_theta0 = np.append(list_theta0,theta0,axis=0)

list_phi0 = np.array(list_phi0)
list_theta0 = np.array(list_theta0)

print(len(list_theta0))

fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(10,3))
h2=ax2.hist(list_theta0,bins=70)
h3=ax3.hist(list_phi0,bins=70)

print(h2[1])
ax2.set_xlabel("$\\theta$")
ax3.set_xlabel("$\\phi$")
#ax2.set_yscale('log')
#ax3.set_yscale('log')
#h = ax1.hist2d(list_phi0,list_theta0,bins=70,norm=colors.LogNorm())
h = ax1.hist2d(list_phi0,list_theta0,bins=70)
ax1.set_xlabel("$\\phi$")
ax1.set_ylabel("$\\theta$")
fig.colorbar(h[3], ax=ax1)
plt.tight_layout()
plt.show()
