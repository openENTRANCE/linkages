from pathlib import Path

# add your GAMS directory name here
DEF_GAMS_DIR = "C:/GAMS/42"

DEF_MAPPINGS_PATH = Path(__file__).parent / 'mappings'
DEF_INPUT_PATH = Path(__file__).parent / 'input'
DEF_OUTPUT_PATH = Path(__file__).parent / 'out'

# define the model version that is used for the output files
DEF_MODEL_AND_VERSION = 'GENeSYS-MOD 3.1'


DEF_PRODUCTION_COLUMNS = ["region",
                          "sector",
                          "technology",
                          "mode",
                          "fuel",
                          "subannual",
                          "type",
                          "unit",
                          "scenario",
                          "year",
                          "value"]
DEF_EMISSION_COLUMNS = ["region",
                        "sector",
                        "emission",
                        "technology",
                        "type",
                        "scenario",
                        "year",
                        "value"]
DEF_CAPACITY_COLUMNS = ["region",
                        "sector",
                        "technology",
                        "type",
                        "scenario",
                        "year",
                        "value"]
DEF_COST_COLUMNS = ["region",
                    "sector",
                    "technology",
                    "type",
                    "scenario",
                    "year",
                    "value"]
DEF_EXOGENOUS_COST_COLUMNS = ["region",
                              "technology",
                              "type",
                              "year",
                              "value"]
DEF_DETAILED_COST_COLUMNS = ["region",
                              "technology",
                             "sector",
                              "type",
                             "unit",
                              "year",
                              "value"]
DEF_TRADE_CAPACITY_COLUMNS = ["region_from",
                              "region_to",
                              "type",
                              "year",
                              "value"]

DEF_PRODUCTION_SHEET = 'output_energy_balance'
DEF_CAPACITY_SHEET = 'output_capacity'
DEF_EMISSION_SHEET = 'output_emissions'
DEF_COST_SHEET = 'output_costs'
DEF_EXOGENOUS_COST_SHEET = 'output_exogenous_costs'
DEF_DETAILED_COST_SHEET = 'output_technology_costs_detailed'
DEF_TRADE_CAPACITY_SHEET = 'output_trade_capacity'

# define the region name that is used for the aggregated outputs
DEF_REGION_NAME = 'Europe (incl. Turkey)'


# define the list of scenarios and map them to the IAMC explorer format
DEF_MAP_SCENARIOS = {
    'TechnoFriendly_globalLimit': 'Techno-Friendly 2.0',
    'DirectedVision_globalLimit': 'Directed Transition 2.0',
    'DirectedTransition_globalLimit': 'Directed Transition 2.0',
    'GradualDevelopment_globalLimit': 'Gradual Development 2.0',
    'SocietalCommitment_globalLimit': 'Societal Commitment 2.0',
}

# define the list of files to use for the respective scenarios
DEF_MAP_FILE_SCENARIOS = {
    'TechnoFriendly': 'Techno-Friendly 2.0',
    'DirectedTransition': 'Directed Transition 2.0',
    'GradualDevelopment': 'Gradual Development 2.0',
    'SocietalCommitment': 'Societal Commitment 2.0',
}

# define the years that should be included in the outputs
DEF_YEARS = [2018, 2020, 2025, 2030, 2035, 2040, 2045, 2050]

DEF_EU27 = ['AT', 'BE', 'BG', 'HR', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT',
                                     'LV', 'LT', 'LU', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE']