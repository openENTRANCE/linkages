import genesysmod_to_iamc.data_reader as dr
import genesysmod_to_iamc.data_wrapper as dw
import pandas as pd
import pyam

from genesysmod_to_iamc._statics import *


def generate_final_energy_series(data_wrapper: dw.DataWrapper, series_name: str, fuel_name:str):
    _finalenergy_demand = data_wrapper.idataframe

    _filtered = _finalenergy_demand[_finalenergy_demand['subannual'] == 'Year']
    _filtered = _filtered[_filtered['variable'] == fuel_name]
    _filtered = _filtered.groupby(['region', 'year']).sum().reset_index()
    _filtered.head(10)

    for year in DEF_YEARS:
        _series = data_wrapper.demand_series[series_name].copy()
        _series['unit'] = 'EJ/yr'
        _series['model'] = DEF_MODEL_AND_VERSION
        _series['fuel'] = fuel_name
        _series['scenario'] = DEF_MAP_FILE_SCENARIOS[data_wrapper.input_file]
        _series['year'] = year
        # group by relevant values and take the sum

        _frame = _series.groupby(
            ['model', 'scenario', 'region', 'fuel', 'unit', 'subannual', 'year']).sum().reset_index()
        _frame.columns = ['Model', 'Scenario', 'Region', 'Variable', 'Unit', 'Subannual', 'Year', 'Value']

    regions = _series['region'].unique()
    outputs = []
    iso2_mapping = dr.loadmap_iso2_countries()

    for year in DEF_YEARS:
        for region in regions:
            _yearly = _filtered.copy()
            #if region == 'UK':
            #    region = 'GB'

            if region == 'NONEU_Balkan':
                region_key = 'Non-EU-Balkans'
            elif region == 'UK':
                region_key = 'United Kingdom'
            else:
                region_key = iso2_mapping[region]

            _yearly = _yearly[(_yearly['region'] == region_key) & (_yearly['year'] == year)]
            if not _yearly.empty:
                _multiplier = _yearly.iloc[0].value

                _filtered_series = _frame[(_frame['Region'] == region)].copy()
                _filtered_series['Year'] = year
                _filtered_series['Value'] = _filtered_series['Value'] * _multiplier
                _filtered_series['Unit'] = 'EJ/yr'

                outputs.append(_filtered_series.copy())

    output_frame = pd.concat(outputs)

    output_frame = output_frame.replace({'Region': 'UK'}, 'GB')
    output_frame = output_frame.replace({'Region': 'NONEU_Balkan'}, 'Non-EU-Balkans')

    for r in iso2_mapping:
        output_frame = output_frame.replace({'Region': r}, iso2_mapping[r])

    data_wrapper.output_series[fuel_name] = output_frame

    output_frame.to_csv(series_name + ".csv")
    return output_frame


def generate_electricity_series(data_wrapper: dw.DataWrapper):
    values = pd.concat(data_wrapper.output_series)
    values = values.groupby(
        ['Model', 'Scenario', 'Region', 'Variable', 'Unit', 'Subannual', 'Year']).sum().reset_index()
    values = values.groupby(['Model', 'Scenario', 'Region', 'Unit', 'Subannual', 'Year']).sum().reset_index()
    values['Variable'] = "Final Energy|Electricity"
    values = values.groupby(
        ['Model', 'Scenario', 'Region', 'Variable', 'Unit', 'Subannual', 'Year']).sum().reset_index()
    values.columns = ['Model', 'Scenario', 'Region', 'Variable', 'Unit', 'Subannual', 'Year', 'Value']

    data_wrapper.output_series['Final Energy|ElectricityDummy'] = values


def output_series(data_wrapper: dw.DataWrapper):
    values = pd.concat(data_wrapper.output_series).reset_index().drop(['level_0','level_1'], axis=1)
    idataframe = pyam.IamDataFrame(values)

    output_file = data_wrapper.input_file + "_series.csv"

    idataframe.to_csv(DEF_OUTPUT_PATH / output_file)