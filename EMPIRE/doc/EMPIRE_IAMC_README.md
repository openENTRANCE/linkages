# EMPIRE - standardizing input/output for model linkage

[EMPIRE](https://github.com/ntnuiotenergy/OpenEMPIRE) is a multi-horizon stochastic capacity expansion model representing the European electricity system implemented in python pyomo. EMPIRE minimizes total system costs for long-term investments towards 2060 under consideration of hour-to-hour operations of country aggregated capacity of generation, storage, and transmission. 

The standard IAMC input/output is implemented for EMPIRE in the following way.

## Input

Work in progress.

The plan is to make a script reading the IAMC standardized values into Python and converting it to .tab-files that are used as input when solving EMPIRE in Pyomo. 

## Output
Once EMPIRE is solved as a linear program, its results are printed to .csv-files. The standardized IAMC print is a module that can be activated in the 'run.py' script of EMPIRE:

```python
IAMC_PRINT = True
``` 

This will make EMPIRE perform its old print in addition to the IAMC print. Using dictionaries for countries and generators, EMPIRE nomenclature is converted to IAMC standard nomenclature. All results are then appended row by row to a pandas DataFrame according to the IAMC format and finally printed/saved as a .csv-file.
