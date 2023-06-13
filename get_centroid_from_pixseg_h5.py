# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 10:32:21 2023

Getting images out of ilastik Seg HDF5 files

@author: dpaynter
"""

import h5py as h
import cv2
import numpy as np
import os
import shutil

# Find the files to convert to PNGs
folder = r'J:\Danielle Paynter\Seg_individuallytrained'
procd_folder = r'J:\Danielle Paynter\Seg_individuallytrained\processed'
output_folder = r'J:\Danielle Paynter\PNGs_of_seg_h5'

h5s = os.listdir(folder)
h5s = [file for file in h5s if ".h5" in file]

for h5 in h5s:
    print("Working on {}".format(h5))
# Import the HDF5 and get the "exported data" part of it
    try:
        h5obj = h.File(os.path.join(folder, h5))
        data = h5obj.get("exported_data")
        
    # Separate out a 2D array image
        im = data[0,0,:,:,0]
    
    # Make a save out file name for the PNG based on the name of the binary seg hdf5
        imsavename = h5.replace(".h5", ".png")
    
    # Make the image binary (it should only have 2 unique pixel values)
        im_min = np.min(im)
        im_max = np.max(im)
        im_h = im.shape[1]
        im_w = im.shape[0] 
        for x in range(im_w):
            for y in range(im_h):
                if im[x,y] == im_min:
                    im[x,y] = int(0)
                elif im[x,y] == im_max:
                    im[x,y] == int(255)
                else:
                    print("Weird pixel value at {},{}".format(x,y))
                    
        cv2.imwrite(os.path.join(output_folder,imsavename), im)
        try:
            h5obj.close()
        except:
            pass
        print("Moving file")
        oldname = os.path.join(folder, h5)
        newname = os.path.join(procd_folder, h5)
        shutil.move(oldname, newname)
    except:
        print("skipped one")
        
# for h5 in h5s:
#     print("Moving file")
#     oldname = os.path.join(folder, h5)
#     newname = os.path.join(procd_folder, h5)
#     shutil.move(oldname, newname)