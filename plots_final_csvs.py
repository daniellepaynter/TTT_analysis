# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:21:39 2023


Plot the TTT data 

@author: dpaynter
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

# Flag for whether plots should print in command line
show_plots = False

# Path to CSVs, one for each plane, with columns for x, y, class, and region
path_to_final_csvs = r'J:\Danielle Paynter\Final_outputs_newmodel'
all_csv_names = os.listdir(path_to_final_csvs)

#TODO decide if 0730D should be added back in
# Short hand names of each mouse in the cohort
mice_to_plot = ['0718A', '0718B', '0718F', '0729A', '0729B', '0729C', '0730E', 
                '0730F', '0730H', '0807C', '0807D', '0807G', '0807H', '0807I']
md_mice = ['0718B', '0729B', '0729C', '0730D', '0730H', '0807H', '0807I']

# Make lists to store the GFP percentages for each region for each mouse; 
# split by mice with MD and controls
md_v1 = []
md_v1_left = []
md_v1_right = []
md_hvas = []
md_hvas_left = []
md_hvas_right = []
md_dlgn = []
md_rsc = []
md_thal = []
md_thal = []
md_amyg = []
md_sc = []
md_hypothal = []
md_claustrum = []
md_audcortex = []

control_v1 = []
control_v1_left = []
control_v1_right = []
control_hvas = []
control_hvas_left = []
control_hvas_right = []
control_dlgn = []
control_rsc = []
control_thal = []
control_amyg = []
control_sc = []
control_hypothal = []
control_claustrum = []
control_audcortex = []

# Make lists to store the total number of cells in a region for each mouse
# All labeled cells, not just GFP-only. ct = count
md_v1_ct = []
md_v1_left_ct = []
md_v1_right_ct = []
control_v1_ct = []
control_v1_left_ct = []
control_v1_right_ct = []
md_hvas_ct = []
md_hvas_left_ct = []
md_hvas_right_ct = []
control_hvas_ct = []
control_hvas_left_ct = []
control_hvas_right_ct = []
md_dlgn_ct = []
control_dlgn_ct = []
md_rsc_ct = []
control_rsc_ct = []
md_thal_ct = []
control_thal_ct = []
md_amyg_ct = []
control_amyg_ct = []
md_sc_ct = []
control_sc_ct = []
md_hypothal_ct = []
control_hypothal_ct = []
md_claustrum_ct = []
control_claustrum_ct = []
md_audcortex_ct = []
control_audcortex_ct = []

# Make lists to store the dataframes of cells in a given region for a given mouse
#TODO use these to plot overall differences in areas? 
dfs_md_v1 = []
dfs_control_v1 = []
dfs_md_hvas = []
dfs_control_hvas = []
dfs_md_dlgn = []
dfs_control_dlgn = []
dfs_md_rsc = []
dfs_control_rsc = []
dfs_md_thal = []
dfs_control_thal = []
dfs_md_amyg = []
dfs_control_amyg = []
dfs_md_sc = []
dfs_control_sc = []
dfs_md_hypothal = []
dfs_control_hypothal = []
dfs_md_claustrum = []
dfs_control_claustrum = []
dfs_md_audcortex = []
dfs_control_audcortex = []
dfs_md_dlgn = []
dfs_control_dlgn = []

md_allregions = []
control_allregions = []

# A list to hold dataframes of cells from regions not specified in the above lists
whatsleft = []

# A list for knowing how many slices per mouse are plotted
unique_slices = []

# Create a text file to store info about this mouse:
f = open(os.path.join(path_to_final_csvs, "data_summary") + '.txt', "w+")

