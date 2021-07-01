import numpy as np
from numpy import cos, arccos, arctan2, sin, pi, log, sqrt, exp
from numpy.random import seed
from numpy.random import rand
from scipy.stats import moyal
from random import random
from pynverse import inversefunc
import Modules.Config as cf

def Conv(deg):
    return (np.pi * deg) / 180.

def RotateZ(V, angle):
    M = np.array([[cos(angle), -sin(angle), 0.],
                  [sin(angle), cos(angle), 0.],
                  [0., 0., 1.]
                  ])
    return V.dot(M.T) #once you figure out if this is alright, ask Gabriel

def RotateZ2(V, angle):
    #can use this to efficiently make a bunch of matrices from a list of angles
    #matrices and vectors are broadcast together for speedy implementation
    c = np.cos(angle)
    s = np.sin(angle)
    z = np.zeros(angle.size)
    u=np.zeros(angle.size)#u for unit ** np.ones
    u.fill(1)
    M = np.array([c,-s,z,s,c,z,z,z,u])#create new row every third element, get z-rot matrix
    M=M.T
    M=M.reshape(angle.size,3,3)
    V = np.einsum('...ikj,...ij->...ik',M,V)#should ensure you understand exactly why
    return V


def RotateX(V, angle):
    M = np.array([[1, 0, 0.],
                  [0, cos(angle), -sin(angle)],
                  [0., sin(angle), cos(angle)]
                  ])
    #dot(a,b)[i,j,k,m]=sum(a[i,j,:]*b[k,:,m])
    #V[i] = V[i,:] -- confusing
    return V.dot(M.T)#same as M.dot(V), but having touble with that

def RotateX2(V,angle):
    #can use this to efficiently make a bunch of matrices from a list of angles
    #matrices and vectors are broadcast together for speedy implementation
    c = np.cos(angle)
    s = np.sin(angle)
    z = np.zeros(angle.size)
    u=np.ones(angle.size)#u for unit ** np.ones
    M = np.array([u,z,z,z,c,-s,z,s,c])#create new row every third element, get x-rot matrix
    M=M.T
    M=M.reshape(angle.size,3,3)
    V = np.einsum('...ikj,...ij->...ik',M,V)#should ensure you understand exactly why
    return V

def SetRaysToZVelocity(V,theta,phi):
    V=RotateZ(V,phi)
    V=RotateX(V,theta)
    return V

def SetRaysToZVelocity2(V, theta, phi):
    V=RotateZ2(V,phi)
    V=RotateX2(V, theta)
    return V

def InvertSetRaysToZVelocity(V,theta,phi):
    V=RotateX(V,-theta)
    V=RotateZ(V,-phi)
    return V

def InvertSetRaysToZVelocity2(V, theta, phi):
    V=RotateX2(V, -theta)
    V=RotateZ2(V, -phi)
    return V


def Landau(mu, sigma):
    #Match TLandau? --Gabriel
    x = (x - mu) / sigma
    A = 1 / (2 * pi)
    A * np.exp(-(x + np.exp(-x)) / 2)


