# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 21:03:36 2020

@author: sarahs
"""
import pyam 
import numpy as np
import h5py


def write_h5(data_el, fname):
    with h5py.File(str(fname), 'a') as f:
        if 'el_demand' in f:
            del f['el_demand']
        f.create_group('el_demand')
        f['el_demand'].create_dataset('values', data=data_el)
        f['el_demand'].attrs['measurement_unit'] = 'MW'
        # if 'result_description' in f:
        #     del f['result_description']
        # f.create_group('result_description')
        # HydroAreaData = f['result_description'].create_dataset('TestData', shape=(1,), dtype=np.dtype([("OMRNAVN", h5py.special_dtype(vlen=str)), ("IVERK", np.int32),
        #                                                                ("NPUMP", np.int32), ("NMOD", np.int32)]))
        # HydroAreaData[0] = ('TEST', 1, 0, 50)



folder = 'C:/Users/sarahs/Desktop/sintef/OE - local/case study 3/EMPS_W/Datasett/HydroCen_LowEmission_V10'
filename = 'Dellast_data.h5'  # this needs to be changed later to timeseries_data.h5
fname_ = "\\".join([folder, filename])



# read from database
# select model, scenario
pyam.iiasa.Connection('openentrance')
df = pyam.read_iiasa(
    'openentrance',
    model = 'HEROSCARS v1.0'
    )
# covert data to pandas dataframe
allData_gusto = df.as_pandas()

# we need only the demand profil 
el_profil = allData_gusto.loc[allData_gusto['variable'] =="Final Energy|Electricity|Profile"]

#extract all region that there is data for: 
regions = el_profil['region'].unique()
region_names_spain = regions #change that
region_names_norway = regions #change that

#extract the relevant data for the two cases (Spain and Norway)
el_profil_spain = el_profil.loc[el_profil['region'].isin(region_names_spain)]
el_profil_No = el_profil.loc[el_profil['region'].isin(region_names_norway)] 

#test with one region
el_profil = el_profil.loc[el_profil['region'] == "ES112"]

#convert from MW to MWh/h - (not necessary)


# here we need different "EMPS" sceanrios (9 to match the nine yeasr of spanish hydro data and ca. 50 for norway)
data_tmp = el_profil.value.to_numpy()

#write to EMPS
write_h5(data_tmp, fname_)
