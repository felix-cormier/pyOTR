import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import colors
import numpy as np

ring = 0
test = 0
loc = 'At M4f'
fig_e, ax_e = plt.subplots()

def set_plot(fig,ax,h_c,xlim,ylim,title,filename):
    ax.set_xlabel("x-axis [mm]",  fontsize  = 15)
    ax.set_ylabel("y-axis [mm]",  fontsize  = 15)
    ax.tick_params(axis = 'both', labelsize = 15)
    # ax.set_xlim(-9, 9)
    # ax.set_ylim(-9, 9)
    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)
    ax.set_title(title)
    cbar = fig.colorbar(h_c, ax = ax)
    cbar.ax.tick_params(labelsize = 15)
    ax.set_aspect('equal')
    fig.set_tight_layout(True)
    fig.savefig(filename+".png")

def fit_ellipse_gen(X1,X2,name,h0):
    A = np.hstack([(X1)**2, X1*X2, X2**2, X1, X2])
    b = np.ones_like(X1)
    x = np.linalg.lstsq(A, b)[0].squeeze()
    print('The ellipse is given by {0:.3}x^2 + {1:.3}xy+{2:.3}y^2+{3:.3}x+{4:.3}y = 1'.format(x[0], x[1], x[2], x[3], x[4]))

    x0 = (2*x[2]*x[3] - x[1]*x[4]) / (x[1]**2 - 4*x[0]*x[2])
    y0 = (2*x[0]*x[4] - x[1]*x[3]) / (x[1]**2 - 4*x[0]*x[2])
    a = -np.sqrt(2 * (x[0]*x[4]**2 + x[2]*x[3]**2 - x[1]*x[3]*x[4] + (x[1]**2 - 4*x[0]*x[2]) * (-1)) * ((x[0]+x[2]) + np.sqrt((x[0]-x[2])**2 + x[1]**2))) / (x[1]**2 - 4*x[0]*x[2])
    b = -np.sqrt(2 * (x[0]*x[4]**2 + x[2]*x[3]**2 - x[1]*x[3]*x[4] + (x[1]**2 - 4*x[0]*x[2]) * (-1)) * ((x[0]+x[2]) - np.sqrt((x[0]-x[2])**2 + x[1]**2))) / (x[1]**2 - 4*x[0]*x[2])
    phi2 = np.arctan(1/x[1] * (x[2] - x[0] - np.sqrt((x[0]-x[2])**2 + x[1]**2)))
    print(f'{name:s} - center: {x0:.3f}, {y0:.3f}; width: {(2*a):.3f}; height: {(2*b):.3f}; phi: {phi2:.3f}')

    X_coord, Y_coord = np.meshgrid(h0[1], h0[2])
    Z_coord = x[0] * X_coord ** 2 + x[1] * X_coord * Y_coord + x[2] * Y_coord**2 + x[3] * X_coord + x[4] * Y_coord
    c1      = ax_e.contour(X_coord, Y_coord, Z_coord, levels=[1], colors=('r'), linewidths=1)
    labels  = ['Original']
    for i in range(len(labels)):
        c1.collections[i].set_label(labels[i])
    # print(f'Expected - center: {0:.3f}, {0:.3f}; width: {(2.5*300/550):.3f}; height: {(2.5*300/550):.3f}; phi: {0:.3f}')

