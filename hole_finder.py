import numpy as np
import argparse
import glob
import json

import cv2

def hole_finder(settings, string):
    # load the image and convert it to grayscale
    input_files = []

    shift_file = open(settings.holeFindingPath+'shift_dictionary.json','r')
    shift_data = json.loads(shift_file.read())

    if shift_data['doShift']:
        for i, (m1shift, m2shift, m3shift, m4shift) in enumerate(zip(shift_data['Mirror1PosShift'],shift_data['Mirror2PosShift'],shift_data['Mirror3PosShift'], shift_data['Mirror4PosShift'])):
            input_files = []
            for hole_name in settings.hole_names:
                if 'none' in hole_name:
                    continue
                path = glob.glob(settings.holeFindingPath+'/'+'shift_'+str(i)+'/'+hole_name+'/images/Image*.pgm')
                if len(path) > 0:
                    input_files.append(path.pop())
            detect_holes(settings, string, input_files, shift_num=i)
    else:
        for hole_name in settings.hole_names:
            if 'none' in hole_name:
                continue
            if 'data' in string:
                input_files.append(glob.glob(settings.holeFindingPath+'/OA_Calib_'+hole_name+'*.pgm'))
            elif 'sim' in string:
                path = glob.glob(settings.holeFindingPath+'/'+hole_name+'/images/Image*.pgm')
                if len(path) > 0:
                    input_files.append(glob.glob(settings.holeFindingPath+'/'+hole_name+'/images/Image*.pgm').pop())
        detect_holes(settings, string, input_files)


def detect_holes(settings, string, input_files, shift_num=None):
    hole_pos = []
    hole_num = []
    input_files = input_files
    for file in input_files:
        print(file)
        if 'sim' in string:
            location  = file.split("/h",2)[1]
            location  = location.split("/",1)[0]
        elif 'data' in string:
            location  = file.split("_h",2)[1]
            location  = location.split(".",1)[0]
        if 'repro' in location and not '4' in location:
            continue
        elif 'repro' in location:
            location = location.split("_",1)[0]
        location = int(location)
        image = cv2.imread(file)
        if 'data' in string:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            image = cv2.flip(image,0)
        orig = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # apply a Gaussian blur to the image then find the brightest
        # region
        radius=41
        gray = cv2.GaussianBlur(gray, (radius, radius), 0)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        hole_pos.append(maxLoc)
        hole_num.append(location)
        image = orig.copy()
        cv2.circle(image, maxLoc, radius, (255, 0, 0), 2)
        # display the results of our newly improved method
        #cv2.imwrite('output/hole_findig_validation/opencv_h'+str(location)+'_'+string+'.png', image)
        cv2.waitKey(0)

        pos_0 = np.array(hole_pos)[:,0] 
        pos_0 = pos_0.reshape(pos_0.shape[0],1)
        pos_1 = np.array(hole_pos)[:,1] 
        pos_1 = pos_1.reshape(pos_1.shape[0],1)
        num = np.array(hole_num)
        num = num.reshape(num.shape[0],1)
        test = np.concatenate((pos_0,pos_1, num), axis=1)
        if shift_num is None:
            np.save(settings.holeFindingPath+'/'+string+'_hole_locator.npy', test)
        else:
            np.save(settings.holeFindingPath+'/'+'shift_'+str(shift_num)+'/'+string+'_hole_locator.npy', test)
