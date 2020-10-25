import concurrent.futures
import numpy as np
import sys
import Config as cf
import Camera as Camera
import DistortionMap as dm
import ControlPoints as cp

# @cf.timer
# def UndistortImage(X, V):
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         results = executor.map(DM.Undistort(), X, V)
#         for i, result in enumerate(results):
#             if i % 100 == 0:
#                 cf.logger.debug(f'Running data piece: {i}')
#             x, v = result
#             assert x.shape == v.shape
#             if i == 0:
#                 Xf = np.array(x)
#                 Vf = np.array(v)
#             else:
#                 Xf = np.concatenate((Xf, x), axis=0)
#                 Vf = np.concatenate((Vf, v), axis=0)
#
#     Xf = np.array(Xf)
#     Vf = np.array(Vf)
#     return Xf, Vf


if __name__ == '__main__':

    cf.GetTime()

    camera = Camera.Camera()

    # Provide the camera image in the configuration file:
    X = camera.BeamToPixelsCam(np.load(cf.inputs.format('X')))[:,0:2]
    CP_foil = cp.control_points_foil(camera)
    CP_cam  = cp.control_points_cam(camera)

    if len(CP_foil) != len(CP_cam):
        print("Control points are not of equal length, please check code")
        sys.exit()

    #To be determined
    # if cf.chunck > 0:
    #     X, V = PrepareData(X, V, chunck=cf.chunck)

    # Run simulation:
    X = dm.Undistort(X, CP_foil, CP_cam)

    if cf.save:
        np.save(f'{cf.name}_Xfinal', X)

    cf.GetTime(start=False)