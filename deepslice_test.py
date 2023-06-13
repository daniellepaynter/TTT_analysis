# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 13:36:35 2023

First try of DeepSlice

@author: dpaynter
"""

from DeepSlice import DSModel
species = 'mouse'

Model = DSModel(species)
folderpath = r'J:\Danielle Paynter\DeepSlice_regi\DP_220807D_slice3'
Model.predict(folderpath, ensemble=True, section_numbers=True)    
Model.propagate_angles()                     
Model.enforce_index_order()    
Model.enforce_index_spacing(section_thickness = None)
savepath = folderpath + '\DS_output'
Model.save_predictions(savepath)

Model = DSModel(species)
folderpath = r'J:\Danielle Paynter\DeepSlice_regi\DP_220730D_slice8\ch00'
Model.predict(folderpath, ensemble=True, section_numbers=True)    
Model.propagate_angles()                     
Model.enforce_index_order()    
Model.enforce_index_spacing(section_thickness = None)
savepath = folderpath + '\DS_output'
Model.save_predictions(savepath)

Model = DSModel(species)
folderpath = r'J:\Danielle Paynter\DeepSlice_regi\DP_220730E_slice5\ch03'
Model.predict(folderpath, ensemble=True, section_numbers=True)    
Model.propagate_angles()                     
Model.enforce_index_order()    
Model.enforce_index_spacing(section_thickness = None)
savepath = folderpath + '\DS_output'
Model.save_predictions(savepath)