# Loop over all mice in the cohort
for mouse in mice_to_plot:

    
    # Find CSVs
    csvs_to_import = [csv for csv in all_csv_names if csv.split(sep='_')[0] == mouse ]
    im_title = mouse
    mouse_slyces = []
    # list for the dataframes imported from CSVs:
    csv_list = []
    
    for csv in csvs_to_import:
        csv_list.append(pd.read_csv(os.path.join(path_to_final_csvs, csv)))
        slyce = csv.split(sep='_s')[0]
        mouse_slyces.append(slyce)
    
    #Append a list with the name of each slice imported
    unique_slices.append(set(mouse_slyces))
    f.write("Mouse {} \n".format(mouse))
    f.write("SLices for {}: \n {} \n".format(mouse, set(mouse_slyces)))
    
    # Break down the dataframe into smaller dfs by region and, for v1 and HVAs,
    # if the cells are on left or right
    df = pd.concat(csv_list)
    
    df_v1 = df[df["Region"].isin(['Primary visual area, layer 5', 'Primary visual area, layer 1', 
                                      'Primary visual area, layer 4', 'Primary visual area, layer 2/3',
                                      'Primary visual area, layer 6a', 'Primary visual area, layer 6b'])].copy()
    df_v1_left = df_v1[df_v1["LR"].isin(["l"])].copy()
    df_v1_right = df_v1[df_v1["LR"].isin(["r"])].copy()

    
    df_dLGN = df[df["Region"].isin(['Dorsal part of the lateral geniculate complex, ipsilateral zone','Dorsal part of the lateral geniculate complex, core',
                                      'Dorsal part of the lateral geniculate complex, shell'])].copy()
    
    df_rsc = df[df["Region"].isin(["Retrosplenial area, dorsal part, layer 2/3", "Retrosplenial area, dorsal part, layer 1",
                                    "Retrosplenial area, dorsal part, layer 5", "Retrosplenial area, dorsal part, layer 6a", 
                                   "Retrosplenial area, lateral agranular part, layer 2/3", "Retrosplenial area, lateral agranular part, layer 1",
                                   "Retrosplenial area, lateral agranular part, layer 4", "Retrosplenial area, ventral part, layer 6b",
                                   "Retrosplenial area, lateral agranular part, layer 5", "Retrosplenial area, lateral agranular part, layer 6a",
                                   "Retrosplenial area, lateral agranular part, layer 6b", "Retrosplenial area, ventral part, layer 5", 
                                   "Retrosplenial area, ventral part, layer 6a", "Retrosplenial area, ventral part, layer 4", 
                                   "Retrosplenial area, ventral part, layer 2/3", "Retrosplenial area, ventral part, layer 1",
                                   "Retrosplenial area, dorsal part, layer 6b"])].copy()
    
    df_thal = df[df["Region"].isin(['Dorsal part of the lateral geniculate complex, ipsilateral zone','Dorsal part of the lateral geniculate complex, core',
                                      'Dorsal part of the lateral geniculate complex, shell', 'Lateral posterior nucleus of the thalamus', 'Thalamus',
                                      'Posterior complex of the thalamus','Ventral posteromedial nucleus of the thalamus', 'Posterior limiting nucleus of the thalamus',
                                      'Lateral dorsal nucleus of thalamus', 'Medial geniculate complex, medial part','Ventral part of the lateral geniculate complex',
                                      'Mediodorsal nucleus of thalamus','Central lateral nucleus of the thalamus', 'Central medial nucleus of the thalamus', 'Paracentral nucleus',
                                      'Submedial nucleus of the thalamus', 'Reticular nucleus of the thalamus', 'Ventral posterolateral nucleus of the thalamus',
                                      'Medial geniculate complex, dorsal part', 'Medial geniculate complex, ventral part', 'Interanterodorsal nucleus of the thalamus',
                                      'Anteroventral nucleus of thalamus', 'Ventral posteromedial nucleus of the thalamus, parvicellular part', 
                                      'Ventral posterolateral nucleus of the thalamus, parvicellular part'])].copy()
    
    df_HVAs = df[df["Region"].isin(["Anterolateral visual area, layer 1", "Anterolateral visual area, layer 2/3", "Anterolateral visual area, layer 4",
                                    "Anterolateral visual area, layer 5", "Anterolateral visual area, layer 6a", "Anterolateral visual area, layer 6b",
                                    "posteromedial visual area, layer 1", "posteromedial visual area, layer 2/3", "posteromedial visual area, layer 4",
                                    "posteromedial visual area, layer 5", "posteromedial visual area, layer 6a", "posteromedial visual area, layer 6b",
                                    "Anteromedial visual area, layer 2/3", "Anteromedial visual area, layer 4", "Anteromedial visual area, layer 5",
                                    "Anteromedial visual area, layer 6a", "Lateral visual area, layer 2/3", "Anteromedial visual area, layer 1",
                                    "Lateral visual area, layer 6b",
                                    "Rostrolateral area, layer 6a", "Lateral visual area, layer 5", "Lateral visual area, layer 4", "Anteromedial visual area, layer 6b",
                                    "Rostrolateral area, layer 1", "Rostrolateral area, layer 2/3", "Rostrolateral area, layer 4", "Rostrolateral area, layer 5",
                                    "Rostrolateral area, layer 6", "Anterior area, layer 4", "Anterior area, layer 5", "Anterior area, layer 1", "Anterior area, layer 2/3",
                                    "Anterior area, layer 6a", "Anterior area, layer 6b", "Laterointermediate area, layer 6a", "Laterointermediate area, layer 6b",
                                    "Laterointermediate area, layer 5", "Laterointermediate area, layer 4", "Laterointermediate area, layer 2/3", "Laterointermediate area, layer 1"])].copy()
    df_HVAs_left = df_HVAs[df_HVAs["LR"].isin(["l"])].copy()
    df_HVAs_right = df_HVAs[df_HVAs["LR"].isin(["r"])].copy()
    
    df_amyg = df[df["Region"].isin(["Lateral amygdalar nucleus", "Basolateral amygdalar nucleus, posterior part", "Basomedial amygdalar nucleus, posterior part",
                                    "Central amygdalar nucleus, lateral part", "Basomedial amygdalar nucleus, anterior part", "Medial amygdalar nucleus", "Cortical amygdalar area, anterior part",
                                    "amygdalar capsule", "Cortical amygdalar area, posterior part, lateral zone", "Posterior amygdalar nucleus", 
                                    "Basolateral amygdalar nucleus, ventral part"])].copy()
    
    df_sc = df[df["Region"].isin(["Superior colliculus, motor related, intermediate gray layer", "brachium of the superior colliculus",
                                  "Superior colliculus, optic layer", "Superior colliculus, motor related, intermediate white layer",
                                  "Superior colliculus, superficial gray layer", "Superior colliculus, zonal layer", 
                                  "Superior colliculus, motor related, deep gray layer", "Superior colliculus, motor related, deep white layer"])].copy()
    
    df_audcortex = df[df["Region"].isin(["Dorsal auditory area, layer 2/3", "Primary auditory area, layer 5", "Dorsal auditory area, layer 6a",
                                         "Primary auditory area, layer 6a", "Dorsal auditory area, layer 5", "Ventral auditory area, layer 6a",
                                         "Primary auditory area, layer 1", "Ventral auditory area, layer 5", "Primary auditory area, layer 2/3",
                                         "Ventral auditory area, layer 6b", "Posterior auditory area, layer 5", "Ventral auditory area, layer 2/3",
                                         "Dorsal auditory area, layer 4", "Primary auditory area, layer 6b", "Primary auditory area, layer 4",
                                         "Dorsal auditory area, layer 6b", "Posterior auditory area, layer 4", "Ventral auditory area, layer 4",
                                         "Dorsal auditory area, layer 1", "Posterior auditory area, layer 6a", "Posterior auditory area, layer 2/3",
                                         "Posterior auditory area, layer 6b"])].copy()
    
    df_hypothal = df[df["Region"].isin(["Hypothalamus", "Lateral hypothalamic area", "Posterior hypothalamic nucleus", "Ventromedial hypothalamic nucleus",
                                        "Periventricular hypothalamic nucleus, intermediate part"])].copy()
    
    df_claustrum = df[df["Region"].isin(["Claustrum"])].copy()
    
    # Get all rows with cells not belonging to regions listed above:
    df_whatsleft = df[~df["Region"].isin(["Claustrum", "Hypothalamus", "Lateral hypothalamic area", "Posterior hypothalamic nucleus", "Ventromedial hypothalamic nucleus",
                                        "Periventricular hypothalamic nucleus, intermediate part","Dorsal auditory area, layer 2/3", "Primary auditory area, layer 5", "Dorsal auditory area, layer 6a",
                                        "Primary auditory area, layer 6a", "Dorsal auditory area, layer 5", "Ventral auditory area, layer 6a",
                                        "Primary auditory area, layer 1", "Ventral auditory area, layer 5", "Primary auditory area, layer 2/3",
                                        "Ventral auditory area, layer 6b", "Posterior auditory area, layer 5", "Ventral auditory area, layer 2/3",
                                        "Dorsal auditory area, layer 4", "Primary auditory area, layer 6b", "Primary auditory area, layer 4",
                                        "Dorsal auditory area, layer 6b", "Posterior auditory area, layer 4", "Ventral auditory area, layer 4",
                                        "Dorsal auditory area, layer 1", "Posterior auditory area, layer 6a", "Posterior auditory area, layer 2/3",
                                        "Posterior auditory area, layer 6b", "Superior colliculus, motor related, intermediate gray layer", "brachium of the superior colliculus",
                                        "Superior colliculus, optic layer", "Superior colliculus, motor related, intermediate white layer",
                                        "Superior colliculus, superficial gray layer", "Superior colliculus, zonal layer", 
                                        "Superior colliculus, motor related, deep gray layer", "Superior colliculus, motor related, deep white layer",
                                        "Lateral amygdalar nucleus", "Basolateral amygdalar nucleus, posterior part", "Basomedial amygdalar nucleus, posterior part",
                                       "Central amygdalar nucleus, lateral part", "Basomedial amygdalar nucleus, anterior part", "Medial amygdalar nucleus", "Cortical amygdalar area, anterior part",
                                        "amygdalar capsule", "Cortical amygdalar area, posterior part, lateral zone", "Posterior amygdalar nucleus", 
                                         "Basolateral amygdalar nucleus, ventral part", "Anterolateral visual area, layer 1", "Anterolateral visual area, layer 2/3", "Anterolateral visual area, layer 4",
                                         "Anterolateral visual area, layer 5", "Anterolateral visual area, layer 6a", "Anterolateral visual area, layer 6b",
                                       "posteromedial visual area, layer 1", "posteromedial visual area, layer 2/3", "posteromedial visual area, layer 4",
                                    "posteromedial visual area, layer 5", "posteromedial visual area, layer 6a", "posteromedial visual area, layer 6b",
                                                "Anteromedial visual area, layer 2/3", "Anteromedial visual area, layer 4", "Anteromedial visual area, layer 5",
                                               "Anteromedial visual area, layer 6a", "Lateral visual area, layer 2/3", "Anteromedial visual area, layer 1",
                                              "Lateral visual area, layer 6b", "Rostrolateral area, layer 6a", "Lateral visual area, layer 5", "Lateral visual area, layer 4", "Anteromedial visual area, layer 6b",
                                            "Rostrolateral area, layer 1", "Rostrolateral area, layer 2/3", "Rostrolateral area, layer 4", "Rostrolateral area, layer 5",
                                             "Rostrolateral area, layer 6", "Anterior area, layer 4", "Anterior area, layer 5", "Anterior area, layer 1", "Anterior area, layer 2/3",
                                   "Anterior area, layer 6a", "Anterior area, layer 6b", "Laterointermediate area, layer 6a", "Laterointermediate area, layer 6b",
                                                 "Laterointermediate area, layer 5", "Laterointermediate area, layer 4", "Laterointermediate area, layer 2/3", "Laterointermediate area, layer 1",
                                                 'Dorsal part of the lateral geniculate complex, ipsilateral zone','Dorsal part of the lateral geniculate complex, core',
                                          'Dorsal part of the lateral geniculate complex, shell', 'Lateral posterior nucleus of the thalamus', 'Thalamus',
                                          'Posterior complex of the thalamus','Ventral posteromedial nucleus of the thalamus', 'Posterior limiting nucleus of the thalamus',
                                     'Lateral dorsal nucleus of thalamus', 'Medial geniculate complex, medial part','Ventral part of the lateral geniculate complex',
                                      'Mediodorsal nucleus of thalamus','Central lateral nucleus of the thalamus', 'Central medial nucleus of the thalamus', 'Paracentral nucleus',
                                     'Submedial nucleus of the thalamus', 'Reticular nucleus of the thalamus', 'Ventral posterolateral nucleus of the thalamus',
                                    'Medial geniculate complex, dorsal part', 'Medial geniculate complex, ventral part', 'Interanterodorsal nucleus of the thalamus',
                              'Anteroventral nucleus of thalamus', 'Ventral posteromedial nucleus of the thalamus, parvicellular part', 
                                          'Ventral posterolateral nucleus of the thalamus, parvicellular part',"Retrosplenial area, dorsal part, layer 2/3", "Retrosplenial area, dorsal part, layer 1",
                                     "Retrosplenial area, dorsal part, layer 5", "Retrosplenial area, dorsal part, layer 6a", 
                                      "Retrosplenial area, lateral agranular part, layer 2/3", "Retrosplenial area, lateral agranular part, layer 1",
                                        "Retrosplenial area, lateral agranular part, layer 4", "Retrosplenial area, ventral part, layer 6b",
                                        "Retrosplenial area, lateral agranular part, layer 5", "Retrosplenial area, lateral agranular part, layer 6a",
                                   "Retrosplenial area, lateral agranular part, layer 6b", "Retrosplenial area, ventral part, layer 5", 
                                       "Retrosplenial area, ventral part, layer 6a", "Retrosplenial area, ventral part, layer 4", 
                                        "Retrosplenial area, ventral part, layer 2/3", "Retrosplenial area, ventral part, layer 1",
                                             "Retrosplenial area, dorsal part, layer 6b",'Dorsal part of the lateral geniculate complex, ipsilateral zone','Dorsal part of the lateral geniculate complex, core',
                                          'Dorsal part of the lateral geniculate complex, shell','Primary visual area, layer 5', 'Primary visual area, layer 1', 
                                       'Primary visual area, layer 4', 'Primary visual area, layer 2/3',
                                        'Primary visual area, layer 6a', 'Primary visual area, layer 6b' ])].copy()
    # and append those rows to the whatsleft df
    whatsleft.append(df_whatsleft)
    
    ## Get total cell count for each class of labelled cell
    # try statements used in case there are no cells of a class for that 
    # mouse and region
    counts = df['Class'].value_counts()
    try:
        both_ct = counts["both"]
    except:
        both_ct = 0
    try:
        gfp_ct = counts["gfp"]
    except:
        gfp_ct = 0
    try:
        tom_ct = counts["tom"]
    except:
        tom_ct = 0

    total = both_ct + gfp_ct + tom_ct
    perc_gfp = gfp_ct/total*100
    
    #Append the percent GFP to appropriate lists
    if mouse in md_mice:
        if perc_gfp > 1:
            md_allregions.append(perc_gfp)
    else:
        if perc_gfp > 1:
            control_allregions.append(perc_gfp)
    f.write("Overall percent GFP: {} \n Total cell count: {}\n".format(perc_gfp, total))
    
    # Plots for each region
    ## Primary visual cortex plot: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if len(df_v1.index) > 0:
        counts = df_v1['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
    
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        if show_plots == True:
            sns.countplot(data=df_v1, x='Class', order=['both','gfp', 'tom'], palette=['gold', 'green',  'red']).set(title='{} v1: {:10.2f} % GFP'.format(im_title, perc_gfp))
            plt.show()
            plt.close()
        print('Percent GFP in V1 for {}: {}'.format(mouse, perc_gfp))
        f.write('Percent GFP in V1 for {}: {}\n'.format(mouse, perc_gfp))

        if mouse in md_mice:
            if perc_gfp > 1:
                md_v1.append(perc_gfp)
                md_v1_ct.append(total)
            dfs_md_v1.append(df_v1)
        else:
            if perc_gfp > 1:
                control_v1.append(perc_gfp)
                control_v1_ct.append(total)
            dfs_control_v1.append(df_v1)
            
    if len(df_v1_left.index) > 0:
        counts = df_v1_left['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
    
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        if mouse in md_mice:
            if perc_gfp > 1:
                md_v1_left.append(perc_gfp)
                md_v1_left_ct.append(total)
        else:
            if perc_gfp > 1:
                control_v1_left.append(perc_gfp)
                control_v1_left_ct.append(total)
        print("left v1 for {}: {}".format(mouse, perc_gfp))
        f.write("Left v1 for {}: {}\n".format(mouse, perc_gfp))

    if len(df_v1_right.index) > 0:
        counts = df_v1_right['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
    
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        if mouse in md_mice:
            if perc_gfp > 1:
                md_v1_right.append(perc_gfp)
                md_v1_right_ct.append(total)
        else:
            if perc_gfp > 1:
                control_v1_right.append(perc_gfp)
                control_v1_right_ct.append(total)
        print("right v1 for {}: {}".format(mouse, perc_gfp))
        f.write("Right v1 for {}: {}\n".format(mouse, perc_gfp))

    ## dLGN plot:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if len(df_dLGN.index) > 0:
        
        counts = df_dLGN['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0    
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
        try:
            total = both_ct + gfp_ct + tom_ct
        except:
            total = 0
        try:
            perc_gfp = gfp_ct/total*100
        except:
            perc_gfp = 0
        
        if show_plots == True:    
            sns.countplot(data=df_dLGN, x='Class', order=['both','gfp', 'tom'], palette=['gold', 'green',  'red']).set(title='{} dLGN: {:10.2f} % GFP'.format(im_title, perc_gfp))
            plt.show()
            plt.close()

        print('Percent GFP in dLGN for {}: {}'.format(mouse, perc_gfp))
        f.write('Percent GFP in dLGN for {}: {}\n'.format(mouse, perc_gfp))

        if mouse in md_mice:
            if perc_gfp > 1:
                md_dlgn.append(perc_gfp)
                md_dlgn_ct.append(total)
            dfs_md_dlgn.append(df_dLGN)
        else:
            if perc_gfp > 1:
                control_dlgn.append(perc_gfp)
                control_dlgn_ct.append(total)
            dfs_control_dlgn.append(df_dLGN)

        
    ## thal plot:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if len(df_thal.index) > 0:
        
        counts = df_thal['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
        
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        
        if show_plots == True:
            sns.countplot(data=df_thal, x='Class', order=['both','gfp', 'tom'], palette=['gold', 'green',  'red']).set(title='{} thal: {:10.2f} % GFP'.format(im_title, perc_gfp))
            plt.show()
            plt.close()

        print('Percent GFP in thal for {}: {}'.format(mouse, perc_gfp))
        f.write('Percent GFP in thal for {}: {}\n'.format(mouse, perc_gfp))

        if mouse in md_mice:
            if perc_gfp > 1:
                md_thal.append(perc_gfp)
                md_thal_ct.append(total)
            dfs_md_thal.append(df_thal)
        else:
            if perc_gfp > 1:
                control_thal.append(perc_gfp)
                control_thal_ct.append(total)
            dfs_control_thal.append(df_thal)
            
    ## HVAs plot:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if len(df_HVAs.index) > 0:
        
        counts = df_HVAs['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0        
        
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100

        if show_plots == True:
            sns.countplot(data=df_HVAs, x='Class', order=['both','gfp', 'tom'], palette=['gold', 'green',  'red']).set(title='{} HVAs: {:10.2f} % GFP'.format(im_title, perc_gfp))
            plt.show()
            plt.close()

        print('Percent GFP in HVAs for {}: {}'.format(mouse, perc_gfp))
        f.write('Percent GFP in HVAs for {}: {}\n'.format(mouse, perc_gfp))

        if mouse in md_mice:
            if perc_gfp > 1:
                md_hvas.append(perc_gfp)
                md_hvas_ct.append(total)
            dfs_md_hvas.append(df_HVAs)
        else:
            if perc_gfp > 1:
                control_hvas.append(perc_gfp)
                control_hvas_ct.append(total)
            dfs_control_hvas.append(df_HVAs)
            
    if len(df_HVAs_left.index) > 0:
        counts = df_HVAs_left['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
    
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        if mouse in md_mice:
            if perc_gfp > 1:
                md_hvas_left.append(perc_gfp)
                md_hvas_left_ct.append(total)
        else:
            if perc_gfp > 1:
                control_hvas_left.append(perc_gfp)
                control_hvas_left_ct.append(total)
            
    if len(df_HVAs_right.index) > 0:
        counts = df_HVAs_right['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0        
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
    
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        if mouse in md_mice:
            if perc_gfp > 1:
                md_hvas_right.append(perc_gfp)
                md_hvas_right_ct.append(total)
        else:
            if perc_gfp > 1:
                control_hvas_right.append(perc_gfp)
                control_hvas_ct.append(total)
    
    ## RSC plot:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if len(df_rsc.index) > 0:
        
        counts = df_rsc['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0        
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
        
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        if show_plots == True:
            sns.countplot(data=df_rsc, x='Class', order=['both','gfp', 'tom'], palette=['gold', 'green',  'red']).set(title='{} RsC: {:10.2f} % GFP'.format(im_title, perc_gfp))
            plt.show()
            plt.close()

        print('Percent GFP in RSC for {}: {}'.format(mouse, perc_gfp))
        f.write('Percent GFP in RSC for {}: {}\n'.format(mouse, perc_gfp))

        if mouse in md_mice:
            if perc_gfp > 1:
                md_rsc.append(perc_gfp)
                md_rsc_ct.append(total)
            dfs_md_rsc.append(df_rsc)
        else:
            if perc_gfp > 1:
                control_rsc.append(perc_gfp)
                control_rsc_ct.append(total)
            dfs_control_rsc.append(df_rsc)    
            
    ## Amygdala plot:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if len(df_amyg.index) > 0:
        
        counts = df_amyg['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
        
        total = both_ct + gfp_ct + tom_ct
        try:
            perc_gfp = gfp_ct/total*100
        except:
            perc_gfp = 0
        if show_plots == True:
            sns.countplot(data=df_amyg, x='Class', order=['both','gfp', 'tom'], palette=['gold', 'green',  'red']).set(title='{} Amygdala: {:10.2f} % GFP'.format(im_title, perc_gfp))
            plt.show()
            plt.close()

        print('Percent GFP in amygdala for {}: {}'.format(mouse, perc_gfp))
        f.write('Percent GFP in amygdala for {}: {}\n'.format(mouse, perc_gfp))

        if mouse in md_mice:
            if perc_gfp > 1:
                md_amyg.append(perc_gfp)
                md_amyg_ct.append(total)
            dfs_md_amyg.append(df_amyg)
        else:
            if perc_gfp > 1:
                control_amyg.append(perc_gfp)
                control_amyg_ct.append(total)
            dfs_control_amyg.append(df_amyg)
                
    ## Superior colliculus plot: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if len(df_sc.index) > 0:
        
        counts = df_sc['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0            
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
    
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        if show_plots == True:
            sns.countplot(data=df_sc, x='Class', order=['both','gfp', 'tom'], palette=['gold', 'green',  'red']).set(title='{} SC: {:10.2f} % GFP'.format(im_title, perc_gfp))
            plt.show()
            plt.close()
        print('Percent GFP in SC for {}: {}'.format(mouse, perc_gfp))
        f.write('Percent GFP in SC for {}: {}\n'.format(mouse, perc_gfp))

        if mouse in md_mice:
            if perc_gfp > 1:
                md_sc.append(perc_gfp)
                md_sc_ct.append(total)
            dfs_md_sc.append(df_sc)
        else:
            if perc_gfp > 1:
                control_sc.append(perc_gfp)
                control_sc_ct.append(total)
            dfs_control_sc.append(df_sc)
      
    ## Claustrum plot: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if len(df_claustrum.index) > 0:
        
        counts = df_claustrum['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0            
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
    
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        if show_plots == True:
            sns.countplot(data=df_claustrum, x='Class', order=['both','gfp', 'tom'], palette=['gold', 'green',  'red']).set(title='{} Claustrum: {:10.2f} % GFP'.format(im_title, perc_gfp))
            plt.show()
            plt.close()
        print('Percent GFP in claustrum for {}: {}'.format(mouse, perc_gfp))
        f.write('Percent GFP in claustrum for {}: {}\n'.format(mouse, perc_gfp))

        if mouse in md_mice:
            if perc_gfp > 1:
                md_claustrum.append(perc_gfp)
                md_claustrum_ct.append(total)
            dfs_md_claustrum.append(df_claustrum)
        else:
            if perc_gfp > 1:
                control_claustrum.append(perc_gfp)
                control_claustrum_ct.append(total)
            dfs_control_claustrum.append(df_claustrum)
        
    ## Hypothalamus plot: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if len(df_hypothal.index) > 0:
        
        counts = df_hypothal['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0            
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
    
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        if show_plots == True:
            sns.countplot(data=df_hypothal, x='Class', order=['both','gfp', 'tom'], palette=['gold', 'green',  'red']).set(title='{} Hypothalamus: {:10.2f} % GFP'.format(im_title, perc_gfp))
            plt.show()
            plt.close()
        print('Percent GFP in hypothalamus for {}: {}'.format(mouse, perc_gfp))
        f.write('Percent GFP in hypothalamus for {}: {}\n'.format(mouse, perc_gfp))

        if mouse in md_mice:
            if perc_gfp > 1:
                md_hypothal.append(perc_gfp)
                md_hypothal_ct.append(total)
            dfs_md_hypothal.append(df_hypothal)
        else:
            if perc_gfp > 1:
                control_hypothal.append(perc_gfp)
                control_hypothal_ct.append(total)
            dfs_control_hypothal.append(df_hypothal)
    ## Auditory cortex plot: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if len(df_audcortex.index) > 0:
        
        counts = df_audcortex['Class'].value_counts()
        try:
            both_ct = counts["both"]
        except:
            both_ct = 0            
        try:
            gfp_ct = counts["gfp"]
        except:
            gfp_ct = 0
        try:
            tom_ct = counts["tom"]
        except:
            tom_ct = 0
    
        total = both_ct + gfp_ct + tom_ct
        perc_gfp = gfp_ct/total*100
        if show_plots == True:
            sns.countplot(data=df_audcortex, x='Class', order=['both','gfp', 'tom'], palette=['gold', 'green',  'red']).set(title='{} Auditory cortex: {:10.2f} % GFP'.format(im_title, perc_gfp))
            plt.show()
            plt.close()
        print('Percent GFP in Auditory cortex for {}: {}'.format(mouse, perc_gfp))
        f.write('Percent GFP in Auditory cortex for {}: {}\n \n \n'.format(mouse, perc_gfp))

        if mouse in md_mice:
            if perc_gfp > 1:
                md_audcortex.append(perc_gfp)
                md_audcortex_ct.append(total)
            dfs_md_audcortex.append(df_audcortex)
        else:
            if perc_gfp > 1:
                control_audcortex.append(perc_gfp)
                control_audcortex_ct.append(total)
            dfs_control_audcortex.append(df_audcortex)
    ##-------------------------------------------------------------------
    # Plot and save a summary of all selected regions, for a given mouse:
    dfs = [df_v1, df_HVAs, df_dLGN, df_thal, df_rsc, df_amyg, df_sc, df_hypothal, df_claustrum, df_audcortex]
    df_concat = pd.concat(dfs, keys=['a df_v1', 'b df_HVAs', 'c df_dLGN', 'df_thal', 'e df_rsc', 'f df_amyg', 'g sc', 'hypothal', 'i claustrum', 'j auditory']).reset_index()
    df_concat = df_concat.rename(columns={"level_0": "Region_name"})
    plt.figure(figsize=(14, 14))
    
    df_plot = df_concat.groupby(['Region_name','Class']).size().reset_index().pivot(index='Region_name', columns='Class', values=0)
    
    fi = df_plot.plot(kind='bar', stacked=True, color=['gold', 'green',  'red'], title=im_title).get_figure()
    if show_plots == True:
        plt.show()
        plt.close()

    fi.savefig(os.path.join(path_to_final_csvs, im_title + 'newmodel.png'), bbox_inches='tight')
    
f.close()
    
    
# Plot summaries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


mean_md_v1 = np.average(md_v1)
print('v1 MD: {}'.format( mean_md_v1))
mean_control_v1 = np.average(control_v1)
print('v1 control: {}'.format( mean_control_v1))

mean_md_hvas = np.average(md_hvas)
mean_control_hvas = np.average(control_hvas)

mean_md_thal = np.average(md_thal)
mean_control_thal = np.average(control_thal)

mean_md_dlgn = np.average(md_dlgn)
mean_control_dlgn = np.average(control_dlgn)

mean_md_rsc = np.average(md_rsc)
mean_control_rsc = np.average(control_rsc)

mean_md_amyg = np.average(md_amyg)
mean_control_amyg = np.average(control_amyg)

mean_md_sc = np.average(md_sc)
mean_control_sc = np.average(control_sc)

mean_md_hypothal = np.average(md_hypothal)
mean_control_hypothal = np.average(control_hypothal)

mean_md_claustrum = np.average(md_claustrum)
mean_control_claustrum = np.average(control_claustrum)

mean_md_audcortex = np.average(md_audcortex)
mean_control_audcortex = np.average(control_audcortex)

labels = ['v1', 'HVAs', 'dLGN', 'thal', 'rsc', 'amyg', 'sc', 'hypothal', 'claustrum', 'audcortex']

x = np.arange(len(labels))
width = 0.35


md_props = [mean_md_v1, mean_md_hvas, mean_md_dlgn, 
            mean_md_thal, mean_md_rsc, mean_md_amyg,
            mean_md_sc, mean_md_hypothal, mean_md_claustrum,
            mean_md_audcortex]
control_props = [mean_control_v1, mean_control_hvas, mean_control_dlgn,
                 mean_control_thal, mean_control_rsc, mean_control_amyg,
                 mean_control_sc, mean_control_hypothal, mean_control_claustrum,
                 mean_control_audcortex] 

fig, ax = plt.subplots(figsize=(8,6))


for i in range(len(md_v1)):
    ax.scatter(x[0] - width/2, md_v1[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_v1)):
    ax.scatter(x[0] + width/2, control_v1[i], 
               zorder=10, color='black', s=10)

for i in range(len(md_hvas)):
    ax.scatter(x[1] - width/2, md_hvas[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_hvas)):
    ax.scatter(x[1] + width/2, control_hvas[i], 
               zorder=10, color='black', s=10)
    
for i in range(len(md_dlgn)):
    ax.scatter(x[2] - width/2, md_dlgn[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_dlgn)):
    ax.scatter(x[2] + width/2, control_dlgn[i], 
               zorder=10, color='black', s=10)
    
for i in range(len(md_thal)):
    ax.scatter(x[3] - width/2, md_thal[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_thal)):
    ax.scatter(x[3] + width/2, control_thal[i], 
               zorder=10, color='black', s=10)
    
for i in range(len(md_rsc)):
    ax.scatter(x[4] - width/2, md_rsc[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_rsc)):
    ax.scatter(x[4] + width/2, control_rsc[i], 
               zorder=10, color='black', s=10)
    
for i in range(len(md_amyg)):
    ax.scatter(x[5] - width/2, md_amyg[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_amyg)):
    ax.scatter(x[5] + width/2, control_amyg[i], 
               zorder=10, color='black', s=10)

for i in range(len(md_sc)):
    ax.scatter(x[6] - width/2, md_sc[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_sc)):
    ax.scatter(x[6] + width/2, control_sc[i], 
               zorder=10, color='black', s=10)

for i in range(len(md_hypothal)):
    ax.scatter(x[7] - width/2, md_hypothal[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_hypothal)):
    ax.scatter(x[7] + width/2, control_hypothal[i], 
               zorder=10, color='black', s=10)

for i in range(len(md_claustrum)):
    ax.scatter(x[8] - width/2, md_claustrum[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_claustrum)):
    ax.scatter(x[8] + width/2, control_claustrum[i], 
               zorder=10, color='black', s=10)
    
for i in range(len(md_audcortex)):
    ax.scatter(x[9] - width/2, md_audcortex[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_audcortex)):
    ax.scatter(x[9] + width/2, control_audcortex[i], 
               zorder=10, color='black', s=10)
        
set1 =  ax.bar(x - width/2, md_props, width, label='MD', color='limegreen')
set2 = ax.bar(x + width/2, control_props, width, label='Control', color='royalblue')

ax.set_ylabel('Percent')
ax.set_xlabel('Brain region')
ax.set_title('Percent GFP-only cells')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontdict ={'fontsize':8})
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()
plt.close()

# Plot summaries of total cell count ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mean_md_v1 = np.average(md_v1_ct)
mean_control_v1 = np.average(control_v1_ct)

mean_md_hvas = np.average(md_hvas_ct)
mean_control_hvas = np.average(control_hvas_ct)

mean_md_thal = np.average(md_thal_ct)
mean_control_thal = np.average(control_thal_ct)

mean_md_dlgn = np.average(md_dlgn_ct)
mean_control_dlgn = np.average(control_dlgn_ct)

mean_md_rsc = np.average(md_rsc_ct)
mean_control_rsc = np.average(control_rsc_ct)

mean_md_amyg = np.average(md_amyg_ct)
mean_control_amyg = np.average(control_amyg_ct)

mean_md_sc = np.average(md_sc_ct)
mean_control_sc = np.average(control_sc_ct)

mean_md_hypothal = np.average(md_hypothal_ct)
mean_control_hypothal = np.average(control_hypothal_ct)

mean_md_claustrum = np.average(md_claustrum_ct)
mean_control_claustrum = np.average(control_claustrum_ct)

mean_md_audcortex = np.average(md_audcortex_ct)
mean_control_audcortex = np.average(control_audcortex_ct)

labels = ['v1', 'HVAs', 'dLGN', 'thal', 'rsc', 'amyg', 'sc', 'hypothal', 'claustrum', 'audcortex']

x = np.arange(len(labels))
width = 0.35


md_props = [mean_md_v1, mean_md_hvas, mean_md_dlgn, 
            mean_md_thal, mean_md_rsc, mean_md_amyg,
            mean_md_sc, mean_md_hypothal, mean_md_claustrum,
            mean_md_audcortex]
control_props = [mean_control_v1, mean_control_hvas, mean_control_dlgn,
                 mean_control_thal, mean_control_rsc, mean_control_amyg,
                 mean_control_sc, mean_control_hypothal, mean_control_claustrum,
                 mean_control_audcortex] 

fig, ax = plt.subplots(figsize=(8,6))


for i in range(len(md_v1_ct)):
    ax.scatter(x[0] - width/2, md_v1_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_v1_ct)):
    ax.scatter(x[0] + width/2, control_v1_ct[i], 
                zorder=10, color='black', s=10)

for i in range(len(md_hvas_ct)):
    ax.scatter(x[1] - width/2, md_hvas_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_hvas_ct)):
    ax.scatter(x[1] + width/2, control_hvas_ct[i], 
                zorder=10, color='black', s=10)
    
for i in range(len(md_dlgn_ct)):
    ax.scatter(x[2] - width/2, md_dlgn_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_dlgn_ct)):
    ax.scatter(x[2] + width/2, control_dlgn_ct[i], 
                zorder=10, color='black', s=10)
    
for i in range(len(md_thal_ct)):
    ax.scatter(x[3] - width/2, md_thal_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_thal_ct)):
    ax.scatter(x[3] + width/2, control_thal_ct[i], 
                zorder=10, color='black', s=10)
    
for i in range(len(md_rsc_ct)):
    ax.scatter(x[4] - width/2, md_rsc_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_rsc_ct)):
    ax.scatter(x[4] + width/2, control_rsc_ct[i], 
                zorder=10, color='black', s=10)
    
for i in range(len(md_amyg_ct)):
    ax.scatter(x[5] - width/2, md_amyg_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_amyg_ct)):
    ax.scatter(x[5] + width/2, control_amyg_ct[i], 
                zorder=10, color='black', s=10)

for i in range(len(md_sc_ct)):
    ax.scatter(x[6] - width/2, md_sc_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_sc_ct)):
    ax.scatter(x[6] + width/2, control_sc_ct[i], 
                zorder=10, color='black', s=10)

for i in range(len(md_hypothal_ct)):
    ax.scatter(x[7] - width/2, md_hypothal_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_hypothal_ct)):
    ax.scatter(x[7] + width/2, control_hypothal_ct[i], 
                zorder=10, color='black', s=10)

for i in range(len(md_claustrum_ct)):
    ax.scatter(x[8] - width/2, md_claustrum_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_claustrum_ct)):
    ax.scatter(x[8] + width/2, control_claustrum_ct[i], 
                zorder=10, color='black', s=10)
    
for i in range(len(md_audcortex_ct)):
    ax.scatter(x[9] - width/2, md_audcortex_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_audcortex_ct)):
    ax.scatter(x[9] + width/2, control_audcortex_ct[i], 
                zorder=10, color='black', s=10)
        
set1 =  ax.bar(x - width/2, md_props, width, label='MD', color='limegreen')
set2 = ax.bar(x + width/2, control_props, width, label='Control', color='royalblue')

ax.set_ylabel('Avg number of cells per mouse')
ax.set_xlabel('Brain region')
ax.set_title('Number of labeled cells')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontdict ={'fontsize':8})
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()
plt.close()

### Plot number of cells for left v right ########################
mean_md_v1_left = np.average(md_v1_left_ct)
mean_control_v1_left = np.average(control_v1_left_ct)

mean_md_hvas_left = np.average(md_hvas_left_ct)
mean_control_hvas_left = np.average(control_hvas_left_ct)

mean_md_v1_right = np.average(md_v1_right_ct)
mean_control_v1_right = np.average(control_v1_right_ct)

mean_md_hvas_right = np.average(md_hvas_right_ct)
mean_control_hvas_right = np.average(control_hvas_right_ct)

labels = ['v1 left','v1 right','HVAs left','HVAs right']
x = np.arange(len(labels))
width = 0.35


md_props = [mean_md_v1_left, mean_md_v1_right, mean_md_hvas_left, mean_md_hvas_right]
control_props = [mean_control_v1_left, mean_control_v1_right, mean_control_hvas_left, mean_control_hvas_right] 

fig, ax = plt.subplots(figsize=(8,6))


for i in range(len(md_v1_left_ct)):
    ax.scatter(x[0] - width/2, md_v1_left_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_v1_left_ct)):
    ax.scatter(x[0] + width/2, control_v1_left_ct[i], 
                zorder=10, color='black', s=10)

