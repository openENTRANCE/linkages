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

#pyam.iiasa.set_config(<username>, <password>)



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
filename_read_EP = 'SAMRES.h5'
filename_write_EP_mean = 'EMPSW_elprices_mean.xlsx'
filename_write_EP_min = 'EMPSW_elprices_min.xlsx'
filename_write_EP_max = 'EMPSW_elprices_max.xlsx'
#fn_conc_reg = 'concordance_regDatasetHydroCen_reg5price.xlsx'
fn_conc_reg = 'concordance_regDatasetHydroCen_regIAMC.xlsx'

file_toread = EMPSW_path/filename_read_EP



    
# standart headers for output format
headers_col = ['model', 'scenario', 'region', 'variable', 'unit', 'subannual', 'value']
headers_col = ['model', 'scenario', 'region', 'variable', 'unit', 'time', 'value']


model = "EMPS-W v1.0"
scenario = "test 1"
region = "tmp"
variable = "Price|Final Energy|Residential|Electricity"
unit = "EURO/GJ" #öre/kWh
subannual = "tmp"
data_ = 0

headers_rows = [model,scenario, region,variable,unit, subannual,data_]
d_labs = {'model': model, 'scenario': scenario, 'region': region, 'variable': variable, 'unit': unit, 'time':subannual, 'value': data_}

df_labs = pd.DataFrame(data = d_labs, index = ['a'])



# - parameters
layer1_ = "market_results"
layer2_ = "price"
layer3_ = "val"




#read region names from concordance
conc_reg = pd.read_excel(EMPSWtoOpenPlatform_path / fn_conc_reg, header = 0, index_col = 0)

# the output regions should be the 5 power regions of norway
#conc_reg_in = pd.read_excel(EMPSWtoOpenPlatform_path / fn_conc_reg, header = [0,1], index_col = 0)
# TMP!!! normalize while no proxy decided
#conc_reg = conc_reg_in / np.matlib.repmat(sum(conc_reg_in.values),11,1)


regions_EMPSW = conc_reg.index
nbr_regionsEMPSW = len(regions_EMPSW)
#regions_price = conc_reg.columns.levels[1]
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

# add costs for grid
#ca. 2000 NOK = 200000 öre per year
grid_cost_1 = 20000/len(dts)  #yearly fee per time step 
grid_cost_2 = 20 #in 2020 20 öre per kWh
grid_cost = grid_cost_1 + grid_cost_2

content_h5_no_gridCosts = content_h5_no_raw + grid_cost


#convert öre/kWh to US$2010/GJ

# -> average NOK to US$2010 0,1657
c = CurrencyConverter()
a = c.convert(100, 'NOK', 'EUR')
#.:ore zu euro -> öre zu kronor 0,01
# -> GJ (1kWh = 0,0036 GJ)
content_h5_no = content_h5_no_gridCosts/0.0036*0.001



# we want to deliver 3 output excel files:
# mean, max, min value (from simulation years)
mean_price = np.mean(content_h5_no, axis = 1)
mean_price = mean_price.transpose()
min_price =  np.min(content_h5_no, axis = 1)
min_price = min_price.transpose()
max_price =  np.max(content_h5_no, axis = 1) 
max_price = max_price.transpose()


# if other region class than orig
# mean_price_formatted = mean_price.dot(conc_reg).flatten()
# min_price_formatted = min_price.dot(conc_reg).flatten()
# max_price_formatted = max_price.dot(conc_reg).flatten()



#convert to time-series for every hour
mean_price_h = pd.DataFrame()
min_price_h = pd.DataFrame()
max_price_h = pd.DataFrame()

for r in range(0,11):
    mean_price_h[r]  = np.transpose(np.matlib.repmat(mean_price[:,r],3,1)).flatten()
    min_price_h[r]  = np.transpose(np.matlib.repmat(min_price[:,r],3,1)).flatten()
    max_price_h[r]  = np.transpose(np.matlib.repmat(max_price[:,r],3,1)).flatten()
    

mean_price_formatted = mean_price_h.to_numpy().flatten()
min_price_formatted = min_price_h.to_numpy().flatten()
max_price_formatted = max_price_h.to_numpy().flatten()


#STEP 3 - create dataframe for print: 

#make row lables accoring to standart
df_labs_repeated_tmp = pd.concat([df_labs]*nbr_regions_price, ignore_index=True)
df_labs_repeated_tmp.region = regions_price
df_labs_repeated = pd.concat([df_labs_repeated_tmp]*len(timesteps), ignore_index=True)
df_labs_repeated.time = dts_rep



#create 3 final dataframes with price data and print to excel
df_mean = df_labs_repeated
df_mean.value = mean_price_formatted
df_mean = df_mean.rename(columns = {"value":2030}) 
df_mean = df_mean.rename(columns = {"value":"value"}) 
df_mean.scenario = "test 1 mean" 
df_mean.to_excel(EMPSWtoOpenPlatform_path / filename_write_EP_mean, index = False)


df_max = df_labs_repeated
df_max.value = max_price_formatted
df_max = df_max.rename(columns = {"value":2050}) 
df_max = df_max.rename(columns = {"value":"value"}) 
df_max.scenario = "test 1 max" 
df_max.to_excel(EMPSWtoOpenPlatform_path / filename_write_EP_max, index = False)


df_min = df_labs_repeated
df_min.value = min_price_formatted
df_min = df_min.rename(columns = {"value":2050}) 
df_min = df_min.rename(columns = {"value":"value"}) 
df_min.scenario = "test 1 min" 
df_min.to_excel(EMPSWtoOpenPlatform_path / filename_write_EP_min, index = False)


# validate data
# run __init__.py
# then validate(df_min)

tst
    

