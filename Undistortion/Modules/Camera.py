import numpy as np
import Config as cf

class Camera:
      def __init__(self, npxlX=484, npxlY=704, fdist=60., taperX=40/18, taperY=40/18, pxlsize_X= 18.0e-3,
                   pxlsize_Y =16.4e-3, xOffset = 0.0, yOffset = 0.0,):
          self.npxlX = npxlX
          self.npxlY = npxlY
          self.fdist = fdist
          self.xOffset = xOffset
          self.yOffset = yOffset
          self.pxlsize_X = pxlsize_X
          self.pxlsize_Y = pxlsize_Y
          self.taperX = taperX
          self.taperY = taperY

      def __del__(self):
          print('Camera deleted.')

      def SetPixels(self, npxlX, npxlY):
          self.npxlX = npxlX
          self.npxlY = npxlY

      def SetDistance(self, dist):
          self.fdist = dist

      def GetPixels(self):
          return self.npxlX, self.npxlY

      def GetDistance(self):
          return self.fdist

      def BeamToPixelsCam(self, X):

          xPxlCenter = self.npxlX / 2.
          yPxlCenter = self.npxlY / 2.

          # Transforming beam coordinates to pixels
          xBeam = X[:, 0]
          yBeam = X[:, 1]

          X_pxl = np.zeros(X.shape)
          X_pxl[:, 0] = -xBeam / (self.taperX * self.pxlsize_X) + xPxlCenter
          X_pxl[:, 1] = yBeam / (self.taperY * self.pxlsize_Y) + yPxlCenter

          X_pxl = X_pxl[X_pxl[:, 0] >= 0]
          X_pxl = X_pxl[X_pxl[:, 0] <= 484]
          X_pxl = X_pxl[X_pxl[:, 1] >= 0]
          X_pxl = X_pxl[X_pxl[:, 1] <= 704]

          return X_pxl

      def PixelsToBeamCam(self, X):

          xPxlCenter = self.npxlX / 2.
          yPxlCenter = self.npxlY / 2.

          # Transforming beam coordinates to pixels
          xPxl = X[:, 2]
          yPxl = X[:, 1]

          X_beam = np.zeros(X.shape)
          X_beam[:, 0] = -(xPxl - xPxlCenter) * (self.taperX * self.pxlsize_X)
          X_beam[:, 1] = (yPxl - yPxlCenter) * (self.taperY * self.pxlsize_Y)

          return X_beam

      def BeamToPixelsFoil(self, X):

          xPxlCenter = self.npxlX / 2.
          yPxlCenter = self.npxlY / 2.

          # Transforming beam coordinates to pixels
          xBeam = X[:, 0]
          yBeam = X[:, 1]

          X_pxl = np.zeros(X.shape)
          X_pxl[:, 0] = -xBeam / (self.taperX * cf.M3['f']/cf.M4['f'] * self.pxlsize_X) + xPxlCenter
          X_pxl[:, 1] = yBeam / (self.taperY * cf.M3['f']/cf.M4['f'] * self.pxlsize_Y) + yPxlCenter

          X_pxl = X_pxl[X_pxl[:, 0] >= 0]
          X_pxl = X_pxl[X_pxl[:, 0] <= 484]
          X_pxl = X_pxl[X_pxl[:, 1] >= 0]
          X_pxl = X_pxl[X_pxl[:, 1] <= 704]

          return X_pxl

      def PixelsToBeamFoil(self, X):

          xPxlCenter = self.npxlX / 2.
          yPxlCenter = self.npxlY / 2.

          # Transforming beam coordinates to pixels
          xPxl = X[:, 2]
          yPxl = X[:, 1]

          X_beam = np.zeros(X.shape)
          X_beam[:, 0] = -(xPxl - xPxlCenter) * (self.taperX * cf.M3['f']/cf.M4['f'] * self.pxlsize_X)
          X_beam[:, 1] = (yPxl - yPxlCenter) * (self.taperY * cf.M3['f']/cf.M4['f'] * self.pxlsize_Y)

          return X_beam