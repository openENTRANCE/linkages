# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 21:39:05 2020

@author: pisciell
"""

import pyam

# set username to get access to the scenario explorer
user_name = 'myusername'
user_password = 'mypassword'
pyam.iiasa.set_config(user_name,user_password)

pyam.iiasa.Connection('openentrance')

df = pyam.read_iiasa(
                    'openentrance', 
                     model = 'GENeSYS-MOD 2.9.0-oe',
                     scenario = 'Directed Transition 1.0',
                     variable = ['SecondaryEnergy|Electricity|Oil', 'SecondaryEnergy|Electricity|Solar'])
data = df.as_pandas()
data.to_excel(r'C:\Users\pisciell.WIN-NTNU-NO\Desktop\oePathway.xlsx', index=False)
