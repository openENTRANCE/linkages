from pathlib import Path

DEF_GAMS_DIR = "C:/GAMS/32"

DEF_MAPPINGS_PATH = Path(__file__).parent / 'mappings'
DEF_INPUT_PATH = Path(__file__).parent / 'input'
DEF_OUTPUT_PATH = Path(__file__).parent / 'out'

DEF_MODEL_AND_VERSION = 'GENeSYS-MOD 2.9'
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
DEF_TRADE_CAPACITY_SHEET = 'output_trade_capacity'

DEF_REGION_NAME = 'Europe (incl. Turkey)'

DEF_MAP_SCENARIOS = {
    'TechnoFriendly_globalLimit': 'Techno-Friendly 1.0',
    'DirectedVision_globalLimit': 'Directed Transition 1.0',
    'DirectedTransition_globalLimit': 'Directed Transition 1.0',
    'GradualDevelopment_globalLimit': 'Gradual Development 1.0',
    'SocietalCommitment_globalLimit': 'Societal Commitment 1.0',
}

DEF_MAP_FILE_SCENARIOS = {
    'TechnoFriendly': 'Techno-Friendly 1.0',
    'DirectedTransition': 'Directed Transition 1.0',
    'GradualDevelopment': 'Gradual Development 1.0',
    'SocietalCommitment': 'Societal Commitment 1.0',
}

DEF_YEARS = [2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050]
