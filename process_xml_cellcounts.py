# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 17:36:35 2022

Functions to work with XML cell count files from FIJI.

@author: dpaynter
"""
import pandas as pd
import xmltodict
xml_path = r'I:\Danielle Paynter\TTT_2022\data\interim\TTT_counts\CellCounter_DP_220729C_slice6_reg1_MH_recount.xml'
#xml_path = r'I:\Danielle Paynter\TTT_2022\data\processed\TTT_counts\CellCounter_competition_section_CL.xml'
def get_cellcounts(xml_path):

    """Function to return GFP, both, and TOM counts from the xml outputs from 
    FIJI's cell counter. xml_path should be the whole xml file location and name. 
    Example:r'I:\Danielle Paynter\TTT_2022\data\processed\TTT_counts\CellCount
    er_DP_220718A_slice2_reg1_CL.xml'"""
    
    # Open the file and read the contents
    with open(xml_path,'r', encoding='utf-8') as file:
        my_xml = file.read()
      
    # Use xmltodict to parse and convert the XML document
    my_dict = xmltodict.parse(my_xml)
    cellfile = my_dict['CellCounter_Marker_File']
    #properties = cellfile['Image_Properties']
    markerdata = cellfile['Marker_Data']
    m = markerdata['Marker_Type']
    GFP_test = m[0]['Name']
    both_test = m[1]['Name']
    TOM_test = m[2]['Name']
    GFP = m[0]
    try:
        GFP_markers = GFP['Marker']
    except:
        print('No GFP cells counted')
        GFP_markers = [[]]
    both = m[1]
    both_markers = both['Marker']
    TOM = m[2]
    try:
        TOM_markers = TOM['Marker']
    except:
        print('No TOM cells counted')
        TOM_markers = []
    # _markers are lists of dictionaries
    
    df_GFP = pd.DataFrame(GFP_markers)
    df_both = pd.DataFrame(both_markers)
    df_TOM = pd.DataFrame([TOM_markers])
    
    print(GFP_test, both_test, TOM_test)
    # Get numbers of cells in each category:
    return(len(df_GFP),len(df_both),len(df_TOM))

def get_counter(xml_path):
    # Print out who counted the slice:
    return xml_path.split("_")[-1].replace('.xml','')
    
def get_region(xml_path):
    return xml_path.split("_")[-2]

def prop_gfp(counts):
    """Takes the output from 'get_cellcounts' (a tuple)"""
    return counts[0]/sum(counts)

def get_im_properties(xml_path):
    # Open the file and read the contents
    with open(xml_path,'r', encoding='utf-8') as file:
        my_xml = file.read()
      
    # Use xmltodict to parse and convert the XML document
    my_dict = xmltodict.parse(my_xml)
    cellfile = my_dict['CellCounter_Marker_File']
    return cellfile['Image_Properties']

def get_xyz_gfp(xml_path):
# Open the file and read the contents
    gfp_points = []
    with open(xml_path,'r', encoding='utf-8') as file:
        my_xml = file.read()
      
    # Use xmltodict to parse and convert the XML document
    my_dict = xmltodict.parse(my_xml)
    cellfile = my_dict['CellCounter_Marker_File']
    markers_gfp = cellfile['Marker_Data']['Marker_Type'][0]['Marker']
    for marker in markers_gfp:
        gfp_points.append((marker['MarkerX'],marker['MarkerY'],marker['MarkerZ']))
    return gfp_points

def get_xyz_both(xml_path):
# Open the file and read the contents
    both_points = []
    with open(xml_path,'r', encoding='utf-8') as file:
        my_xml = file.read()
      
    # Use xmltodict to parse and convert the XML document
    my_dict = xmltodict.parse(my_xml)
    cellfile = my_dict['CellCounter_Marker_File']
    markers_both = cellfile['Marker_Data']['Marker_Type'][1]['Marker']
    for marker in markers_both:
        both_points.append((marker['MarkerX'],marker['MarkerY'],marker['MarkerZ']))
    return both_points
     
def get_xyz_tom(xml_path):
# Open the file and read the contents
    tom_points = []
    with open(xml_path,'r', encoding='utf-8') as file:
        my_xml = file.read()
      
    # Use xmltodict to parse and convert the XML document
    my_dict = xmltodict.parse(my_xml)
    cellfile = my_dict['CellCounter_Marker_File']
    markers_tom = cellfile['Marker_Data']['Marker_Type'][2]['Marker']
    for marker in markers_tom:
        tom_points.append((marker['MarkerX'],marker['MarkerY'],marker['MarkerZ']))
    return tom_points