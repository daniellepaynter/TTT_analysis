# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 16:58:01 2023

Find "null" examples to add to training set

@author: dpaynter
"""

from skimage.io import imread, imsave
import numpy as np
import os
import matplotlib.pyplot as plt
import shutil
import pandas as pd
import cv2


png_path = r'J:\Danielle Paynter\PNGs_to_classify\0718F_5_redo_s08'
class_names = [ 'gfp', 'both', 'tom', 'null']

## Import CSV

df = pd.read_csv(os.path.join(png_path,r'0718F_5_redo_s08_classification.csv' ))
slice_plane = df['Slice_plane'][0]

    

## Make plots of each cell type

ims_to_plot = [[], [], [], []] # GFP, both, TOM, null
coord_list = [[0,0], [0,1], [1,0], [1,1]]
ims_to_check = []

# Import PNGs and append to proper list based on class
for index, row in df.iterrows():
    
    pred_class = row['Class']
    x = row['X']
    y = row['Y']
    png_name = slice_plane + '_y' + f'{y:04}' + '_x' + f'{x:04}'
    ims_to_check.append(os.path.join(png_path, png_name + '.png'))


for impath in ims_to_check:
    try:
        im = cv2.imread(impath)[:,:,::-1]
        scaled = np.asarray(im*(255/np.max(im)), dtype=int)
        plt.imshow(scaled[:,:,:3])
        plt.show()
        move = input("Move to null dataset?") # press y or n
        if move == 'y':
            shutil.move(impath, impath.replace(png_path, r"J:\Danielle Paynter\null_examples" ))
        plt.close()
    except:
        pass
    