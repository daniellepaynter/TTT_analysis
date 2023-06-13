# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 13:50:55 2022

Get info about how confocal data collection and analysis is going

@author: dpaynter
"""
import numpy as np
import pandas as pd
import os
import sys

raw_path = r'I:\Danielle Paynter\TTT_2022\data\raw\confocal'
proc_path = r'I:\Danielle Paynter\TTT_2022\data\processed\stitched_confocal_tifs'

raw_data = [os.listdir(os.path.join(raw_path,os.listdir(raw_path)[it])) for it, name in enumerate(os.listdir(raw_path))]
raw_lifs = []
for folder in raw_data:
    mouse = []
    for file in folder:
        if "ext" not in file:
            mouse.append(file)
    raw_lifs.append(mouse)

proc_folders = [os.listdir(os.path.join(proc_path,os.listdir(proc_path)[it]))
              for it, name in enumerate(os.listdir(proc_path))]

for lif in raw_lifs[1]:
    print(lif)
    
for folder in proc_folders[1]:
    print(folder)
    
