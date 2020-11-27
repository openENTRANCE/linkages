import gdxpds
import yaml

import pandas as pd
import genesysmod_to_iamc.data_wrapper as dw
import logging
from genesysmod_to_iamc._statics import *


def loadmap_primary_energy_fuels():
    # currently static
    return {
        'Biomass': 'Primary Energy|Biomass',
        'Hardcoal': 'Primary Energy|Coal',
        'Gas_Natural': 'Primary Energy|Gas',
        'Oil': 'Primary Energy|Oil',
        'Lignite': 'Primary Energy|Coal',
        'Gas_Bio': 'Primary Energy|Biomass',
        'Biofuel': 'Primary Energy|Biomass',
    }


def loadmap_non_bio_renewables():
    # currently static
    return {
        'RES_CSP': 'Solar',
        'RES_Geothermal': 'Geothermal',
        'RES_Hydro_Large': 'Hydro',
        'RES_Hydro_Small': 'Hydro',
        'RES_Ocean': 'Ocean',
        'RES_PV_Rooftop_Commercial': 'Solar',
        'RES_PV_Rooftop_Residential': 'Solar',
        'RES_PV_Utility_Avg': 'Solar',
        'RES_PV_Utility_Inf': 'Solar',
        'RES_PV_Utility_Opt': 'Solar',
        'RES_Wind_Offshore_Transitional': 'Wind',
        'RES_Wind_Offshore_Shallow': 'Wind',
        'RES_Wind_Offshore_Deep': 'Wind',
        'RES_Wind_Onshore_Avg': 'Wind',
        'RES_Wind_Onshore_Inf': 'Wind',
        'RES_Wind_Onshore_Opt': 'Wind',
        'HLR_Solar_Thermal': 'Solar',
        'HLR_Geothermal': 'Geothermal',
        'HLI_Solar_Thermal': 'Solar',
        'HLI_Geothermal': 'Geothermal',
        'HLT_Rooftop_Residential': 'Solar',
        'HLT_Rooftop_Commercial': 'Solar',
        'HLT_Geothermal': 'Geothermal',
        'HHT_Geothermal': 'Geothermal',
    }


def loadmap_from_csv(file):
    filename = file + ".csv"
    return pd.read_csv(DEF_MAPPINGS_PATH / filename, header=None, index_col=0, squeeze=True).to_dict()


def loadmap_iso2_countries():
    with open(DEF_MAPPINGS_PATH / 'countries.yaml', 'r') as stream:
        country_codelist = yaml.load(stream, Loader=yaml.FullLoader)

    iso2_mapping = dict(
        [(country_codelist[c]['iso2'], c) for c in country_codelist]
        # add alternative iso2 codes used by the European Commission to the mapping
        + [(country_codelist[c]['iso2_alt'], c) for c in country_codelist
           if 'iso3_alt' in country_codelist[c]]
    )

    return iso2_mapping


def load_gdx_file(input_file, gams_dir):
    file_name = input_file + ".gdx"
    logging.info('Loading gdx with output results')
    output_gdx = gdxpds.to_dataframes(DEF_INPUT_PATH / file_name, gams_dir=gams_dir)

    return dw.DataWrapper(input_file, output_gdx)
