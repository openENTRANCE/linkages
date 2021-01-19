import genesysmod_to_iamc.data_reader as dr
import pandas as pd
import pyam
import logging

from genesysmod_to_iamc._statics import *


def generate_idataframe(data_wrapper, filter_only_yearly_values=False):
    logging.info('Executing: generate_idataframe')
    frames = []

    for frame in data_wrapper.transformed_data:
        frames.append(data_wrapper.transformed_data[frame])

    values = pd.concat(frames)
    idataframe = pyam.IamDataFrame(values)

    idataframe.aggregate(variable='Primary Energy', append=True, recursive=False)
    idataframe.aggregate(variable='Primary Energy|Non-Biomass Renewables',
                         components=['Primary Energy|Solar'
                             , 'Primary Energy|Wind'
                             , 'Primary Energy|Ocean'
                             , 'Primary Energy|Geothermal'
                             , 'Primary Energy|Hydro'], append=True, recursive=False)
    idataframe.aggregate_region(variable='Primary Energy|*', append=True)

    idataframe.aggregate(variable='Final Energy|Industry|Liquids', append=True, recursive=False)
    idataframe.aggregate(variable='Final Energy|Industry|Solids', append=True, recursive=False)
    idataframe.aggregate(variable='Final Energy|Industry', append=True, recursive=False)
    idataframe.aggregate(variable='Final Energy|Residential and Commercial|Liquids', append=True, recursive=False)
    idataframe.aggregate(variable='Final Energy|Residential and Commercial|Solids', append=True, recursive=False)
    idataframe.aggregate(variable='Final Energy|Residential and Commercial', append=True, recursive=False)
    idataframe.aggregate(variable='Final Energy|Transportation|Liquids', append=True, recursive=False)
    idataframe.aggregate(variable='Final Energy|Transportation', append=True, recursive=False)

    idataframe.aggregate(variable='Final Energy|Electricity',
                         components=['Final Energy|Residential and Commercial|Electricity'
                             , 'Final Energy|Industry|Electricity'
                             , 'Final Energy|Transportation|Electricity'
                             , 'Final Energy|ElectricityDummy'], append=True, recursive=False)

    idataframe.aggregate(variable='Final Energy|Electricity|Heat',
                         components=['Final Energy|Residential and Commercial|Electricity'
                             , 'Final Energy|Industry|Electricity'], append=True, recursive=False)

    idataframe.aggregate(variable='Final Energy|Electricity|Transportation',
                         components=['Final Energy|Transportation|Electricity'], append=True, recursive=False)

    idataframe.aggregate(variable='Final Energy|Electricity|Other (excl. Heat, Cooling, Transport)',
                         components=['Final Energy|ElectricityDummy'], append=True, recursive=False)

    idataframe.aggregate(variable='Final Energy',
                         components=['Final Energy|Residential and Commercial'
                             , 'Final Energy|Industry'
                             , 'Final Energy|Transportation'
                             , 'Final Energy|ElectricityDummy'], append=True, recursive=False)

    idataframe.data = changeFinalEnergyToGWh(idataframe.data, 'Final Energy|Electricity|Transportation')
    idataframe.data = changeFinalEnergyToGWh(idataframe.data, 'Final Energy|Electricity|Other (excl. Heat, Cooling, Transport)')
    idataframe.data = changeFinalEnergyToGWh(idataframe.data, 'Final Energy|Electricity|Heat')

    idataframe.data = idataframe.data[idataframe.data['variable'] != 'Final Energy|ElectricityDummy']

    idataframe.aggregate_region(variable='Final Energy|*', append=True)

    idataframe.aggregate(variable='Capacity|Electricity|Biomass', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Coal', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Gas|CCGT', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Gas', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Solar', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Wind', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Hydro', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Heat|Residential and Commercial|Electricity', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Heat|Residential and Commercial', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Heat|Industrial', append=True, recursive=False)

    idataframe.aggregate_region(variable='Capacity|*', append=True)

    idataframe.aggregate(variable='Maximum Storage|Electricity|Energy Storage System', append=True, recursive=False)
    idataframe.aggregate_region(variable='Maximum Storage|Electricity|Energy Storage System', append=True)

    idataframe.aggregate(variable='Emissions|CO2|Electricity|Coal', append=True, recursive=False)
    idataframe.aggregate(variable='Emissions|CO2|Electricity|Gas|CCGT', append=True, recursive=False)
    idataframe.aggregate(variable='Emissions|CO2|Electricity|Gas', append=True, recursive=False)
    idataframe.aggregate(variable='Emissions|CO2|Electricity', append=True, recursive=False)
    idataframe.aggregate(variable='Emissions|CO2|Residential and Commercial Heat|Electricity', append=True, recursive=False)
    idataframe.aggregate(variable='Emissions|CO2|Residential and Commercial Heat', append=True, recursive=False)
    idataframe.aggregate(variable='Emissions|CO2|Industrial Heat', append=True, recursive=False)
    idataframe.aggregate_region(variable='Emissions|CO2|*', append=True)

    idataframe.aggregate(variable='Energy Service|Transportation|Freight|Road|Internal Combustion Engine', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Freight|Road|Electric', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Freight|Road', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Freight|Maritime', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Freight|Rail', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Freight', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Passenger|Road|Internal Combustion Engine', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Passenger|Road|Electric', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Passenger|Road', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Passenger|Air', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Passenger|Rail', append=True, recursive=False)
    idataframe.aggregate(variable='Energy Service|Transportation|Passenger', append=True, recursive=False)
    # idataframe.aggregate(variable='Energy Service|Transportation', append=True, recursive=False)
    idataframe.aggregate_region(variable='Energy Service|*', append=True)

    idataframe.aggregate(variable='Secondary Energy|Electricity|Biomass', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Coal', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Gas', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Oil', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Solar', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Wind', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Gases', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Heat', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Hydrogen', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Liquids', append=True, recursive=False)
    idataframe.aggregate_region(variable='Secondary Energy|*', append=True)

    idataframe.data = idataframe.data.replace({'region': 'UK'}, 'GB')

    iso2_mapping = dr.loadmap_iso2_countries()

    for r in iso2_mapping:
        idataframe.data = idataframe.data.replace({'region': r}, iso2_mapping[r])

    idataframe.data = idataframe.data.replace({'region': 'World'}, DEF_REGION_NAME)
    idataframe.rename(region={'NONEU_Balkan': 'Non-EU-Balkans'}, inplace=True)

    if filter_only_yearly_values:
        idataframe.filter(subannual='Year', inplace=True)

    return idataframe


def changeFinalEnergyToGWh(final_energy, variable):
    final_energy.loc[(final_energy['variable'] == variable), 'value'] \
        = final_energy.loc[
              (final_energy['variable'] == variable), 'value'] * 1000 * 1000 / 3.6
    final_energy.loc[(final_energy['variable'] == variable), 'unit'] = 'GWh/yr'

    return final_energy


def generate_idataframe_renewable_series(data_wrapper):
    logging.info('Executing: generate_idataframe')
    frames = []

    for frame in data_wrapper.transformed_data:
        frames.append(data_wrapper.transformed_data[frame])

    values = pd.concat(frames)
    idataframe = pyam.IamDataFrame(values)

    return idataframe
