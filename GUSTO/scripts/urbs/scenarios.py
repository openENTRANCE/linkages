import pandas as pd
import os

def scenario_baseline(data, ub):
    return data


########################################################################################################################
# Model Energy Communities (MEC)S

def scenario_City_EC(data, ub):
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')['LMAB'].values
    data['demand']['LMAB1', 'Elec'] = _demand
    data['demand']['LMAB2', 'Elec'] = _demand
    data['demand']['LMAB3', 'Elec'] = _demand
    data['demand']['LMAB4', 'Elec'] = _demand
    data['demand']['LMAB5', 'Elec'] = _demand
    data['demand']['LMAB6', 'Elec'] = _demand
    data['demand']['LMAB7', 'Elec'] = _demand
    data['demand']['LMAB8', 'Elec'] = _demand
    data['demand']['LMAB9', 'Elec'] = _demand
    data['demand']['LMAB10', 'Elec'] = _demand

    pro = data['process']
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'inst-cap'] = 15
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'cap-up'] = 15
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'inst-cap'] = 55
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'cap-up'] = 55
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'inst-cap'] = 55
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'cap-up'] = 55


    pro = data['storage']
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-c'] = 65
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-c'] = 65
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-c'] = 65
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-p'] = 8
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-p'] = 8
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-p'] = 8

    return data


def scenario_Rural_EC(data, ub):
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')
    _demand1 = _demand['SFH1'].values
    _demand2 = _demand['SFH2'].values
    _demand3 = _demand['SFH3'].values

    data['demand']['LMAB1', 'Elec'] = _demand1
    data['demand']['LMAB2', 'Elec'] = _demand1
    data['demand']['LMAB3', 'Elec'] = _demand1
    data['demand']['LMAB4', 'Elec'] = _demand2
    data['demand']['LMAB5', 'Elec'] = _demand2
    data['demand']['LMAB6', 'Elec'] = _demand2
    data['demand']['LMAB7', 'Elec'] = _demand3
    data['demand']['LMAB8', 'Elec'] = _demand3
    data['demand']['LMAB9', 'Elec'] = _demand3
    data['demand']['LMAB10', 'Elec'] = _demand1

    pro = data['process']
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'inst-cap'] = 5
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'cap-up'] = 5
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'inst-cap'] = 5
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'cap-up'] = 5
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'inst-cap'] = 5
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'cap-up'] = 5

    pro = data['storage']
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-c'] = 8
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-c'] = 8
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-c'] = 8
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-p'] = 5
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-p'] = 5
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-p'] = 5

    return data


def scenario_Town_EC(data, ub):
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')['SMAB'].values
    data['demand']['LMAB1', 'Elec'] = _demand
    data['demand']['LMAB2', 'Elec'] = _demand
    data['demand']['LMAB3', 'Elec'] = _demand
    data['demand']['LMAB4', 'Elec'] = _demand
    data['demand']['LMAB5', 'Elec'] = _demand
    data['demand']['LMAB6', 'Elec'] = _demand
    data['demand']['LMAB7', 'Elec'] = _demand
    data['demand']['LMAB8', 'Elec'] = _demand
    data['demand']['LMAB9', 'Elec'] = _demand
    data['demand']['LMAB10', 'Elec'] = _demand

    pro = data['process']
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'inst-cap'] = 8
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'cap-up'] = 8
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'inst-cap'] = 16
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'cap-up'] = 16
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'inst-cap'] = 16
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'cap-up'] = 16

    pro = data['storage']
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-c'] = 20
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-c'] = 20
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-c'] = 20
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-p'] = 5
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-p'] = 5
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-p'] = 5

    return data


