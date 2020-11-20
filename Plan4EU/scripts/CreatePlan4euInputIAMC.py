#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Import packages
import pandas as pd ## necessary data analysis package
import pyam
import nomenclature as nc
import fileinput
import os
import sys
import yaml

# parameters and dictionnaries
cfg={}
with open("settingsCreatePlan4euInputIAMC.yml","r") as mysettings:
	cfg=yaml.safe_load(mysettings)

vardict={}
with open("OpenEntrance_plan4ey_VariablesDict.yml","r") as myvardict:
	vardict=yaml.safe_load(myvardict)

with open('..\\Nomenclature\\nomenclature\\definitions\\region\\countries.yaml',"r") as mycountries:
    dict_reg=yaml.safe_load(mycountries)

# create reverse dictionnary
plan4euRegDict={}

# include countries
for key, values in dict_reg.items():
	for value in values:
		if value=='iso2' or value=='iso2_alt':
			myvalue=dict_reg[key][value]
			plan4euRegDict[myvalue]=key

# add additional regions
for aggreg in cfg['regions']:
	plan4euRegDict[aggreg]=cfg['regions'][aggreg]

inputfile=cfg['inputpath']+cfg['inputfile']
outputfile=cfg['outputpath']+cfg['model']+'__'+cfg['scenario']+'.csv'
	
## open input data file	
print('opening '+inputfile)
dataxls=pd.ExcelFile(inputfile)
	
if os.path.exists(outputfile):
	os.remove(outputfile)

# Sheet IN_Interconnections
####################################################################################
print('treating interconnections')
interco = pd.read_excel(dataxls,'IN_Interconnections', index_col=False, skiprows=2, header=None) 

# converting region names from plan4eu to OpenEntrance
interco.columns=['Name','Type','direction','StartLine','EndLine','MaxPowerFlow','MinPowerFlow','Impedance','year']
interco=interco.replace({"StartLine":plan4euRegDict})
interco=interco.replace({"EndLine":plan4euRegDict})
interco=interco.dropna()

# creating names of transmission lines
start=interco['StartLine']
end= interco['EndLine']
iamc_line=start+">"+end
interco=interco.dropna()

# creation variables 
i=0
#for name_plan4eu in (varIN.columns):
for name_plan4eu in vardict['VarIn'].keys():
	iamc_value=interco[name_plan4eu]
	iamc_unit=vardict['VarIn'][name_plan4eu]['unit']
	iamc_variable=vardict['VarIn'][name_plan4eu]['variable']

	iamc=pd.DataFrame({'Model':cfg['model'],'Scenario':cfg['scenario'],'Region':iamc_line,'Variable':iamc_variable, 'Unit':iamc_unit,'2050':iamc_value})

	if i==0:
		# first variable => include header
		iamc.to_csv(outputfile,index=False)
		i=1
	else:
		iamc.to_csv(outputfile,index=False,mode='a',header=False)

# Sheet ZV_ZoneValue
####################################################################################
print('treatement ZV_ZoneValues ') 
sheet = pd.read_excel(dataxls,'ZV_ZoneValues', index_col=False) 

# converting region and variable names from plan4eu to OpenEntrance
sheet=sheet.replace({"Zone":plan4euRegDict})
sheet=sheet.replace({"Type":vardict['VarZV']})

# drop useless lines
indexnames=sheet[sheet['Type'].isin(cfg['DropLines'])].index
sheet.drop(indexnames,inplace=True)

# getting values
iamc_region=sheet['Zone']
iamc_variable=sheet['Type']
iamc_value=sheet['value']
iamc_unit=sheet['Unit']

iamc=pd.DataFrame({'Model':cfg['model'],'Scenario':cfg['scenario'],'Region':iamc_region,'Variable':iamc_variable, 'Unit':iamc_unit,'2050':iamc_value})
iamc=iamc.dropna()

if i==0:
	# first variable => include header
	iamc.to_csv(outputfile,index=False)
	i=1
else:
	iamc.to_csv(outputfile,index=False,mode='a',header=False)

# Treatment technologies sheets
####################################################################################

for key, value in vardict['technos_list'].items():
	print('treatment '+value)
	sheet = pd.read_excel(dataxls,value, index_col=False,header=1) 

	#delete lines with 0 units
	sheet=sheet[ sheet.NumberUnits>0 ]

	# converting region names from plan4eu to OpenEntrance
	sheet=sheet.replace({"Zone":plan4euRegDict})
	sheet=sheet.replace({"Name":vardict['technos']})

	iamc_region=sheet['Zone']
	iamc_techno=sheet['Name']

	for name_plan4eu in vardict[key].keys():
		iamc_value=sheet[name_plan4eu]
		iamc_unit=vardict[key][name_plan4eu]['unit']
		iamc_variable=vardict[key][name_plan4eu]['variable']+iamc_techno
		
		#conversion needed?
		if name_plan4eu in vardict['conversion'].keys():
			if vardict['conversion'][name_plan4eu] == 'DivideByMaxPower':
				iamc_value=iamc_value/sheet['MaxPower']

		iamc=pd.DataFrame({'Model':cfg['model'],'Scenario':cfg['scenario'],'Region':iamc_region,'Variable':iamc_variable, 'Unit':iamc_unit,'2050':iamc_value})
		iamc.to_csv(outputfile,index=False,mode='a',header=False)
nc.validate(outputfile)



