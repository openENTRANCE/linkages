# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 10:30:40 2020

read eTransport data and 
convert to pickle for faster handling in python

do data handling in other scripts


read back in and write back to excel

@author: sarahs
"""


#IMPORTANT - this is for a minor test case!

import pandas as pd
import manipulateData_readGenesysModData4eTransport as a

        
#project folder
path_et = "C:/Users/sarahs/Desktop/sintef/OE - local/case study 6/"
path_et_adj = "C:/Users/sarahs/Desktop/sintef/OE - local/case study 6/adj/"
filename_in_out = "CASE_299_ATTR.xlsx"



#read from excel
data_eTrans = pd.read_excel(path_et + filename_in_out)
#dump to pickl
data_eTrans.to_pickle(path_et + "./eTrans_Furuset.pkl")


#run manipulate data script
a.manipulate()


#read from pickle
data_final = pd.read_pickle(path_et_adj + "eTrans_Furuset_adj.pkl")
#dump t excel
data_final.to_excel(path_et_adj + filename_in_out)
