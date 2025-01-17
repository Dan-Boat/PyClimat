# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 15:30:34 2023

@author: dboateng
1. Calculate the lapse rate across the Alps for the control experiments
"""

# import models
import os 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import xarray as xr
import matplotlib.colors as col
import matplotlib as mpl 
from cartopy.util import add_cyclic_point
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import cartopy.crs as ccrs


# import pyClimat models 
from pyClimat.plot_utils import *
from pyClimat.plots import scatter_plot_laspe_rate
from pyClimat.data import read_ECHAM_processed
from pyClimat.analysis import extract_var, compute_lterm_mean, extract_transect, linregression


path_to_data = "D:/Datasets/Model_output_pst"
path_to_plots = "C:/Users/dboateng/Desktop/Python_scripts/ClimatPackage_repogit/examples/Alps/Miocene/plots"


# read data

CTL_filename = "a002_hpc-bw_e5w2.3_t159_PI_Alps_east_100_t159l31.6h"
W1E1_278_filename = "a015_hpc-bw_e5w2.3_t159_MIO_W1E1_278ppm_t159l31.6h"
W1E1_450_filename = "a014_hpc-bw_e5w2.3_t159_MIO_W1E1_450ppm_t159l31.6h"

W2E1_PI_filename = "a009_hpc-bw_e5w2.3_t159_PI_AW200E100_t159l31.6h"
W2E1_Mio278_filename = "a017_hpc-bw_e5w2.3_t159_MIO_W2E1_278ppm_t159l31.6h"
W2E1_Mio450_filename = "a016_hpc-bw_e5w2.3_t159_MIO_W2E1_450ppm_t159l31.6h"

W2E0_PI_filename="a010_hpc-bw_e5w2.3_t159_PI_AW200E0_t159l31.6h"
W2E0_Mio278_filename="a019_hpc-bw_e5w2.3_t159_MIO_W2E0_278ppm_t159l31.6h"
W2E0_Mio450_filename="a018_hpc-bw_e5w2.3_t159_MIO_W2E0_450ppm_t159l31.6h"

W2E2_PI_filename="t017_hpc-bw_e5w2.3_PI_Alps150_t159l31.6h"
W2E2_Mio278_filename="a020_dkrz-levante_e5w2.3_t159_MIO_W2E2_278ppm_t159l31.6h"
W2E2_Mio450_filename="a021_dkrz-levante_e5w2.3_t159_MIO_W2E2_450ppm_t159l31.6h"

years = "1003_1017"

years_not_complete="1003_1010"


period = "1m"

CTL_data, CTL_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=CTL_filename, years=years, 
                                          period=period, read_wiso=True)

W1E1_278_data, W1E1_278_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W1E1_278_filename, years=years, 
                                          period=period, read_wiso=True)

W1E1_450_data, W1E1_450_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W1E1_450_filename, years=years, 
                                          period=period, read_wiso=True)


W2E1_PI_data, W2E1_PI_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W2E1_PI_filename, years=years, 
                                          period=period, read_wiso=True)

W2E1_278_data, W2E1_278_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W2E1_Mio278_filename, years=years, 
                                          period=period, read_wiso=True)

W2E1_450_data, W2E1_450_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W2E1_Mio450_filename, years=years, 
                                          period=period, read_wiso=True)

W2E0_PI_data, W2E0_PI_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W2E0_PI_filename, years=years, 
                                          period=period, read_wiso=True)

W2E0_278_data, W2E0_278_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W2E0_Mio278_filename, 
                                                    years=years_not_complete, period=period, read_wiso=True)

W2E0_450_data, W2E0_450_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W2E0_Mio450_filename, years=years, 
                                          period=period, read_wiso=True)


W2E2_PI_data, W2E2_PI_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W2E2_PI_filename, years=years, 
                                          period=period, read_wiso=True)

W2E2_278_data, W2E2_278_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W2E2_Mio278_filename, 
                                                    years=years, period=period, read_wiso=True)

W2E2_450_data, W2E2_450_wiso = read_ECHAM_processed(main_path=path_to_data, exp_name=W2E2_Mio450_filename, years=years, 
                                          period=period, read_wiso=True)



def extract_relevant_vars_sections(data, wiso):

    d18op = extract_var(Dataset=data , varname="d18op", units="per mil", Dataset_wiso= wiso)
    elev = extract_var(Dataset=data , varname="elev", units="m")

    # compute annual means
    d18op_alt = compute_lterm_mean(data=d18op, time="annual")
    elev_alt = compute_lterm_mean(data=elev, time="annual")
    
    maxlat_west, minlat_west, maxlon_west, minlon_west = 47, 44, 8, 1
    maxlat_south, minlat_south, maxlon_south, minlon_south = 47, 43, 15, 7.5
    maxlat_north, minlat_north, maxlon_north, minlon_north = 50, 46.5, 16, 5
    
    elev_north = extract_transect(data=elev_alt, maxlon=maxlon_north, minlon=minlon_north , 
                                  maxlat=maxlat_north , minlat=minlat_north , sea_land_mask=True, 
                                  Dataset=data)
    
    elev_south = extract_transect(data=elev_alt, maxlon=maxlon_south, minlon=minlon_south, 
                                  maxlat=maxlat_south, minlat=minlat_south, sea_land_mask=True, 
                                  Dataset=data)
    
    
    elev_west = extract_transect(data=elev_alt, maxlon=maxlon_west, minlon=minlon_west, 
                                  maxlat=maxlat_west, minlat=minlat_west, sea_land_mask=True, 
                                  Dataset=data)
    
    
    d18op_north = extract_transect(data=d18op_alt, maxlon=maxlon_north, minlon=minlon_north , 
                                  maxlat=maxlat_north , minlat=minlat_north , sea_land_mask=True, 
                                  Dataset=data)
    
    d18op_south = extract_transect(data=d18op_alt, maxlon=maxlon_south, minlon=minlon_south, 
                                  maxlat=maxlat_south, minlat=minlat_south, sea_land_mask=True, 
                                  Dataset=data)
    
    
    d18op_west = extract_transect(data=d18op_alt, maxlon=maxlon_west, minlon=minlon_west, 
                                  maxlat=maxlat_west, minlat=minlat_west, sea_land_mask=True, 
                                  Dataset=data)
   
   
    west_reg, west_df = linregression(data_x=elev_west, data_y=d18op_west, return_yhat=True)
    north_reg, north_df = linregression(data_x=elev_north, data_y=d18op_north, return_yhat=True)
    south_reg, south_df = linregression(data_x=elev_south, data_y=d18op_south, return_yhat=True)
    
    
    
    return north_reg, north_df, south_reg, south_df, west_reg, west_df





#plot 

apply_style(fontsize=22, style=None, linewidth=2)

def plot_lape_rate_per_section():
    
    
    
    CTL_reg_north, CTL_df_north, CTL_reg_south, CTL_df_south, CTL_reg_west, CTL_df_west = extract_relevant_vars_sections(data=CTL_data, wiso=CTL_wiso)
    W1E1_278_reg_north, W1E1_278_df_north, W1E1_278_reg_south, W1E1_278_df_south, W1E1_278_reg_west, W1E1_278_df_west = extract_relevant_vars_sections(data=W1E1_278_data, wiso=W1E1_278_wiso)
    W1E1_450_reg_north, W1E1_450_df_north, W1E1_450_reg_south, W1E1_450_df_south, W1E1_450_reg_west, W1E1_450_df_west = extract_relevant_vars_sections(data=W1E1_450_data, wiso=W1E1_450_wiso)
    
    W2E1_reg_north, W2E1_df_north, W2E1_reg_south, W2E1_df_south, W2E1_reg_west, W2E1_df_west = extract_relevant_vars_sections(data=W2E1_PI_data, wiso=W2E1_PI_wiso)
    W2E1_278_reg_north, W2E1_278_df_north, W2E1_278_reg_south, W2E1_278_df_south, W2E1_278_reg_west, W2E1_278_df_west = extract_relevant_vars_sections(data=W2E1_278_data, wiso=W2E1_278_wiso)
    W2E1_450_reg_north, W2E1_450_df_north, W2E1_450_reg_south, W2E1_450_df_south, W2E1_450_reg_west, W2E1_450_df_west = extract_relevant_vars_sections(data=W2E1_450_data, wiso=W2E1_450_wiso)
    
    W2E0_reg_north, W2E0_df_north, W2E0_reg_south, W2E0_df_south, W2E0_reg_west, W2E0_df_west = extract_relevant_vars_sections(data=W2E0_PI_data, wiso=W2E0_PI_wiso)
    W2E0_278_reg_north, W2E0_278_df_north, W2E0_278_reg_south, W2E0_278_df_south, W2E0_278_reg_west, W2E0_278_df_west = extract_relevant_vars_sections(data=W2E0_278_data, wiso=W2E0_278_wiso)
    W2E0_450_reg_north, W2E0_450_df_north, W2E0_450_reg_south, W2E0_450_df_south, W2E0_450_reg_west, W2E0_450_df_west = extract_relevant_vars_sections(data=W2E0_450_data, wiso=W2E0_450_wiso)
    
    W2E2_reg_north, W2E2_df_north, W2E2_reg_south, W2E2_df_south, W2E2_reg_west, W2E2_df_west = extract_relevant_vars_sections(data=W2E2_PI_data, wiso=W2E2_PI_wiso)
    W2E2_278_reg_north, W2E2_278_df_north, W2E2_278_reg_south, W2E2_278_df_south, W2E2_278_reg_west, W2E2_278_df_west = extract_relevant_vars_sections(data=W2E2_278_data, wiso=W2E2_278_wiso)
    W2E2_450_reg_north, W2E2_450_df_north, W2E2_450_reg_south, W2E2_450_df_south, W2E2_450_reg_west, W2E2_450_df_west = extract_relevant_vars_sections(data=W2E2_450_data, wiso=W2E2_450_wiso)
    
    

    fig, ((ax1,ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9), 
          (ax10, ax11, ax12)) = plt.subplots(nrows = 4, ncols = 3, figsize=(25, 28))
    
    #ax1 (west)
    axes = [ax1,ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12]
    
    scatter_plot_laspe_rate(ax=ax1, reg_params= CTL_reg_west , df_x_y_yhat=CTL_df_west , color=black, marker= "*", label= "PI",
                           title="West (W1E1)", xmax=1500, xmin=0,
                            ymax=-4, ymin= -12, bottom_labels=True)
    scatter_plot_laspe_rate(ax=ax1, reg_params= W1E1_278_reg_west , df_x_y_yhat=W1E1_278_df_west , color=red, marker= "D", label= "MIO 278ppm",
                           bottom_labels=True)
    scatter_plot_laspe_rate(ax=ax1, reg_params= W1E1_450_reg_west , df_x_y_yhat=W1E1_450_df_west , color=green, marker= "^", label= "MIO 450ppm",
                           bottom_labels=True)
    
    
    #ax2 (north)
    scatter_plot_laspe_rate(ax=ax2, reg_params= CTL_reg_north , df_x_y_yhat=CTL_df_north , color=black, marker= "*", label= "PI",
                            left_labels=False, xmax=1500, xmin=0, title= "North (W1E1)",
                             ymax=-4, ymin= -12,)
    scatter_plot_laspe_rate(ax=ax2, reg_params= W1E1_278_reg_north , df_x_y_yhat=W1E1_278_df_north , color=red, marker= "D", label= "MIO 278ppm",
                            left_labels=False)
    
    scatter_plot_laspe_rate(ax=ax2, reg_params= W1E1_450_reg_north , df_x_y_yhat=W1E1_450_df_north , color=green, marker= "^", label= "MIO 450ppm",
                            left_labels=False)

    
    #ax3 (south)
    scatter_plot_laspe_rate(ax=ax3, reg_params= CTL_reg_south , df_x_y_yhat=CTL_df_south , color=black, marker= "*", label= "PI",
                            left_labels=False, xmax=1500, xmin=0, title= "South (W1E1)",
                             ymax=-4, ymin= -12, add_label=True)
    scatter_plot_laspe_rate(ax=ax3, reg_params= W1E1_278_reg_south , df_x_y_yhat=W1E1_278_df_south , color=red, marker= "^", label= "MIO 278ppm",
                           left_labels=False, add_label=True)
    scatter_plot_laspe_rate(ax=ax3, reg_params= W1E1_450_reg_south, df_x_y_yhat=W1E1_450_df_south, color=green, marker= "D", label= "MIO 450ppm",
                           left_labels=False, add_label=True)
    

    
    scatter_plot_laspe_rate(ax=ax4, reg_params= W2E1_reg_west , df_x_y_yhat=W2E1_df_west , color=black, marker= "*", label= "W2E1 (PI)",
                           title="West (W2E1)", xmax=4000, xmin=0,
                            ymax=-4, ymin= -20, bottom_labels=True)
    scatter_plot_laspe_rate(ax=ax4, reg_params= W2E1_278_reg_west , df_x_y_yhat=W2E1_278_df_west , color=red, marker= "D", label= "W2E1 (MIO 278ppm)",
                           bottom_labels=True)
    scatter_plot_laspe_rate(ax=ax4, reg_params= W2E1_450_reg_west , df_x_y_yhat=W2E1_450_df_west , color=green, marker= "^", label= "W2E1 (MIO 450ppm)",
                           bottom_labels=True)
    
    
    #ax2 (north)
    scatter_plot_laspe_rate(ax=ax5, reg_params= W2E1_reg_north , df_x_y_yhat=W2E1_df_north , color=black, marker= "*", label= "W2E1 (PI)",
                            left_labels=False, xmax=4000, xmin=0, title= "North (W2E1)",
                             ymax=-4, ymin= -20,)
    scatter_plot_laspe_rate(ax=ax5, reg_params= W2E1_278_reg_north , df_x_y_yhat=W2E1_278_df_north , color=red, marker= "D", label= "W2E1 (MIO 278ppm)",
                            left_labels=False)
    
    scatter_plot_laspe_rate(ax=ax5, reg_params= W2E1_450_reg_north , df_x_y_yhat=W2E1_450_df_north , color=green, marker= "^", label= "W2E1 (MIO 450ppm)",
                            left_labels=False)
    
    #ax3 (south)
    scatter_plot_laspe_rate(ax=ax6, reg_params= W2E1_reg_south , df_x_y_yhat=W2E1_df_south , color=black, marker= "*", label= "W2E1 (PI)",
                            left_labels=False, xmax=4000, xmin=0, title= "South (W2E1)",
                             ymax=-4, ymin= -20, add_label=False)
    scatter_plot_laspe_rate(ax=ax6, reg_params= W2E1_278_reg_south , df_x_y_yhat=W2E1_278_df_south , color=red, marker= "^", label= "W2E1 (MIO 278ppm)",
                           left_labels=False, add_label=False)
    scatter_plot_laspe_rate(ax=ax6, reg_params= W2E1_450_reg_south, df_x_y_yhat=W2E1_450_df_south, color=green, marker= "D", label= "W2E1 (MIO 450ppm)",
                           left_labels=False, add_label=False)
    


    
    scatter_plot_laspe_rate(ax=ax7, reg_params= W2E0_reg_west , df_x_y_yhat=W2E0_df_west , color=black, marker= "*", label= "W2E0 (PI)",
                           title="West (W2E0)", xmax=4000, xmin=0,
                            ymax=-4, ymin= -20, bottom_labels=True)
    scatter_plot_laspe_rate(ax=ax7, reg_params= W2E0_278_reg_west , df_x_y_yhat=W2E0_278_df_west , color=red, marker= "D", label= "W2E0 (MIO 278ppm)",
                           bottom_labels=True)
    scatter_plot_laspe_rate(ax=ax7, reg_params= W2E0_450_reg_west , df_x_y_yhat=W2E0_450_df_west , color=green, marker= "^", label= "W2E0 (MIO 450ppm)",
                           bottom_labels=True)

    
    
    #ax2 (north)
    scatter_plot_laspe_rate(ax=ax8, reg_params= W2E0_reg_north , df_x_y_yhat=W2E0_df_north , color=black, marker= "*", label= "W2E0 (PI)",
                            left_labels=False, xmax=4000, xmin=0, title= "North (W2E0)",
                             ymax=-4, ymin= -20,)
    scatter_plot_laspe_rate(ax=ax8, reg_params= W2E0_278_reg_north , df_x_y_yhat=W2E0_278_df_north , color=red, marker= "D", label= "W2E0 (MIO 278ppm)",
                            left_labels=False)
    
    scatter_plot_laspe_rate(ax=ax8, reg_params= W2E0_450_reg_north , df_x_y_yhat=W2E0_450_df_north , color=green, marker= "^", label= "W2E0 (MIO 450ppm)",
                            left_labels=False)
   
    #ax3 (south)
    scatter_plot_laspe_rate(ax=ax9, reg_params= W2E0_reg_south , df_x_y_yhat=W2E0_df_south , color=black, marker= "*", label= "W2E0 (PI)",
                            left_labels=False, xmax=4000, xmin=0, title= "South (W2E0)",
                             ymax=-4, ymin= -20, add_label=False)
    scatter_plot_laspe_rate(ax=ax9, reg_params= W2E0_278_reg_south , df_x_y_yhat=W2E0_278_df_south , color=red, marker= "^", label= "W2E0 (MIO 278ppm)",
                           left_labels=False, add_label=False)
    scatter_plot_laspe_rate(ax=ax9, reg_params= W2E0_450_reg_south, df_x_y_yhat=W2E0_450_df_south, color=green, marker= "D", label= "W2E0 (MIO 450ppm)",
                           left_labels=False, add_label=False)
    
    
    scatter_plot_laspe_rate(ax=ax10, reg_params= W2E2_reg_west , df_x_y_yhat=W2E2_df_west , color=black, marker= "*", label= "W2E2 (PI)",
                           title="West (W2E2)", xmax=4000, xmin=0,
                            ymax=-4, ymin= -20, bottom_labels=True)
    scatter_plot_laspe_rate(ax=ax10, reg_params= W2E2_278_reg_west , df_x_y_yhat=W2E2_278_df_west , color=red, marker= "D", label= "W2E2 (MIO 278ppm)",
                           bottom_labels=True)
    scatter_plot_laspe_rate(ax=ax10, reg_params= W2E2_450_reg_west , df_x_y_yhat=W2E2_450_df_west , color=green, marker= "^", label= "W2E2 (MIO 450ppm)",
                           bottom_labels=True)

    
    
    #ax2 (north)
    scatter_plot_laspe_rate(ax=ax11, reg_params= W2E2_reg_north , df_x_y_yhat=W2E2_df_north , color=black, marker= "*", label= "W2E2 (PI)",
                            left_labels=False, xmax=4000, xmin=0, title= "North (W2E2)",
                             ymax=-4, ymin= -20,)
    scatter_plot_laspe_rate(ax=ax11, reg_params= W2E2_278_reg_north , df_x_y_yhat=W2E2_278_df_north , color=red, marker= "D", label= "W2E2 (MIO 278ppm)",
                            left_labels=False)
    
    scatter_plot_laspe_rate(ax=ax11, reg_params= W2E2_450_reg_north , df_x_y_yhat=W2E2_450_df_north , color=green, marker= "^", label= "W2E2 (MIO 450ppm)",
                            left_labels=False)
    
    #ax3 (south)
    scatter_plot_laspe_rate(ax=ax12, reg_params= W2E2_reg_south , df_x_y_yhat=W2E2_df_south , color=black, marker= "*", label= "W2E2 (PI)",
                            left_labels=False, xmax=4000, xmin=0, title= "South (W2E2)",
                             ymax=-4, ymin= -20, add_label=False)
    scatter_plot_laspe_rate(ax=ax12, reg_params= W2E2_278_reg_south , df_x_y_yhat=W2E2_278_df_south , color=red, marker= "^", label= "W2E2 (MIO 278ppm)",
                           left_labels=False, add_label=False)
    scatter_plot_laspe_rate(ax=ax12, reg_params= W2E2_450_reg_south, df_x_y_yhat=W2E2_450_df_south, color=green, marker= "D", label= "W2E2 (MIO 450ppm)",
                           left_labels=False, add_label=False)
    
    for ax in axes:
        ax.set_box_aspect(1)
        ax.legend(frameon=True, fontsize=20, loc="upper left", framealpha=0.5, ncol=1)
        ax.grid(visible=False)
    
    plt.tight_layout()
    plt.subplots_adjust(left=0.15, right=0.88, top=0.97, bottom=0.05, wspace=0.01)
    plt.savefig(os.path.join(path_to_plots, "lapse_rate_pi_mio.svg"), format= "svg", bbox_inches="tight", dpi=600)
    
    
 
    
if __name__ == '__main__':

    plot_lape_rate_per_section()                                                                                                                           