for i in range(len(md_v1_right_ct)):
    ax.scatter(x[1] - width/2, md_v1_right_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_v1_right_ct)):
    ax.scatter(x[1] + width/2, control_v1_right_ct[i], 
                zorder=10, color='black', s=10)


for i in range(len(md_hvas_left_ct)):
    ax.scatter(x[2] - width/2, md_hvas_left_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_hvas_left_ct)):
    ax.scatter(x[2] + width/2, control_hvas_left_ct[i], 
                zorder=10, color='black', s=10)
    
for i in range(len(md_hvas_right_ct)):
    ax.scatter(x[3] - width/2, md_hvas_right_ct[i], 
                zorder=10, color='black', s=10)
for i in range(len(control_hvas_right_ct)):
    ax.scatter(x[3] + width/2, control_hvas_right_ct[i], 
                zorder=10, color='black', s=10)


        
set1 =  ax.bar(x - width/2, md_props, width, label='MD', color='limegreen')
set2 = ax.bar(x + width/2, control_props, width, label='Control', color='royalblue')

ax.set_ylabel('Avg number of cells per mouse')
ax.set_xlabel('Brain region')
ax.set_title('Number of labeled cells')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontdict ={'fontsize':8})
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()
plt.close()


## Plot number of cells without individual pts
fig, ax = plt.subplots(figsize=(8,6))
        
