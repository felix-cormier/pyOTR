import numpy as np
import Geometry
import os
import pyOTR.Beam.Modules.MakeCalibHoles as MakeCalibHoles
import pyOTR.Undistortion.Modules.Geometry as Geometry
import pyOTR.OTR.pyOTR as pyOTR
import Config as cf


def control_points_foil(camera):
    file = cf.control_points_foil

    if os.path.isfile(file):
        control_points_foil_pxl = np.load(file)
        return control_points_foil_pxl

    else:
        control_points_foil_mm = MakeCalibHoles.MakeHoles()[:, [0, 2]]

    control_points_foil_mm = control_points_foil_mm[
        np.lexsort((-control_points_foil_mm[:, 0], control_points_foil_mm[:, 1]))]

    control_points_foil_mm[:, 0] = control_points_foil_mm[:, 0] * 0.5 * np.sqrt(2)
    np.save('data/calib_holes', control_points_foil_mm)

    control_points_foil_pxl = camera.BeamToPixelsFoil(control_points_foil_mm)
    control_points_foil_pxl = clean_controlpoints_foil(control_points_foil_pxl)

    np.save('data/calib_holes_foil', control_points_foil_pxl)

    return control_points_foil_pxl

def control_points_cam(camera):
    file = cf.control_points_cam

    if cf.data:
        control_points_cam_pxl = np.genfromtxt(file, delimiter=',')
        control_points_cam_pxl = clean_controlpoints_cam(control_points_cam_pxl)
        return control_points_cam_pxl

    else:
        if os.path.isfile(file):
            control_points_cam_pxl = np.load(file)
            return control_points_cam_pxl

        else:
            control_points_f = np.load('data/calib_holes.npy')
            system = Geometry.GetGeometry()

            V = np.zeros([len(control_points_f), 3])
            V[:, 2] = 1.
            control_points_f = np.c_[control_points_f, np.ones(len(control_points_f)) * -200]

            control_points_cam_mm, V = pyOTR.SimulateOTR(
                control_points_f.reshape(len(control_points_f), 1, 3),
                V.reshape(len(control_points_f), 1, 3), system)

            control_points_cam_pxl = camera.BeamToPixelsCam(control_points_cam_mm)

            np.save("data/calib_holes_cam.npy", control_points_cam_pxl)

            return control_points_cam_pxl
def clean_controlpoints_foil(X):

    X_clean = X[X[:,1]!=np.min(X[:, 1])]
    X_clean = X_clean[X_clean[:, 1] != np.max(X_clean[:, 1])]

    return X_clean

def clean_controlpoints_cam(X, X_offset = -7.335, Y_offset= 30.4):

    X_clean = X[X[:,1]!=np.min(X[:, 1])]
    X_clean = X_clean[X_clean[:, 1] != np.max(X_clean[:, 1])]
    X_clean[:, 0] = X_clean[:, 0] + X_offset
    X_clean[:, 1] = X_clean[:, 1] + Y_offset

    return X_clean