def fit_ellipse_obs(X1,X2,name,h):
    A = np.hstack([(X1)**2, X1*X2, X2**2, X1, X2])
    b = np.ones_like(X1)
    x = np.linalg.lstsq(A, b)[0].squeeze()
    print('The ellipse is given by {0:.3}x^2 + {1:.3}xy+{2:.3}y^2+{3:.3}x+{4:.3}y = 1'.format(x[0], x[1], x[2], x[3], x[4]))

    x0 = (2*x[2]*x[3] - x[1]*x[4]) / (x[1]**2 - 4*x[0]*x[2])
    y0 = (2*x[0]*x[4] - x[1]*x[3]) / (x[1]**2 - 4*x[0]*x[2])
    a = -np.sqrt(2 * (x[0]*x[4]**2 + x[2]*x[3]**2 - x[1]*x[3]*x[4] + (x[1]**2 - 4*x[0]*x[2]) * (-1)) * ((x[0]+x[2]) + np.sqrt((x[0]-x[2])**2 + x[1]**2))) / (x[1]**2 - 4*x[0]*x[2])
    b = -np.sqrt(2 * (x[0]*x[4]**2 + x[2]*x[3]**2 - x[1]*x[3]*x[4] + (x[1]**2 - 4*x[0]*x[2]) * (-1)) * ((x[0]+x[2]) - np.sqrt((x[0]-x[2])**2 + x[1]**2))) / (x[1]**2 - 4*x[0]*x[2])
    phi2 = np.arctan(1/x[1] * (x[2] - x[0] - np.sqrt((x[0]-x[2])**2 + x[1]**2)))
    print(f'{name:s} - center: {x0:.3f}, {y0:.3f}; width: {(2*a):.3f}; height: {(2*b):.3f}; phi: {phi2:.3f}')

    X_coord, Y_coord = np.meshgrid(h[1], h[2])
    Z_coord = x[0] * X_coord ** 2 + x[1] * X_coord * Y_coord + x[2] * Y_coord**2 + x[3] * X_coord + x[4] * Y_coord
    # X_coord*=550/300
    # Y_coord*=550/300
    c2 = ax_e.contour(X_coord, Y_coord, Z_coord, levels = [1], colors = ('b'), linewidths = 1)
    ax_e.set_xlim(np.min(X_coord) - 0.5, np.max(X_coord) + 0.5)
    ax_e.set_ylim(np.min(Y_coord) - 0.5, np.max(Y_coord) + 0.5)
    ax_e.set_aspect('equal')
    ax_e.set_xlabel("x-axis [mm]",  fontsize  = 15)
    ax_e.set_ylabel("y-axis [mm]",  fontsize  = 15)
    ax_e.tick_params(axis = 'both', labelsize = 15)
    labels = [loc]
    for i in range(len(labels)):
        c2.collections[i].set_label(labels[i])
    ax_e.legend()
    fig_e.set_tight_layout(True)
    fig_e.savefig("output/gen_light_ray_ring%d_compare%d"%(ring,test)+".png")
    # print(f'Expected - center: {0:.3f}, {0:.3f}; width: {(2.5*300/550):.3f}; height: {(2.5*300/550):.3f}; phi: {0:.3f}')

def plot_gen_top(X):
    ### Plot the Generated Pattern ###
    fig0, ax0 = plt.subplots()
    h0        = ax0.hist2d(X[:,2], X[:,1]-6522, bins=100)
    fit_ellipse_gen(X[:,2:], X[:,1:2]-6522, 'Original', h0)
    set_plot(fig0, ax0, h0[3], max(abs(X[:,2])) + 0.5, max(abs(X[:,1]-6522)) + 0.5, "Generated",   "output/gen_light_ray_ring%d_test%d"%(ring, test))
    return h0

def plot_gen_bottom(X):
    ### Plot the Generated Pattern ###
    fig0, ax0 = plt.subplots()
    h0        = ax0.hist2d(X[:,2], X[:,1], bins=100)
    # h0 = ax0.hist2d(X[:,0], X[:,1], bins=100)
    fit_ellipse_gen(X[:,2:], X[:,1:2], 'Original', h0)
    set_plot(fig0, ax0, h0[3], max(abs(X[:,2])) + 0.5, max(abs(X[:,1]    )) + 0.5, "Generated",   "output/gen_light_ray_ring%d_test%d"%(ring, test))
    return h0

def plot_obs(X):
    ### Plot the Observed Pattern ###
    fig, ax = plt.subplots()
    h       = ax.hist2d(-X[:,0], X[:,1], bins=100)

    # edges   = np.array([np.min(h[0]),np.max(h[0]),np.min(h[1]),np.max(h[1]),np.min(h[2]),np.max(h[2])])
    # with open("output/camera_light_ray_ring%d_test%d_zoom_edge.txt"%(ring,test),'a') as f:
    #     for item in edges:
    #         f.write("%.7f "%(item))
    #     f.write("\n")
    # # np.savetxt("output/camera_light_ray_ring%d_test%d_zoom_edge.txt"%(ring,test),)
    print('observed events:%d'%(h[0].sum()))
    fit_ellipse_obs(-X[:,0:1], X[:,1:2], loc, h)
    set_plot(fig, ax, h[3],    max(abs(X[:,0])) + 0.5, max(abs(X[:,1]   )) + 0.5, "Observed",    "output/camera_light_ray_ring%d_test%d"%(ring, test))
    return h

def plot_dist(X,h,h0):
    ### Find and Plot the Distortion ###
    fig1, ax1 = plt.subplots()
    diff      = h[0]-h0[0]
    norm      = colors.TwoSlopeNorm(vcenter=0)
    # norm    = colors.SymLogNorm(linthresh=1, linscale=1,vmin=-np.max(abs(diff)), vmax=np.max(abs(diff)), base=10)
    h1        = ax1.pcolor(h[1], h[2], diff.T, cmap='bwr',norm=norm)
    # ax1.text(0.7, 0.9, 'M4f', transform=ax1.transAxes,fontsize=20)
    set_plot(fig1, ax1, h1,    max(abs(h[1])) + 0.5,   max(abs(h[2])) + 0.5,      "Distortion",  "output/camera_light_ray_ring%d_diff%d"%(ring, test))
