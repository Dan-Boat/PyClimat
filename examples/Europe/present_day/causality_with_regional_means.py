# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:29:45 2023

@author: dboateng
"""

import os
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator
import matplotlib.dates as mdates

from pyClimat.plot_utils import *
from pyClimat.plots import plot_eofsAsCovariance
from pyClimat.stats import sliding_correlation, StatCorr, GrangerCausality
from pyClimat.data import read_ERA_processed, read_from_path
from pyClimat.analysis import extract_var, extract_transect
from pyClimat.utils import extract_region


from paths_to_data import *
echam_pd_data_path = "D:/Datasets/Model_output_pst/PD"
ERA5_path = "C:/Users/dboateng/Desktop/Datasets/ERA5/monthly_1950_2021"
        
        
# read all the required datsets (for winter)
df_era_pcs = pd.read_csv(PCs_ERA_DJF_path , parse_dates=["time"])
df_echam_pcs = pd.read_csv(PCs_ECHAM_DJF_path, parse_dates=["time"])

#select the node ands convert to xarray

nao_index_era = xr.DataArray(df_era_pcs[str(1)] * -1, dims="time", coords={"time": df_era_pcs["time"]})
nao_index_echam = xr.DataArray(df_echam_pcs[str(1)] *-1, dims="time", coords={"time": df_echam_pcs["time"]})


ea_index_era = xr.DataArray(df_era_pcs[str(3)], dims="time", coords={"time": df_era_pcs["time"]})
ea_index_echam = xr.DataArray(df_echam_pcs[str(2)], dims="time", coords={"time": df_echam_pcs["time"]})

scan_index_era = xr.DataArray(df_era_pcs[str(2)], dims="time", coords={"time": df_era_pcs["time"]})
scan_index_echam = xr.DataArray(df_echam_pcs[str(3)] *-1, dims="time", coords={"time": df_echam_pcs["time"]})




def perform_causality_testing_with_regional_means(maxlon, minlon, maxlat, minlat, Y_varname=None,
                                                  Y_units=None, Z_units=None, Z_varname=None, X_varname=None,
                                                  X_units=None,):
    
    echam_data = read_from_path(echam_pd_data_path, "PD_1980_2014_monthly.nc", decode=True)   
    echam_wiso = read_from_path(echam_pd_data_path, "PD_1980_2014_monthly_wiso.nc", decode=True)
    
    if Y_varname =="NAO":
        data_Y = nao_index_echam
        
    elif Y_varname == "EA":
        data_Y = ea_index_echam
    else:
        data_Y = extract_var(Dataset=echam_data, varname=Y_varname, units=Y_units, Dataset_wiso=echam_wiso,
                           )
        data_Y = extract_region(data=data_Y, maxlon=maxlon, minlon=minlon, maxlat=maxlat, minlat=minlat, time="season", 
                                     season="DJF", regional_mean=True)
        
    if X_varname =="NAO":
        data_X = nao_index_echam
    else:
        data_X = extract_var(Dataset=echam_data, varname=X_varname, units=X_units, Dataset_wiso=echam_wiso,
                           )
        data_X = extract_region(data=data_X, maxlon=maxlon, minlon=minlon, maxlat=maxlat, minlat=minlat, time="season", 
                                     season="DJF", regional_mean=True)
        
    if Z_varname =="NAO":
        data_Z = nao_index_echam
    elif Z_varname == "EA":
        data_Z = ea_index_echam
    else:
        data_Z = extract_var(Dataset=echam_data, varname=Z_varname, units=Z_units, Dataset_wiso=echam_wiso,
                           )
        data_Z = extract_region(data=data_Z, maxlon=maxlon, minlon=minlon, maxlat=maxlat, minlat=minlat, time="season", 
                                     season="DJF", regional_mean=True)
    
    
    Granger_object = GrangerCausality(maxlag=18, test="params_ftest")
    
    
    
    pval = Granger_object.perform_granger_test(X=data_X, Y=data_Y, Z=data_Z, 
                                                       apply_standardize=True)
    
    return pval
  


def perform_for_all_regions(Y_varname=None, Y_units=None, Z_units=None, Z_varname=None, X_varname=None, 
                            X_units=None):
    
    column_names = ["IP", "FR", "ALPS", "MED", "EE", "SCAND", "CE", "BI", "ICE"]
    df = pd.DataFrame(columns=column_names, index=np.arange(1))
    
    
    df["IP"] = perform_causality_testing_with_regional_means(maxlon=3, minlon=-11, maxlat=44, minlat=36,
                                                             Y_varname=Y_varname, Y_units=Y_units, Z_units=Z_units, 
                                                             Z_varname=Z_varname, X_varname=X_varname, 
                                                                                         X_units=X_units)
    
    df["FR"] = perform_causality_testing_with_regional_means(maxlon=6.5, minlon=-5.5, maxlat=50, minlat=44,
                                                             Y_varname=Y_varname, Y_units=Y_units, Z_units=Z_units, 
                                                             Z_varname=Z_varname, X_varname=X_varname, 
                                                                                         X_units=X_units)
    
    
    df["ALPS"] = perform_causality_testing_with_regional_means(maxlon=17, minlon=5, maxlat=48, minlat=45,
                                                             Y_varname=Y_varname, Y_units=Y_units, Z_units=Z_units, 
                                                             Z_varname=Z_varname, X_varname=X_varname, 
                                                                                         X_units=X_units)
    
    
    df["MED"] = perform_causality_testing_with_regional_means(maxlon=26, minlon=2.5, maxlat=44, minlat=36,
                                                             Y_varname=Y_varname, Y_units=Y_units, Z_units=Z_units, 
                                                             Z_varname=Z_varname, X_varname=X_varname, 
                                                                                         X_units=X_units)
    
    df["EE"] = perform_causality_testing_with_regional_means(maxlon=32, minlon=18, maxlat=55, minlat=46,
                                                             Y_varname=Y_varname, Y_units=Y_units, Z_units=Z_units, 
                                                             Z_varname=Z_varname, X_varname=X_varname, 
                                                                                         X_units=X_units)
    
    df["SCAND"] = perform_causality_testing_with_regional_means(maxlon=34, minlon=1, maxlat=67, minlat=55,
                                                             Y_varname=Y_varname, Y_units=Y_units, Z_units=Z_units, 
                                                             Z_varname=Z_varname, X_varname=X_varname, 
                                                                                         X_units=X_units)
    
    df["CE"] = perform_causality_testing_with_regional_means(maxlon=16, minlon=3, maxlat=54, minlat=48,
                                                             Y_varname=Y_varname, Y_units=Y_units, Z_units=Z_units, 
                                                             Z_varname=Z_varname, X_varname=X_varname, 
                                                                                         X_units=X_units)
    
    df["BI"] = perform_causality_testing_with_regional_means(maxlon=2, minlon=-14, maxlat=59, minlat=51,
                                                             Y_varname=Y_varname, Y_units=Y_units, Z_units=Z_units, 
                                                             Z_varname=Z_varname, X_varname=X_varname, 
                                                                                         X_units=X_units)
    
    df["ICE"] = perform_causality_testing_with_regional_means(maxlon=-11, minlon=-30, maxlat=67, minlat=61,
                                                             Y_varname=Y_varname, Y_units=Y_units, Z_units=Z_units, 
                                                             Z_varname=Z_varname, X_varname=X_varname, 
                                                                                         X_units=X_units)
    
    return df
    
    
    
def plot_causal_to_d18op():    
    pval_t2m_prec_to_d18op = perform_for_all_regions(Z_varname="temp2", Z_units="°C", Y_varname="prec", 
                                                                Y_units="mm/month", X_varname="d18op", X_units="per mil",
                                                               )
    
    pval_nao_ea_to_d18op = perform_for_all_regions(Z_varname="EA", Z_units=None, Y_varname="NAO", 
                                                                Y_units=None, X_varname="d18op", X_units="per mil",
                                                               )
    
    pval_t2m_nao_to_d18op = perform_for_all_regions(Y_varname="prec", Y_units="mm/month", Z_varname="temp2", 
                                                                Z_units="°C", X_varname="NAO", X_units=None,
                                                               )
    
    apply_style(fontsize=23, style="seaborn-talk", linewidth=3,)
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, sharey=True, figsize=(20, 15), sharex=True)
    
    pval_t2m_prec_to_d18op.iloc[0].plot(kind="barh", ax=ax1)
    pval_nao_ea_to_d18op.iloc[0].plot(kind="barh", ax=ax2)
    pval_t2m_nao_to_d18op.iloc[0].plot(kind="barh", ax=ax3)
    
    axes = [ax1, ax2, ax3]
    titles = ["(a) Y(t2m, Prec) to X($\delta^{18}$Op)", "(b) Y(NAO, EA) to X($\delta^{18}$Op)",  
              "(c) Y(t2m, NAO) to X($\delta^{18}$Op)"]
    
    for i, ax in enumerate(axes):
        ax.set_title(titles[i], fontdict= {"fontsize": 22, "fontweight":"bold"}, loc="left")
        ax.axvline(x=0.1, linestyle="-", color="red")
        ax.axvline(x=0.33, linestyle="-", color="blue")
        ax.axvline(x=0.66, linestyle="-", color="magenta")
        
    plt.savefig(os.path.join(path_to_plots, "causal_regional_means_d18op.svg"), format= "svg", 
                bbox_inches="tight", dpi=300)


def plot_causal_to_nao():
    pval_t2m_prec_to_nao = perform_for_all_regions(Z_varname="temp2", Z_units="°C", Y_varname="prec", 
                                                                Y_units="mm/month", X_varname="NAO", X_units=None,
                                                               )
    
    pval_d18op_t2m_to_nao = perform_for_all_regions(Z_varname="d18op", Z_units="per mil", Y_varname="temp2", 
                                                                Y_units="°C", X_varname="NAO", X_units=None,
                                                               )
    
    pval_d18op_prec_to_nao = perform_for_all_regions(Z_varname="prec", Z_units="mm/month", Y_varname="d18op", 
                                                                Y_units="per mil", X_varname="NAO", X_units=None,
                                                               )
    
    apply_style(fontsize=23, style="seaborn-talk", linewidth=3,)
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, sharey=True, figsize=(20, 15), sharex=True)
    
    pval_t2m_prec_to_nao.iloc[0].plot(kind="barh", ax=ax1)
    pval_d18op_t2m_to_nao.iloc[0].plot(kind="barh", ax=ax2)
    pval_d18op_prec_to_nao.iloc[0].plot(kind="barh", ax=ax3)
    
    axes = [ax1, ax2, ax3]
    titles = ["(a) Y(t2m, Prec) to X(NAO)", "(b) Y($\delta^{18}$Op, t2m) to X(NAO)",  
              "(c) Y($\delta^{18}$Op, Prec) to X(NAO)"]
    
    for i, ax in enumerate(axes):
        ax.set_title(titles[i], fontdict= {"fontsize": 22, "fontweight":"bold"}, loc="left")
        ax.axvline(x=0.1, linestyle="-", color="red")
        ax.axvline(x=0.33, linestyle="-", color="blue")
        ax.axvline(x=0.66, linestyle="-", color="magenta")
        
    plt.savefig(os.path.join(path_to_plots, "causal_regional_means_nao.svg"), format= "svg", 
                bbox_inches="tight", dpi=300)
    
    
def plot_causal_EA_to_nao():
    pval_t2m_ea_to_nao = perform_for_all_regions(Y_varname="temp2", Y_units="°C", Z_varname="EA", 
                                                                Z_units=None, X_varname="NAO", X_units=None,
                                                               )
    
    pval_prec_ea_to_nao = perform_for_all_regions(Y_varname="prec", Y_units="mm/month", Z_varname="EA", 
                                                                Z_units=None, X_varname="NAO", X_units=None,
                                                               )
    
    pval_d18op_ea_to_nao = perform_for_all_regions(Y_varname="d18op", Y_units="per mil", Z_varname="EA", 
                                                                Z_units=None, X_varname="NAO", X_units=None,
                                                               )
    
    apply_style(fontsize=23, style="seaborn-talk", linewidth=3,)
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, sharey=True, figsize=(20, 15), sharex=True)
    
    pval_t2m_ea_to_nao.iloc[0].plot(kind="barh", ax=ax1)
    pval_prec_ea_to_nao.iloc[0].plot(kind="barh", ax=ax2)
    pval_d18op_ea_to_nao.iloc[0].plot(kind="barh", ax=ax3)
    
    axes = [ax1, ax2, ax3]
    titles = ["(a) Y(t2m, EA) to X(NAO)", "(b) Y(Prec, EA) to X(NAO)",  
              "(c) Y($\delta^{18}$Op, EA) to X(NAO)"]
    
    for i, ax in enumerate(axes):
        ax.set_title(titles[i], fontdict= {"fontsize": 22, "fontweight":"bold"}, loc="left")
        ax.axvline(x=0.1, linestyle="-", color="red")
        ax.axvline(x=0.33, linestyle="-", color="blue")
        ax.axvline(x=0.66, linestyle="-", color="magenta")
        
    plt.savefig(os.path.join(path_to_plots, "causal_regional_means_ea_climate_to_nao.svg"), format= "svg", 
                bbox_inches="tight", dpi=300)
    
    
def plot_causal_to_climate():
    pval_nao_ea_to_prec = perform_for_all_regions(Z_varname="EA", Z_units=None, Y_varname="NAO", 
                                                                Y_units=None, X_varname="prec", X_units="mm/month",
                                                               )
    
    pval_nao_ea_to_t2m = perform_for_all_regions(Z_varname="EA", Z_units=None, Y_varname="NAO", 
                                                                Y_units=None, X_varname="temp2", X_units="°C",
                                                               )
    
    pval_nao_ea_to_d18op = perform_for_all_regions(Z_varname="EA", Z_units=None, Y_varname="NAO", 
                                                                Y_units=None, X_varname="d18op", X_units="per mil",
                                                               )
    
    apply_style(fontsize=23, style="seaborn-talk", linewidth=3,)
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, sharey=True, figsize=(20, 15), sharex=True)
    
    pval_nao_ea_to_prec.iloc[0].plot(kind="barh", ax=ax1)
    pval_nao_ea_to_t2m.iloc[0].plot(kind="barh", ax=ax2)
    pval_nao_ea_to_d18op.iloc[0].plot(kind="barh", ax=ax3)
    
    axes = [ax1, ax2, ax3]
    titles = ["(a) Y(NAO, EA) to X(Prec)", "(b)  Y(NAO, EA) to X(t2m)",  
              "(c)  Y(NAO, EA) to X($\delta^{18}$Op)"]
    
    for i, ax in enumerate(axes):
        ax.set_title(titles[i], fontdict= {"fontsize": 22, "fontweight":"bold"}, loc="left")
        ax.axvline(x=0.1, linestyle="-", color="red")
        ax.axvline(x=0.33, linestyle="-", color="blue")
        ax.axvline(x=0.66, linestyle="-", color="magenta")
        
    plt.savefig(os.path.join(path_to_plots, "causal_regional_means_nao_ea_to_climate.svg"), format= "svg", 
                bbox_inches="tight", dpi=300)



plot_causal_EA_to_nao()