set1 =  ax.bar(x - width/2, md_props, width, label='MD', color='limegreen')
set2 = ax.bar(x + width/2, control_props, width, label='Control', color='royalblue')

ax.set_ylabel('Avg number of cells per mouse')
ax.set_xlabel('Brain region')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontdict ={'fontsize':8})
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()
plt.close()

# Plot left vs right ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mean_md_v1_left = np.average(md_v1_left)
mean_md_v1_right = np.average(md_v1_right)
mean_control_v1_left = np.average(control_v1_left)
mean_control_v1_right = np.average(control_v1_right)

mean_md_hvas_left = np.average(md_hvas_left)
mean_md_hvas_right = np.average(md_hvas_right)
mean_control_hvas_left = np.average(control_hvas_left)
mean_control_hvas_right = np.average(control_hvas_right)

labels = ['v1 left', 'v1 right', 'HVAs left', 'HVAs right' ]

x = np.arange(len(labels))
width = 0.35


md_props2 = [mean_md_v1_left, mean_md_v1_right, mean_md_hvas_left, mean_md_hvas_right]
control_props2 = [mean_control_v1_left, mean_control_v1_right, mean_control_hvas_left, mean_control_hvas_right]

fig, ax = plt.subplots(figsize=(8,6))

for i in range(len(md_v1_left)):
    ax.scatter(x[0] - width/2, md_v1_left[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_v1_left)):
    ax.scatter(x[0] + width/2, control_v1_left[i], 
               zorder=10, color='black', s=10)
