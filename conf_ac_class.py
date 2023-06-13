# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 15:45:16 2022

@author: dpaynter
"""

import pandas as pd
import xmltodict
import os
import cv2
from PIL import Image

#path_to_tifs = r'I:\Danielle Paynter\TTT_2022\data\raw\stitched_confocal_tifs\DP_220730G\DP_220730G_slice3'

class conf_ac(object):
    """Class that holds a single confocal acquisition from TTT2022 experiments.
    path_to_tifs should point to a folder with Metadata, and one tif per
    channel per plane of a given 'lif' file."""

    def __init__( self, path_to_tifs ) :
        self.path_to_tifs = path_to_tifs
        self.mouse = path_to_tifs.split("\\")[-2]
        try:
            logo_jpg = os.path.join(path_to_tifs, "Metadata", "LeicaLogo.jpg")
        except:
            pass
        metadata_files = os.listdir(os.path.join(path_to_tifs, "Metadata"))
        if os.path.isfile(logo_jpg):
            os.remove(logo_jpg)
        #find metadata files
        #with open(os.path.join(path_to_tifs,"Metadata",metadata_files[1]),'r', encoding='utf-8') as file:
        with open(os.path.join(path_to_tifs,"Metadata",metadata_files[0]),'r') as file:

            my_xml = file.read()
        self.dic = xmltodict.parse(my_xml)
        self.df = pd.DataFrame.from_dict(self.dic["Data"]["Image"]["ImageDescription"]["Channels"]["ChannelDescription"])
        self.fluo_list = list(self.df["@LUTName"])
        
        #try:
        #    self.num_zplanes = self.dic["Data"]["Image"]["Attachment"][3]["ATLConfocalSettingDefinition"]["@Sections"]
        #except:
        #    self.num_zplanes = self.dic["Data"]["Image"]["Attachment"][4]["ATLConfocalSettingDefinition"]["@Sections"]
            
       # try:
        #    self.zoom = round(float(self.dic["Data"]["Image"]["Attachment"][3]["ATLConfocalSettingDefinition"]["@Zoom"]),2)
        #except:
        #    self.zoom = round(float(self.dic["Data"]["Image"]["Attachment"][4]["ATLConfocalSettingDefinition"]["@Zoom"]),2)
            
        #try:
        #    self.objective = self.dic["Data"]["Image"]["Attachment"][3]["ATLConfocalSettingDefinition"]["@ObjectiveName"]
        #except:
        #    self.objective = self.dic["Data"]["Image"]["Attachment"][4]["ATLConfocalSettingDefinition"]["@ObjectiveName"]
       
        #try:
        #    self.scope = self.dic["Data"]["Image"]["Attachment"][3]["@SystemTypeName"]
        #except:
            #self.scope = self.dic["Data"]["Image"]["Attachment"][4]["@SystemTypeName"]
        ## Assign fluorophores to channels:
        if self.fluo_list.count("Gray") == 2:
            self.fluo_list[1] = "Cyan"
        
        if "Gray" in self.fluo_list:
            self.DAPI_idx = self.fluo_list.index("Gray")
            self.fluo_list[self.DAPI_idx] = "DAPI"
        if "Cyan" in self.fluo_list:
            self.mTurq_idx = self.fluo_list.index("Cyan")
            self.fluo_list[self.mTurq_idx] = "mTurq"
        if "Blue" in self.fluo_list:
            self.mTurq_idx = self.fluo_list.index("Blue")
            self.fluo_list[self.mTurq_idx] = "mTurq"
        self.GFP_idx = self.fluo_list.index("Green")
        self.fluo_list[self.GFP_idx] = "GFP"

        self.TOM_idx = self.fluo_list.index("Red")
        self.fluo_list[self.TOM_idx] = "TOM"
        try: 
            self.ch00 = self.fluo_list[0]
            self.ch01 = self.fluo_list[1]
            self.ch02 = self.fluo_list[2]
            self.ch03 = self.fluo_list[3]
        except:
            pass
            
        self.fluo_dict = dict()
        
        try:
            self.fluo_dict['DAPI'] = self.DAPI_idx
        except:
            pass
        try:
            self.fluo_dict['mTurq'] = self.mTurq_idx
        except:
            pass
        try:
            self.fluo_dict['GFP'] = self.GFP_idx
        except:
            pass
        try:
            self.fluo_dict['TOM'] = self.TOM_idx
        except:
            pass
        
    def convert_to_gray(self, chan):
        # for DAPI image in the folder, change format to JPEG
        ims = []
        chan_path = self.path_to_tifs+"\\ch0" + str(self.fluo_dict[chan])
        tifs = os.listdir(chan_path)
        for it, im in enumerate(tifs):
            if "ch0"+str(self.fluo_dict[chan]) in tifs[it]:
                ims.append(im)
        for im in ims:
            file_path = '{}/{}'.format(chan_path, im)
            img = Image.open(file_path).convert('L')
            img.save(file_path)
                
    def convert_to_jpeg(self, chan):
        # for DAPI image in the folder, change format to JPEG
        ims = []
        chan_path = self.path_to_tifs+"\\ch0" + str(self.fluo_dict[chan])
        save_path = chan_path.replace('raw','interim\\registration')
        os.makedirs(save_path, exist_ok=True)
        tifs = os.listdir(chan_path)
        for it, im in enumerate(tifs):
            if "ch0"+str(self.fluo_dict[chan]) in tifs[it]:
                ims.append(im)
        for im in ims:
            tif_path = '{}\\{}'.format(chan_path, im)
            newname = '{}\\{}.jpg'.format(save_path, im)
            output = os.rename(tif_path, newname)
    
    def dwnsmpl_jpgs(self, chan, new_width_pixels):
        new_width = int(new_width_pixels)
        chan_path = self.path_to_tifs.replace('raw', 'interim\\registration') +"\\ch0" + str(self.fluo_dict[chan])
        for im in os.listdir(chan_path):
            if ".jpg" in im:
                im_path = '{}/{}'.format(chan_path, im)
                src = cv2.imread(im_path)
                w = src.shape[1]
                h = src.shape[0]
                new_w = new_width
                new_h = int(new_width*h/w)
                dsize = (new_w, new_h)
                output = cv2.resize(src, dsize)
                cv2.imwrite(im_path, output)
                

                
                
                
        
        