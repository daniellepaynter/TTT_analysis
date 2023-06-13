# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 15:52:04 2023

Import a model and PNGs, export x, y, classification for each plane.

@author: dpaynter
"""

import tensorflow as tf
import keras
from skimage.io import imread, imsave
import numpy as np
import os
import matplotlib.pyplot as plt
import shutil
import pandas as pd

model_path = r'C:\Users\dpaynter\Documents\Python Scripts\rv_tf\model_nulldendrites20_2023_04_26'
model = keras.models.load_model(model_path)
class_names = ["gfp","both","tom","null"]

png_paths = r'J:\Danielle Paynter\PNGs_to_classify\NotDoneYet'
png_im_paths = [ name for name in os.listdir(png_paths) if os.path.isdir(os.path.join(png_paths, name)) ]
class_dir = r'J:\Danielle Paynter\Class_outputs'


for png_path in png_im_paths:
    
    png_im_path = os.path.join(png_paths, png_path)
    print("Working on {}".format(png_path))

        
    # Loop through PNGs
    ims = os.listdir(png_im_path)
    ims = [im for im in ims if '.png' in im]
    df = pd.DataFrame(columns=['Slice_plane', 'X', 'Y', 'Class'])
    
    for im in ims:
        slyce = im.split(sep='_y')[0]

  #      if os.path.exists(os.path.join(png_im_path, slyce + "_classification.csv")):
     #       pass
      
        path = os.path.join(png_im_path, im)
        try:
            image = tf.keras.preprocessing.image.load_img(path)
            input_arr = tf.keras.preprocessing.image.img_to_array(image)
            input_arr = np.array([input_arr])  # Convert single image to a batch.
        
            predictions = model.predict(input_arr)
        
            tf.keras.preprocessing.image.load_img(
            path, grayscale=False, color_mode="rgb", target_size=(34,34), interpolation="nearest"
            )
        
            pred_index = predictions.argmax()
            pred = class_names[pred_index]
            
            # get x and y:
            split1 = im.split(sep='_s')
            slyce = im.split(sep='_y')[0]
            split2 = split1[1].split(sep='_')
            z = split2[0]
            y = split2[1].replace('y','')
            x = split2[2].replace('x','').replace('.png', '')
            
            new_row = [slyce, x, y, pred]
            df.loc[len(df)] = new_row    
        except:
            print('passed one')
    df.to_csv(os.path.join(class_dir, slyce + "_classification.csv"))
    
    old_dir = png_im_path
    new_dir = os.path.join(png_im_path.split(sep='\\NotDoneYet\\')[0], png_im_path.split(sep='\\NotDoneYet\\')[1])
    if os.path.isdir(new_dir):
        pass
    else:
        
    
        os.mkdir(new_dir)
        shutil.move(old_dir, new_dir)