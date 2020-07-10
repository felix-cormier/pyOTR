   #For calibration foil
   def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get X interaction points and V reflected:
        Xint, Vr = self.PlaneTransport(X, V) #but PlaneTransport still removes
        passed = self.PassHole(Xint)
        # Remain V if P because goes through, otherwise bounces back as Vr
        Vr = np.array([v if p else vr
                       for p, v, vr in zip(passed, V, Vr)])
        # Transform back to the global coords:
        Xint = self.transform_coord.TransfrmPoint(Xint, inv=True)
        Vr = self.transform_coord.TransfrmVec(Vr, inv=True)
        return Xint, Vr
  
  #For metal foil
  def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get X interaction points and V reflected:
        Xint, Vr = self.PlaneTransport(X, V)

        #Vr = self.LightDist.GetLightRay(Vr)
    
        # Transform back to the global coords:
        Xint = self.transform_coord.TransfrmPoint(Xint, inv=True)
        Vr = self.transform_coord.TransfrmVec(Vr, inv=True)
        return Xint, Vr
