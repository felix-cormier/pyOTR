import concurrent.futures
import numpy as np
import Modules.Config as cf
import Modules.Geometry as Geometry
from include.PrepareData import PrepareData
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import colors


@cf.timer
def SimulateOTR(X, V, system):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(system.TraceRays, X, V)
        for i, result in enumerate(results):
            if i % 100 == 0:
                cf.logger.debug(f'Running data piece: {i}')
            x, v = result
            assert x.shape == v.shape
            if i == 0:
                Xf = np.array(x)
                Vf = np.array(v)
            else:
                Xf = np.concatenate((Xf, x), axis=0)
                Vf = np.concatenate((Vf, v), axis=0)

    Xf = np.array(Xf)
    Vf = np.array(Vf)
    # print (Xf)
    return Xf, Vf

def set_plot(fig,ax,h_c,title,filename):
    ax.set_xlabel("x-axis [mm]")
    ax.set_ylabel("y-axis [mm]")
    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
    ax.set_title(title)
    fig.colorbar(h_c, ax=ax)
    fig.savefig(filename+".pdf")

if __name__ == '__main__':

    cf.GetTime()

    ### Get details about the beam ###
    #X = np.load(cf.inputs.format('X'))
    #V = np.load(cf.inputs.format('V'))

    ### test data ###
    # from the origin
    # X = np.array([[0,2,1],[0,1.5,0.5],[0,1.5,0.5],[0,0,2.5],[0,1,2]])
    # V = np.array([[1,0,0,],[1,0,0],[1,0,0],[1,0,0],[1,0,0]])

    # from the top
    # X = np.array([[-1100. + 2*cf.M4['f'],6522+2,1],[-1100. + 2*cf.M4['f'],6522+1.5,0.5],[-1100. + 2*cf.M4['f'],6522+1.5,0.5],[-1100. + 2*cf.M4['f'],6522+0,2.5],[-1100. + 2*cf.M4['f'],6522+1,2]])
    # V = np.array([[-1,0,0,],[-1,0,0],[-1,0,0],[-1,0,0],[-1,0,0]])

    ### Monte-Carlo data ###
    N = 500000
    # r = 2.5 * np.random.uniform(0,1,N) # light rays in Gaussian
    r = 2.5                            # light rays in Circular Ring

    zero  = np.zeros(N)
    one   = np.ones(N)
    theta = np.random.uniform(0,2*np.pi,N)
    x     = r*np.cos(theta)
    y     = r*np.sin(theta)

    # from the origin
    # X = np.transpose(np.array([zero,y,x]))
    # V = np.transpose(np.array([1*one,zero,zero]))
    # h_p = np.histogram2d(-X[:,2]*300/550,X[:,1]*300/550, bins=100)

    # from the top
    X = np.transpose(np.array([(-1100. + 2*cf.M4['f'])*one,6522+y,x]))
    V = np.transpose(np.array([-1*one,zero,zero]))


    ### Plot the Generated Pattern ###
    fig0, ax0 = plt.subplots()
    h0 = ax0.hist2d(-X[:,2],X[:,1]-6522,bins=100)
    set_plot(fig0,ax0,h0[3],"Generated","gen_light_ray_ring2_test3")

    ### Start the simulation ###
    if cf.chunck > 0:
        X, V = PrepareData(X, V, chunck=cf.chunck)

    # Get the optical components to be simulated:
    system = Geometry.GetGeometry()

    # Run simulation:
    X, V = SimulateOTR(X, V, system)

    if cf.save:
        np.save(f'{cf.name}_Xfinal', X)
        np.save(f'{cf.name}_Vfinal', V)

    cf.GetTime(start=False)


    ### Plot the Observed Pattern ###
    fig, ax = plt.subplots()
    h = ax.hist2d(X[:,0],X[:,1],bins=100)
    # h = ax.hist2d(X[:,0],X[:,1], bins=100)
    set_plot(fig,ax,h[3],"Observed","camera_light_ray_ring2_test3")


    ### Find and Plot the Distortion ###
    fig1, ax1 = plt.subplots()
    diff = h[0] - h0[0]
    # diff = h[0] - h_p[0] # if from the bottom
    norm = colors.TwoSlopeNorm(vcenter=0)
    h1   = ax1.pcolorfast(h[1],h[2],diff,cmap='bwr',norm=norm)
    set_plot(fig1,ax1,h1,"Distortion","camera_light_ray_ring2_diff3")

    plt.show()
