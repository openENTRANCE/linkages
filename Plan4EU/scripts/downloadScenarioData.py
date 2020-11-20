#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Import packages
import pyam
import pandas as pd ## necessary data analysis package
import fileinput
import os
import sys
import yaml

cfg={}
with open("settingsDownloadScenarioData.yml","r") as mysettings:
    cfg=yaml.load(mysettings,Loader=yaml.FullLoader)



pyam.iiasa.set_config(cfg['user'],cfg['password'])
pyam.iiasa.Connection('openentrance')
# upload of relevant data from openentrance scenarii
# for variables :
	#	-needed to compute technologies MaxPower: 'Capacity|Electricity|all technologies (available)
	#	-needed to compute electricity demand: 'Final Energy|Electricity', 'Final Energy|Electricity|Heat', 
	# 					'Final Energy|Electricity|Transportation', (not yet available) (unit: PJ)
			# 'Final Energy|Electricity|Cooling (will not be available, value from plan4res DB will be used)
	#	-for computing investment costs  : 'CapitalCost|Electricity|<all technos> (not yet available) (unit: M€2015/MW)
	#	-for computing emissions per technologies : CO2 Emmissions|Electricity|<allgenerationtechnologies> (not yet available) (unit: tons)
	#	-for computing variable costs : VariableCost|Electricity||<all generation technologies> (not yet available)
	#	-for pumping: Pumping Efficiency|Electricity|Hydro|Pumped Storage (not yet available - unit:%)
	
df=pyam.read_iiasa('openentrance',model=cfg['model'],
	variable=cfg['listvariables'],
	region=cfg['listregionsScen'],year=cfg['years'],
	scenario=cfg['scenarios']
	)

#conversion final energy from PJ to MWh
df.convert_unit('PJ', to='MWh') #check wether this conversion already exist....

#regional aggregations
for reg in cfg['aggregateregions'].keys():
	df.aggregate_region(df.variable, region=reg, subregions=cfg['aggregateregions'][reg], append=True)	

#remove aggregated subregions
df=df.filter(region=cfg['listregionsPlan4eu'])
df=df.filter(year=cfg['years'])
	
output=cfg['outputpath']+cfg['model']+'__'+pd.to_datetime('today').strftime("%Y-%m-%d")+'.csv'
if os.path.exists(output):
	os.remove(output)
df.to_csv(output)
data=df.as_pandas(meta_cols=True)