for i in range(len(md_v1_right)):
    ax.scatter(x[1] - width/2, md_v1_right[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_v1_right)):
    ax.scatter(x[1] + width/2, control_v1_right[i], 
               zorder=10, color='black', s=10)

for i in range(len(md_hvas_left)):
    ax.scatter(x[2] - width/2, md_hvas_left[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_hvas_left)):
    ax.scatter(x[2] + width/2, control_hvas_left[i], 
               zorder=10, color='black', s=10)
for i in range(len(md_hvas_right)):
    ax.scatter(x[3] - width/2, md_hvas_right[i], 
               zorder=10, color='black', s=10)
for i in range(len(control_hvas_right)):
    ax.scatter(x[3] + width/2, control_hvas_right[i], 
               zorder=10, color='black', s=10)

set1 =  ax.bar(x - width/2, md_props2, width, label='MD', color='limegreen')
set2 = ax.bar(x + width/2, control_props2, width, label='Control', color='royalblue')

ax.set_ylabel('Percent')
ax.set_xlabel('Region + hemisphere')
ax.set_title('Percent GFP-only cells')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontdict ={'fontsize':8})
ax.legend()
ax.set_ylim(bottom= 0, top=100)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()
plt.close()



## Read in summary spreadsheet with IOS data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

summary_csv = df = pd.read_excel(r'I:\Danielle Paynter\TTT_2022\references\TTT_2022_mouse_summary.xlsx')

