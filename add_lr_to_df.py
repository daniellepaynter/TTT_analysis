# -*- coding: utf-8 -*-
"""
Created on Wed May 10 10:43:57 2023

Run this script on the "Final Output" CSVs to add a column saying whether 
each labeled cell is on the right or left side of the brain.

@author: dpaynter
"""

import os
import pandas as pd

path_to_finalcsvs = r'J:\Danielle Paynter\Final_outputs_newmodel'
hemisphere_file = r'J:\Danielle Paynter\slice_rotations.xlsx'
hemi_df = pd.read_excel(hemisphere_file).dropna()
lrs_big = []


#start with the hemi_df files to decide which csvs to import
slices = list(hemi_df['Slice'])
#slices = ['0718A_1']
for slyce in slices:
    csv_list = []
    
# equation of a line splitting left and right
    slope = float(list(hemi_df[hemi_df['Slice'] == slyce]['Slope'])[0])
    intercept = float(list(hemi_df[hemi_df['Slice'] == slyce]['Intercept'])[0])
    mirrored = list(hemi_df[hemi_df['Slice'] == slyce]['Mirrored'])[0]
    flipped = list(hemi_df[hemi_df['Slice'] == slyce]['Upsidedown'])[0]



# Get the final_output CSVs
    csvs = [ os.path.join(path_to_finalcsvs, csv) for csv in os.listdir(path_to_finalcsvs) if slyce in csv]
    for csv in csvs:
        csv_list.append(pd.read_csv(csv))
    for i, df in enumerate(csv_list):   

            
        xs = list(df["X"])
        ys = list(df["Y"])
        
        lrs = []
        for x, y in zip(xs, ys):
            x_form = int(slope*x + intercept)
            lr = 'l'
            if y > x_form and slope > 0:
                if mirrored != flipped:
                    lr = 'r'
                elif mirrored == flipped:
                    lr = 'l'
                else :
                    print(csv)
            elif y > x_form and slope < 0:
                if mirrored != flipped:
                    lr = 'l'
                elif mirrored == flipped:
                    lr = 'r'
                else :
                    print(csv)
                   
            elif y < x_form and slope > 0:

                if mirrored != flipped:
                    lr = 'l'
                elif mirrored == flipped:
                    lr = 'r'

                else :
                    print(csv)
            elif y < x_form and slope < 0:

                if mirrored != flipped:
                    lr = 'r'
                elif mirrored == flipped:
                    lr = 'l'

                else :
                    print(csv)
            
            else:
                print("Couldn't figure out one")
                print(x, x_form, y)
                lr = 'na'

            lrs.append(lr)
            lrs_big.append(lr)
           # print(lr)
        df["LR"] = lrs[:]
        df = df[["Slice_plane", 	"X",	"Y", "Class",	"Region",	"LR"]]
        df.to_csv(csvs[i])
        #print(csv)
print('r: {}'.format(lrs_big.count('r')))
print('l: {}'.format(lrs_big.count('l')))

