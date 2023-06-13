# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 17:47:22 2023

Check and validate outputs from ilastik, nutil, and possibly registration software


@author: dpaynter
"""
import os
from os import path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

flag_plots = False

slice_folder = r'J:\Danielle Paynter\binobj'
slyce = slice_folder.split(sep="\\")[-1]

## Check for objclass folder
objclass_folder = [item for item in os.listdir(slice_folder) if item == 'objclass'][0]
objclass_path = os.path.join(slice_folder, objclass_folder)
objclass_csvs = [file for file in os.listdir(objclass_path) if '.csv' in file]
try:
    trained_csv = [file for file in objclass_csvs if 'data_table' in file][0]
except:
    print('Not sure which plane this model was trained on')
    trained_csv = 'unknown'
    
    
    
## Import and plot for trained_csv
if path.exists(path.join(objclass_path,trained_csv)):
    df = pd.read_csv(os.path.join(objclass_path,trained_csv))
    hist_bins = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.80, 0.85, 0.9, 0.95, 1.0]
    type_groups = df.groupby('Predicted Class')
    means = type_groups.mean()
    st_devs = type_groups.std()
    type_groups.groups.keys()
    if flag_plots == True:    
        fig = plt.figure()
        plt.suptitle("Trained plane: {}".format(slyce))
        ax1 = fig.add_subplot(231)
        ax2 = fig.add_subplot(232)
        ax3 = fig.add_subplot(233)
        ax4 = fig.add_subplot(234)
        ax5 = fig.add_subplot(235)
        ax6 = fig.add_subplot(236)
        df_obj = df[df['Predicted Class'].isin(['GFP', 'Both', 'TOM', 'NotCell'])].copy()
    
        if 'TOM' not in df['Predicted Class'].unique():
            sns.histplot(data=df, x='Probability of TOM', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold'],bins=hist_bins, ax=ax1).set(title='Probability TOM-only')
            sns.histplot(data=df, x='Probability of Both', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold'],bins=hist_bins, ax=ax2).set(title='Probability Double-labeled')
            sns.histplot(data=df, x='Probability of GFP', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold'],bins=hist_bins, ax=ax3).set(title=r'Probability GFP-only')
            sns.histplot(data=df_obj, x='Size in pixels', hue='Predicted Class',palette=['gold', 'green', 'slategray'], ax=ax6, log_scale=True).set(title='Size in pixels distribution')
    
        if 'TOM' in df['Predicted Class'].unique():
            sns.histplot(data=df, x='Probability of TOM', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold', 'red'],bins=hist_bins, ax=ax1).set(title='Probability TOM-only')
            sns.histplot(data=df, x='Probability of Both', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold', 'red'],bins=hist_bins, ax=ax2).set(title='Probability Double-labeled')
            sns.histplot(data=df, x='Probability of GFP', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold', 'red'],bins=hist_bins, ax=ax3).set(title=r'Probability GFP-only')
            sns.histplot(data=df_obj, x='Size in pixels', hue='Predicted Class',palette=['gold', 'green', 'slategray', 'red'], ax=ax6, log_scale=True).set(title='Size in pixels distribution')
    
        df_gfp_both = df[df['Predicted Class'].isin(['GFP', 'Both'])].copy()
        sns.scatterplot(data=df_gfp_both, x='Probability of GFP', y='Probability of Both', hue='Predicted Class', palette=['green', 'gold'], ax=ax5)
        
        df_gfp_not = df[df['Predicted Class'].isin(['GFP', 'NotCell'])].copy()
        sns.scatterplot(data=df_gfp_not, x='Probability of GFP', y='Probability of NotCell', hue='Predicted Class', palette=['slategrey', 'green'], ax=ax4)
    
    

## Import and concatenate CSVs
li = []
for it, filename in enumerate(objclass_csvs):
    if it%2 != 0:
        df_mini = pd.read_csv(path.join(objclass_path,filename), index_col=None, header=0)
        li.append(df_mini)
df_all = pd.concat(li, axis=0, ignore_index=True)

hist_bins = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.80, 0.85, 0.9, 0.95, 1.0]
type_groups = df_all.groupby('Predicted Class')
means = type_groups.mean()
st_devs = type_groups.std()
type_groups.groups.keys()
if flag_plots == True:
    fig = plt.figure()
    plt.suptitle("All planes: {}".format(slyce))
    ax1 = fig.add_subplot(231)
    ax2 = fig.add_subplot(232)
    ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(234)
    ax5 = fig.add_subplot(235)
    ax6 = fig.add_subplot(236)
    df_gfp_both = df_all[df_all['Predicted Class'].isin(['GFP', 'Both'])].copy()
    df_gfp_not = df_all[df_all['Predicted Class'].isin(['GFP', 'NotCell'])].copy()
    df_obj = df_all[df_all['Predicted Class'].isin(['GFP', 'Both', 'TOM', 'NotCell'])].copy()
    
    #if 'TOM' not in df_all['Predicted Class'].unique():
     #   sns.histplot(data=df_all, x='Probability of TOM', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold'],bins=hist_bins, ax=ax1).set(title='Probability TOM-only')
     #   sns.histplot(data=df_all, x='Probability of Both', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold'],bins=hist_bins, ax=ax2).set(title='Probability Double-labeled')
     #   sns.histplot(data=df_all, x='Probability of GFP', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold'],bins=hist_bins, ax=ax3).set(title=r'Probability GFP-only')
     #   sns.histplot(data=df_obj, x='Size in pixels', hue='Predicted Class',palette=['gold', 'green', 'slategray'], ax=ax6, log_scale=True).set(title='Size in pixels distribution')
    
    if 'TOM' in df_all['Predicted Class'].unique():
        sns.histplot(data=df_all, x='Probability of TOM', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold', 'red'],bins=hist_bins, ax=ax1).set(title='Probability TOM-only')
        sns.histplot(data=df_all, x='Probability of Both', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold', 'red'],bins=hist_bins, ax=ax2).set(title='Probability Double-labeled')
        sns.histplot(data=df_all, x='Probability of GFP', hue='Predicted Class', palette=['black', 'gray', 'green', 'gold', 'red'],bins=hist_bins, ax=ax3).set(title=r'Probability GFP-only')
        sns.histplot(data=df_obj, x='Size in pixels', hue='Predicted Class',palette=['gold', 'green', 'slategray', 'red'], ax=ax6, log_scale=True).set(title='Size in pixels distribution')
    
    sns.scatterplot(data=df_gfp_both, x='Probability of GFP', y='Probability of Both', hue='Predicted Class', palette=['green', 'gold'], ax=ax5)
    
    sns.scatterplot(data=df_gfp_not, x='Probability of GFP', y='Probability of NotCell', hue='Predicted Class', palette=['slategrey', 'green'], ax=ax4)

# get percentages
counts = df_all.groupby('Predicted Class')['Predicted Class'].count()
total_cellcount = counts['GFP'] + counts['Both']
perc_gfp = counts['GFP']/total_cellcount
print(slice_folder)
print('Percent GFP-only: {}'.format(perc_gfp))
##########################################################

np_all = df_all.to_numpy()
objs_big = np_all[(np_all[:,9] > 10)]
gfp_objs = np_all[ (np_all[:,4] == 'GFP')]
both_objs = np_all[ (np_all[:,4] == 'Both')]
gfp_objs_big = gfp_objs[ (gfp_objs[:,9] > 10)]
both_objs_big = both_objs[ (both_objs[:,9] > 10)]

gfp_objs_ch = gfp_objs[ (gfp_objs[:,12] > 5)]
both_objs_ch = both_objs[ (both_objs[:,12] > 5)]

print('Percent GFP, exclude small objects:{}'.format(len(gfp_objs_big)/len(objs_big)))
bb_sym_gfp = (gfp_objs[:,18] - gfp_objs[:,16])/(gfp_objs[:,19] - gfp_objs[:,17])
bb_sym_both = (both_objs[:,18] - both_objs[:,16])/(both_objs[:,19] - both_objs[:,17])

# Plot all gfp and both pts:
sns.scatterplot(x=gfp_objs[:,20], y=gfp_objs[:,21])
sns.scatterplot(x=both_objs[:,20], y=both_objs[:,21])

# Plot gfp and both pts with 3 or more pixels:
sns.scatterplot(x=gfp_objs_big[:,20], y=gfp_objs_big[:,21])
sns.scatterplot(x=both_objs_big[:,20], y=both_objs_big[:,21])

# Plot gfp and both pts with convex hull area greater than 5:
sns.scatterplot(x=gfp_objs_ch[:,20], y=gfp_objs_ch[:,21])
sns.scatterplot(x=both_objs_ch[:,20], y=both_objs_ch[:,21])

# Plot filtering by CH area and pixel size:
gfp_objs_ch_pix = gfp_objs[ (gfp_objs[:,12] > 45) & (gfp_objs[:,9] > 20)]
both_objs_ch_pix = both_objs[ (both_objs[:,12] > 45) & (both_objs[:,9] > 20)]
sns.scatterplot(x=gfp_objs_ch_pix[:,20], y=gfp_objs_ch_pix[:,21])
sns.scatterplot(x=both_objs_ch_pix[:,20], y=both_objs_ch_pix[:,21])


gfp_filter = gfp_objs[(gfp_objs[:,9] > 20) & (bb_sym_gfp > -2) & (bb_sym_gfp <2) & (gfp_objs[:,9] < 500)]
sns.scatterplot(x=gfp_filter[:,20], y=gfp_filter[:,21])
both_filter = both_objs[(both_objs[:,9] > 20) & (bb_sym_both > -2) & (bb_sym_both <2) & (both_objs[:,9] < 500) ]
sns.scatterplot(x=both_filter[:,20], y=both_filter[:,21])