from genesysmod_to_iamc._statics import *
from enum import Enum

import genesysmod_to_iamc.data_reader as dr
import genesysmod_to_iamc.data_transform as dt
import genesysmod_to_iamc.series_generator as sg

import nomenclature
import pyam

import logging
import os

logging.basicConfig(level=logging.INFO)


class Pathways(Enum):
    TF = "TechnoFriendly"
    DT = "DirectedTransition"
    GD = "GradualDevelopment"
    SC = "SocietalCommitment"


def generate_data(input_file: str, generate_series_data: bool = False, generate_load_factors: bool = False,
                  combine_outputs: bool = False):

    if not os.path.exists(DEF_OUTPUT_PATH):
        os.makedirs(DEF_OUTPUT_PATH)

    data_wrapper = _generate_yearly_values(input_file)
    output_name = data_wrapper.input_file + "_yearly.csv"
    data_wrapper.idataframe.to_csv(DEF_OUTPUT_PATH / output_name)

    if generate_series_data:
        _generate_series_data(data_wrapper)

    if generate_load_factors:
        data_wrapper_load = _generate_load_factors(input_file)
        output_name_load = data_wrapper_load.input_file + "_loadfactors.csv"
        data_wrapper_load.idataframe.to_csv(DEF_OUTPUT_PATH / output_name_load)

    if combine_outputs:
        _combine_data(input_file, generate_series_data, generate_load_factors)


def generate_combined_excel_yearly():
    lst = []

    for file in Pathways:
        filename = file.value + '_yearly.csv'
        df = pyam.IamDataFrame(str(DEF_OUTPUT_PATH / filename))
        lst.append(df)

    genesys = pyam.concat(lst)
    genesys = pyam.IamDataFrame(genesys.data[pyam.IAMC_IDX + ['year', 'value']])
    genesys.to_excel(f'GENeSYS-MOD-pathways.xlsx')


def _generate_yearly_values(input_file):
    data_wrapper = dr.load_gdx_file(input_file, DEF_GAMS_DIR)

    dt.generate_transmission_capacity_values(data_wrapper)
    dt.generate_load_demand_series(data_wrapper)
    dt.generate_primary_energy_values(data_wrapper)
    dt.generate_final_energy_values(data_wrapper)
    dt.generate_capacity_values(data_wrapper)
    dt.generate_transport_capacity_values(data_wrapper)
    dt.generate_storage_capacity_values(data_wrapper)
    dt.generate_emissions_values(data_wrapper)
    # dt.generate_additional_emissions_values(data_wrapper) - currently not in nomenclature
    dt.generate_secondary_energy(data_wrapper)
    dt.generate_exogenous_costs(data_wrapper)
    dt.generate_co2_prices(data_wrapper)

    data_wrapper.generate_idataframe(True)
    nomenclature.validate(data_wrapper.idataframe)
    return data_wrapper


def _generate_load_factors(input_file):
    data_wrapper_series = dr.load_gdx_file(input_file, DEF_GAMS_DIR)
    dt.generate_load_factors(data_wrapper_series)
    data_wrapper_series.generate_idataframe_renewable_series()
    nomenclature.validate(data_wrapper_series.idataframe)
    return data_wrapper_series


def _generate_series_data(data_wrapper):
    if data_wrapper.idataframe is None:
        raise Exception('IamDataFrame of data_wrapper is empty')

    sg.generate_final_energy_series(data_wrapper, 'HeatingLow', 'Final Energy|Residential and Commercial|Electricity')
    sg.generate_final_energy_series(data_wrapper, 'HeatingHigh', 'Final Energy|Industry|Electricity')
    sg.generate_final_energy_series(data_wrapper, 'Transport', 'Final Energy|Transportation|Electricity')
    sg.generate_final_energy_series(data_wrapper, 'Power', 'Final Energy|Electricity')
    sg.generate_final_energy_series(data_wrapper, 'HeatingLow', 'Final Energy|Residential and Commercial')
    sg.generate_final_energy_series(data_wrapper, 'HeatingHigh', 'Final Energy|Industry')

    sg.output_series(data_wrapper)


def _combine_data(input_file, generate_series_data: bool = False, generate_load_factors: bool = False):
    file_combined = input_file + "_combined.csv"
    file_yearly = input_file + '_yearly.csv'
    file_load = input_file + '_loadfactors.csv'
    file_series = input_file + '_series.csv'

    idataframe_base = pyam.IamDataFrame(str(DEF_OUTPUT_PATH / file_yearly))

    if generate_load_factors:
        idataframe_load = pyam.IamDataFrame(str(DEF_OUTPUT_PATH / file_load))
        idataframe_base_with_load = idataframe_base.append(idataframe_load)
    else:
        idataframe_base_with_load = idataframe_base

    if generate_series_data:
        idataframe_series = pyam.IamDataFrame(str(DEF_OUTPUT_PATH / file_series))
        idataframe_all = idataframe_base_with_load.append(idataframe_series)
    else:
        idataframe_all = idataframe_base_with_load

    idataframe_all.to_csv(DEF_OUTPUT_PATH / file_combined)