class LightDist():
    def __init__(self, seed=0):
        self.beam_gamma = cf.beam['gamma']
        self.theta_range = cf.foil['tht_range']  # rad
        self.f_thtMax = self.OTRcdf(self.theta_range) # cdf is monotonically increasing

    def OTRcdf(self, theta):
        gmma = self.beam_gamma #light beam gamma
        y = (theta*theta)*(gmma*gmma)
        otr = (lambda x: 0.5*(log(x+1)*(x+1)-x)/(x+1))
        return otr(y)

    def OTRcdf_inv(self, cdf_vals):
        gmma = self.beam_gamma #light beam gamma
        otr = (lambda x: 0.5*(log(x+1)*(x+1)-x)/(x+1))
        otr_inv = inversefunc(otr)
        theta = sqrt(otr_inv(cdf_vals))/gmma #solve for otr angle
        return theta

    def otr_func(self, x):
        gmma = self.beam_gamma
        y = (x*gmma)**2
        return 0.5*(log(y+1)*(y+1)-y)/(y+1)

    def otr_cdf(self, x):
        return self.otr_func(x)/self.otr_func(self.theta_range)

    def otr_pdf(self, x):
        norm = self.otr_func(self.theta_range)
        gmma = self.beam_gamma
        y = ((x*x*sin(x))/((gmma**-2+x**2)**2))/norm
        return y

    def GetOTRRays(self, V):
        theta=arccos(V[0][2])
        phi=arctan2(V[0][0],V[0][1])
        V=SetRaysToZVelocity(V,theta,phi)
        for x in range(0,V.shape[0]):
            rand= self.f_thtMax*random() #random angle 0-max
            oangle = self.OTRcdf_inv(rand)
            rand=Conv(360)*random() #random angle 0-360
            V[x]=RotateX(V[x],-oangle)
            V[x]=RotateZ(V[x],rand)
        V=InvertSetRaysToZVelocity(V,theta,phi)
        return V

    def GetOTRRays2(self, V):
        #seed(1)
        theta=arccos(V[:,2])
        phi=arctan2(V[:,0],V[:,1])
        V=SetRaysToZVelocity2(V,theta,phi)
        #rand_angs = self.f_thtMax*rand(theta.size)
        #oangle = self.OTRcdf_inv(rand_angs)
        #rand_angs = Conv(360)*rand(theta.size)
        oangle = np.zeros(theta.size)
        rand = np.zeros(theta.size)

        for i in range(0,V.shape[0]):
            otr_rand = self.f_thtMax*random() #random angle 0-max
            oangle[i] = self.OTRcdf_inv(otr_rand) #slow step
            rand[i] = Conv(360)*random() #random angle 0-360

        V = RotateX2(V,-oangle)
        V = RotateZ2(V,rand)
        V = InvertSetRaysToZVelocity2(V,theta,phi)
        return V

    def GetOTRRays3(self, V):
        #seed(1)
        theta=arccos(V[:,2])
        phi=arctan2(V[:,0],V[:,1])
        V=SetRaysToZVelocity2(V,theta,phi)
        rand_angs = self.f_thtMax*rand(theta.size)
        oangle = self.OTRcdf_inv(rand_angs)
        rand_angs = Conv(360)*rand(theta.size)
        V = RotateX2(V,-oangle)
        V = RotateZ2(V,rand_angs)
        V = InvertSetRaysToZVelocity2(V,theta,phi)
        return V

    def GetOTRRays4(self,V):
        #Initialize
        n = V.shape[0]
        val = sqrt(3)/self.beam_gamma
        xmin, xmax = 0, self.theta_range
        fmin,fmax = 0, self.otr_pdf(val)
        oangles = np.zeros(n)
        rangles = Conv(360)*rand(n)

        #Loop for OTR angles
        i = 0
        while i < n:
            x = xmin + random()*(xmax-xmin)
            u = fmin + random()*(fmax-fmin)
            if u < self.otr_pdf(x):
                oangles[i] = x
                i = i+1

        np.save('mc_otr',oangles)
        #Set V to z-axis
        theta=arccos(V[:,2])
        phi=arctan2(V[:,0],V[:,1])
        V=SetRaysToZVelocity2(V,theta,phi)

        #Create OTR photons
        V = RotateX2(V,-oangles)
        V = RotateZ2(V,rangles)
        V = InvertSetRaysToZVelocity2(V,theta,phi)
        return V

    def MoyalScatter(self, V):
        #Point ray to z axis
        theta=arccos(V[:,2])
        phi=arctan2(V[:,0],V[:,1])
        #Scatter according to landau approximation
        mean = 5.794
        sigma = 3.766
        V=SetRaysToZVelocity2(V,theta,phi)
        sangles = moyal.rvs(size=V.shape[0])*sigma+mean#in degrees
        sangles=Conv(sangles) #now radians
        rand_angs = Conv(360)*rand(theta.size)
        V = RotateX2(V,-sangles)
        V = RotateZ2(V,rand_angs)
        #Reorient ray
        V = InvertSetRaysToZVelocity2(V,theta,phi)
        return V

