# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 08:51:09 2020

@author: sarahs
"""
import pandas as pd
import re

#f = open('MASKENETT.DATA')
#transmission_data = f.read()


def readMaskenett():
    td = {} #transmission data
    counter = 0
    
    with open('MASKENETT.DATA', 'r') as f:
        for line in f:
            #line = line.strip()
            td[counter] = line#.split()
            counter = counter +1
            #print(repr(line))    
    return td



def print2dotData(filename, maskenett):
    with open(filename, 'a', encoding="iso-8859-1", errors="ignore") as file:
        for element in maskenett:
         file.write(element)
         file.write('\n')
    file.close()



##############################################################################
# STEP 0 : define names, parameters, path, etc.
# some user input requiered here: 
# if you want to udate an existing file set to 1
# if you want to recycle only some data from a preexisting file, set to 2
# if you want to create a new file from scratch, set to 0
recycle = 2

#! if you are creating a whole new file please enter here the data for the first row as a string:
# following this setup: ["""version_nbr, 'MASKENETT', nbr_prisavsnitt,"""]
first_row_MASKENETT = []
# if recycle :
#     sdf
#     else:
#         first_row_MASKENETT
    
path_in = ''
filename_in = "MASKENETT.DATA"
filename_out = "MASKENETT.DATA"

#if you are adding som new regions please provide them in an excel file
#Format: 2 columns; 1 column: region names, 2 column: region number in dataset
filename_new_regions = 'region_codes_spain.xlsx'

fnut = """'"""


#########################################################################3
# STEP 1 - read in existing Maskenett file (if you want to use some of the existing info)

if recycle in [1,2]: #if some/all existing data should be used
    #1 read existig data - each line as a list entry to a dict
    trans_data = readMaskenett() 
    first_row_MASKENETT = trans_data[0]
    #2: for easier processing we get temporarily rid of header (first line) 
    del trans_data[0]

    # create separate dataframes for each block (line) of data (4 different)
    type = ['del2a','b','c','d']
    nbrRowsBlock = 4 
    count = list(range(int((len(trans_data) - 5)/nbrRowsBlock)-1)) # 5: last block is different
    counter = 1
    trans_data_sep = {}
    for t in type:
        tmp = {}
        for c in count:
            tmp[c] = trans_data[(c)*nbrRowsBlock+counter]
        counter = counter+1
        trans_data_sep[t] = tmp
    

#########################################################################3
# STEP 2 - format new content to match MASKENETT style



#read in region numbers and region names
regions_new = pd.read_excel(filename_new_regions)

# read in data from Tepes
filename = 'oT_IAMC_openTEPES_SEP2030oE.csv'
trans_data_TEPES = pd.read_csv(filename)
#extract capacity
capacity = "Maximum Flow|Electricity|Transmission|Line"
trans_data_TEPES_cap = trans_data_TEPES.loc[trans_data_TEPES.Variable == capacity].reset_index(drop = True)
#extract losses
losses = "Loss Factor|Electricity|Transmission|Line"
trans_data_TEPES_los = trans_data_TEPES.loc[trans_data_TEPES.Variable == losses].reset_index(drop = True)

#extract info from region
col_reg = trans_data_TEPES_cap.Region.reset_index(drop = True)
#get rid of |cc1
col_reg = col_reg.str[0:9]

# now we go through the list and convert it to masknett style
count = list(range(int(len(trans_data_TEPES_cap))))

#initiate dataframe for del2a
#del2a_Tepes = pd.DataFrame(columns=['nbr1', 'reg1', 'nbr2', 'reg2'])
del2a_Tepes = []#['nbr1', 'reg1', 'nbr2', 'reg2']]
del2b_Tepes = []#['loss', 'trans cost t','trans cost r']]
del2ca_Tepes = []#['time','capMWr','capMWr']]
del2cb_Tepes = ["0,"]*len(trans_data_TEPES_cap)
     
#create each block of the maskenett file

for i in count:
    #take each row of the capacity block and split regions into two
    tmp = re.split('>',col_reg[i])
    # del2a: fill each row according to maskenet structure with name and number of region
    i1 = str(regions_spain.loc[regions_spain['name'] == tmp[0], 'code'].iloc[0])
    i2 = fnut + tmp[0] + fnut
    i3 = str(regions_spain.loc[regions_spain['name'] == tmp[1], 'code'].iloc[0])
    i4 = fnut + tmp[1]+ fnut
    del2a_Tepes.append(i1 + ','+ i2+ ','+ i3+ ','+ i4 + ',')

    #del2ca: fill each row with 0 = for all tiemsteps, ans trans cap
    i5 = "0"
    i6 = str(int(trans_data_TEPES_cap.iloc[i].loc['2030']))
    del2ca_Tepes.append(i5 + ',' + i6 + ',' + i6)

    # del2b:fill each row according to maskenet structure with values
    i7 = str(trans_data_TEPES_los.iloc[i].loc['2030'])
    i8 = "0"
    del2b_Tepes.append(i7 + ',' + i8 + ',' + i8 + ',')
    #will the order of the transmission lines always be the same across different variables
    #check with Erik... all loss factors are zero
    
# combine the blocks into one list
maskenett_Tepes_1 = []#first_row_MASKENETT
for i in count:
    maskenett_Tepes_1.append(del2a_Tepes[i])
    maskenett_Tepes_1.append(del2b_Tepes[i])
    maskenett_Tepes_1.append(del2ca_Tepes[i])
    maskenett_Tepes_1.append(del2cb_Tepes[i])
    
    
    
#create the final file content      
maskenett_updated = first_row_MASKENETT





#### print to new MASKENETT FILE

print2dotData(filename_out, maskenett_Tepes_1)


    
    













