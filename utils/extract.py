from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import glob
import numpy as np
from tqdm import tqdm
import config as mc
from skimage import feature
from sklearn.svm import LinearSVC
from imutils import paths
import argparse
import cv2
import os
import threading
import time
from datetime import datetime
import mahotas
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
