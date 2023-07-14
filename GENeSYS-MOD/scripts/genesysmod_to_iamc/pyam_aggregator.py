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
    idataframe.aggregate(variable='Primary Energy|Biomass|Electricity', append=True, recursive=False)
    idataframe.aggregate(variable='Primary Energy|Coal|Electricity', append=True, recursive=False)
    idataframe.aggregate(variable='Primary Energy|Oil|Electricity', append=True, recursive=False)
    idataframe.aggregate(variable='Primary Energy|Gas|Electricity', append=True, recursive=False)

    idataframe.aggregate(variable='Primary Energy|Non-Biomass Renewables',
                         components=['Primary Energy|Solar'
                             , 'Primary Energy|Wind'
                             , 'Primary Energy|Ocean'
                             , 'Primary Energy|Geothermal'
                             , 'Primary Energy|Hydro'], append=True, recursive=False)
    idataframe.aggregate_region(variable='Primary Energy*', subregions=['EU27 (excl. Malta & Cyprus)','NO','NONEU_Balkan','TR','UK','CH'], append=True)

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
                         components=['Final Energy|Residential and Commercial',
                                     'Final Energy|Industry',
                                     'Final Energy|Transportation',
                                     'Final Energy|ElectricityDummy'], append=True, recursive=False)


    idataframe.aggregate(variable='Final Energy|Gases',
                         components=['Final Energy|Residential and Commercial|Gases',
                                     'Final Energy|Transportation|Gases',
                                     'Final Energy|Heat|Gases',
                                     'Final Energy|Electricity|Gases',
                                     'Final Energy|Industry|Gases'], append=True, recursive=False)


    idataframe.aggregate(variable='Final Energy|Hydrogen',
                         components=['Final Energy|Residential and Commercial|Hydrogen',
                                     'Final Energy|Transportation|Hydrogen',
                                     'Final Energy|Heat|Hydrogen',
                                     'Final Energy|Electricity|Hydrogen',
                                     'Final Energy|Industry|Hydrogen'], append=True, recursive=False)


    idataframe.aggregate(variable='Final Energy|Liquids',
                         components=['Final Energy|Residential and Commercial|Liquids',
                                     'Final Energy|Transportation|Liquids',
                                     'Final Energy|Heat|Liquids',
                                     'Final Energy|Electricity|Liquids',
                                     'Final Energy|Industry|Liquids'], append=True, recursive=False)


    idataframe.aggregate(variable='Final Energy|Solids',
                         components=['Final Energy|Residential and Commercial|Solids',
                                     'Final Energy|Transportation|Solids',
                                     'Final Energy|Heat|Solids',
                                     'Final Energy|Electricity|Solids',
                                     'Final Energy|Industry|Solids'], append=True, recursive=False)

    idataframe.aggregate(variable='Final Energy|Solids|Biomass',
                         components=['Final Energy|Residential and Commercial|Solids|Biomass',
                                     'Final Energy|Transportation|Solids|Biomass',
                                     'Final Energy|Heat|Solids|Biomass',
                                     'Final Energy|Electricity|Solids|Biomass',
                                     'Final Energy|Industry|Solids|Biomass'], append=True, recursive=False)

    idataframe.aggregate(variable='Final Energy|Solids|Coal',
                         components=['Final Energy|Residential and Commercial|Solids|Coal',
                                     'Final Energy|Transportation|Solids|Coal',
                                     'Final Energy|Heat|Solids|Coal',
                                     'Final Energy|Electricity|Solids|Coal',
                                     'Final Energy|Industry|Solids|Coal'], append=True, recursive=False)


    idataframe.aggregate(variable='Final Energy|Industry|Heat',
                         components=['Final Energy|Industry'], append=True, recursive=False)



    idataframe.aggregate(variable='Final Energy|Residential and Commercial|Heat',
                         components=['Final Energy|Residential and Commercial'], append=True, recursive=False)


    idataframe.aggregate_region(variable='Final Energy*', subregions=['EU27 (excl. Malta & Cyprus)','NO','NONEU_Balkan','TR','UK','CH'], append=True)

    idataframe.aggregate(variable='Final Energy|Solar',
                         components=['Primary Energy|Solar'], append=True, recursive=False)

    idataframe = pyam.IamDataFrame(changeFinalEnergyToGWh(idataframe.data, 'Final Energy|Electricity|Transportation'))
    idataframe = pyam.IamDataFrame(changeFinalEnergyToGWh(idataframe.data, 'Final Energy|Electricity|Other (excl. Heat, Cooling, Transport)'))
    idataframe = pyam.IamDataFrame(changeFinalEnergyToGWh(idataframe.data, 'Final Energy|Electricity|Heat'))

    idataframe = pyam.IamDataFrame(idataframe.data[idataframe.data['variable'] != 'Final Energy|ElectricityDummy'])

    #remove subsector where exogenous electricity demand cannot be added ex-post
    #idataframe = pyam.IamDataFrame(idataframe.data[idataframe.data['variable'] != 'Final Energy|Residential and Commercial|Electricity'])
    #idataframe = pyam.IamDataFrame(idataframe.data[idataframe.data['variable'] != 'Final Energy|Industry|Electricity'])
    #idataframe = pyam.IamDataFrame(idataframe.data[idataframe.data['variable'] != 'Final Energy|Transportation|Electricity'])


    idataframe.aggregate(variable='Capacity|Electricity|Biomass', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Coal|Hard coal', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Coal|Lignite', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Coal', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Gas|CCGT', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Gas|OCGT', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Gas', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Solar|PV|Rooftop', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Solar|PV', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Solar', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Wind', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Hydro', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity|Oil', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Electricity', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Heat|Residential and Commercial', append=True, recursive=False)
    idataframe.aggregate(variable='Capacity|Heat|Industrial', append=True, recursive=False)
    idataframe.aggregate_region(variable='Capacity|*', subregions=['EU27 (excl. Malta & Cyprus)','NO','NONEU_Balkan','TR','UK','CH'], append=True)

    idataframe.aggregate(variable='Maximum Storage|Electricity|Energy Storage System', append=True, recursive=False)
    idataframe.aggregate_region(variable='Maximum Storage|Electricity|Energy Storage System*', subregions=['EU27 (excl. Malta & Cyprus)','NO','NONEU_Balkan','TR','UK','CH'], append=True)


    idataframe.aggregate(variable='Emissions|CO2|Energy|Supply', append=True, recursive=False)
    idataframe.aggregate(variable='Emissions|CO2|Energy|Demand', append=True, recursive=False)
    idataframe.aggregate(variable='Emissions|CO2|Energy', append=True, recursive=False)
    idataframe.aggregate_region(variable='Emissions|CO2|*', subregions=['EU27 (excl. Malta & Cyprus)','NO','NONEU_Balkan','TR','UK','CH'], append=True)


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
    idataframe.aggregate_region(variable='Energy Service|Transportation|*', subregions=['EU27 (excl. Malta & Cyprus)','NO','NONEU_Balkan','TR','UK','CH'], append=True)


    idataframe.aggregate(variable='Secondary Energy|Electricity|Biomass', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Coal|Hard coal', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Coal|Lignite', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Coal', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Gas|OCGT', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Gas|CCGT', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Oil', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Solar', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Electricity|Wind', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Gases', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Heat|Coal|Hard coal', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Heat|Coal|Lignite', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Heat|Coal', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Heat', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Hydrogen', append=True, recursive=False)
    idataframe.aggregate(variable='Secondary Energy|Liquids', append=True, recursive=False)


    idataframe.aggregate(variable='Secondary Energy|Electricity|Gas',
                         components=['Secondary Energy|Electricity|Gas|OCGT'
                             , 'Secondary Energy|Electricity|Gas|CCGT'
                             , 'Secondary Energy|Electricity|Gas|w/ CCS'
                             , 'Secondary Energy|Electricity|Gas|w/o CCS'], append=True, recursive=False)

    idataframe.aggregate(variable='Secondary Energy|Electricity', append=True, recursive=False)
    idataframe.aggregate_region(variable='Secondary Energy|*', subregions=['EU27 (excl. Malta & Cyprus)','NO','NONEU_Balkan','TR','UK','CH'], append=True)


    # idataframe.aggregate_region(variable='Capital Cost|*', append=True)
    # idataframe.aggregate_region(variable='Fixed Cost|*', append=True)
    # idataframe.aggregate_region(variable='Variable Cost|*', append=True)


    idataframe = pyam.IamDataFrame(idataframe.data.replace({'region': 'UK'}, 'GB'))

    iso2_mapping = dr.loadmap_iso2_countries()

    for r in iso2_mapping:
        idataframe.rename(region={r: iso2_mapping[r]}, inplace=True)
        #idataframe = pyam.IamDataFrame(idataframe.data.replace({'region': r}, iso2_mapping[r]))

    idataframe = pyam.IamDataFrame(idataframe.data.replace({'region': 'World'}, DEF_REGION_NAME))
    idataframe.rename(region={'NONEU_Balkan': 'Non-EU-Balkans'}, inplace=True)

    if filter_only_yearly_values:
        idataframe.filter(subannual='Year', inplace=True)


    # test = idataframe[idataframe['region'].all('Germany')]
    # test = test.groupby(['model', 'scenario', 'variable', 'unit', 'subannual', 'year']).sum().reset_index()
    # test['region'] = 'test'
    #
    # idataframe = pd.concat([idataframe, test])


    return idataframe




def changeFinalEnergyToGWh(final_energy, variable):
    final_energy.loc[(final_energy['variable'] == variable), 'value'] \
        = final_energy.loc[
              (final_energy['variable'] == variable), 'value'] * 1000 * 1000 / 3.6
    final_energy.loc[(final_energy['variable'] == variable), 'unit'] = 'GWh'

    return final_energy


def generate_idataframe_renewable_series(data_wrapper):
    logging.info('Executing: generate_idataframe')
    frames = []

    for frame in data_wrapper.transformed_data:
        frames.append(data_wrapper.transformed_data[frame])

    values = pd.concat(frames)
    idataframe = pyam.IamDataFrame(values)

    return idataframe
