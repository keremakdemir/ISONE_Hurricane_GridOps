# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 21:29:55 2018

@author: jkern
"""

############################################################################
#                               DATA SETUP                                 #
#                                                                          #
# This file selects different scenarios and organizes the data in a form   #
# that is accessible to the unit commitment/economic dispatch (UC/ED)      #
# simulation model.                                                        #
############################################################################

import ISONE_data_setup

all_scenarios = ['2012-base','2030-Offshore-2x','2030-Offshore-3x','2030-Offshore-4x','2030-Offshore-ReplaceISO',\
             '2030-Onshore-0.5x','2030-Onshore-2x','2030-Onshore-3x','2030-Onshore-ReplaceISO',\
             '2030-PV-2x','2030-PV-3x','2030-PV-4x','2030-PV-5x','2030-PV-6x','2030-PV-ReplaceISO','2030-NREL',\
             '2030-ISONE','2040-Offshore-2x','2040-Offshore-3x','2040-Offshore-4x','2040-Offshore-5x',\
             '2040-Offshore-6x','2040-Offshore-7x','2040-Offshore-8x','2040-Offshore-9x','2040-Offshore-10x',\
             '2040-Offshore-ReplaceISO','2040-Onshore-0.5x','2040-Onshore-2x','2040-Onshore-3x','2040-Onshore-ReplaceISO',\
             '2040-PV-2x','2040-PV-3x','2040-PV-4x','2040-PV-5x','2040-PV-6x','2040-PV-ReplaceISO','2040-NREL','2040-ISONE']
      
for scenario in all_scenarios:
     
    print('Creating files for {} scenario...'.format(scenario))
    
############################################################################
#                          UC/ED Data File Setup                           #
############################################################################
    
    ISONE_data_setup.setup(scenario)
    
print('All folders are created successfully.')

