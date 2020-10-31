from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
from skimage import feature
from pathlib import Path
import argparse
import numpy as np
from tqdm import tqdm
import cv2
import os
import threading
import time
from datetime import datetime
import mahotas


class LocalBinaryPatterns:
    def __init__(self, numPoints, radius):
        # store the number of points and radius
        self.numPoints = numPoints
        self.radius = radius

    def describe(self, image, eps=1e-7, direct_lbp=False):
        # compute the Local Binary Pattern representation
        # of the image, and then use the LBP representation
        # to build the histogram of patterns
        lbp = feature.local_binary_pattern(image, self.numPoints,
                                           self.radius, method="uniform")
        if direct_lbp:
            return lbp

        (hist, _) = np.histogram(lbp.ravel(),
                                 bins=np.arange(0, self.numPoints + 3),
                                 range=(0, self.numPoints + 2))

        # normalize the histogram
        hist = hist.astype("float")
        hist /= (hist.sum() + eps)

        # return the histogram of Local Binary Patterns
        return hist


def parse_args():
    parser = argparse.ArgumentParser(
        description='Deep Learning Using Support Vector Machine for Malware Classification')
    group = parser.add_argument_group('Arguments')
    group.add_argument('-m', '--model', required=True, type=int,
                       help='[1] Local Binary Pattern')
    group.add_argument('-i', '--input_path', required=True, type=str,
                       help='path to the input db')
    group.add_argument('-o', '--output_path', required=True, type=str,
                       help='path in where features are saved')
    group.add_argument('-t', '--max_threads', required=False, type=int, default=4,
                       help='max number of threads')

    arguments = parser.parse_args()
    return arguments

def main(arguments):

    model_choice = arguments.model
    assert model_choice == 1 or model_choice == 2 ,\
        'Invalid choice: Choose among 1, 2, 3, 4 and 5 only.'


    #base_path = '/home/vincenzo/TesiVincenzo/DATASET1/realdata_PREPROCESSED/'
    input_db = arguments.input_path
    output_db = arguments.output_path
    files = sorted(glob.glob(input_db + "*.png"))
    in_path = ['training/train/Malware/', 'training/train/Trusted/',
               'training/validation/Malware/', 'training/validation/Trusted/',
               'test/Malware/', 'test/Trusted/']


    if model_choice == 1:
        model_name = "LBP_{}".format(datetime.now().strftime("%d-%b-%Y_%H%M"))
        desc = LocalBinaryPatterns(30, 16)
        i = 0
        for paths in in_path:
            path_ = input_db + in_path[i]
            print(path_)
            files = sorted(glob.glob(path_ + '*.png'))
            print(files)
            j = 0
            for myFile in tqdm(files):
                filename = Path(files[j]).name
                image = cv2.imread(files)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                feat = desc.describe(gray)
                out_name = output_db + filename
                print('feature shape: ' + feat.shape)
                print(out_name)
                cv2.imwrite(out_name, feat)#dovrebbe salvare np in png
                j += 1
            i += 1
    elif model_choice == 2:
        model_name = "Haralick_{}".format(datetime.now().strftime("%d-%b-%Y_%H%M"))
        i = 0
        for paths in in_path:
            files = sorted(glob.glob(in_path[i]+'*png'))
            filename = Path(files).name
            for myFile in tqdm(files):
                image = cv2.imread(files)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # compute the haralick texture feature vector
                haral = mahotas.features.haralick(gray).mean(axis=0)
                humom = cv2.HuMoments(cv2.moments(gray)).flatten()
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                # compute the color histogram
                hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
                # normalize the histogram
                cv2.normalize(hist, hist)
                hist = hist.flatten()
                feat = np.hstack([hist, haral, humom])
                out_name = output_db + filename
                print('feature shape: ' + feat.shape)
                print(out_name)
                cv2.imwrite(out_name, feat)#dovrebbe salvare np in png
            i += 1


if __name__ == '__main__':
    args = parse_args()

    main(args)
