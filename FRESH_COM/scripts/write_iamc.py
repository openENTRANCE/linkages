# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 17:39:14 2023

@author: perger
"""
import pandas as pd 
import nomenclature as nc

filename_output = 'output_FRESHCOM.xlsx'

# Define function 

def write_IAMC(output_df, model, scenario, region, variable, unit, time, values):
    
    _df=pd.DataFrame({'model': model,
                  'scenario': scenario,
                  'region': region,
                  'variable': variable,
                  'unit': unit,
                  'time': time,
                  'value': values})
    output_df = output_df.append(_df)
    return output_df

output_df = pd.DataFrame()
model = 'FRESH:COM v2.0'
scenario = 'openENTRANCE_CS2_Societal_Commitment'
region = 'Austria'
variable = 'Final Energy|Residential and Commercial|Electricity'
unit = 'MWh'
values = 10
time = 2019

output_IAMC = write_IAMC(output_df, model, scenario, region, 
                         variable, unit, time, values)
# write to excel file
output_IAMC.to_excel(filename_output, index=None)
# validate nomenclature
nc.validate(filename_output)