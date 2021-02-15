#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Import packages
import pyam
import pandas as pd ## necessary data analysis package
import fileinput
import os
import sys
import yaml
import nomenclature as nc
from include import append_df_to_excel

cfg={}
with open("settingsDownloadCreatePlan4eu.yml","r") as mysettings:
    cfg=yaml.load(mysettings,Loader=yaml.FullLoader)

if cfg['mode']=='platform':
	pyam.iiasa.set_config(cfg['user'],cfg['password'])
	pyam.iiasa.Connection('openentrance')

output=cfg['outputpath']+cfg['datagroups']['plan4res']['model']+'__'+pd.to_datetime('today').strftime("%Y-%m-%d")+'.csv'
if os.path.exists(output):
	os.remove(output)

vardict={}
with open("OpenEntrance_plan4eu_VariablesDict.yml","r") as myvardict:
	vardict=yaml.safe_load(myvardict)

timeseriesdict={}
with open("plan4euDictTimeSeries.yml","r") as mytimeseries:
	timeseriesdict=yaml.safe_load(mytimeseries)

# opening input excel file and get parameters
###############################################
inputfile=cfg['inputpath']+cfg['inputfile']
print('opening '+inputfile)
dataxls=pd.ExcelFile(inputfile)
paramZone=pd.read_excel(dataxls,'Parameter', usecols=[0,2],index_col=False, skiprows=1, skip_footer = 10) 
listdelete=[ 'Calendar' ,'UCBegin','UCEnd' ,'UCTimeStep' ,'UCScenarios' ,'SSVTimeStep' ,'DataScenarios' ,'Mode']
paramZone=paramZone[ ~paramZone.Name.isin(listdelete)]
paramZone=paramZone.dropna()
NbSkipRows=len(pd.read_excel(dataxls,'Parameter', index_col=False, skiprows=1, skip_footer = 10, header=None))-6
paramDate=pd.read_excel(dataxls,'Parameter', index_col=False, skiprows=NbSkipRows, skipfooter=5, header=None)
years=pd.to_datetime(paramDate[2],format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y').tolist()

# upload of relevant data from platform
# creation of a csv file and a pandas dataframe containing all data
#########################################################"
i=0

if cfg['mode']=='platform':
	for datagroup in cfg['datagroups'].keys():
		groupdf=pyam.read_iiasa('openentrance',model=cfg['datagroups'][datagroup]['model'],
	variable=cfg['datagroups'][datagroup]['listvariables'],
	region=cfg['datagroups'][datagroup]['listregionsGET'],year=years[0],
	scenario=cfg['datagroups'][datagroup]['scenario']
	)
		if i==0:
			df=groupdf
			i=1
		else:
			df=df.append(groupdf)
			
else:
	file=cfg['inputfilepath']+cfg['inputdata']
	df=pyam.IamDataFrame(data=file)
	
#regional aggregations 
for datagroup in cfg['datagroups'].keys():
	if isinstance(cfg['datagroups'][datagroup]['aggregateregions'],dict) :
		for reg in cfg['datagroups'][datagroup]['aggregateregions'].keys():
			df.aggregate_region(df.variable, region=reg, subregions=cfg['datagroups'][datagroup]['aggregateregions'][reg], append=True)	

#remove aggregated subregions
if cfg['mode']=='platform':
	df=df.filter(region=cfg['partition']['Level1'])
df=df.filter(year=years)

#conversion final energy from PJ to MWh
#df=df.convert_unit('PJ', to='MWh') #check wether this conversion already exist....
df=df.convert_unit('GW', to='MW') #check wether this conversion already exist....

bigdata=df.as_pandas(meta_cols=True)

if cfg['mode']=='platform': df.to_csv(output,mode='a',header=False)
		
# creation of plan4eu dataset
################################"

# filling sheet ZP_ZonePartition
print('Treating ZonePartition')
#myregions = pd.Series(cfg['listregionsPlan4eu'])
dictzone = dict(zip(paramZone['Name'], paramZone['Partition']))
nbreg=len(cfg['partition']['Level1'])
nbpartition=len(cfg['partition'])

ZP = pd.DataFrame(columns=list(cfg['partition'].keys()),index=range(nbreg))
for partition in list(cfg['partition'].keys()):
	ZP[partition]=pd.Series(cfg['partition'][partition],name=partition,index=range(nbreg))
	
append_df_to_excel(inputfile, ZP, sheet_name='ZP_ZonePartition', index=False, startrow=0)

# filling sheet ZV_ZoneValues
print('Treating ZoneValues')
datapartition=bigdata[ bigdata.variable.isin(vardict['VarZV'].values()) ]
datapartition=datapartition.rename(columns={"variable": "Type", "region": "Zone", "unit":"Unit"})

# rename variables using OpenEntrance_plan4eu_VariablesDict
# create reverse dict
dictZV={}
dictZV=vardict['VarZV']
reversedictZV={}
for key, values in dictZV.items():
	for value in values:
		myvalue=dictZV[key]
		reversedictZV[myvalue]=key
datapartition=datapartition.replace({"Type":reversedictZV})

# include timeseries names from plan4euDictTimeSeries
for row in datapartition.index:
	if datapartition.loc[row,'Type'] in timeseriesdict['ZV'].keys():
		datapartition.loc[row, 'Profile_Timeserie']=timeseriesdict['ZV'][datapartition.loc[row,'Type']][datapartition.loc[row,'Zone']]

y=0	
for year in years:
	yearsdel=years.remove(year)
	datapartitionyear=datapartition
	if isinstance(yearsdel,list):
		if len(yearsdel)>0:
			datapartitionyear=datapartitionyear.drop(datapartition.columns[yearsdel], axis='columns')
	datapartitionyear.rename(columns={year:"value"})
	
	if y==0: 
		ZV=datapartitionyear
		y=1
	else:
		ZV.append(datapartitionyear)

columnsZV=['Type','Zone','value','Profile_Timeserie','Unit','year']
ZV=ZV[columnsZV]	
append_df_to_excel(inputfile, ZV, sheet_name='ZV_ZoneValues', index=False, startrow=0)


# filling sheet IN_Interconnections

print('Treating Interconnections')
listvariables=[]
for variable in list(vardict['VarIn'].keys()):
	oevar=vardict['VarIn'][variable]['variable']
	listvariables.append(oevar)

datainterco=bigdata[ bigdata.variable.isin(listvariables) ]
datainterco=datainterco.reset_index(drop=True)
startendline=pd.DataFrame(datainterco.region.str.split('>').tolist())
startendline=startendline.reset_index(drop=True)
datainterco=datainterco.join(startendline)

v=0
for variable in list(vardict['VarIn'].keys()):
	dataintercovariable=datainterco [ datainterco.variable==vardict['VarIn'][variable]['variable'] ]
	#dataintercovariable=dataintercovariable.reset_index(drop=True)
	valeur=dataintercovariable['value']
	valeur=valeur.rename(variable)
	dataintercovariable=dataintercovariable.join(valeur)
	if v==0:
		newdatainterco=dataintercovariable
		v=1
	else:
		newdatainterco=newdatainterco.append(dataintercovariable)
newdatainterco=newdatainterco.rename(columns={"region": "Name", 0:"StartLine", 1:"EndLine",'year':"Year"})
newdatainterco['Type']='AC'
newdatainterco['Direction']='Bidirectional'
newdatainterco=newdatainterco[['Name','Type','Direction','StartLine','EndLine','MaxPowerFlow','MinPowerFlow','Impedance','Year']]
#newdatainterco=newdatainterco.groupby(['Name','Type','Direction','StartLine','EndLine','Year']).agg({'MaxPowerFlow':sum,'MinPowerFlow':sum,'Impedance':sum })
newdatainterco=newdatainterco.groupby(['Name','Type','Direction','StartLine','EndLine','Year']).sum().reset_index()
print(newdatainterco)
print(newdatainterco.columns)
append_df_to_excel(inputfile, newdatainterco, sheet_name='IN_Interconnections', index=False, startrow=1)



# filling sheet TU_ThermalUnits

print('Treating ThermalUnits')
listvar=[]
for variable in list(vardict['VarTU'].keys()):
	oevar=vardict['VarTU'][variable]['variable']
	if variable!='NumberUnits':
		listvar.append(oevar)
	
v=0
for oetechno in cfg['datagroups']['scenario']['technos']['thermal']:
	print('traitement ',oetechno)
	# get capacity per region for the current technology
	capacitytechnovar='Capacity|Electricity|'+oetechno
	datacapa=bigdata [ bigdata.variable==capacitytechnovar ]
	datacapa=datacapa.set_index('region')
	
	TU=pd.DataFrame({'Name':oetechno,'region':cfg['partition']['Level1']})
	TU=TU.set_index('region')
	capacity=datacapa[['value']]
	for region in cfg['partition']['Level1']:
		if region not in capacity.index:
			capacity.loc[region]=0.0
	TU=pd.concat([TU, capacity], axis=1)
	TU=TU.rename(columns={"value":"Capacity"})
	
	#find corresponding plan4res techno
	if vardict['technosgenesys2p4r'][oetechno]['varp4r']!='None' and cfg['sourcetechnodata']=='plan4resdata':
		p4rtechno=vardict['technosgenesys2p4r'][oetechno]['varp4r']
		# create list of plan4res variables
		listvariables=[]
		for var in listvar:
			vartechno=var+p4rtechno
			listvariables.append(vartechno)
	 
		# get sub dataframes with all variables for the given techno
		datainter=bigdata[ bigdata.variable.isin(listvariables) ]
		data= datainter[ datainter.region.isin(cfg['partition']['Level1']) ]
		data=data.set_index('region')
		
		# get plan4res variables for the given techno
		for varp4r in vardict['VarTU'].keys():
			if varp4r != 'NumberUnits':
				print('treat via p4r database variable ',varp4r)
				subdata=data [ data.variable==vardict['VarTU'][varp4r]['variable']+p4rtechno ]
				subdata=subdata.rename(columns={"value":varp4r})
				newcol=subdata[[varp4r]]
				
				# treat case variable does not exist in plan4res database
				for region in cfg['partition']['Level1']:
					if region not in newcol.index:
						print('no data in p4r database for techno ',oetechno,' variable ',varp4r,' in region ',region)
						newcol.loc[region]=[ cfg['defaultvalues'][oetechno][varp4r] ]
						print('replaced by value from config file ',cfg['defaultvalues'][oetechno]['MaxPower'])
				TU=pd.concat([TU, newcol], axis=1)

	else:
		print('treat via dictionnary variable ',oetechno)
		for varp4r in vardict['VarTU'].keys():
			if varp4r != 'NumberUnits':
				TU[varp4r]=cfg['defaultvalues'][oetechno][varp4r]
	
	TU['NumberUnits']=round(TU['Capacity']/TU['MaxPower'])
	
	if v==0:
		BigTU=TU
		v=1
	else:
		BigTU=BigTU.append(TU)
	
TUColumns=['Name','Zone','NumberUnits','Capacity']
for varp4r in vardict['VarTU'].keys():
	if varp4r != 'NumberUnits':
		TUColumns.append(varp4r)

BigTU=BigTU[BigTU.NumberUnits >0]

BigTU['Zone']=BigTU.index
BigTU=BigTU[TUColumns]
append_df_to_excel(inputfile, BigTU, sheet_name='TU_ThermalUnits', index=False, startrow=1)

# filling sheet SS_SeasonalStorage and STS_ShortTermStorage

print('Treating SeasonalStorage and ShortTerStorage')
listvarSS=[]
listvarSTS=[]
for variable in list(vardict['VarSS'].keys()):
	oevar=vardict['VarSS'][variable]['variable']
	if variable!='NumberUnits':
		listvarSS.append(oevar)
for variable in list(vardict['VarSTS'].keys()):
	oevar=vardict['VarSTS'][variable]['variable']
	if variable!='NumberUnits':
		listvarSTS.append(oevar)
	
oetechno=cfg['datagroups']['scenario']['technos']['hydro']
print('traitement ',oetechno)
# get capacity per region for the current technology
capacitytechnovar='Capacity|Electricity|'+oetechno
datacapa=bigdata [ bigdata.variable==capacitytechnovar ]
datacapa=datacapa.set_index('region')

HydroScen=pd.DataFrame({'Name':oetechno,'region':cfg['partition']['Level1']})
HydroScen=HydroScen.set_index('region')
capacity=datacapa[['value']]
for region in cfg['partition']['Level1']:
	if region not in capacity.index:
		capacity.loc[region]=0.0
HydroScen=pd.concat([HydroScen, capacity], axis=1)
HydroScen=HydroScen.rename(columns={"value":"Capacity"})

#find corresponding plan4res technos
if cfg['sourcetechnodata']=='plan4resdata':
	# compute capacities of reservoir, pumped storage and run of river
	
	# build list of p4r maxpower variables
	listpmaxvariables=[]
	for tecp4r in vardict['technosgenesys2p4r'][oetechno]['varp4r']:
		listpmaxvariables.append('Maximum Active power|Electricity|'+tecp4r)
		# get sub dataframes with all variables 
	
	# get plan4res maxpower for all kind of hydro units
	datainter=bigdata[ bigdata.variable.isin(listpmaxvariables) ]
	capacity= datainter[ datainter.region.isin(cfg['partition']['Level1']) ]
	capacity = capacity.set_index('region')
	capacity=capacity.rename(columns={"value":'Capacity'})
	name=capacity['variable'].str.split("|",expand=True)
	capacity['Name']=name[2]+'|'+name[3]		
	capacity=capacity[['Name','Capacity']]
	reservoircapacity=capacity[ capacity.Name.isin(['Hydro|Reservoir'])]
	pumpedstoragecapacity=capacity[ capacity.Name.isin(['Hydro|Pumped Storage'])]
	rorcapacity=capacity[ capacity.Name.isin(['Hydro|Run of River'])]
	
	# compute real capacity given scenario total capacity
	totalcapacity=capacity.groupby(capacity.index).sum()
	HydroScen['Reservoir Capacity']=reservoircapacity['Capacity']*HydroScen['Capacity']/totalcapacity['Capacity']
	HydroScen['Pumped Storage Capacity']=pumpedstoragecapacity['Capacity']*HydroScen['Capacity']/totalcapacity['Capacity']
	HydroScen['Run of River Capacity']=rorcapacity['Capacity']*HydroScen['Capacity']/totalcapacity['Capacity']
	HydroScen=HydroScen.fillna(0)
	
	#filling data for SS
	SS=	HydroScen[['Reservoir Capacity']]
	SS['Name']='Hydro|Reservoir'
	SS.rename(columns={"Capacity":'MaxPower'})

	for varp4r in vardict['VarSS'].keys():
		if varp4r != 'NumberUnits' and varp4r !='MaxPower':
			subdata=bigdata [ bigdata.variable==vardict['VarSS'][varp4r]['variable']+'Hydro|Reservoir' ]
			subdata=subdata.rename(columns={"value":varp4r})
			subdata=subdata.set_index('region')
			subdata=subdata[ subdata.index.isin(cfg['partition']['Level1']) ]
			newcol=subdata[[varp4r]]
			
			# treat case variable does not exist in plan4res database
			for region in cfg['partition']['Level1']:
				if region not in newcol.index:
					print('no data in p4r database for hydro reservoir '+varp4r+' in region '+region)
					newcol.loc[region]=cfg['defaultvalues']['Hydro|Reservoir'][varp4r] 
					print('replaced by value from config file ',cfg['defaultvalues']['Hydro|Reservoir'][varp4r])
			SS=pd.concat([SS, newcol], axis=1)
			
	#filling data for STS
	STS=	HydroScen[['Pumped Storage Capacity']]
	STS['Name']='Hydro|Pumped Storage'
	STS.rename(columns={"Capacity":'MaxPower'})

	for varp4r in vardict['VarSTS'].keys():
		if varp4r != 'NumberUnits' and varp4r !='MaxPower':
			subdata=bigdata [ bigdata.variable==vardict['VarSTS'][varp4r]['variable']+'Hydro|Pumped Storage' ]
			subdata=subdata.rename(columns={"value":varp4r})
			subdata=subdata.set_index('region')
			subdata=subdata[ subdata.index.isin(cfg['partition']['Level1']) ]
			newcol=subdata[[varp4r]]
			
			# treat case variable does not exist in plan4res database
			for region in cfg['partition']['Level1']:
				if region not in newcol.index:
					print('no data in p4r database for pumped storage '+varp4r+' in region '+region)
					newcol.loc[region]=cfg['defaultvalues']['Hydro|Pumped Storage'][varp4r]
					print('replaced by value from config file ',cfg['defaultvalues']['Hydro|Pumped Storage'][varp4r])
			STS=pd.concat([STS, newcol], axis=1)	
else:
	# filling sheets VarSS and VarSTS from dictionnary
	HydroScen['ExistsInflows']=HydroScen.index in timeseriesdict['SS']['Inflows']
	HydroScen['Reservoir Capacity']=HydroScen['Capacity'] * 1
	HydroScen['Pumped Storage Capacity']=HydroScen['Capacity']-HydroScen['Reservoir Capacity']
	HydroScen['Run of River Capacity']=0
	HydroScen=HydroScen.fillna(0)
	
	for varp4r in vardict['VarSS'].keys():
		if varp4r != 'NumberUnits' and varp4r != 'MaxPower':
			SS[varp4r]=cfg['defaultvalues']['Hydro|Reservoir'][varp4r]
		if varp4r=='MaxPower':
			SS[varp4r]=HydroScen['Reservoir Capacity']
	
	for varp4r in vardict['VarSTS'].keys():
		if varp4r != 'NumberUnits' and varp4r != 'MaxPower':
			STS[varp4r]=cfg['defaultvalues']['Hydro|Pumped Storage'][varp4r]
		if varp4r=='MaxPower':
			STS[varp4r]=HydroScen['Pumped Storage Capacity']
			
# include inflows profiles: include timeseries names from plan4euDictTimeSeries
SS['Profile_Timeserie']=''
for row in SS.index:
	if row in timeseriesdict['SS']['Inflows'].keys():
		SS.loc[row, 'InflowsProfile']=timeseriesdict['SS']['Inflows'][row]
SS['NumberUnits']=SS['Reservoir Capacity']>0
SS['NumberUnits']=SS['NumberUnits'].astype(int)

STS['NumberUnits']=STS['Pumped Storage Capacity']>0
STS['NumberUnits']=STS['NumberUnits'].astype(int)
		
SSColumns=['Name','Zone','NumberUnits','InflowsProfile']
for varp4r in vardict['VarSS'].keys():
	SSColumns.append(varp4r)
	
STSColumns=['Name','Zone','NumberUnits']
for varp4r in vardict['VarSTS'].keys():
	STSColumns.append(varp4r)

SS['Zone']=SS.index
STS['Zone']=STS.index

STS=STS.rename(columns={'Pumped Storage Capacity':'MaxPower'})
SS=SS.rename(columns={'Reservoir Capacity':'MaxPower'})

STS['MaxPrimaryPower']=STS['MaxPower']*STS['MaxPrimaryPower']
STS['MaxSecondaryPower']=STS['MaxPower']*STS['MaxSecondaryPower']


STS=STS[STSColumns]
SS=SS[SSColumns]
SS=SS[SS.NumberUnits >0]
STS=STS[STS.NumberUnits >0]

append_df_to_excel(inputfile, SS, sheet_name='SS_SeasonalStorage', index=False, startrow=1)
append_df_to_excel(inputfile, STS, sheet_name='STS_ShortTermStorage', index=False, startrow=1)

# treating res

print('Treating Renewable units')
listvarRES=[]
for variable in list(vardict['VarRES'].keys()):
	oevar=vardict['VarRES'][variable]['variable']
	if variable!='NumberUnits':
		listvarRES.append(oevar)

listtechno=cfg['datagroups']['scenario']['technos']['res']
print(listtechno)
listtechno.append('Hydro|Run of River')
print(listtechno)
v=0
for oetechno in listtechno:
	print('traitement ',oetechno)
	# get capacity per region for the current technology
	if oetechno=='Hydro|Run of River':
		data=pd.DataFrame({'value': HydroScen['Run of River Capacity']})
	else:
		capacitytechnovar='Capacity|Electricity|'+oetechno
		data=bigdata [ bigdata.variable==capacitytechnovar ]
		data=data.set_index('region')

	data['Name']=oetechno
	data=data.rename(columns = {"value":'MaxPower'})
	data=data[['MaxPower','Name']]

	if cfg['sourcetechnodata']=='plan4resdata':
		for varp4r in vardict['VarRES'].keys():
			if varp4r != 'NumberUnits' and varp4r !='MaxPower':
				subdata=bigdata [ bigdata.variable==vardict['VarSS'][varp4r]['variable']+'Hydro|Reservoir' ]
				subdata=subdata.rename(columns={"value":varp4r})
				subdata=subdata.set_index('region')
				newcol=subdata[[varp4r]]
				
				# treat case variable does not exist in plan4res database
				for region in cfg['partition']['Level1']:
					if region not in newcol.index:
						print('no data in p4r database for techno ',oetechno,' variable ',varp4r,' in region '+region)
						newcol.loc[region]=cfg['defaultvalues'][oetechno][varp4r]
						print('replaced by value from config file ',cfg['defaultvalues'][oetechno][varp4r])
				data=pd.concat([data, newcol], axis=1)
	else:
		for varp4r in vardict['VarRES'].keys():
			if varp4r != 'NumberUnits' and varp4r != 'MaxPower':
				data[varp4r]=cfg['defaultvalues'][oetechno][varp4r]
				
	# include res profiles: include timeseries names from plan4euDictTimeSeries
	data['Profile_Timeserie']=''
	for row in data.index:
		if row in timeseriesdict['RES'][oetechno].keys():
			data.loc[row, 'MaxPowerProfile']=timeseriesdict['RES'][oetechno][row]

	#include Gamma (1 for ror, mean(primaryrho,secondaryrho) for others
	if oetechno=='Hydro|Run of River':
		data['Gamma']=1
	else:
		#data['Gamma']=0.5*(data['PrimaryRho']+data['SecondaryRho'])
		data['Gamma']=0.5
	
	if v==0:
		RES=data
		v=1
	else:
		RES=RES.append(data)

RES['NumberUnits']=RES['MaxPower']>0
RES['NumberUnits']=RES['NumberUnits'].astype(int)

		
resColumns=['Name','Zone','NumberUnits','MaxPowerProfile']
for varp4r in vardict['VarRES'].keys():
	resColumns.append(varp4r)
	
RES['Zone']=RES.index

RES=RES[resColumns]
RES=RES[RES.NumberUnits >0]

append_df_to_excel(inputfile, RES, sheet_name='RES_RenewableUnits', index=False, startrow=1)

