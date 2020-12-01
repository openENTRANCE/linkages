# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 15:02:39 2020

@author: zwickl-nb
"""


# import required packages
import pandas as pd
import xlrd
import xlsxwriter
import os
import glob
from datetime import datetime, timedelta


def write_to_iamc_format():
    
    model_name = 'GUSTO v1.0' # define model name
    _variable = 'Final Energy|Electricity|Profile' # write variable to IAMC
    _unit = 'MW' # define corresponding variable unit
    
    # print(os.getcwdb())
    
    # os.path.join( os.path.dirname( __file__ ), '..' )
    
    
    # e = glob.glob(os.path.join(os.path.join( os.path.dirname( __file__ ), '..' )) # get all entries in "Output"
    # e.sort(key=lambda x: os.path.getmtime(x)) # sort entries by creation time
    # e = e[-1]

    name_files = os.listdir(os.getcwd()) # get all file names

    # only consider 'scenario*.xlsx' files
    for _n in reversed(range(len(name_files))):
        if not ('scenario_' in name_files[_n] and '.xlsx' in name_files[_n]):
            name_files.pop(_n)
        elif '$' in name_files[_n]:
            name_files.pop[_n]
   
    _scenarios = []
    _regions = []

    for _name in name_files:
        _string = _name.replace(
                'scenario_','').replace('.xlsx','').split('+')
        _scenarios.append(_string[0].replace('_',' '))
        _regions.append(_string[1].replace('_',' '))
    
    list_ts=[]
    
    for _file in name_files:
        worksheet = xlrd.open_workbook(filename=_file, on_demand=True)
        
        _dict = pd.read_excel(_file, sheet_name=None)
        _to_drop=[]
        
        for k in _dict.keys():
            if 'timeseries' in k:
                _dict[k] = _dict[k].drop(columns=['Unnamed: 0'])
                _dict[k].columns=_dict[k].loc[0,:]
                if 'Feed-in public grid' in _dict[k].columns:
                    _dict[k]=_dict[k].iloc[2:,][
                            'Supply from public grid']-_dict[k].iloc[2:,][
                                    'Feed-in public grid']
                else:
                   _dict[k]=_dict[k].iloc[2:,]['Supply from public grid'] 
                   pass
        
            else:
                _to_drop.append(k)
        
        for _d in _to_drop:    
            _dict.pop(_d)
            
            
        list_ts.append(sum(_dict.values()))
    
    # create IAMC-format template
    workbook = xlsxwriter.Workbook('GUSTO_results_annual_timeseries.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'model', bold)
    worksheet.write('B1', 'scenario', bold)
    worksheet.write('C1', 'region', bold)
    worksheet.write('D1', 'variable', bold)
    worksheet.write('E1', 'unit', bold)
    worksheet.write('F1', 'time', bold)
    worksheet.write('G1', 'value', bold)
        
    _string = "2030-01-01 00:00"
    _var_time = datetime.strptime(_string, '%Y-%m-%d %H:%M')
    
        
    # write data to IAMC format
    for index in range(len(_scenarios)):
        for _entry in range(len(list_ts[0])):
            worksheet.write('A'+str(
                    2+_entry+index*len(list_ts[0])), model_name)
            worksheet.write('B'+str(
                    2+_entry+index*len(list_ts[0])), _scenarios[index])
            worksheet.write('C'+str(
                    2+_entry+index*len(list_ts[0])), _regions[index])
            worksheet.write('D'+str(
                    2+_entry+index*len(list_ts[0])), _variable)
            worksheet.write('E'+str(
                    2+_entry+index*len(list_ts[0])), _unit)
            worksheet.write('F'+str(
                    2+_entry+index*len(list_ts[0])), str(
                            _var_time+timedelta(hours=_entry)
                            )+' +01:00')
            worksheet.write('G'+str(
                    2+_entry+index*len(
                            list_ts[0])), list_ts[index].iloc[_entry])
            
    workbook.close()
    
if __name__ == '__main__':
    write_to_iamc_format()