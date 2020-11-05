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
    group.add_argument('-i', '--input_path', required=True, type=str,
                       help='path to the input db')
    group.add_argument('-o', '--output_path', required=True, type=str,
                       help='path in where features are saved')
    arguments = parser.parse_args()
    return arguments


def flat_to_square(flat):
    size = flat.size
    dim = 5
    square = dim*dim
    while square < size:
        dim += 1
        square = dim*dim
    if square == size:
        flat = np.reshape(flat, (dim, dim))
        return flat
    else:
        padding = square - size
        flat = np.pad(flat, (0, padding), 'constant', constant_values=0)
        flat = np.reshape(flat, (dim, dim))
        return flat


def main(arguments):
    input_db = arguments.input_path
    output_db = arguments.output_path
    in_path = ['training/train/malware/', 'training/train/trusted/',
               'training/val/malware/', 'training/val/trusted/',
               'test/malware/', 'test/trusted/']
    desc = LocalBinaryPatterns(30, 16)
    i = 0
    for paths in in_path:
        path_ = input_db + in_path[i]
        files = sorted(glob.glob(path_ + '*.png'))
        j = 0
        for myFile in tqdm(files):
            filename = Path(files[j]).name
            image = cv2.imread(files[j])
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # compute the haralick texture feature vector
            lbp = desc.describe(gray, cv2.COLOR_BGR2GRAY)
            haral = mahotas.features.haralick(gray).mean(axis=0)
            humom = cv2.HuMoments(cv2.moments(gray)).flatten()
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            # compute the color histogram
            hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            # normalize the histogram
            cv2.normalize(hist, hist)
            hist = hist.flatten()
            lbp = lbp.flatten()
            feat = np.hstack([lbp, hist, haral, humom])
            #feat = np.pad(feat, (0, 12), 'constant', constant_values=0) #lenght:576 (24,24)
            #feat = np.reshape(feat, (24, 24))
            out_name = output_db + in_path[i] + filename
            #print('feature shape: {}' .format(feat.shape))
            feat = flat_to_square(feat)
            feat = cv2.convertScaleAbs(feat, alpha=(255.0))
            cv2.imwrite(out_name, feat)#dovrebbe salvare np in png
            j += 1
        i += 1


if __name__ == '__main__':
    args = parse_args()

    main(args)
