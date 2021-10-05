# -*- coding: utf-8 -*-
"""
Created on Wed May 03 15:01:31 2017

@author: jdkern
"""

import pandas as pd
import numpy as np
import os
from shutil import copy
from pathlib import Path

#reading renewable timeseries
Offshore_ISO_2012 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Off_Shore_wind_ISO.xlsx',header=0,sheet_name='All Zones Time Series - 2018')
Offshore_ISO_2030 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Off_Shore_wind_ISO.xlsx',header=0,sheet_name='All Zones Time Series - 2030')
Offshore_ISO_2040 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Off_Shore_wind_ISO.xlsx',header=0,sheet_name='All Zones Time Series - 2040')
Offshore_NREL_2012 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Off_Shore_wind_NREL.xlsx',header=0,sheet_name='All Zones Time Series - 2018')
Offshore_NREL_2030 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Off_Shore_wind_NREL.xlsx',header=0,sheet_name='All Zones Time Series - 2030')
Offshore_NREL_2040 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Off_Shore_wind_NREL.xlsx',header=0,sheet_name='All Zones Time Series - 2040')

Onshore_ISO_2012 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/On_Shore_Wind_ISO.xlsx',header=0,sheet_name='All Zones Time Series - 2018')
Onshore_ISO_2030 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/On_Shore_Wind_ISO.xlsx',header=0,sheet_name='All Zones Time Series - 2030')
Onshore_ISO_2040 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/On_Shore_Wind_ISO.xlsx',header=0,sheet_name='All Zones Time Series - 2040')
Onshore_NREL_2012 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/On_Shore_Wind_NREL.xlsx',header=0,sheet_name='All Zones Time Series - 2018')
Onshore_NREL_2030 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/On_Shore_Wind_NREL.xlsx',header=0,sheet_name='All Zones Time Series - 2030')
Onshore_NREL_2040 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/On_Shore_Wind_NREL.xlsx',header=0,sheet_name='All Zones Time Series - 2040')

Solar_ISO_2012 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Solar_ISO.xlsx',header=0,sheet_name='All Zones Time Series - 2018')
Solar_ISO_2030 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Solar_ISO.xlsx',header=0,sheet_name='All Zones Time Series - 2030')
Solar_ISO_2040 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Solar_ISO.xlsx',header=0,sheet_name='All Zones Time Series - 2040')
Solar_NREL_2012 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Solar_NREL.xlsx',header=0,sheet_name='All Zones Time Series - 2018')
Solar_NREL_2030 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Solar_NREL.xlsx',header=0,sheet_name='All Zones Time Series - 2030')
Solar_NREL_2040 = pd.read_excel('ISONE_data_file/Scenarios/Renewable_timeseries/Solar_NREL.xlsx',header=0,sheet_name='All Zones Time Series - 2040')

#read transmission path parameters into DataFrame
df_paths = pd.read_csv('ISONE_data_file/paths.csv',header=0)

#list zones
zones = ['CT', 'ME', 'NH', 'NEMA', 'RI', 'SEMA', 'VT', 'WCMA']

#time series of load for each zone
df_load_all = pd.read_excel('Demand/Hourly_demand.xlsx',header=0)

#daily hydropower availability 
df_hydro = pd.read_csv('Hydropower/ISONE_dispatchable_hydro.csv',header=0)

#natural gas prices
df_ng_all = pd.read_csv('Fuel_prices/NG_prices.csv', header=0)

#oil prices
df_oil_all = pd.read_csv('Fuel_prices/Oil_prices.csv', header=0)

#daily time series of dispatchable imports by path
df_imports = pd.read_csv('Interchange/ISONE_dispatchable_imports.csv',header=0)

#hourly time series of exports by zone
df_exports = pd.read_csv('Interchange/ISONE_exports.csv',header=0)

