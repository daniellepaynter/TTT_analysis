# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:26:59 2023

Trying to merge TIFs and the PNGs that show object classification

@author: dpaynter
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

# Get a list of slices to do the thing for
path_to_PNGs = r'J:\Danielle Paynter\Unchecked_objclass'
files = os.listdir(path_to_PNGs)
files = [file for file in files if '.png' in file]
planes = list(set([file.split(sep='_obj')[0] for file in files]))
tifs = []
# Read the merged TIF:
path_to_tifs = r'J:\Danielle Paynter\TTT_proc'
for root, dirs, files in os.walk(path_to_tifs):
    print(root)
    for name in files:
        tifs.append(os.path.join(root,name))
tifs = [tif for tif in tifs if '.tif' in tif]

# Find and import a TIF that matches a plane in the list of PNGs
for plane in planes:
    possibles = [tif for tif in tifs if plane in tif]
    if len(possibles) == 1:
        print('cool')
        tif_im = cv2.imread(possibles[0])
        png_path_GFP = os.path.join(path_to_PNGs, plane+'_objclassGFP.png')
        png_path_Both = os.path.join(path_to_PNGs, plane+'_objclassBoth.png')
        if  os.path.isfile(png_path_GFP):
            gfp_mask = cv2.imread(png_path_GFP)
            gfp_mask = gfp_mask*(1/255)
            gfp_check = gfp_mask*tif_im
            cv2.imwrite(png_path_GFP.replace('GFP', 'GFP_mask'), gfp_check.astype(dtype='uint8'))
        if os.path.isfile(png_path_Both):
            both_mask = cv2.imread(png_path_Both)
            both_mask = both_mask*(1/255)
            both_check = both_mask*tif_im
            cv2.imwrite(png_path_Both.replace('Both', 'Both_mask'), both_check.astype(dtype='uint8'))
    else:
        impath = min(possibles, key=len)
        tif_im = cv2.imread(impath)

        png_path_GFP = os.path.join(path_to_PNGs, plane+'_objclassGFP.png')
        png_path_Both = os.path.join(path_to_PNGs, plane+'_objclassBoth.png')
        if  os.path.isfile(png_path_GFP):
            gfp_mask = cv2.imread(png_path_GFP)
            gfp_mask = gfp_mask*(1/255)
            gfp_check = gfp_mask*tif_im
            cv2.imwrite(png_path_GFP.replace('GFP', 'GFP_mask'), gfp_check.astype(dtype='uint8'))
        if os.path.isfile(png_path_Both):
            both_mask = cv2.imread(png_path_Both)
            both_mask = both_mask*(1/255)
            both_check = both_mask*tif_im
            cv2.imwrite(png_path_Both.replace('Both', 'Both_mask'), both_check.astype(dtype='uint8'))

