#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Import packages
import pandas as pd ## necessary data analysis package
import pyam
import nomenclature as nc
import fileinput
import yaml
import os
import sys

if len(sys.argv) <3:
	print('python imputdir outputdir')
else:
	inputdir=sys.argv[1]
	outputfile=sys.argv[2]

# open config file
with open("settingsUploadOutputsPlan4eu.yml","r") as myyaml:
    cfg=yaml.load(myyaml,Loader=yaml.FullLoader)

# compute date range
cfg['T'] = pd.date_range(start=pd.to_datetime(cfg['date_start']),end=pd.to_datetime(cfg['date_end']), freq='1H')	

#delete output file if already exists
if os.path.exists(outputfile):
	os.remove(outputfile)
	
i=0
	
# loop on outputfiles: 
# TO BE DONE: include scenarised outputs
if cfg['scenarios']>1:
	# compute list of files
	for file in cfg['listfiles']:
		namefile=file[0:-7]
		for i in range(cfg['scenarios']):
			listfiles.append(namefile+'_Scen'+i+'_OUT.csv')
else:
	listfiles=cfg['listfiles']
for file in listfiles:
	if file.find('Scen'):
		# find scenario number
		scen_index=file[0:-8].split('Scen')[1]
		scenario=cfg['scenario']+'|'+scen_index
		listscenarios.append(scenario)
	else:
		scenario=cfg['scenario']
		
	print('writing '+file)
	variable=cfg['listfiles'][file]
	print(variable)
	data=pd.read_csv(inputdir+'\\'+file)
	columns=list(data)
	data.drop(['Timestep'], axis='columns', inplace=True)
	for col in data.columns:
		print('dealing with column '+col)
		#count number of '_'
		Number_=col.count('_')	
		print(Number_)
		
		#split column name
		tech_reg_index=col.split('_')
		print(tech_reg_index)
		
		fill=0
		
		# files ActivePowerOUT, PrimaryOUT, SecondaryOUT, VolumeOUT
		if file=='ActivePowerOUT.csv' or file=='PrimaryOUT.csv' or file=='SecondaryOUT.csv' or file=='VolumeOUT.csv':
			print('fichier MWh')
			iamc_unit="MWh"
			techno=tech_reg_index[0]
			region=tech_reg_index[1]
			if Number_==2:
				print('hydro')
				# this is a hydro unit with pumping 
				# in ActivePowerOUT, PrimaryOUT, SecondaryOUT and VolumeOUT => there are 2 columns for the same unit, one for turbining and one for pumping
				if tech_reg_index[2]=='0':
					iamc_variable=cfg['listfiles'][file]+techno
				else:
					iamc_variable=cfg['pumping']+techno
			if Number_==1:
				print('autre')
				# this is all other kinds of units
				iamc_variable=cfg['listfiles'][file]+techno
			fill=1
		
		if file.find('Cost')>-1:
			print('cost')
			iamc_unit="euro/MWh"
			iamc_variable=cfg['listfiles'][file]
			region=col
			fill=1
				
		if file.find('Flow')>-1:
			print('flow')
			iamc_unit="MWh"	
			region=col
			iamc_variable=cfg['listfiles'][file]
			fill=1
		
		if fill==1:		
			iamc=pd.DataFrame({'Model':cfg['model'],'Scenario':scenario,'Region':region,'Variable':iamc_variable, 'Unit':iamc_unit,'time':cfg['T'],'value':data[col]})
			if i==0:
				big_iamc=iamc
				i=1
			else:
				big_iamc=pyam.concat(big_iamc,iamc)
			
# aggregate scenarios if more than 1
if cfg['scenarios']>1 and cfg['aggregate scenarios']=='yes':
	
	# aggregate the scenarios 
	###########################"
	
	# get pandas from iamc
	_data=big_iamc.data
	
	# group by scenarios and get mean
	_meandata=_data.groupby('Scenario').mean().reset_index()
	_meandata['Scenario']=cfg['scenario']
	_meandata=_meandata[['Model','Scenario','Region','Variable','Unit','time','value']]
				
	# convert to iamc
	big_iamc=pd.DataFrame({'Model':_meandata['Model'],'Scenario':_meandata['Scenario'],'Region':_meandata['Region'],'Variable':_meandata['Variable'], 'Unit':_meandata['Unit'],'time':_meandata['time'],'value':_meandata['value']})
			
big_iamc.to_csv(outputfile,index=False,mode='w',header=True)
			
	
	