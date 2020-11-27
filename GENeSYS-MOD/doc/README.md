## GENeSYS-MOD to openENTRANCE
This document and the accompanying scripts describe the linkage of GENeSYS-MOD to the openENTRANCE plattform. Currently, the linkage is one-directional: The results of GENeSYS-MOD can be transformed to openENTRANCE compatible datasets.

### General Workflow
1. Run GENeSYS-MOD or use the available pathway result files. If you use the available pathway results, skip step 2.
2. Place the according ouput gdx files in the 'input' folder for the conversion scripts:  ```openEntrance_linkages\GENeSYS-MOD\scripts\genesysmod_to_iamc\input```
3. Run the jupyter notebook ```genesysmod_to_oE.ipynb```
4. Use or upload the resulting csv-files or the combined Excel-file.

### GENeSYS-MOD to openEntrance conversion script
The ```genesysmod_to_oE.ipynb``` explains the basic usage of the conversion scripts. The actual script are written in python and are located in the python module ```genesysmod_to_iamc```.

The python module uses the following external packages:
- pandas
- pyam (https://github.com/IAMconsortium/pyam)
- nomenclature (https://github.com/openENTRANCE/nomenclature)
- gdxpds (https://github.com/NREL/gdx-pandas)

#### File structure of the module
- \_\_this\_file\_\_ : Jupyter notebook with general guidelines
- /genesysmod\_to\_iamc : Folder with actual conversion scripts
 - /genesysmod\_to\_iamc/mappings/ : Folder with mappings of GENeSYS-MOD variables to openEntrance nomenclature
 - /genesysmod\_to\_iamc/inputs/ : Folder with original GENeSYS-MOD pathway results
 - /genesysmod\_to\_iamc/out/ : Folder with generated csv files in openEntrance format
 
 The folder _mappings_ contains the mappings and aggregations of GENeSYS-MOD technologies, fuels, and variables to the openENTRANCE nomenclature. Most of the mappings represent dictionaries (key-value pairs) and will be read in automatically. Hence, these mappings can be changed for most cases to be adjusted to changes in the nomenclature or bugs.
 
 Aggregations of the variables (regional and aggregating sub-variables) are handled in the file ```pyam_aggregator.py```. Here, you can check for missing aggregations and add custom aggregations as needed.
 
 #### Changes to the scripts required to run the conversion
 This script uses gdxpds which was unable to succesfully locate the GAMS directory in its newsest version. Therefore, the path to GAMS needed to be set manually. You will need to change the directory such that it correctly points to you installed GAMS distribution. The variable is called *DEF_GAMS_DIR* and is set in the file *genesysmod_to_iamc/\_statics.py*.
 
 #### Usage of the module
 The general usage of the module and the scripts are explained in the jupyter notebook ```genesysmod_to_oE.ipynb```. The following information is also presented in it:
 
 The jupyter notebook shows an exemplary conversion of GENeSYS-MOD results to the common openEntrance data fromat. The outputs of the scripts in this module will be csv files, that represent GENeSYS-MOD data in openEntrance nomenclature. First, the corresponding scripts will be imported as module to this notebook:
 ```python
 import genesysmod_to_iamc
 ```
 Next, the actual result file conversion can be started by calling ```genesysmod_to_iamc.generate_data(FileName : str)```. For the ease of use, the module ```genesysmod_to_iamc``` also includes a enumeration ```Pathways``` that includes references to the filenames for the openEntrance Pathways:

```python
__init__.py:
class Pathways(Enum):
    TF = "TechnoFriendly"
    DT = "DirectedTransition"
    GD = "GradualDevelopment"
    SC = "SocietalCommitment"
```
Furthermore, ```genesysmod_to_iamc.generate_data(FileName : str)``` has three optional parameters ```generate_series_data```, ```generate_load_factors``` and ```combine_outputs``` that all default to ```False```. 

If ```generate_series_data``` is set to ```True```, full hourly demand time series for Final Energy|Residential and Commercial|Electricity, Final Energy|Industry|Electricity, Final Energy|Transportation|Electricity, Final Energy|Electricity, Final Energy|Residential and Commercial and Final Energy|Industry will be generated. Full hourly demand series will be written to an extra file. **Note:** setting this parameter will significantly increase the computing time.

If ```generate_load_factors``` is set to ```True```, full hourly load series for Solar PV, Wind Onshore and Wind Offshore will be generated. Full hourly load series will be written to an extra file. **Note:** setting this parameter will significantly increase the computing time.

If ```combine_outputs``` is set to ```True```, the different result files for a pathway (yearly, hourly, load factors) can be combined to one single file. 

Example creation of TechnoFriendly (TF) Pathway results:
```python
generate_series_data = False
generate_load_factors = False
combine_outputs = True
genesysmod_to_iamc.generate_data(genesysmod_to_iamc.Pathways.TF.value, 
                                 generate_series_data, 
                                 generate_load_factors, 
                                 combine_outputs)
```

Results will be written to ```\GENEeSYS-MOD\scripts\genesysmod_to_iamc\out```. The following line of code creates a unified Excel-File with all pathways combined:

```python
genesysmod_to_iamc.generate_combined_excel()
```