def scenario_Mixed_EC(data, ub):
    data = scenario_Rural_EC(data, ub)
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')['LMAB'].values
    data['demand']['LMAB9', 'Elec'] = _demand
    data['demand']['LMAB10', 'Elec'] = _demand

    pro = data['process']
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
                pro.index.get_level_values('Process') == 'Solar|PV')), 'inst-cap'] = 15
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Process') == 'Solar|PV')), 'cap-up'] = 15
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
                pro.index.get_level_values('Process') == 'Solar|PV')), 'inst-cap'] = 15
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Process') == 'Solar|PV')), 'cap-up'] = 15

    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
                pro.index.get_level_values('Process') == 'Supply from public grid')), 'inst-cap'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Process') == 'Supply from public grid')), 'cap-up'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
                pro.index.get_level_values('Process') == 'Supply from public grid')), 'inst-cap'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Process') == 'Supply from public grid')), 'cap-up'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
                pro.index.get_level_values('Process') == 'Feed-in public grid')), 'inst-cap'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Process') == 'Feed-in public grid')), 'cap-up'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
                pro.index.get_level_values('Process') == 'Feed-in public grid')), 'inst-cap'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Process') == 'Feed-in public grid')), 'cap-up'] = 60

    pro = data['storage']
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'inst-cap-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-lo-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-up-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'inst-cap-p'] = 8
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-lo-p'] = 8
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-up-p'] = 8

    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'inst-cap-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-lo-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-up-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'inst-cap-p'] = 8
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-lo-p'] = 8
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-up-p'] = 8

    return data


def scenario_Austria(data, ub):
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')
    _solar = _solar.loc[_solar['region'] == 'Austria']

    data['supim']['LMAB1', 'Solar'] = _solar['value'].values
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    _price = pd.read_excel('files/EMPSW_elprices_mean.xlsx')
    _price = _price.loc[_price['region'] == 'Norway|Vestmidt']['2030'].values
    data['buy_sell_price']['Elec buy',] = _price
    data['buy_sell_price']['Elec sell',] = _price * 0.98  # to prevent buying and selling at same time step.

    return data

def scenario_IBERIAN(data, ub):
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')
    _solar = _solar.loc[_solar['region'] == 'ES11']

    data['supim']['LMAB1', 'Solar'] = _solar['value'].values
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    _price = pd.read_excel('files/EMPSW_elprices_mean.xlsx')
    _price = _price.loc[_price['region'] == 'Norway|Vestmidt']['2030'].values
    data['buy_sell_price']['Elec buy',] = _price
    data['buy_sell_price']['Elec sell',] = _price * 0.98  # to prevent buying and selling at same time step.

    return data


def scenario_Norway(data, ub):
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')
    _solar = _solar.loc[_solar['region'] == 'Norway|Vestmidt']

    data['supim']['LMAB1', 'Solar'] = _solar['value'].values
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    _price = pd.read_excel('files/EMPSW_elprices_mean.xlsx')
    _price = _price.loc[_price['region'] == 'Norway|Vestmidt']['2030'].values
    data['buy_sell_price']['Elec buy',] = _price
    data['buy_sell_price']['Elec sell',] = _price * 0.98  # to prevent buying and selling at same time step.
    print(data['supim'])

    return data

########################################################################################################################
########################################################################################################################
########################################################################################################################
# AUSTRIA

def scenario_Societal_CommitmentxAustriaxCityEC(data, ub):
    data = scenario_City_EC(data, ub)
    data = scenario_Austria(data, ub)
    return data


def scenario_Societal_CommitmentxAustriaxTownEC(data, ub):
    data = scenario_Town_EC(data, ub)
    data = scenario_Austria(data, ub)
    return data


def scenario_Societal_CommitmentxAustriaxMixedEC(data, ub):
    data = scenario_Mixed_EC(data, ub)
    data = scenario_Austria(data, ub)
    return data


def scenario_Societal_CommitmentxAustriaxRuralEC(data, ub):
    data = scenario_Rural_EC(data, ub)
    data = scenario_Austria(data, ub)
    return data

########################################################################################################################
# SPAIN & PORTUGAL (IBERIAN PENINSULA)

def scenario_SocietalxCommitmentxIBERIANxCityEC(data, ub):
    data = scenario_City_EC(data, ub)
    data = scenario_IBERIAN(data, ub)

    return data

