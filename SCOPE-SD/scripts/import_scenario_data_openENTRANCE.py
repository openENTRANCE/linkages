"""
Import of Data for the SCOPE-SD Model.
"""
import pandas as pd
import pyam
import nomenclature as nc
import xlwings

# In settings it is stored where to store which variable of GENeSYS-MOD
# in the Excel sheet of the SCOPE Model
settings = pd.read_excel("settings.xlsx")

# set up the connection to openENTRANCE with pyam
# and read the GENeSYS-MOD
conn = pyam.iiasa.Connection()
conn.connect("openentrance")
df = pyam.read_iiasa("openentrance", model="GENeSYS-MOD 2.9.0-oe")

# Convert EJ/yr to TWh/yr
df = df.convert_unit("EJ/yr", to="TWh/yr")

# filter for the scenario specified in the settings sheet.
# and filter for the year 2050
df = df.filter(scenario=settings["scenario"][0])
df = df.filter(year=[2050])

# read the excel workbook that is used by the SCOPE-Model
scope = pd.read_excel("input_SCOPE_SD.xlsx", sheet_name="2050")

# open the excel workbook that is used by the SCOPE-Model with xlwings, to
# store later the new values in the sheets.
wb = xlwings.Book("input_SCOPE_SD.xlsx")

# a loop over the specified variables in the settings excel sheet.
for n in range(len(settings["scenario"])):

    # filter for the current variable from the setting sheet.
    dfv = df.filter(variable=settings["variable"][n])

    # change Slovak Republic into Slovakia
    mapping_s = {"Slovak Republic": "Slovakia"}
    dfv = dfv.data.replace({"region": mapping_s})

    # change countrynames in genesys data to the accronym used in scope.
    # via th nc.iso_mapping
    half = dict(list(nc.iso_mapping.items())[: len(nc.iso_mapping) // 2 - 1])
    mapping = dict(zip(half.values(), half.keys()))
    dfv = dfv.replace({"region": mapping})

    # drop the rows from dfv that correspond to countries not needed in SCOPE
    for row in dfv.region:
        if row not in scope.Country.tolist():
            indexName = dfv[dfv["region"] == row].index
            dfv.drop(indexName, inplace=True)

    # reset the indices
    dfv = dfv.reset_index(drop=True)

    # get the countries like they are stored in the SCOPE-Model
    countries = scope.Country[1:29].tolist()

    # get the dataframe in the order of scope.
    new_order = []
    for scope_country in countries:
        if scope_country not in dfv.region.tolist():  # to catch errors
            print("Warning, the results have the wrong ordering, because one scope country was not in the GENeSYS data.")
            print("this is for the variable:")
            print(settings["variable"][n])
            print("And the country:")
            print(scope_country)
        for i, gen_country in enumerate(dfv.region):
            if scope_country == gen_country:
                new_order.append(i)
    df_order = dfv.reindex(new_order)

    # get the settings on where to store the current variable.
    Sheet = wb.sheets[settings["sheet"][n]]
    cell = settings["cell"][n]
    x = Sheet.range(cell).row
    y = Sheet.range(cell).column

    # store the values in template.xlsx in the defined sheet,
    # at defined position.
    # And print out variables that are not there for whicht countries. To
    # see if errors occur.
    for i in range(len(df_order.value.tolist())):
        if pd.isna(df_order.value.tolist()[i]):
            print("the variable: " + settings["variable"][n] + "  is not there for the country:")
            print(countries[i])
        else:
            Sheet.range(x + i, y).value = df_order.value.tolist()[i]

# save and close the changed Excel Workbook from the SCOPE-Model.
wb.save()
wb.close()
