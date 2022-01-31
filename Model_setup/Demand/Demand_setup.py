# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 17:26:48 2022

@author: kakdemi
"""

import pandas as pd

#reading 2018 load values
load_2018 = pd.read_excel('Hourly_demand_2018.xlsx',header=0)

#reading solar behind the meter timeseries
Solar_ISO_BTM_2012 = pd.read_excel('../ISONE_data_file/Scenarios/Renewable_timeseries/Solar_ISO_BTM.xlsx',header=0,sheet_name='All Zones Time Series - 2018')
Solar_ISO_BTM_2030 = pd.read_excel('../ISONE_data_file/Scenarios/Renewable_timeseries/Solar_ISO_BTM.xlsx',header=0,sheet_name='All Zones Time Series - 2030')
Solar_ISO_BTM_2040 = pd.read_excel('../ISONE_data_file/Scenarios/Renewable_timeseries/Solar_ISO_BTM.xlsx',header=0,sheet_name='All Zones Time Series - 2040')
Solar_NREL_BTM_2012 = pd.read_excel('../ISONE_data_file/Scenarios/Renewable_timeseries/Solar_NREL_BTM.xlsx',header=0,sheet_name='All Zones Time Series - 2018')
Solar_NREL_BTM_2030 = pd.read_excel('../ISONE_data_file/Scenarios/Renewable_timeseries/Solar_NREL_BTM.xlsx',header=0,sheet_name='All Zones Time Series - 2030')
Solar_NREL_BTM_2040 = pd.read_excel('../ISONE_data_file/Scenarios/Renewable_timeseries/Solar_NREL_BTM.xlsx',header=0,sheet_name='All Zones Time Series - 2040')

#creating and saving load timeseries for each solar BTM case
load_ISO_2030 = load_2018 + Solar_ISO_BTM_2012 - Solar_ISO_BTM_2030
load_ISO_2030.to_excel('Hourly_demand_2030_ISO.xlsx',index=False)

load_ISO_2040 = load_2018 + Solar_ISO_BTM_2012 - Solar_ISO_BTM_2040
load_ISO_2040.to_excel('Hourly_demand_2040_ISO.xlsx',index=False)

load_NREL_2030 = load_2018 + Solar_NREL_BTM_2012 - Solar_NREL_BTM_2030
load_NREL_2030.to_excel('Hourly_demand_2030_NREL.xlsx',index=False)

load_NREL_2040 = load_2018 + Solar_NREL_BTM_2012 - Solar_NREL_BTM_2040
load_NREL_2040.to_excel('Hourly_demand_2040_NREL.xlsx',index=False)