# Calculate mean baseline ODI + standard deviation
baseline_ODIs = summary_csv[["ODI_baseline1", "ODI_baseline2", "ODI_baseline3", "ODI_baseline4"]]
df_baseline = summary_csv[["Mouse","MD", "ODI_baseline1", "ODI_baseline2", "ODI_baseline3", "ODI_baseline4"]]
df_baseline["baseline_mean"] = baseline_ODIs.mean(axis=1)
df_baseline["baseline_std"] = baseline_ODIs.std(axis=1)

# Plot last ODI session
df_ODIs = summary_csv[~summary_csv['ODI_readout'].isnull()]
df_ODIs["baseline_mean"] = df_baseline["baseline_mean"]
df_ODIs["baseline_std"] = df_baseline["baseline_std"]

group_MD = df_ODIs.groupby('MD')
baseline_means = group_MD['baseline_mean'].mean()
baseline_STDs = group_MD['baseline_mean'].std()

ODI_means = group_MD['ODI_readout'].mean()
ODI_STDs = group_MD['ODI_readout'].std()

control_ODIs = df_ODIs[df_ODIs['MD'] == 0]
MD_ODIs = df_ODIs[df_ODIs['MD'] == 1]



###########################################################################
#Plots for MD mice OD data


v1_pts = []
v1_left_pts = []
v1_right_pts = []
dLGN_pts = []
thal_pts = []
HVAs_pts = []
rsc_pts= []

