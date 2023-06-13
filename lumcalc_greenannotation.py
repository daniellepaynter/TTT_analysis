# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:45:18 2022

@author: dpaynter
"""

import numpy as np
import pandas as pd
import sys, os
import process_xml_cellcounts as pxc
import seaborn as sns
import matplotlib.pyplot as plt
import xmltodict
import cv2
import glob
from skimage import color

xml_path = r'C:\Users\dpaynter\Desktop\CellCounter_C2-DP_220718F_slice5_redo_reg2.xml'
xml_path2 = r'I:\Danielle Paynter\TTT_2022\data\interim\TTT_counts\CellCounter_DP_220718F_slice5_redo_reg2_LG.xml'


   
with open(xml_path2,'r', encoding='utf-8') as file:
    my_xml = file.read()


counts = pxc.get_cellcounts(xml_path2)
my_dict = xmltodict.parse(my_xml)
cellfile = my_dict['CellCounter_Marker_File']
markerdata = cellfile['Marker_Data']
m = markerdata['Marker_Type']
Both_markers = m[1]['Marker']
GFP_markers = m[0]['Marker']
gfp_df = pd.DataFrame(GFP_markers)
both_df = pd.DataFrame(Both_markers)
both_df['Type'] = 'both'
gfp_df['Type'] = 'gfp'
cellcount_df = pd.concat([both_df, gfp_df])

tom_stack = []
for filename in glob.glob(r'C:/Users/dpaynter/Desktop/0718F_slice5_reg2_TOM/DP_220718F_slice*.tif'):
    im = plt.imread(filename)
    imx = im.shape[0]
    imy = im.shape[1]
    j = color.rgb2gray(im[:,:,:3])
    j = j*(255/np.max(j))
    j_med = np.median(j) - 3
    for x in range(imx):
            for y in range(imy):
                if j[x,y] < j_med:
                    j[x,y] = 0
    
    j = j.astype(np.uint8)
    
    
    tom_stack.append(j[:,:])
    print(filename)
    
tom_arr = np.asanyarray(tom_stack, dtype=float)
tom_arr = np.transpose(tom_arr, [1,2,0])

gfp_stack = []
for filename in glob.glob(r'C:/Users/dpaynter/Desktop/0718F_slice5_reg2_GFP/DP_220718F_slice*.tif'):
    im = plt.imread(filename)
    imx = im.shape[0]
    imy = im.shape[1]
    j = color.rgb2gray(im[:,:,:3])
    j = j*(255/np.max(j))
    j_med = np.median(j) - 3
    for x in range(imx):
            for y in range(imy):
                if j[x,y] < j_med:
                    j[x,y] = 0
    
    j = j.astype(np.uint8)
    
    
    gfp_stack.append(j[:,:])
    print(filename)
    
gfp_arr = np.asanyarray(gfp_stack, dtype=float)
gfp_arr = np.transpose(gfp_arr, [1,2,0])



cell_arr = cellcount_df[['MarkerX','MarkerY','MarkerZ']].to_numpy(dtype=int)
cell_arr[:,2] = cell_arr[:,2]/2 + 1


def lumcalc(procd_im_arr, cell_coords):
    means = []
    for cell in range(0,cell_coords.shape[0]):

        mask=np.zeros(procd_im_arr[:,:,0].shape)
        r = 3
        b = cell_coords[cell,0]
        a = cell_coords[cell,1]
        nx = procd_im_arr.shape[0]
        ny = procd_im_arr.shape[1]
        y,x = np.ogrid[-a:nx-a, -b:ny-b]
        mask = (x*x + y*y <= r*r)*1.0
        masked_im = mask * procd_im_arr[:,:,cell_coords[cell-1,2]]
        lum = sum(sum(masked_im))/sum(sum(mask))
        
        means.append(lum)
    return(means)
means_tom = lumcalc(tom_arr, cell_arr)
means_gfp = lumcalc(gfp_arr, cell_arr)

def circleblobs(blobs, image):
    from skimage import color
    zplanes = image.shape[2]
    
    sendback = []
    for z in range(zplanes):
        im = color.gray2rgb(image[:,:,z])
        blob_z = np.array([blob for blob in blobs if blob[2] == z+1])
        
        how_many_blobs=list(range(blob_z.shape[0]))
        for blob_num in how_many_blobs:
            y=int(blob_z[blob_num,0])
            x=int(blob_z[blob_num,1])
            r=5
            cv2.circle(im,(y,x), r, (255,255,0), 10)
        im_conv = color.rgb2gray(im)
        sendback.append(im_conv)
    return(sendback)

try4 = circleblobs(cell_arr, tom_arr)
plt.imshow(try4[9])