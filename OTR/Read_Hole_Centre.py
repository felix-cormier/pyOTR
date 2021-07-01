import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy.optimize import curve_fit

def func_x(x, a,b):
    return a+b*x

def func_y(x, a,b):
    return a+b*x

# def func_y(x, a,b):
#     return a+b*x
# def func_y(x, a,b,c,d):
#     return a+b*x+c*x**2+d*x**3
# def func_y(x, a, b,c,d,e,f):
#     return a+b*x+c*x**2+d*x**3+e*x**4+f*x**5
# px = np.arange(50,650,100);px=np.append(px,600);px=np.append(0,px)
px=np.arange(-5,6,1)
# px=np.arange(-10,11,1)
# px=np.arange(-50,60,5)
# px=0.1*px
print(px)
oc="M1"
# direction="vertical"
direction="horizontal"
centre = np.loadtxt("output/Holecentre_%s.txt"%(oc))
x = centre[:,0]
y = centre[:,1]
n=5
list_avg_x=[]
list_err_m_x=[]
list_avg_y=[]
list_err_m_y=[]
for i in range (0,len(px)*5,n):
    avg_x = sum(x[i:i+n])/n
    sd_x = np.sqrt(sum((x[i:i+n]-avg_x)**2)/(n-1))
    err_m_x=sd_x/np.sqrt(n)
    avg_y = sum(y[i:i+n])/n
    sd_y = np.sqrt(sum((y[i:i+n]-avg_y)**2)/(n-1))
    err_m_y=sd_y/np.sqrt(n)
    list_avg_x.append(avg_x)
    list_err_m_x.append(err_m_x)
    list_avg_y.append(avg_y)
    list_err_m_y.append(err_m_y)

popt_x, pcov_x = curve_fit(func_x,px,list_avg_x,sigma=list_err_m_x)
popt_y, pcov_y = curve_fit(func_y,px,list_avg_y,sigma=list_err_m_y)
perr_x = np.sqrt(np.diag(pcov_x))
perr_y = np.sqrt(np.diag(pcov_y))

print(list_avg_x)
print(list_avg_y)
print(popt_x,perr_x)
print(popt_y,perr_y)

f_x = popt_x[0]/popt_x[1]
f_x_err = np.sqrt((perr_x[0]/popt_x[1])**2+(popt_x[0]*perr_x[1]/popt_x[1]**2)**2)
f_y = popt_y[0]/popt_y[1]
f_y_err = np.sqrt((perr_y[0]/popt_y[1])**2+(popt_y[0]*perr_y[1]/popt_y[1]**2)**2)
print(f_x,f_x_err)
print(f_y,f_y_err)


y_true = -(px*popt_y[0]/(-f_x)-popt_y[0])
y_diff = list_avg_y-y_true
print(y_true)
print("y_diff",y_diff)
y_diff_err=[]
for i in range(len(y_diff)):
    y_true_err=((px[i]/(-f_x)-1)*perr_y[0])**2+(px[i]*popt_y[0]*f_x_err/(f_x**2))**2
    print(y_true_err)
    y_diff_err0 = np.sqrt((list_err_m_y[i])**2+y_true_err)
    y_diff_err.append(y_diff_err0)
# y_diff_err = [np.sqrt((list_err_m_y[i])**2+(f_x_err*px[i])**2) for i in len(y_diff)]



nstd = 1. # to draw 5-sigma intervals
popt_up_x = popt_x + nstd * perr_x
popt_dw_x = popt_x - nstd * perr_x
popt_up_y = popt_y + nstd * perr_y
popt_dw_y = popt_y - nstd * perr_y

fit_x = func_x(px, *popt_x)
fit_up_x = func_x(px, *popt_up_x)
fit_dw_x = func_x(px, *popt_dw_x)
fit_y = func_y(px, *popt_y)
fit_up_y = func_y(px, *popt_up_y)
fit_dw_y = func_y(px, *popt_dw_y)


fig_x,ax_x = plt.subplots()
fig_y,ax_y = plt.subplots()
fig_y_diff,ax_y_diff = plt.subplots()

rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
rcParams['font.size']= 20
ax_x.errorbar(px,list_avg_x, yerr=list_err_m_x,marker='x',ms=5,capsize=2,ls="",ecolor='k', label='data')
ax_y.errorbar(px,list_avg_y, yerr=list_err_m_y,marker='x',ms=5,capsize=2,ls="",ecolor='k', label='data')
ax_y_diff.errorbar(px,y_diff, yerr=y_diff_err,marker='x',ms=5,capsize=2,ls="",ecolor='k', label='diff')

ax_x.plot(px,fit_x,'r', lw=2, label='best-fit (k=%.1e$\pm$%.1e)'%(popt_x[1],perr_x[1]))
ax_y.plot(px,fit_y,'r', lw=2, label='best-fit (k=%.1e$\pm$%.1e)'%(popt_y[1],perr_y[1]))
ax_x.fill_between(px, fit_up_x, fit_dw_x, alpha=.25, label='1-sigma')
ax_y.fill_between(px, fit_up_y, fit_dw_y, alpha=.25, label='1-sigma')
ax_x.set_xlabel("Shift from %s %s [mm]"%(oc,direction))
ax_x.set_ylabel("Centre x [mm]")
ax_y.set_xlabel("Shift from %s %s [mm]"%(oc,direction))
ax_y.set_ylabel("Centre y [mm]")
ax_y_diff.set_xlabel("Shift from %s %s [mm]"%(oc,direction))
ax_y_diff.set_ylabel("Diff y [mm]")

#plot
# fig, ax = plt.subplots(1)


# title(‘fit with only Y-error’, fontsize=18)


ax_x.legend(loc='lower right',fontsize=10)
ax_y.legend(loc='lower right',fontsize=10)
ax_y_diff.legend(loc='lower right',fontsize=10)
fig_x.savefig("output/FindHoleCentre1_%s_x"%(oc)+".png")
fig_y.savefig("output/FindHoleCentre1_%s_y"%(oc)+".png")
fig_y_diff.savefig("output/FindHoleCentre1_%s_y_diff"%(oc)+".png")

plt.show()
