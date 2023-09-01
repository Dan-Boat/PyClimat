# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 09:00:22 2023

@author: dboateng
"""

# import modules 
import os
import numpy as np
import pandas as pd 
import xarray as xr
import matplotlib.pyplot as plt 
import netCDF4 as nc 
import glob
from datetime import datetime

# set paths 

main_path_to_data = "D:/Datasets/OCO2/Data/"
glob_name = "oco2_LtCO2_15*.nc4"

# function to detect the number of files to load

def count_files_in_directory(path_to_data, glob_pattern="*.nc4"):
    files = glob.glob(path_to_data + "/" + glob_pattern)
    print(len(files))
    return files


# function to convert the nc file to csv

def conv_date(d):
    return datetime.strptime(str(d), '%Y%m%d%H%M%S%f')

def convHdf(path_file, frames_folder):
    data = nc.Dataset(path_file)

    df_xco2 = pd.DataFrame({
        'Xco2': data.variables['xco2'][:],
        'Latitude': data.variables['latitude'][:],
        'Longitude': data.variables['longitude'][:],
        'quality_flag': data.variables['xco2_quality_flag'][:],
        'DateTime': [conv_date(d) for d in data.variables['sounding_id'][:]],
    })

    df_xco2['DateTime'] = pd.to_datetime(df_xco2['DateTime'])
    df_xco2['Year'] = df_xco2['DateTime'].dt.year
    df_xco2['Month'] = df_xco2['DateTime'].dt.month
    df_xco2['Day'] = df_xco2['DateTime'].dt.day

    df_xco2 = df_xco2[df_xco2['quality_flag'] == 0]

    date = str(data.variables['sounding_id'][0])
    output_file = os.path.join(frames_folder, f'_xco2_{date}_.csv')
    df_xco2.to_csv(output_file, index=False)




if __name__=="__main__":
    files = count_files_in_directory(main_path_to_data, glob_name)
    for file in files:
        convHdf(path_file=file, frames_folder=os.path.join(main_path_to_data, "csv_files"))
        
    
    