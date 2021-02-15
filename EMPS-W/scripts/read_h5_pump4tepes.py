# -*- coding: utf-8 -*-
"""
read from .h5 and convert to excel 
- formatted for the open platform
@author: sarahs
"""

from pathlib import Path 
import numpy as np
import numpy.matlib
import pandas as pd
import h5py
import copy
import pyam
from datetime import datetime, timedelta

from currency_converter import CurrencyConverter




def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta



def read_h5_oneVAR(file_toread,layer1,layer2,layer3):
    f = h5py.File(file_toread, 'r')
    if len(layer3)==0:
        #values_tmp = pd.DataFrame(f[layer1][layer2])
        values_tmp = [x.decode() for x in f[layer1][layer2]]
    else:
        values_tmp = np.array(f[layer1][layer2][layer3])
    return values_tmp        
        
        

   
# ------------------ main code ------------------------------------


EMPSW_path = Path("C:/Users/sarahs/Desktop/sintef/OE - local/case study 3/EMPS_W/Datasett/HydroCen_LowEmission_V10/")
EMPSWtoOpenPlatform_path = Path("C:/Users/sarahs/Desktop/sintef/OE - local/linking2openPlatform/")

#EP = electricity prices
filename_read_PE = 'SAMRES.h5'
filename_write_PE_mean = 'EMPSW_pumpEnergy_mean.xlsx'
filename_write_PE_min = 'EMPSW_pumpEnergy_min.xlsx'
filename_write_PE_max = 'EMPSW_pumpEnergy_max.xlsx'
fn_conc_reg = 'concordance_regDatasetHydroCen_regIAMC.xlsx'

file_toread = EMPSW_path/filename_read_PE



   
# standart headers for output format
headers_col = ['model', 'scenario', 'region', 'variable', 'unit', 'subannual', 'value']
headers_col = ['model', 'scenario', 'region', 'variable', 'unit', 'time', 'value']


model = "EMPS-W v1.0"
scenario = "test 1"
region = "tmp"
variable = "Storage|Electricity|Hydro|Reservoir"
unit = "MWh" 
subannual = "tmp"
data_ = 0

headers_rows = [model,scenario, region,variable,unit, subannual,data_]
d_labs = {'model': model, 'scenario': scenario, 'region': region, 'variable': variable, 'unit': unit, 'time':subannual, 'value': data_}

df_labs = pd.DataFrame(data = d_labs, index = ['a'])



# - parameters
layer1_ = "hydro_results"
layer2_ = "reservoir"
layer3_ = "val"



#read region names from concordance
conc_reg = pd.read_excel(EMPSWtoOpenPlatform_path / fn_conc_reg, header = 0, index_col = 0)
regions_price = conc_reg.columns
nbr_regions_price = len(regions_price)


#create timestamps for the time steps
dts = [dt.strftime('%Y-%m-%d %H:%M +01:00') for dt in 
           datetime_range(datetime(2050,1, 1, 0), datetime(2050,12, 31, 0), 
           timedelta(hours=1))]
timesteps = list(range(0,len(dts)))

dts_rep = np.transpose(np.matlib.repmat(dts,nbr_regions_price,1)).flatten()


# read data from SAMRES.h5 file with dimensions:
# regions/nodes, simulation years, time steps
content_h5 = read_h5_oneVAR(file_toread, layer1_, layer2_,layer3_)

#OBS: hard coded!! first 11 regions are Norway, so delete the rest
content_h5_no_raw = content_h5[:11,:]


#convert unit
#from GWh to MWh
content_h5_no = content_h5_no_raw*1000


# we want to deliver 3 output excel files:
# mean, max, min value (from simulation years)
mean_energy = np.mean(content_h5_no, axis = 1)
mean_energy = mean_energy.transpose()
min_energy =  np.min(content_h5_no, axis = 1)
min_energy = min_energy.transpose()
max_energy =  np.max(content_h5_no, axis = 1) 
max_energy = max_energy.transpose()


#convert to time-series for every hour
mean_energy_h = pd.DataFrame()
min_energy_h = pd.DataFrame()
max_energy_h = pd.DataFrame()

for r in range(0,11):
    mean_energy_h[r]  = np.transpose(np.matlib.repmat(mean_energy[:,r],7*24,1)).flatten()
    min_energy_h[r]  = np.transpose(np.matlib.repmat(min_energy[:,r],7*24,1)).flatten()
    max_energy_h[r]  = np.transpose(np.matlib.repmat(max_energy[:,r],7*24,1)).flatten()
    

mean_energy_formatted = mean_energy_h.to_numpy().flatten()
min_energy_formatted = min_energy_h.to_numpy().flatten()
max_energy_formatted = max_energy_h.to_numpy().flatten()



#STEP 3 - create dataframe for print: 

#make row lables accoring to standart
df_labs_repeated_tmp = pd.concat([df_labs]*nbr_regions_price, ignore_index=True)
df_labs_repeated_tmp.region = regions_price
df_labs_repeated = pd.concat([df_labs_repeated_tmp]*len(timesteps), ignore_index=True)
df_labs_repeated.time = dts_rep



#create 3 final dataframes with energy data and print to excel
df_mean = df_labs_repeated
df_mean.value = mean_energy_formatted
df_mean = df_mean.rename(columns = {"value":2030}) 
df_mean = df_mean.rename(columns = {"value":"value"}) 
df_mean.scenario = "test 1 mean" 
df_mean.to_excel(EMPSWtoOpenPlatform_path / filename_write_PE_mean, index = False)


df_max = df_labs_repeated
df_max.value = max_energy_formatted
df_max = df_max.rename(columns = {"value":2030}) 
df_max = df_max.rename(columns = {"value":"value"}) 
df_max.scenario = "test 1 max" 
df_max.to_excel(EMPSWtoOpenPlatform_path / filename_write_PE_max, index = False)


df_min = df_labs_repeated
df_min.value = min_energy_formatted
df_min = df_min.rename(columns = {"value":2030}) 
df_min = df_min.rename(columns = {"value":"value"}) 
df_min.scenario = "test 1 min" 
df_min.to_excel(EMPSWtoOpenPlatform_path / filename_write_PE_min, index = False)


# validate data
# run __init__.py
# then validate(df_min)


