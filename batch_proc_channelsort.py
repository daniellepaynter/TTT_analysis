# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 11:32:35 2022

@author: dpaynter
"""

### Imports
import os
import random

# Separate output tifs into a folder for each channel
folds = []
path = r'I:\Danielle Paynter\TTT_2022\data\raw\stitched_confocal_tifs'
mouse_folds = os.listdir(path)
for mouse_fold in mouse_folds:
    folds.append(os.listdir((os.path.join(path, mouse_fold))))

folder_path = r'I:\Danielle Paynter\TTT_2022\data\processed\stitched_confocal_tifs\DP_220729A\DP_220729A_slice4_redo'
num_chans = 4
chans = ['ch00', 'ch01', 'ch02', 'ch03']
for it, mouse_fold in enumerate(mouse_folds):
    print(mouse_fold)
    for fold in folds[it]:
        
        folder_path = os.path.join( path, mouse_fold, fold )
    
        ## Make a folder for each channel
        for chan in range(num_chans):
            try:
                os.mkdir(os.path.join(folder_path,chans[chan]))
            except:
                strings = ['Hey', 'Whats up', 'youre pretty cool', 'science is weird',
                           'is it lunch time yet', 'nice', 'nopeskerdoodles', 'neat',
                           'hahaha', 'very well', 'it failednt', 'nap time']
                print(random.choice(strings))
                    
            
        ## Iterate over each image, move it into the appropriate folder
        for im in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, im)) and '.png' in im:
                imname = os.fsdecode(im)
                chan_num = imname.split("_")[-1]
                if chan_num == "ch00.tif":
                    dest_file = os.path.join(folder_path,chans[0],imname)
                if chan_num == "ch01.tif":
                    dest_file = os.path.join(folder_path,chans[1],imname)
                if chan_num == "ch02.tif":
                    dest_file = os.path.join(folder_path,chans[2],imname)
                if chan_num == "ch03.tif":
                    dest_file = os.path.join(folder_path,chans[3],imname)
                try:
                    os.rename(os.path.join(folder_path,imname),os.path.join(dest_file))
                except:
                    print('File swooooosh')
                