def scenario_SocietalxCommitmentxIBERIANxTownEC(data, ub):
    data = scenario_Town_EC(data, ub)
    data = scenario_IBERIAN(data, ub)

    return data

def scenario_SocietalxCommitmentxIBERIANxMixedEC(data, ub):
    data = scenario_Mixed_EC(data, ub)
    data = scenario_IBERIAN(data, ub)

    return data

def scenario_SocietalxCommitmentxIBERIANxRuralEC(data, ub):
    data = scenario_Mixed_EC(data, ub)
    data = scenario_IBERIAN(data, ub)

    return data

########################################################################################################################
# NORWAY

def scenario_SocietalxCommitmentxNORWAY_RURALEC(data, ub):
    data = scenario_Rural_EC(data, ub)
    data = scenario_Norway(data, ub)
    return data


########################################################################################################################
########################################################################################################################
########################################################################################################################

def scenario_SocietalxCommitment_Norway(data, ub):
    # set solar radiation or Loadfactor|Electricity|Solar accordingly 
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')
    _solar = _solar.loc[_solar['region']=='Norway|Vestmidt']
    data['supim']['LMAB1', 'Solar'] = _solar['value'].values
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values
    # print( data['supim']['LMAB10', 'Solar'])
    
    
    # set electricity demand of the buidlings within the neighborhood
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')
    _demand1 = _demand['SFH1'].values
    _demand2 = _demand['SFH2'].values
    _demand3= _demand['SFH3'].values
    
    data['demand']['LMAB1', 'Elec'] = _demand1
    data['demand']['LMAB2', 'Elec'] = _demand1
    data['demand']['LMAB3', 'Elec'] = _demand1
    data['demand']['LMAB4', 'Elec'] = _demand2
    data['demand']['LMAB5', 'Elec'] = _demand2
    data['demand']['LMAB6', 'Elec'] = _demand2
    data['demand']['LMAB7', 'Elec'] = _demand3
    data['demand']['LMAB8', 'Elec'] = _demand3
    data['demand']['LMAB9', 'Elec'] = _demand3
    data['demand']['LMAB10', 'Elec'] = _demand1
    # print(data['demand']['LMAB10', 'Elec'])
    
    _price = pd.read_excel('files/EMPSW_elprices_mean.xlsx')
    _price = _price.loc[_price['region']=='Norway|Vestmidt']['2030'].values
    data['buy_sell_price']['Elec buy', ] = _price
    data['buy_sell_price']['Elec sell', ] = _price*0.98 # to prevent buying and selling at same time step.
    # print(data['buy_sell_price']['Elec sell', ])
    return data


def scenario_Austrian_RuralxEC(data, ub):
    data = scenario_SocietalxCommitment_Norway(data, ub)

    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')
    _solar = _solar.loc[_solar['region'] == 'Austria']
    data['supim']['LMAB1', 'Solar'] = _solar['value'].values
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    return data

def scenario_Austria_TownxEC(data, ub):
    data = scenario_Austrian_RuralxEC(data, ub) # set solar profile and electricity price accordingly

    # set demand profiles in the EC
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')['SMAB'].values
    data['demand']['LMAB1', 'Elec'] = _demand
    data['demand']['LMAB2', 'Elec'] = _demand
    data['demand']['LMAB3', 'Elec'] = _demand
    data['demand']['LMAB4', 'Elec'] = _demand
    data['demand']['LMAB5', 'Elec'] = _demand
    data['demand']['LMAB6', 'Elec'] = _demand
    data['demand']['LMAB7', 'Elec'] = _demand
    data['demand']['LMAB8', 'Elec'] = _demand
    data['demand']['LMAB9', 'Elec'] = _demand
    data['demand']['LMAB10', 'Elec'] = _demand

    pro = data['process']
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'),'inst-cap'] = 8
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'cap-up'] = 8
    print(data['process'])

    return data
