# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:17:32 2023

Check output of model when it classifies previously-unseen cells.

@author: dpaynter
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from matplotlib.gridspec import GridSpec


classifications_path = r'J:\Danielle Paynter\Class_outputs'
im_path = r'J:\Danielle Paynter\PNGs_to_classify'
class_names = [ 'gfp', 'both', 'tom', 'null']

slices_to_plot = []
csvs = sorted(os.listdir(classifications_path))
slice_names = [csv.split(sep='_s')[0] for csv in csvs if '0718A_2_redo' not in csv and '.csv' in csv]

for slyce in slice_names:
    if not os.path.exists(os.path.join(classifications_path, slyce + '.png')):  
        planes = sorted([thing for thing in os.listdir(classifications_path) if slyce in thing and '.csv' in thing])
        # take middle plane
        mid_plane = planes[len(planes)//2] 
        mid_plane_int = len(planes)//2
    
        dfs = []
    ## Import CSV
        for file in planes[mid_plane_int-5:mid_plane_int+5]:
            dfs.append(pd.read_csv(os.path.join(classifications_path, file), converters={'Class' : str}))
        
        df = pd.concat(dfs)
        
    ## Make plots of each cell type
    
        ims_to_plot = [[], [], [], []] # GFP, both, TOM, null
        coord_list = [[0,0], [0,1], [1,0], [1,1]]
        
        # Import PNGs and append to proper list based on class
        for index, row in df.iterrows():
            
            pred_class = row['Class']
            slice_plane = row['Slice_plane']
            x = row['X']
            y = row['Y']
            png_name = slice_plane + '_y' + f'{y:04}' + '_x' + f'{x:04}'
            
            if pred_class == 'gfp':
                if len(ims_to_plot[0]) < 49:
                    ims_to_plot[0].append(cv2.imread(os.path.join(im_path, slice_plane, slice_plane, png_name + '.png'))[:,:,::-1])
            elif pred_class == 'both':
                if len(ims_to_plot[1]) < 49:
                    ims_to_plot[1].append(cv2.imread(os.path.join(im_path, slice_plane, slice_plane, png_name + r'.png'))[:,:,::-1])
            elif pred_class == 'tom':
                ims_to_plot[2].append(cv2.imread(os.path.join(im_path, slice_plane, slice_plane,png_name + r'.png'))[:,:,::-1])
            elif pred_class == 'null':
                ims_to_plot[3].append(cv2.imread(os.path.join(im_path, slice_plane, slice_plane,png_name + r'.png'))[:,:,::-1])
                    
        
        gfp_len = len(ims_to_plot[0])
        both_len = len(ims_to_plot[1])
        tom_len = len(ims_to_plot[2])    
        null_len = len(ims_to_plot[3])
        
        for it, cat in enumerate(ims_to_plot):    
            while len(cat) < 49:
                cat.append(np.zeros((34,34)))
            while len(cat) > 49:
                del cat[-1]
                
                
        fig = plt.figure(figsize=(10,9))
        gs = GridSpec(2, 2, hspace=.15)
        for i, img_list in enumerate(ims_to_plot):
            subgrid = gs[i].subgridspec(7, 7)
            for j, img in enumerate(img_list):
                    row, col = divmod(j, 7)
                    scaled = np.asarray(img*(255/np.max(img)), dtype=int)
                    ax = fig.add_subplot(subgrid[row, col])
                    ax.imshow(scaled)
                    plt.axis("off")
            if i == 0:
                fig.text(0.26, .895, "GFPs", fontsize=14)
            elif i == 1:
                fig.text(0.7, .895, "Boths", fontsize=14)
            elif i == 2:
                fig.text(0.26, 0.49, "TOMs",  fontsize=14)
            elif i == 3:
                fig.text(0.7, 0.49, "Nulls",  fontsize=14)
        fig.suptitle('{} Classification Examples'.format(slice_plane.split(sep='_s')[0]), fontsize=16)
        fig.tight_layout()
        plt.savefig(os.path.join(classifications_path, slice_plane.split(sep='_s')[0] + '.png'), bbox_inches='tight')
        plt.show()
        plt.close()