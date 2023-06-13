# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 15:34:03 2022

Batch process confocal tifs: 
    - make them gray scale
    - convert DAPI to JPEG and move to interim
    - downsample the DAPI JPEGs

@author: dpaynter
"""

import conf_ac_class as cac
import os


path_to_tifs = r'I:\Danielle Paynter\TTT_2022\data\raw\stitched_confocal_tifs'
mice = os.listdir(path_to_tifs)
slices = []
for it, mouse in enumerate(mice):
    slices.extend(os.listdir(os.path.join(path_to_tifs, mice[it])))
        
    for slyce in slices:
        if os.path.isdir(os.path.join(path_to_tifs, mouse, slyce)):
            ac_path = os.path.join(path_to_tifs, mouse, slyce)
            if os.path.exists(os.path.join(ac_path, 'done.txt')) == True:
                print("{} is done already".format(slyce))
            elif os.path.exists(os.path.join(ac_path, 'MetaData')):
            # Make an object of this acquisition
                ac = cac.conf_ac(ac_path)
                print('Working on ac {}'.format(slyce))
                for chan in ac.fluo_list:
                    print('Starting chan {}'.format(chan))
                    ac.convert_to_gray(chan)
                if "DAPI" in ac.fluo_list:
                    ac.convert_to_jpeg("DAPI")
                    ac.dwnsmpl_jpgs("DAPI", 2000)
                f = open((os.path.join(ac_path, 'done.txt')), "w")
                f.close()
            else: 
                print( "Something went wrong for {} maybe".format(ac_path))