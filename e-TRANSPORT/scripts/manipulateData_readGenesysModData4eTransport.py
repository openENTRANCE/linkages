# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 10:30:40 2020

read eTransport data and 
convert to pickle for faster handling in python

do handling in other scripts
read back in and write back to excel

@author: sarahs
"""


def manipulate():
    
    import pandas as pd
    import pyam 
    
    def download():
        pyam.iiasa.Connection('openentrance')
        # read from database    
        # select model, scenario, regions
        #! Adjust as soon as GENeSYS-MOD data available
        data_IAMC = pyam.read_iiasa(
            'openentrance',
            model = 'GENeSYS-MOD 2.9.0-oe', 
            scenario = 'Directed Transition 1.0',
            region ="Norway"
            )
        # covert data to pandas dataframe
        data = data_IAMC.as_pandas()
    
        return data
            
    #project folder
    path_et = "C:/Users/sarahs/Desktop/sintef/OE - local/case study 6/"
    path_et_adj = "C:/Users/sarahs/Desktop/sintef/OE - local/case study 6/adj/"
    filename_timestep_conc = "time_step_conc.xlsx"
    
    # STEP 1 - read data
    
    #read data from eTransport (from pickle) 
    data_et = pd.read_pickle(path_et +"./eTrans_Furuset.pkl")
    
    #read teim step concordance 
    conc_ts = pd.read_excel(path_et + filename_timestep_conc)
    conc_ts['eT'] = conc_ts['eT'].astype('str')
    
    # download data from scenario explorer = se
    data_se = download()
    
    #to do: include this in the download function
    #select data from sc 
    # we need the demand profil 
    el_profil = data_se.loc[data_se['variable'] =="Final Energy|Electricity|Profile"]
    
    #tmp - use GUSTOS
    el_profil =  pd.read_excel(path_et +'el_profil.xlsx')
    
    
    
    # fix etrans data
    #extract var that we want to have
    data_tmp = data_et.loc[data_et['ATTRID'] == "El_load"]
    data_tmp1 = data_tmp.copy()
    
    #divide DESCRIPTION column in two
    data_tmp1['Object_'] = data_tmp1['DESCRIPTION'].str.split(',').str[0]
    data_tmp1['Time_step'] = data_tmp1['DESCRIPTION'].str.split(',').str[1]
    data_tmp1['Object_'] = data_tmp1['Object_'].replace({'Object::':''}, regex=True)
    data_tmp1['Time_step'] = data_tmp1['Time_step'].replace({' Time step::':''}, regex=True)
    
    data_tmp1['Time_step'] = data_tmp1['Time_step'].astype('str')
    data_tmp1['Object_'] = data_tmp1['Object_'].astype('str')
    
    #test for 2 time steps and 2 objects
    objects_et = ['s8','b2']
    
    for t in conc_ts['eT'].values:   
        ts_se = conc_ts.loc[conc_ts.eT == t, 'se']
        value_se = el_profil.loc[el_profil.subannual == ts_se.iloc[0], 'value' ] 
        for o in objects_et:
            data_tmp1.loc[(data_tmp1.Time_step == t) & (data_tmp1.Object_ == o), 'VAL' ] = value_se.iloc[0]
    
    
    #put back into data_et .. orig eTransport file
    data_et.loc[data_tmp1.index.to_list(), 'VAL'] = data_tmp1.VAL
    
    
    
    
    data_final = data_et
    
    #dump data to pickle 
    data_final.to_pickle(path_et_adj + "./eTrans_Furuset_adj.pkl")
