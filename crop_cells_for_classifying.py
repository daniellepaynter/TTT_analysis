# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 13:54:58 2023

Script to extract coordinates from the CSVs in 
'J:\Danielle Paynter\CSV_counts_from_seg' and build a dataset of cropped images
of cells to feed into the rv_keras network for classification.

@author: dpaynter
"""

import os
import numpy as np
from skimage.io import imread, imsave
import pandas as pd
from fnmatch import fnmatch
import shutil
import random

# Set up some things
annot_radius = 17

csv_folder = r'J:\Danielle Paynter\CSV_counts_from_seg'
csv_procd_folder = r'J:\Danielle Paynter\CSV_counts_from_seg_processed'
tif_folder = r'J:\Danielle Paynter\TTT_proc'
png_output = r'J:\Danielle Paynter\PNGs_to_classify\NotDoneYet'
path_to_pngs = r'J:\Danielle Paynter\PNGs_to_classify\NotDoneYet'


# Get a list of tifs:
tif_subfolders = os.listdir(tif_folder)
tif_names = []
root = tif_folder
pattern = "*.tif"
for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            tif_names.append(os.path.join(path, name))
            


for csv in os.listdir(csv_folder):
# Get a CSV from the CSV folder; make it a dataframe
    df_csv = pd.read_csv(os.path.join(csv_folder, csv))
    print('Working on {}'.format(csv))
# Get a TIF from the TIF folder that matches the CSV name
    zplane_name = csv.split('_b')[0]
    possible_matches = [tif for tif in tif_names if zplane_name in tif]
    if len(possible_matches) > 1:
        tif_path = min(possible_matches, key=len)
    else:
        tif_path = possible_matches[0]
    image = imread(tif_path)

# Get a list of x coords 
    xs = list(df_csv['X'])
# Get a list of y coords
    ys = list(df_csv['Y'])


# Loop markers
    for it, (x, y) in enumerate(zip(xs, ys)):

        y1 = int(y)-annot_radius
        y2 = int(y)+annot_radius
        x1 = int(x)-annot_radius
        x2 = int(x)+annot_radius
    
        # Get cropped image
        crop = image[y1:y2,x1:x2,:]
        crop = np.concatenate([ crop, np.zeros((crop.shape[0],crop.shape[1],1)) ], axis=2).astype(np.uint8)
    
        # write image to class data folder
        try:
            imname = "{}_y{:04.0f}_x{:04.0f}.png".format( zplane_name, y, x )
            imsave( os.path.join(png_output,imname), crop, check_contrast=False )
        except SystemError:
            print('Skipped one')
            # usually this error happens because the coordinate is less than 17 pixels (radius) from the edge of the image
            # "skipped one" means one cell was skipped, not one whole plane or CSV
    # Move CSV into the processed folder
    oldname = os.path.join(csv_folder, csv)
    newname = os.path.join(csv_procd_folder, csv)
    shutil.move(oldname, newname)
    
### Sort the PNGs into folders

ims_to_sort = os.listdir(path_to_pngs)
ims_to_sort = [im for im in ims_to_sort if '.png' in im]

for im in ims_to_sort:
    slyce = im.split('_y')[0]
    dirpath = os.path.join(path_to_pngs, slyce)
    try:
        os.mkdir(dirpath)
    except:
        strings = ['Hey', 'Whats up', 'youre pretty cool', 'science is weird',
                   'is it lunch time yet', 'nice', 'nopeskerdoodles', 'neat',
                   'hahaha', 'very well', 'it failednt', 'nap time']
        print(random.choice(strings))
    
    oldpath = os.path.join(path_to_pngs, im)
    newpath = os.path.join(dirpath, im)
    shutil.move(oldpath, newpath)