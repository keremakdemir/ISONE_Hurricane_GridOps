# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 20:44:43 2021

@author: kakdemi
"""

import pandas as pd

#reading hourly interchange data (positive values are imports, negatives are exports)
hourly_interchange = pd.read_csv('Interchange_hourly.csv', header=0)

#creating hypothetical dates and hours to resample data
days = pd.date_range(start='2019-10-21',end='2019-11-5',freq='D')
hours = pd.date_range(start='2019-10-21 00:00:00',end='2019-11-5 23:00:00',freq='H')

#reindexing hourly interchange and finding daily total interchange
hourly_interchange.index = hours
daily_interchange = hourly_interchange.resample('D').sum()

#select dispatchable imports (positive flow days) by excluding exports (negative values)
daily_interchange[daily_interchange < 0] = 0
      
#find dispatchable imports for each line and export imports data during hurricane
imports_total = daily_interchange.copy()
imports_total.rename(columns={'SALBRYNB':'NB_imports_ME'}, inplace=True)
imports_total['HYDRO_QUEBEC'] = imports_total['HQ_P1_P2'] + imports_total['HQHIGATE']
imports_total['NEWYORK'] = imports_total['ROSETON'] + imports_total['SHOREHAM'] + imports_total['NORTHPORT']
imports_total['NY_imports_CT'] = imports_total['NEWYORK'].mul(4).div(9)
imports_total['NY_imports_WCMA'] = imports_total['NEWYORK'].div(9)
imports_total['NY_imports_VT'] = imports_total['NEWYORK'].mul(4).div(9)
imports_total.rename(columns={'HYDRO_QUEBEC':'HQ_imports_VT'}, inplace=True)
del imports_total['ROSETON']
del imports_total['HQ_P1_P2']
del imports_total['HQHIGATE']
del imports_total['SHOREHAM']
del imports_total['NORTHPORT']
del imports_total['NEWYORK']
imports_total.to_csv('ISONE_dispatchable_imports.csv',index=False) 

#select exports (negative flow days) by excluding imports (positive values)
hourly_interchange[hourly_interchange > 0] = 0

#find exports for each line and export hourly export data during hurricane
exports_total = hourly_interchange.copy()
exports_total.rename(columns={'SALBRYNB':'ME_exports_NB'}, inplace=True)
exports_total['HYDRO_QUEBEC'] = exports_total['HQ_P1_P2'] + exports_total['HQHIGATE']
exports_total['NEWYORK'] = exports_total['ROSETON'] + exports_total['SHOREHAM'] + exports_total['NORTHPORT']
exports_total['CT_exports_NY'] = exports_total['NEWYORK'].mul(4).div(9)
exports_total['WCMA_exports_NY'] = exports_total['NEWYORK'].div(9)
exports_total['VT_exports_NY'] = exports_total['NEWYORK'].mul(4).div(9)
exports_total.rename(columns={'HYDRO_QUEBEC':'VT_exports_HQ'}, inplace=True)
del exports_total['ROSETON']
del exports_total['HQ_P1_P2']
del exports_total['HQHIGATE']
del exports_total['SHOREHAM']
del exports_total['NORTHPORT']
del exports_total['NEWYORK']
exports_total = exports_total*-1
exports_total.to_csv('ISONE_exports.csv',index=False)

