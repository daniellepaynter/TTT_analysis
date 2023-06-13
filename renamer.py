# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 15:24:09 2023

@author: dpaynter
"""
import os

filepath = r'J:\Danielle Paynter\Class_outputs'
ugh = []

slyces = os.listdir(filepath)
for slyce in slyces:
    
    if '.tif.h5' in slyce:
        print(slyce)
        oldname = os.path.join(filepath, slyce)
        newname = os.path.join(filepath, slyce.replace('.tif.h5', '.h5'))
    #    newname = newname.replace('.jpg', '_ch03.jpg')
     #   newname= oldname
        ugh.append(newname)
        os.replace(oldname, newname)
           
slyces = os.listdir(filepath)
for slyce in slyces:
    
    if '_cropped' not in slyce:
        print('cool')
        oldname = os.path.join(filepath, slyce)
        newname = os.path.join(filepath, slyce.replace('_3', '_3_cropped'))
      #  newname = newname.replace('.jpg', '_ch00.jpg')
     #   newname= oldname
        ugh.append(newname)
        os.replace(oldname, newname)
           
slyces = os.listdir(filepath)
for slyce in slyces:
    
    if '0730H_4_redo' in slyce:
        print('cool')
        oldname = os.path.join(filepath, slyce)
        newname = os.path.join(filepath, slyce.replace('0730H_4_redo', '0730H_4_redo_s'))
      #  newname = newname.replace('.jpg', '_ch00.jpg')
     #   newname= oldname
        ugh.append(newname)
        os.replace(oldname, newname)
           



    #########################################################################       

import os 
import shutil


class_dir = r'J:\Danielle Paynter\PNGs_to_classify\NotDoneYet'
dir_of_classifications = r'J:\Danielle Paynter\Class_outputs'


for root, dirs, files in os.walk(class_dir):
    for name in files:
        if 'redo' in name:
            print(name)
            oldname = os.path.join(root, name)
            newname = os.path.join(root, name.replace('redo', 'redo_s'))
          #  newname = newname.replace('.tif', '')
            shutil.move(oldname, newname)

            #shutil.move(oldpath, newpath)
            
plane = 45
source = r'J:\Danielle Paynter\PNGs_to_classify\NotDoneYet\0730H_4_redo{}\0730H_4_redo{}'.format(plane, plane)
dest = r'J:\Danielle Paynter\PNGs_to_classify\NotDoneYet\0730H_4_redo{}'.format(plane)
files = os.listdir(source)
for file in files:
    file_name = os.path.join(source, file)
    shutil.move(file_name, dest)
print("Files Moved")

import os

root = r'J:\Danielle Paynter\PNGs_to_classify\NotDoneYet'
folders = list(os.walk(root))[1:]

for folder in folders:
    # folder example: ('FOLDER/3', [], ['file'])
    if not folder[2]:
        os.rmdir(folder[0])
          
import os

filepath = r'F:\iLastik\new\DP_220807C_slice3'
ugh = []
slyces = os.listdir(filepath)
for slyce in slyces:
    spath = os.path.join(filepath, slyce)
    files = os.listdir(spath)
    for file in files:
        if '_Region 3' in file:
            oldname = os.path.join(spath, file)
            newname = oldname.replace('_Region 3', '')
            ugh.append(newname)
            
            os.rename(oldname, newname)




import os
import sys
import fileinput
fileToSearch  = r'J:\Danielle Paynter\DeepSlice_regi\DP_220718F_slice4_redo\ch00'
dontwant = 'merged'
dowant = 's'
tempFile = open( fileToSearch, 'r+' )
for line in fileinput.input( fileToSearch ):
    if dontwant in line :
        print('Match Found')
    else:
        print('Match Not Found!!')
    tempFile.write( line.replace( dontwant, dowant ) )
tempFile.close()