#   def OtrCDF(self, x=[], pars=[]):
#       y = x[0] * x[0] * pars[0] * pars[0]
#       return 0.5 * ((y + 1) * np.log(y + 1) - y) / (y + 1)
#
#   def SetScatterOption(self, h, s, o):
#       # Note that hav_on negates scat_on/otr_on
#       # Having scat_on/otr_on as separatue values allows user to look at
#       # 1)Perfect otr -- just otr_on
#       # 2)Scatter sans otr -- just scat_on
#       # 3)The full combination -- otr_on/scat_on
#       # 4)Perfect reflection -- all options set to false
#       self.hav_on = h
#       self.scat_on = s
#       self.otr_on = o
#
#   def GetScatterOption(self, type):
#       if type == 1:
#           return self.hav_on
#       elif type == 2:
#           return self.scat_on
#       elif type == 3:
#           return self.otr_on
#       return -1
#
#   def ScatterAngle(self, i):
#       # mean / sigma are hardcoded as the values obtained for landau distributions
#       # at 600 nm, averaged paralell and perpendicular striations
#       # order for possible choices = {Ti - 15V - 3Cr - 3Sn - 3Al, Ti - 6Al - 4V}
#       mean = [5.794, 1.986]
#       sigma = [3.766, 2.663]
#       angle = -1
#       while(angle < 0):
#           angle = 1  # -> Landau(mean[i], sigma[i])
#       return angle * pi / 180.
#
#   def SetAxesToZVelocity(self, light_ray):
#       # This function rotates a vector with the coordinates of the light ray up onto the z axis
#       # Once rotated, using probabilistic scatter distribution to alter direction of light ray is simple
#       # Note that rotations in reverse happen in the opposite order in GetLightRay
#       return_ray = light_ray.copy()
#       theta, phi = self.GetAngles(return_ray)
#       # need to define these rotations:
#       return_ray = RotateZ(return_ray, pi / 2 - phi)
#       return_ray = RotateX(return_ray, theta)
#       return return_ray
#
#   def DistributeLight(self, light_ray, sangle):
#       # This is where the random scatter occurs -- sangle from scatter distribution
#       # or otr distribution later in the code, then rangle randomly selected 0 - 2pi
#       return_ray = np.zeros(3)
#       rangle = 2 * pi * np.random.uniform(0, 1)
#       return_ray[0] = light_ray[2] * sin(sangle) * cos(rangle)
#       return_ray[1] = light_ray[2] * sin(sangle) * sin(rangle)
#       return_ray[2] = light_ray[2] * cos(sangle)
#       return return_ray
#
#   def SetGamma(self, gamma):
#       self.beam_gamma = gamma
#       fOtrCdf -> SetParameter(0, fBeamGamma)
#       fTht_max = fOtrCdf -> GetMaximum(0.0, fTht_range)
#
#   def SampleOtr(self, gamma, fillh):
#       if gamma != self.beam_gamma:
#           self.SetGamma(gamma)
#       fval = self.fTht_max * np.random.uniform(0, 1.)
#       xval = fOtrCdf -> GetX(fval, 0, fTht_range)
#       if fillh:
#           if fHdist:
#               fHdist -> Fill(xval)
#           else:
#               fHdist = new TH1D("ang_dist", "ang_dist", 100, 0.0, fTht_range)
#               fHdist -> Fill(xval)
#       return xval
#
#   def SampleDiff(self, tht_range, fillh):
#       if(tht_range == 0)
#           return 0.0
#       cosa = 1 + (cos(tht_range) - 1) * np.random.uniform(0, 1.)
#       xval = np.arccos(cosa)
#       if fillh:
#           if fHdist:
#               fHdist -> Fill(xval)
#       else:
#           fHdist = new TH1D("ang_dist", "ang_dist", 100, 0.0, fTht_range)
#           fHdist -> Fill(xval)
#   return xval
#
#   def GetAngles(self, ray):
#       r = np.sqrt(ray[0] * ray[0] + ray[1] * ray[1] + ray[2] * ray[2])
#       return np.arccos(ray[2] / r), np.arctan2(ray[1] / ray[0])
#
#   def GetLightRay(self, V, angl_sprd, gamma, tht_range):
#       # New method
#       light_ray = np.array(V)
#       sangle = self.ScatterAngle(0)
#       oangle
#       theta_one, phi_one = self.GetAngles(light_ray)
#       # Original method
#       tht0, phi0 = self.GetAngles(V)
#       count = 0
#       rval = 1.
#       # New method for OTR light distribution
#       if(self.hav_on == 0):
#           # Rotate axes s.t. z axis points in the direction in which particle travels
#           light_ray = self.SetAxesToZVelocity(light_ray, true)
#           # Choose value for oangle
#           if(gamma != 0.):  # Otr light
#               oangle = self.SampleOtr(gamma)
#           else:
#               oangle = self.SampleDiff(tht_range)
#           # Incorporate scatter
#           if(self.scat_on == 1):
#               # Light is scattered about reflection axis given experimental data
#               light_ray = self.DistributeLight(light_ray, sangle, true)
#               theta_two, phi_two = self.GetAngles(light_ray)
#               # Rotate into coordinate system of scattered particle
#               light_ray = self.SetAxesToZVelocity(light_ray, true)
#               # Light comes out in a cone with angular distribution given by OTR_CDF / SamleDiff
#               if(self.otr_on == 1):
#                   light_ray = self.DistributeLight(light_ray, oangle, true)
#               # Rotate back - - inverse rotations have inverse order
#               if(self.scat_on == 1):
#                   light_ray.RotateX(-theta_two)
#                   light_ray.RotateZ(-M_PI / 2 + phi_two)
#
#               light_ray.RotateX(-theta_one)
#               light_ray.RotateZ(-M_PI / 2 + phi_one)
#               # Set final vx, vy, vz
#               vx = light_ray[0]
#               vy = light_ray[1]
#               vz = light_ray[2]
#       else:
#           # Original method for OTR light distribution
#           if(gamma != 0.):  # Otr light
#               oangle = self.SampleOtr(gamma)
#           else:
#               oangle = self.SampleDiff(tht_range)
#           count = 0
#           rval = 1.
#           while (rval > angl_sprd):
#               if(count > 10000):
#                   print("WARNING: ")
#                   break
#               tht1 pi / 3 * np.random.uniform(0, 1.) + tht0 - pi / 6
#               phi1 = 2 * pi i * np.random.uniform(0, 1.)
#               rval = self.DistanceDiff(oangle, phi0, tht0, phi1, tht1)
#               count += 1
#           # Calculate the ray direction
#           vx = cos(phi1) * sin(tht1)
#           vy = sin(phi1) * sin(tht1)
#           vz = cos(tht1)
#       V = np.array([vx, vy, vz])
#       return V
#
#   def DistanceDiff(self, oangle, phi0, theta0, phi1, theta1):
#       lat0 = pi / 2 - theta0
#       lat1 = pi / 2 - theta1
#       dlat = lat1 - lat0
#       dphi = phi1 - phi0
#       sindl = sin(dlat / 2)
#       sindphi = sin(dphi / 2)
#       sina = sin(oangle / 2)
#       lhs = sina * sina
#       rhs = sindl * sindl + cos(lat0) * cos(lat1) * sindphi * sindphi
#       return np.fabs(lhs - rhs)
