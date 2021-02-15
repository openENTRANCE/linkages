import pandas as pd
import nomenclature as nc
import pyam

# Read SCOPE output file
TEST_DF = pd.read_excel("scope_sd_20201120_test_data.xlsx")

# Create dictionary and convert regions with iso_mapping into IAMC format
TEST_DICT = TEST_DF.to_dict()
DICT_REGIO = {}
DICT_REGIO["Region"] = {}
for i in range(len(TEST_DICT["Region"].keys())):
    try:
        DICT_REGIO["Region"][i] = nc.iso_mapping[TEST_DICT["Region"][i]]
    except KeyError:
        DICT_REGIO["Region"][i] = TEST_DICT["Region"][i]

NEW_DICT = {}
NEW_DICT["Model"] = TEST_DICT["Model"]
NEW_DICT["Scenario"] = TEST_DICT["Scenario"]
NEW_DICT["Region"] = DICT_REGIO["Region"]
NEW_DICT["Variable"] = TEST_DICT["Variable"]
NEW_DICT["Unit"] = TEST_DICT["Unit"]
NEW_DICT["Subannual"] = TEST_DICT["Subannual"]
NEW_DICT[2050] = TEST_DICT[2050]
NEW_DF = pd.DataFrame.from_dict(NEW_DICT)

# Save dict into new excel file
NEW_DF.to_excel("scope_sd_20201120_test_data_validated.xlsx")

# Check the created excel file with the openENTRANCE nomenclature
nc.validate("scope_sd_20201120_test_data_validated.xlsx")
