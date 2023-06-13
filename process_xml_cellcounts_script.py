# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:52:33 2022

Process all cell count files in TTT_cellcounts folder.

@author: dpaynter
"""
import pandas as pd
import os
import process_xml_cellcounts as pxc
import seaborn as sns

folder = r'R:\Share\Danielle\TTT2022_countable_sections\Counts_Priority_single_planes'
xmls = os.listdir(folder)

gfps = []
boths = []
toms = []
df = pd.DataFrame(columns=['Mouse', 'slice', 'region_ID', 'gfp', 'both', 'tom', 'counter', 'uniqueID'])
for file in xmls:
   counts = pxc.get_cellcounts(os.path.join(folder,file))
   print(file, '\n', counts)
   gfps.append(counts[0]) 
   boths.append(counts[1]) 
   toms.append(counts[2]) 
   counter = file.split(sep='_')[-1].replace('.xml', '')
   mouse = file.split(sep='_')[1]
   slyce = file.split(sep='_')[2] + file.split(sep='_')[3]
   region_ID = file.split(sep='_')[-2]
   unique_ID = slyce + region_ID
   new_row = [mouse, slyce, region_ID, counts[0], counts[1], counts[2], counter, unique_ID]
   df.loc[len(df)] = new_row
#df = df.drop([1, 4, 18, 19, 21])

df['total'] = df["gfp"] + df["both"] + df["tom"]
df['perc_gfp'] = df["gfp"] / df["total"]
groups_mouse = df.groupby('Mouse')

#sns.catplot(data=df, x='counter', y='total')

reg_dic = {'reg1': 'viscor_l', 'reg2': 'viscor_r', 'reg3': 'lgn_l', 
           'reg4': 'thal_l', 'reg5': 'rsc_l', 'reg6': 'rsc_r', 
           'reg7': 'cortex_l', 'reg8': 'cortex_r'}
cond_dic = {'220718A': 'control', '220718B':'MD', '220718F': 'control',
            '220729A': 'control', '220729B':'MD', '220729C': 'MD',
            '220730D': 'MD', '220730E': 'control', '220730F': 'control',
            '220730G': 'control', '220730H':'MD', '220807C': 'control',
            '220807D': 'control', '220807G': 'control', '220807H':'MD',
            '220807I': 'MD'}

df['reg_name'] = df['region_ID'].map(reg_dic)
df['condition'] = df['Mouse'].map(cond_dic)

#sns.catplot(data=df, y='perc_gfp', x='reg_name', units='uniqueID', hue='condition')

vis_regs = ['viscor_l','viscor_r','lgn_l']
df_subsample = df[df.reg_name.isin(vis_regs)]
#sns.catplot(data=df_subsample, y='perc_gfp', x='reg_name', units='uniqueID', hue='condition')
df_manual = df.copy()