# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 08:59:32 2023

Integrate CSVs from Nutil and cell classification

@author: dpaynter
"""

import pandas as pd
import numpy as np
import os 
from scipy.spatial.distance import cdist
from scipy.spatial import KDTree


nutil_dir = r'J:\Danielle Paynter\Nutil'
class_dir = r'J:\Danielle Paynter\Class_outputs'
output_dir = r'J:\Danielle Paynter\Final_outputs_newmodel'

#hemisphere_file = r'J:\Danielle Paynter\slice_rotations.csv'

#hemi_df = pd.read_csv(hemisphere_file)

def closest_point(point, points):
    """ Find closest point from a list of points. """
    pts = points[cdist([point], points).argmin()]
    if cdist([point], points).argmin() > 2:
        return None
    else:
        return pts
def match_value(df, col1, x, col2):
    """ Match value x from col1 row to value in col2. """
    return df[df[col1] == x][col2].values[0]

# Find the paths to CSVs


nutil_file_list = []
class_file_list = []
print ("starting")
for root, dirs, files in os.walk(nutil_dir):
    for name in files:
        if '_Objects' in name and '_All' not in name:
            nutil_file_list.append(os.path.join(root, name))
print ("going")
            
for root, dirs, files in os.walk(class_dir):
    for name in files:
        if 'classification' in name:
            class_file_list.append(os.path.join(root, name))

print("zero")

# Import the CSVs

nutil_csv_list = []
class_csv_list = []

for csv in nutil_file_list:
    n_csv = pd.read_csv(csv, sep=';').dropna(axis='columns', how='all')
    name = csv.split(sep='\\')[-1]
    name = name.replace("_Objects__s", "_s")
    name = name.replace(".csv", "")
    n_csv["Slice_plane"] = name
    nutil_csv_list.append(n_csv)

print("one")

for csv in class_file_list:
    class_csv_list.append(pd.read_csv(csv).dropna(axis='columns', how='all'))

# Make the coords integers    
print("two")

for i, df in enumerate(class_csv_list):
    try:
        class_csv_list[i].Y = class_csv_list[i].Y.round(0).astype(int)
        class_csv_list[i].X = class_csv_list[i].X.round(0).astype(int)
    except:
        pass

for i, df in enumerate(nutil_csv_list):
    nutil_csv_list[i] = df.rename(columns={'Center X': 'X', 'Center Y': 'Y', 'Region Name': 'Region'})
 #   nutil_csv_list[i].Y = nutil_csv_list[i].Y.round(0).astype(int)
   # nutil_csv_list[i].X = nutil_csv_list[i].X.round(0).astype(int)

print("3")

# Merge them
for i1, df in enumerate(nutil_csv_list):
    if len(df.index) > 0:
        matchy = nutil_csv_list[i1]["Slice_plane"].unique()[0]

        for i2, df in enumerate(class_csv_list):
            try:
                mtchy = class_csv_list[i2]["Slice_plane"].unique()[0].replace('DP_220718F_slice2_Region 1_Merged_z', '0718F_2_s').replace('.tif', '')
                
                if matchy == mtchy and not os.path.exists(os.path.join(output_dir, matchy + "_final.csv")):
                    print("Matched planes {}".format(matchy))
                    slyce = matchy.split(sep='_s')[0]
                    df1 = class_csv_list[i2]
                    df2 = nutil_csv_list[i1]
                    df1['point'] = [(x, y) for x,y in zip(df1['X'], df1['Y'])]
                    df2['point'] = [(x, y) for x,y in zip(df2['X'], df2['Y'])]
                    list1 = np.array(df1["point"])
                    list2 = np.array(df2["point"])
                    list1 = [list(ele) for ele in list1]
                    list2 = [list(ele) for ele in list2]
                    # Build a k-d tree for the second list of coordinates
                    kdtree = KDTree(list2)
                    # Set the maximum distance
                    max_distance = 2.0
                    # Find the closest point in list2 for each point in list1
                    matches = []
                    count = 0
                    for point in list1:
                        dist, idx = kdtree.query(point)
                        closest_point_output = list2[idx]
                        # Check the distance and exclude points that exceed the maximum distance
                        if dist <= max_distance:
                            matches.append((point, closest_point_output))
                            count +=1
                    print("slice {}: {} matches".format(matchy, count))
                  # Use the matches list to get rows for a good dataframe
                    new_df = pd.DataFrame(columns=["Slice_plane", "X", "Y", "Class", "Region"])
                    for i, match in enumerate(matches): 
                        df1_pt = match[0]
                        df2_pt = match[1]
                        cla = list(df1.loc[df1['point'] == tuple(df1_pt)]["Class"])[0]
                        reg = list(df2.loc[df2['point'] == tuple(df2_pt)]["Region"])[0]
                        x = df1_pt[0]
                        y = df1_pt[1]
                        new_row = [matchy, x, y, cla, reg]
                        new_df.loc[len(new_df)] = new_row
                    new_df.to_csv(os.path.join(output_dir, matchy + "_final.csv"))
                    print("slice {}: {} matches".format(matchy, count))
                    print('test')
                    if count == 0:
                        print("no cells for {}".format(matchy))
            except:
                pass
            
