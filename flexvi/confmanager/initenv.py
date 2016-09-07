# -*- coding: utf-8 -*-

'''
Module aimed at initializing the environment for the further SintefCV usage

@author: Oleksandr Semeniuta 
'''

import os
from flexvi.confmanager.cmbasic import BasicConfigManager

def create_directories():
    ''' 
    Creates the directory tree according to the configuration files    
    '''
    cm = BasicConfigManager()
    for key, d in cm.get_directories().iteritems():
        if not os.path.exists(d):        
            print 'Creating %s' % d
            os.makedirs(d)
        else: 
            print 'Path %s exists' % d 