#0718B 
v1_pts.append([.0947-.0736, 30.57]) #v1
v1_left_pts.append([.0947-.0736, 29.92])
v1_right_pts.append([.0947-.0736, 36.28])
dLGN_pts.append([.0947-.0736, 28.91]) #dLGN
thal_pts.append([.0947-.0736, 33.96]) #thal
HVAs_pts.append([.0947-.0736, 37.09]) # HVAs
rsc_pts.append([.0947-.0736, 39.15]) # RsC

#0729B 
v1_pts.append([.2558-.0971, 34.95]) #v1
v1_left_pts.append([.2558-.0971, 33.57])
v1_right_pts.append([.2558-.0971, 52.67])
#[.2558-.0971, ] #dLGN
thal_pts.append([.2558-.0971, 52.20]) #thal
HVAs_pts.append([.2558-.0971, 40.61]) # HVAs
rsc_pts.append([.2558-.0971, 50.25]) # RsC


#0729C
v1_pts.append([.1903-.0867, 68.54]) #v1
v1_left_pts.append([.1903-.0867, 68.62])
v1_right_pts.append([.1903-.0867, 54.55])
dLGN_pts.append([.1903-.0867, 44.23]) #dLGN
thal_pts.append([.1903-.0867, 51.54 ]) #thal
HVAs_pts.append([.1903-.0867, 60.87]) # HVAs
rsc_pts.append([.1903-.0867, 67.68]) # RsC


#0730D 
v1_pts.append([.1683-.0796, 20.11]) #v1
v1_left_pts.append([.1683-.0796, 20.11])
v1_right_pts.append([.1683-.0796, 20.11])
dLGN_pts.append([.1683-.0796, 19.51]) #dLGN
thal_pts.append([.1683-.0796, 28.51]) #thal
rsc_pts.append([.1683-.0796, 28.11]) # RsC

#0730H 
v1_pts.append([.1933-.2289, 50.54]) #v1
v1_left_pts.append([.1933-.2289, 49.38])
v1_right_pts.append([.1933-.2289, 65.82])
dLGN_pts.append([.1933-.2289, 32.71]) #dLGN
thal_pts.append([.1933-.2289, 42.88]) #thal
HVAs_pts.append([.1933-.2289, 55.30]) # HVAs
rsc_pts.append([.1933-.2289, 51.30]) # RsC

#0807H
v1_pts.append([.23+.037, 46.25]) #v1
v1_left_pts.append([.23+.037, 44.91])
v1_right_pts.append([.23+.037, 64.07])
dLGN_pts.append([.23+.037, 23.30]) #dLGN
thal_pts.append([.23+.037, 59.59]) #thal
HVAs_pts.append([.23+.037, 53.90]) # HVAs
rsc_pts.append([.23+.037, 56.13]) # RsC

#0807I
v1_pts.append([.25+.0634, 33.32]) #v1
v1_left_pts.append([.25+.0634, 31.01])
v1_right_pts.append([.25+.0634, 42.46])
dLGN_pts.append([.25+.0634, 23.76]) #dLGN
thal_pts.append([.25+.0634, 35.32]) #thal
HVAs_pts.append([.25+.0634, 33.86]) # HVAs
rsc_pts.append([.25+.0634, 34.82]) # RsC