def setup(selected_scenario): 
        
    #reading generator file
    df_gen = pd.read_excel('ISONE_data_file/Scenarios/Generator_files/generators-{}.xlsx'.format(selected_scenario),header=0,sheet_name='Generators (dispatch)')
    
    #must run resources (LFG,ag_waste,nuclear)
    df_must = pd.read_excel('ISONE_data_file/Scenarios/Generator_files/generators-{}.xlsx'.format(selected_scenario),header=0,sheet_name='Generators (must run)')
    mustrun_each_zone = np.zeros((1,len(zones)))
    
    for zone in zones:
        zonal_mustrun = df_must.loc[df_must['State']==zone]['Product'].sum()
        mustrun_each_zone[0,zones.index(zone)] = zonal_mustrun
        
    hourly_mustrun = np.repeat(mustrun_each_zone, 384, axis=0)
    df_total_must_run = pd.DataFrame(hourly_mustrun,columns=zones) 
    
    #saving relevant renewable time series
    if selected_scenario == '2012-base':
        df_solar_data = Solar_NREL_2012.copy()
        df_onshore_data = Onshore_NREL_2012.copy()
        df_offshore_data = Offshore_NREL_2012.copy()
        
    elif selected_scenario == '2030-Offshore-2x':
        df_solar_data = Solar_NREL_2030.copy()
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()        
        df_offshore_data = df_offshore_data*2
        
    elif selected_scenario == '2030-Offshore-3x':
        df_solar_data = Solar_NREL_2030.copy()
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()        
        df_offshore_data = df_offshore_data*3
        
    elif selected_scenario == '2030-Offshore-4x':
        df_solar_data = Solar_NREL_2030.copy()
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()        
        df_offshore_data = df_offshore_data*4
        
    elif selected_scenario == '2030-Offshore-ReplaceISO':
        df_solar_data = Solar_NREL_2030.copy()
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_ISO_2030.copy() 
        
    elif selected_scenario == '2030-Onshore-0.5x':
        df_solar_data = Solar_NREL_2030.copy()
        df_onshore_data = Onshore_NREL_2030.copy()
        df_onshore_data = df_onshore_data*0.5
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-Onshore-2x':
        df_solar_data = Solar_NREL_2030.copy()
        df_onshore_data = Onshore_NREL_2030.copy()
        df_onshore_data = df_onshore_data*2
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-Onshore-3x':
        df_solar_data = Solar_NREL_2030.copy()
        df_onshore_data = Onshore_NREL_2030.copy()
        df_onshore_data = df_onshore_data*3
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-Onshore-ReplaceISO':
        df_solar_data = Solar_NREL_2030.copy()
        df_onshore_data = Onshore_ISO_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-PV-2x':
        df_solar_data = Solar_NREL_2030.copy()
        df_solar_data = df_solar_data*2
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-PV-3x':
        df_solar_data = Solar_NREL_2030.copy()
        df_solar_data = df_solar_data*3
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-PV-4x':
        df_solar_data = Solar_NREL_2030.copy()
        df_solar_data = df_solar_data*4
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-PV-5x':
        df_solar_data = Solar_NREL_2030.copy()
        df_solar_data = df_solar_data*5
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-PV-6x':
        df_solar_data = Solar_NREL_2030.copy()
        df_solar_data = df_solar_data*6
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-PV-ReplaceISO':
        df_solar_data = Solar_ISO_2030.copy()
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-NREL':
        df_solar_data = Solar_NREL_2030.copy()
        df_onshore_data = Onshore_NREL_2030.copy()
        df_offshore_data = Offshore_NREL_2030.copy()
        
    elif selected_scenario == '2030-ISONE':
        df_solar_data = Solar_ISO_2030.copy()
        df_onshore_data = Onshore_ISO_2030.copy()
        df_offshore_data = Offshore_ISO_2030.copy()
        
    elif selected_scenario == '2040-Offshore-2x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()        
        df_offshore_data = df_offshore_data*2
        
    elif selected_scenario == '2040-Offshore-3x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()        
        df_offshore_data = df_offshore_data*3
        
    elif selected_scenario == '2040-Offshore-4x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()        
        df_offshore_data = df_offshore_data*4
        
    elif selected_scenario == '2040-Offshore-5x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()        
        df_offshore_data = df_offshore_data*5
        
    elif selected_scenario == '2040-Offshore-6x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()        
        df_offshore_data = df_offshore_data*6
        
    elif selected_scenario == '2040-Offshore-7x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()        
        df_offshore_data = df_offshore_data*7
        
    elif selected_scenario == '2040-Offshore-8x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()        
        df_offshore_data = df_offshore_data*8
        
    elif selected_scenario == '2040-Offshore-9x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()        
        df_offshore_data = df_offshore_data*9
        
    elif selected_scenario == '2040-Offshore-10x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()        
        df_offshore_data = df_offshore_data*10
        
    elif selected_scenario == '2040-Offshore-ReplaceISO':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_ISO_2040.copy()
        
    elif selected_scenario == '2040-Onshore-0.5x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_onshore_data = df_onshore_data*0.5
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-Onshore-2x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_onshore_data = df_onshore_data*2
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-Onshore-3x':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_onshore_data = df_onshore_data*3
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-Onshore-ReplaceISO':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_ISO_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-PV-2x':
        df_solar_data = Solar_NREL_2040.copy()
        df_solar_data = df_solar_data*2
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-PV-3x':
        df_solar_data = Solar_NREL_2040.copy()
        df_solar_data = df_solar_data*3
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-PV-4x':
        df_solar_data = Solar_NREL_2040.copy()
        df_solar_data = df_solar_data*4
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-PV-5x':
        df_solar_data = Solar_NREL_2040.copy()
        df_solar_data = df_solar_data*5
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-PV-6x':
        df_solar_data = Solar_NREL_2040.copy()
        df_solar_data = df_solar_data*6
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-PV-ReplaceISO':
        df_solar_data = Solar_ISO_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-NREL':
        df_solar_data = Solar_NREL_2040.copy()
        df_onshore_data = Onshore_NREL_2040.copy()
        df_offshore_data = Offshore_NREL_2040.copy()
        
    elif selected_scenario == '2040-ISONE':
        df_solar_data = Solar_ISO_2040.copy()
        df_onshore_data = Onshore_ISO_2040.copy()
        df_offshore_data = Offshore_ISO_2040.copy()
        
    #time series of natural gas prices for each zone
    df_ng = df_ng_all.copy()
    
    #time series of oil prices for each zone
    df_oil = df_oil_all.copy()
    
    #time series of load for each zone
    df_load = df_load_all.copy()
    
    #time series of operational reserves for each zone
    rv= df_load.values
    reserves = np.zeros((len(rv),1))
    for i in range(0,len(rv)):
            reserves[i] = np.sum(rv[i,:])*.04
    df_reserves = pd.DataFrame(reserves)
    df_reserves.columns = ['reserves']
    
    ############
    #  sets    #
    ############
    
    #write data.dat file
    path = str(Path.cwd().parent) + str(Path('/UCED/LR/'+selected_scenario))
    os.makedirs(path,exist_ok=True)
    
    generators_file='ISONE_data_file/Scenarios/Generator_files/generators-{}.xlsx'.format(selected_scenario)
    dispatch_file='../UCED/ISONE_dispatch.py'
    dispatchLP_file='../UCED/ISONE_dispatchLP.py'
    wrapper_file='../UCED/ISONE_wrapper.py'
    simulation_file='../UCED/ISONE_simulation.py'
    
    copy(dispatch_file,path)
    copy(wrapper_file,path)
    copy(simulation_file,path)
    copy(dispatchLP_file,path)
    copy(generators_file,path)
    
    os.rename('{}/generators-{}.xlsx'.format(path,selected_scenario), '{}/generators.xlsx'.format(path))
    
    filename = path + '/data.dat'
    
    #write data.dat file
    with open(filename, 'w') as f:
        
        # generator sets by zone
        for z in zones:
            # zone string
            z_int = zones.index(z)
            f.write('set Zone%dGenerators :=\n' % (z_int+1))
            # pull relevant generators
            for gen in range(0,len(df_gen)):
                if df_gen.loc[gen,'zone'] == z:
                    unit_name = df_gen.loc[gen,'name']
                    unit_name = unit_name.replace(' ','_')
                    f.write(unit_name + ' ')
            f.write(';\n\n')   
            
        # NY imports
        f.write('set NY_Imports_CT :=\n')
        # pull relevant generators
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'typ'] == 'imports' and df_gen.loc[gen,'zone'] == 'NYCT_I':
                unit_name = df_gen.loc[gen,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + ' ')
        f.write(';\n\n')   
    
        # NY imports
        f.write('set NY_Imports_WCMA :=\n')
        # pull relevant generators
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'typ'] == 'imports' and df_gen.loc[gen,'zone'] == 'NYWCMA_I':
                unit_name = df_gen.loc[gen,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + ' ')
        f.write(';\n\n') 
        
        # NY imports
        f.write('set NY_Imports_VT :=\n')
        # pull relevant generators
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'typ'] == 'imports' and df_gen.loc[gen,'zone'] == 'NYVT_I':
                unit_name = df_gen.loc[gen,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + ' ')
        f.write(';\n\n')
        
        # HQ imports
        f.write('set HQ_Imports_VT :=\n')
        # pull relevant generators
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'typ'] == 'imports' and df_gen.loc[gen,'zone'] == 'HQVT_I':
                unit_name = df_gen.loc[gen,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + ' ')
        f.write(';\n\n')
            
        # NB imports
        f.write('set NB_Imports_ME :=\n')
        # pull relevant generators
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'typ'] == 'imports' and df_gen.loc[gen,'zone'] == 'NBME_I':
                unit_name = df_gen.loc[gen,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + ' ')
        f.write(';\n\n')
            
        # generator sets by type
        # coal
        f.write('set Coal :=\n')
        # pull relevant generators
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'typ'] == 'coal':
                unit_name = df_gen.loc[gen,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + ' ')
        f.write(';\n\n')    
            
        # Slack
        f.write('set Slack :=\n')
        # pull relevant generators
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'typ'] == 'slack':
                unit_name = df_gen.loc[gen,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + ' ')
        f.write(';\n\n')  
    
        # Hydro
        f.write('set Hydro :=\n')
        # pull relevant generators
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'typ'] == 'hydro':
                unit_name = df_gen.loc[gen,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + ' ')
        f.write(';\n\n')   
        
        # Ramping
        f.write('set Ramping :=\n')
        # pull relevant generators
        for gen in range(0,len(df_gen)):
            if df_gen.loc[gen,'typ'] == 'hydro' or df_gen.loc[gen,'typ'] == 'imports':
                unit_name = df_gen.loc[gen,'name']
                unit_name = unit_name.replace(' ','_')
                f.write(unit_name + ' ')
        f.write(';\n\n')   
    
    
        # gas generator sets by zone and type
        for z in zones:
            # zone string
            z_int = zones.index(z)
            
            # Natural Gas
            # find relevant generators
            trigger = 0
            for gen in range(0,len(df_gen)):
                if df_gen.loc[gen,'zone'] == z and (df_gen.loc[gen,'typ'] == 'ngcc' or df_gen.loc[gen,'typ'] == 'ngct' or df_gen.loc[gen,'typ'] == 'ngst'):
                    trigger = 1
            if trigger > 0:
                # pull relevant generators
                f.write('set Zone%dGas :=\n' % (z_int+1))      
                for gen in range(0,len(df_gen)):
                    if df_gen.loc[gen,'zone'] == z and (df_gen.loc[gen,'typ'] == 'ngcc' or df_gen.loc[gen,'typ'] == 'ngct' or df_gen.loc[gen,'typ'] == 'ngst'):
                        unit_name = df_gen.loc[gen,'name']
                        unit_name = unit_name.replace(' ','_')
                        f.write(unit_name + ' ')
                f.write(';\n\n')
                
        
        # oil generator sets by zone and type
        for z in zones:
            # zone string
            z_int = zones.index(z)
            
            # find relevant generators
            trigger = 0
            for gen in range(0,len(df_gen)):
                if (df_gen.loc[gen,'zone'] == z) and (df_gen.loc[gen,'typ'] == 'oil'):
                    trigger = 1
            if trigger > 0:
                # pull relevant generators
                f.write('set Zone%dOil :=\n' % (z_int+1))      
                for gen in range(0,len(df_gen)):
                    if (df_gen.loc[gen,'zone'] == z) and (df_gen.loc[gen,'typ'] == 'oil'):
                        unit_name = df_gen.loc[gen,'name']
                        unit_name = unit_name.replace(' ','_')
                        f.write(unit_name + ' ')
                f.write(';\n\n')
       
                
        # zones
        f.write('set zones :=\n')
        for z in zones:
            f.write(z + ' ')
        f.write(';\n\n')
        
        # sources
        f.write('set sources :=\n')
        for z in zones:
            f.write(z + ' ')
        f.write(';\n\n')
        
        # sinks
        f.write('set sinks :=\n')
        for z in zones:
            f.write(z + ' ')
        f.write(';\n\n')
        
    ################
    #  parameters  #
    ################
        
        # simulation details
        SimHours = 384
        f.write('param SimHours := %d;' % SimHours)
        f.write('\n')
        f.write('param SimDays:= %d;' % int(SimHours/24))
        f.write('\n\n')
        HorizonHours = 48
        f.write('param HorizonHours := %d;' % HorizonHours)
        f.write('\n\n')
        HorizonDays = int(HorizonHours/24)
        f.write('param HorizonDays := %d;' % HorizonDays)
        f.write('\n\n')
        
    
        # create parameter matrix for transmission paths (source and sink connections)
        f.write('param:' + '\t' + 'limit' + '\t' +'hurdle :=' + '\n')
        for z in zones:
            for x in zones:           
                f.write(z + '\t' + x + '\t')
                match = 0
                for p in range(0,len(df_paths)):
                    source = df_paths.loc[p,'start_zone']
                    sink = df_paths.loc[p,'end_zone']
                    if source == z and sink == x:
                        match = 1
                        p_match = p
                if match > 0:
                    f.write(str(round(df_paths.loc[p_match,'limit'],3)) + '\t' + str(round(df_paths.loc[p_match,'hurdle'],3)) + '\n')
                else:
                    f.write('0' + '\t' + '0' + '\n')
        f.write(';\n\n')
        
    # create parameter matrix for generators
        f.write('param:' + '\t')
        for c in df_gen.columns:
            if c != 'name':
                f.write(c + '\t')
        f.write(':=\n\n')
        for i in range(0,len(df_gen)):    
            for c in df_gen.columns:
                if c == 'name':
                    unit_name = df_gen.loc[i,'name']
                    unit_name = unit_name.replace(' ','_')
                    f.write(unit_name + '\t')  
                elif c == 'typ' or c == 'zone':
                    f.write(str(df_gen.loc[i,c]) + '\t')    
                else:
                    f.write(str(round(df_gen.loc[i,c],3)) + '\t')               
            f.write('\n')
                
        f.write(';\n\n')     
        
        # times series data
        # zonal (hourly)
        f.write('param:' + '\t' + 'SimDemand' + '\t' + 'SimOffshoreWind' \
        + '\t' + 'SimSolar' + '\t' + 'SimOnshoreWind' + '\t' + 'SimMustRun:=' + '\n')      
        for z in zones:
            for h in range(0,len(df_load)): 
                f.write(z + '\t' + str(h+1) + '\t' + str(round(df_load.loc[h,z],3))\
                + '\t' + str(round(df_offshore_data.loc[h,z],3))\
                + '\t' + str(round(df_solar_data.loc[h,z],3))\
                + '\t' + str(round(df_onshore_data.loc[h,z],3))\
                + '\t' + str(round(df_total_must_run.loc[h,z],3)) + '\n')
        f.write(';\n\n')
        
        # zonal (daily)
        f.write('param:' + '\t' + 'SimGasPrice' + '\t' + 'SimOilPrice:=' + '\n')      
        for z in zones:
            for d in range(0,int(SimHours/24)): 
                f.write(z + '\t' + str(d+1) + '\t' + str(round(df_ng.loc[d,z], 3)) + '\t' + str(round(df_oil.loc[d,z], 3)) + '\n')
        f.write(';\n\n')
    
        #system wide (daily)
        f.write('param:' + '\t' + 'SimNY_imports_CT' + '\t' + 'SimNY_imports_VT' + '\t' + 'SimNY_imports_WCMA' + '\t' + 'SimNB_imports_ME' + '\t' + 'SimHQ_imports_VT' + '\t' + 'SimCT_hydro' + '\t' + 'SimME_hydro' + '\t' +  'SimNH_hydro' + '\t' +  'SimNEMA_hydro' + '\t' +  'SimRI_hydro' + '\t' +  'SimVT_hydro' + '\t' + 'SimWCMA_hydro:=' + '\n')
        for d in range(0,len(df_imports)):
                f.write(str(d+1) + '\t' + str(round(df_imports.loc[d,'NY_imports_CT'],3)) + '\t' + str(round(df_imports.loc[d,'NY_imports_VT'],3)) + '\t' + str(round(df_imports.loc[d,'NY_imports_WCMA'],3)) + '\t' + str(round(df_imports.loc[d,'NB_imports_ME'],3)) + '\t' + str(round(df_imports.loc[d,'HQ_imports_VT'],3)) + '\t' + str(round(df_hydro.loc[d,'CT'],3)) + '\t' + str(round(df_hydro.loc[d,'ME'],3)) + '\t' + str(round(df_hydro.loc[d,'NH'],3)) + '\t' + str(round(df_hydro.loc[d,'NEMA'],3)) + '\t' + str(round(df_hydro.loc[d,'RI'],3)) + '\t' + str(round(df_hydro.loc[d,'VT'],3)) + '\t' + str(round(df_hydro.loc[d,'WCMA'],3)) + '\n')
        f.write(';\n\n')
            
        #system wide (hourly)
        f.write('param:' + '\t' + 'SimCT_exports_NY' + '\t' + 'SimWCMA_exports_NY' + '\t' + 'SimVT_exports_NY' + '\t' + 'SimVT_exports_HQ' + '\t' + 'SimME_exports_NB' + '\t' + 'SimReserves:=' + '\n')
        for h in range(0,len(df_load)):
                f.write(str(h+1) + '\t' + str(round(df_exports.loc[h,'CT_exports_NY'],3)) + '\t' + str(round(df_exports.loc[h,'WCMA_exports_NY'],3)) + '\t' + str(round(df_exports.loc[h,'VT_exports_NY'],3)) + '\t' + str(round(df_exports.loc[h,'VT_exports_HQ'],3)) + '\t' + str(round(df_exports.loc[h,'ME_exports_NB'],3)) + '\t' + str(round(df_reserves.loc[h,'reserves'],3))  + '\n')
        f.write(';\n\n')
    
    return None
    
    
    
