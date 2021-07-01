import matplotlib.pyplot as plt
import numpy as np
ring = 3
test = 0
x=np.array([0,50,150,250,350,450,550,600,605,630,660,690,730,734,735,736,737,737.5,738,738.5,739,739.5,740,741,742,743,750,780,810,850,900,950,1050,1100])
print(len(x))
edge=np.loadtxt("output/camera_light_ray_ring%d_test%d_zoom_edge.txt"%(ring,test))
x_length = edge[:,3]-edge[:,2]
print(len(x_length ))
plt.plot(x,x_length)
plt.axvline(x=738.5,color="r",ls="--",label="min at x=738.5")
plt.xlabel("Distance from M4 [mm]")
plt.ylabel("Image Size along local x-axis [mm]")
plt.legend()
plt.show()