fig, ax = plt.subplots()
x, y = zip(*thal_pts)
ax.scatter(*zip(*thal_pts))
z = np.polyfit(*zip(*thal_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('Thalamus - MD')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)


fig, ax = plt.subplots()
x, y = zip(*v1_pts)
ax.scatter(*zip(*v1_pts))
z = np.polyfit(*zip(*v1_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('v1 - MD')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)



fig, ax = plt.subplots()
x, y = zip(*v1_left_pts)
ax.scatter(*zip(*v1_left_pts))
z = np.polyfit(*zip(*v1_left_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('v1 left - MD')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)



fig, ax = plt.subplots()
x, y = zip(*v1_right_pts)
ax.scatter(*zip(*v1_right_pts))
z = np.polyfit(*zip(*v1_right_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('v1 right - MD')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)


fig, ax = plt.subplots()
x, y = zip(*HVAs_pts)
ax.scatter(*zip(*HVAs_pts))
z = np.polyfit(*zip(*HVAs_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('HVAs - MD')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)


fig, ax = plt.subplots()
x, y = zip(*rsc_pts)
ax.scatter(*zip(*rsc_pts))
z = np.polyfit(*zip(*rsc_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('RsC - MD')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)


fig, ax = plt.subplots()
ax.scatter(*zip(*dLGN_pts))
x, y = zip(*dLGN_pts)
z = np.polyfit(*zip(*dLGN_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('dLGN - MD')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)

# #TODO change these to variables, not the numbers, so the %s update with more slices
# ###########################################################################
# #Plots for control mice OD data
v1_pts = []
v1_left_pts = []
v1_right_pts = []
dLGN_pts = []
thal_pts = []
HVAs_pts = []
rsc_pts= []

#0718A
v1_pts.append([.1151-.1366, 26.46]) #v1
v1_left_pts.append([.1151-.1366, 26.94])
v1_right_pts.append([.1151-.1366, 24.11])
dLGN_pts.append([.1151-.1366, 19.11]) #dLGN
thal_pts.append([.1151-.1366, 19.67]) #thal
HVAs_pts.append([.1151-.1366, 31.76]) # HVAs
rsc_pts.append([.1151-.1366, 32.29]) # RsC

#0718F
v1_pts.append([.2874-.125, 16.01]) #v1
v1_left_pts.append([.2874-.125, 30.95])
v1_right_pts.append([.2874-.125, 10.50])
dLGN_pts.append([.2874-.125, 37.01]) #dLGN
thal_pts.append([.2874-.125, 29.65]) #thal
HVAs_pts.append([.2874-.125, 23.58]) # HVAs
rsc_pts.append([.2874-.125, 34.71]) # RsC

#0729A
v1_pts.append([.3005-.3908, 31.99]) #v1
v1_left_pts.append([.3005-.3908, 31.89])
v1_right_pts.append([.3005-.3908, 35.55])
dLGN_pts.append([.3005-.3908, 31.40]) #dLGN
thal_pts.append([.3005-.3908, 36.84]) #thal
HVAs_pts.append([.3005-.3908, 45.78]) # HVAs
rsc_pts.append([.3005-.3908, 42.86]) # RsC

#0730E
v1_pts.append([.1845-.0667, 25.43]) #v1
v1_left_pts.append([.1845-.0667, 23.73])
v1_right_pts.append([.1845-.0667, 42.32])
dLGN_pts.append([.1845-.0667, 11.65]) #dLGN
thal_pts.append([.1845-.0667, 29.41]) #thal
HVAs_pts.append([.1845-.0667, 26.93]) # HVAs
rsc_pts.append([.1845-.0667, 25.86]) # RsC

#0730F
v1_pts.append([.1525+0.0085, 29.44]) #v1
v1_left_pts.append([.1525+0.0085, 32.13])
v1_right_pts.append([.1525+0.0085, 23.41])
dLGN_pts.append([.1525+0.0085, 19.23]) #dLGN
thal_pts.append([.1525+0.0085, 26.99]) #thal
HVAs_pts.append([.1525+0.0085, 27.56]) # HVAs
rsc_pts.append([.1525+0.0085, 36.35]) # RsC

#0807C
v1_pts.append([.2238-.3803, 46.09]) #v1
v1_left_pts.append([.2238-.3803, 45.90])
v1_right_pts.append([.2238-.3803, 57.53])
dLGN_pts.append([.2238-.3803, 31.16]) #dLGN
thal_pts.append([.2238-.3803, 59.21]) #thal
HVAs_pts.append([.2238-.3803, 52.06]) # HVAs
rsc_pts.append([.2238-.3803, 60.04]) # RsC

#0807D
v1_pts.append([.3032-.1893, 34.91]) #v1
v1_left_pts.append([.3032-.1893, 31.61])
v1_right_pts.append([.3032-.1893, 47.23])
dLGN_pts.append([.3032-.1893, 47.71]) #dLGN
thal_pts.append([.3032-.1893, 49.41]) #thal
HVAs_pts.append([.3032-.1893, 47.44]) # HVAs
rsc_pts.append([.3032-.1893, 46.16]) # RsC

#0807G
v1_pts.append([.2543-.609, 17.47]) #v1
v1_left_pts.append([.2543-.609, 17.25])
v1_right_pts.append([.2543-.609, 18.11])
dLGN_pts.append([.2543-.609, 32.85]) #dLGN
thal_pts.append([.2543-.609, 56.72]) #thal
HVAs_pts.append([.2543-.609, 21.47]) # HVAs
rsc_pts.append([.2543-.609, 26.00]) # RsC



fig, ax = plt.subplots()
ax.scatter(*zip(*thal_pts))
x, y = zip(*thal_pts)
z = np.polyfit(*zip(*thal_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('Thalamus - Control')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)




fig, ax = plt.subplots()
ax.scatter(*zip(*v1_pts))
x, y = zip(*v1_pts)
z = np.polyfit(*zip(*v1_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('v1 - Control')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)

fig, ax = plt.subplots()
ax.scatter(*zip(*v1_left_pts))
x, y = zip(*v1_left_pts)
z = np.polyfit(*zip(*v1_left_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('v1 left - Control')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)

fig, ax = plt.subplots()
ax.scatter(*zip(*v1_right_pts))
x, y = zip(*v1_right_pts)
z = np.polyfit(*zip(*v1_right_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('v1 right - Control')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)




fig, ax = plt.subplots()
ax.scatter(*zip(*HVAs_pts))
x, y = zip(*HVAs_pts)
z = np.polyfit(*zip(*HVAs_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('HVAs - Control')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)


fig, ax = plt.subplots()
ax.scatter(*zip(*rsc_pts))
x, y = zip(*rsc_pts)
z = np.polyfit(*zip(*rsc_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('RsC - Control')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)




fig, ax = plt.subplots()
ax.scatter(*zip(*dLGN_pts))
x, y = zip(*dLGN_pts)
z = np.polyfit(*zip(*dLGN_pts), 1)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('dLGN - Control')
ax.set_xlabel('ODI Shift \n baseline minus readout')
ax.set_ylabel('Percent GFP-only')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= 0, top=100)


## Regions that aren't being plotted
unplotted_areas = list(pd.concat(whatsleft)["Region"].unique())


###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###########################################################################
#Plots for MD mice OD data
#right - left

v1_pts = []

#0718B 
v1_pts.append([.0947-.0736, 36.18-29.05]) #v1


#0729B 
v1_pts.append([.2558-.0971, 52.67-33.57]) #v1



#0729C
v1_pts.append([.1903-.0867, 54.55-68.62]) #v1



#0730D 
#v1_pts.append([.1683-.0796, 20.11]) #v1


#0730H 
v1_pts.append([.1933-.2289, 65.82-49.38]) #v1


#0807H
v1_pts.append([.23+.037, 64.07-44.91]) #v1


#0807I
v1_pts.append([.25+.0634, 42.46-31.01]) #v1



fig, ax = plt.subplots(figsize=(8,4))
x, y = zip(*v1_pts)
ax.scatter(*zip(*v1_pts))
z = np.polyfit(x, y, 1)
md_pearsons_coefficient = np.corrcoef(x, y)
md_slope = z[0]
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('ODI shift vs difference in % GFP L vs R \n MD mice')
ax.set_xlabel('Shift in ODI')
ax.set_ylabel('Right hemi minus left hemi % GFP')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= -30, top=60)

plt.show()
plt.close()
###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ###########################################################################
# #Plots for control mice OD data
v1_pts = []
dLGN_pts = []
thal_pts = []
HVAs_pts = []
rsc_pts= []

#0718A
v1_pts.append([.1151-.1366, 24.11-26.94]) #v1


#0718F
v1_pts.append([.2874-.125, 30.95-10.5]) #v1


#0729A
v1_pts.append([.3005-.3908, 35.56-31.89]) #v1


#0730E
v1_pts.append([.1845-.0667, 42.32-23.42]) #v1


#0730F
v1_pts.append([.1525+0.0085, 23.41-32.85]) #v1


#0807C
v1_pts.append([.2238-.3803, 57.53-45.90]) #v1

#0807D
v1_pts.append([.3032-.1893, 47.23-31.61]) #v1

#0807G
v1_pts.append([.2543-.609, 18.11-17.25]) #v1

fig, ax = plt.subplots(figsize=(8,4))
ax.scatter(*zip(*v1_pts))
x, y = zip(*v1_pts)
z = np.polyfit(x, y, 1)
control_slope = z[0]
control_pearsons_coefficient = np.corrcoef(x,y)
p = np.poly1d(z)
ax.plot(x,p(x),"r--")
ax.set_title('ODI shift vs difference in % GFP L vs R \n Control mice')
ax.set_xlabel('Shift in ODI')
ax.set_ylabel('Right hemi minus left hemi % GFP')
ax.set_xticks([ -.4,-.35,-.3,-.25,-.2,-.150, -.100, -.050, 0.000,  0.050,  0.100, 0.150,  0.2,  0.250,  0.30, 0.35])
ax.set_xlim(left = -.4, right=0.35)
ax.set_ylim(bottom= -30, top=60)

plt.show()

md_mean_gfp = np.average(md_allregions)
control_mean_gfp = np.average(control_allregions)

print(md_mean_gfp)
print(control_mean_gfp)