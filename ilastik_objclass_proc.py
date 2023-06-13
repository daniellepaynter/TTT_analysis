# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 10:53:41 2023

Process binobj CSV outputs from iLastik

@author: dpaynter
"""

import os
from os import path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

folder = r'J:\Danielle Paynter\binobj'
objclass_csvs = [file for file in os.listdir(folder) if '.csv' in file]
count = 0
slice_df = pd.DataFrame(columns=['Mouse','Slice','Plane','PercGFP','GFPcount','Bothcount','ProbGFP','ProbBoth', 'PixelsGFP', 'PixelsBoth'])


for csv in objclass_csvs:
    slice_name = csv.split(sep='_s')[0]
    plane = csv.split(sep='_table')[0].split(sep='_')[-1]
    mouse = slice_name.split(sep='_')[0]
    df = pd.read_csv(os.path.join(folder, csv))
    df = df.rename(columns={'Size in pixels': 'Size_in_pixels', 'Probability of GFP': 'Probability_of_GFP', 
                            'Probability of Both': 'Probability_of_Both', 'Probability of NotCell': 'Probability_of_NotCell'})
### Filters for bad objects ###
    df = df[df.Size_in_pixels >= 90 ]

###################################
    
    counts = df.groupby('Predicted Class')['Predicted Class'].count()
    type_groups = df.groupby('Predicted Class')
    means = type_groups.mean()
    st_devs = type_groups.std()
    sums = type_groups.sum()
    if 'GFP' in counts:
        num_gfp = counts['GFP']
        prob_gfp = means['Probability_of_GFP']['GFP']
        prob_gfp_dev = st_devs['Probability_of_GFP']['GFP']
        pix_gfp = sums['Size_in_pixels']['GFP']
    else: 
        num_gfp = 0
        prob_gfp = 0
        prob_gfp_dev = 0
        pix_gfp = 0
        
    if 'NotCell' in counts:
        num_notcell = counts['NotCell']
        prob_notcell = means['Probability_of_NotCell']['NotCell']
        prob_notcell_dev = st_devs['Probability_of_NotCell']['NotCell']
    else:
        num_notcell = 0
        prob_notcell = 0
        prob_notcell_dev = 0
        
    if 'Both' in counts:
        num_both = counts['Both']
        total_cellcount = num_gfp + num_both
        perc_gfp = num_gfp/total_cellcount
        print(perc_gfp)
        prob_both = means['Probability_of_Both']['Both']
        prob_both_dev = st_devs['Probability_of_Both']['Both']
        pix_both = sums['Size_in_pixels']['Both']

    else:
        num_both = 0
        total_cellcount = num_gfp + num_both
        perc_gfp = 1
        print(perc_gfp)
        prob_both = 0
        prob_both_dev = 0
        pix_both = 0
        
    new_row = [mouse, slice_name, plane, perc_gfp, num_gfp, num_both, prob_gfp, prob_both, pix_gfp, pix_both]
    slice_df.loc[len(slice_df)] = new_row

slice_groups = slice_df.groupby('Slice')
slice_means = slice_groups.mean()
slice_sums = slice_groups.sum()

mouse_groups = slice_df.groupby('Mouse')
mouse_means = mouse_groups.mean()
mouse_sums = mouse_groups.sum()