import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import colors
import numpy as np

ring=0
test=0

def set_plot(fig,ax,h_c,title,filename):
    ax.set_xlabel("x-axis [mm]")
    ax.set_ylabel("y-axis [mm]")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_title(title)
    fig.colorbar(h_c, ax=ax)
    fig.savefig(filename+".pdf")

def fit_ellipse(X1,X2,name):
    A = np.hstack([(X1)**2, X1*X2, X2**2, X1, X2])
    b = np.ones_like(X1)
    x = np.linalg.lstsq(A, b)[0].squeeze()
    print('The ellipse is given by {0:.3}x^2 + {1:.3}xy+{2:.3}y^2+{3:.3}x+{4:.3}y = 1'.format(x[0], x[1], x[2], x[3], x[4]))
    x0 = (2*x[2]*x[3] - x[1]*x[4]) / (x[1]**2 - 4*x[0]*x[2])
    y0 = (2*x[0]*x[4] - x[1]*x[3]) / (x[1]**2 - 4*x[0]*x[2])
    a = -np.sqrt(2 * (x[0]*x[4]**2 + x[2]*x[3]**2 - x[1]*x[3]*x[4] + (x[1]**2 - 4*x[0]*x[2]) * (-1)) * ((x[0]+x[2]) + np.sqrt((x[0]-x[2])**2 + x[1]**2))) / (x[1]**2 - 4*x[0]*x[2])
    b = -np.sqrt(2 * (x[0]*x[4]**2 + x[2]*x[3]**2 - x[1]*x[3]*x[4] + (x[1]**2 - 4*x[0]*x[2]) * (-1)) * ((x[0]+x[2]) - np.sqrt((x[0]-x[2])**2 + x[1]**2))) / (x[1]**2 - 4*x[0]*x[2])
    phi2 = np.arctan(1/x[1] * (x[2] - x[0] - np.sqrt((x[0]-x[2])**2 + x[1]**2)))
    print(f'{name:s} - center: {x0:.3f}, {y0:.3f}; width: {a:.3f}; height: {b:.3f}; phi: {phi2:.3f}')
    # X_coord, Y_coord = np.meshgrid(h[1],h[2])
    # Z_coord = x[0] * X_coord ** 2 + x[1] * X_coord * Y_coord + x[2] * Y_coord**2 + x[3] * X_coord + x[4] * Y_coord
    # ax.contour(X_coord, Y_coord, Z_coord, levels=[1], colors=('r'), linewidths=1)
    # print(f'Expected - center: {0:.3f}, {0:.3f}; width: {(2.5*300/550):.3f}; height: {(2.5*300/550):.3f}; phi: {0:.3f}')

def plot_gen_top(X):
    ### Plot the Generated Pattern ###
    fig0, ax0 = plt.subplots()
    h0 = ax0.hist2d(-X[:,2], X[:,1]-6522, bins=100)
    fit_ellipse(-X[:,2:], X[:,1:2]-6522, 'Generated')
    set_plot(fig0, ax0, h0[3], "Generated","output/gen_light_ray_ring%d_test%d"%(ring,test))
    return h0

def plot_gen_bottom(X):
    ### Plot the Generated Pattern ###
    fig0, ax0 = plt.subplots()
    h0 = ax0.hist2d(-X[:,2], X[:,1], bins=100)
    fit_ellipse(-X[:,2:], X[:,1:2], 'Generated')
    set_plot(fig0, ax0, h0[3], "Generated","output/gen_light_ray_ring%d_test%d"%(ring,test))
    return h0

def plot_obs(X):
    ### Plot the Observed Pattern ###
    fig, ax = plt.subplots()
    h = ax.hist2d(X[:,0], X[:,1], bins=100)
    print(h[0].sum())
    fit_ellipse(X[:,0:1], X[:,1:2], 'Observed')
    set_plot(fig, ax, h[3], "Observed","output/camera_light_ray_ring%d_test%d"%(ring,test))
    return h

def plot_dist(X,h,h0):
    ### Find and Plot the Distortion ###
    fig1, ax1 = plt.subplots()
    diff = h[0]-h0[0]
    # diff = h[0]-h_p[0] # if from the bottom
    norm = colors.TwoSlopeNorm(vcenter=0)
    h1   = ax1.pcolor(h[1], h[2], diff.T, cmap='bwr', norm=norm)
    set_plot(fig1, ax1, h1, "Distortion", "output/camera_light_ray_ring%d_diff%d"%(ring,test))
