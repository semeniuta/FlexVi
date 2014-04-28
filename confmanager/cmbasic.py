# -*- coding: utf-8 -*-

'''
Configuration manager for SintefCV

In the files where reading configuraion is needed, the usage of
the configuration manager is the following:
    
    from cvapplications.confmanager import ConfigManager
    cm = ConfigManager()

@author: Oleksandr Semeniuta 
'''

from ConfigParser import ConfigParser
import os
from glob import glob

SYSTEM_CONFIG_FILE = r'conf_system.ini'
IMAGESETS_CONFIG_FILE = r'conf_imagesets.ini'

class BasicConfigManager:
    def __init__(self):
        
        self.imgconfig = ConfigParser()
        self.imgconfig.read(os.path.join(IMAGESETS_CONFIG_FILE))
        self.systemconfig = ConfigParser()
        self.systemconfig.read(os.path.join(SYSTEM_CONFIG_FILE))
        
        ''' 
        Fix the location of root_directory - 
        make its path absolute (it is assumed that in SYSTEM_CONFIG_FILE it
        is specified in relation to the location of SYSTEM_CONFIG_FILE)
        '''        
        abs_path = os.path.abspath(self.get_root_directory())
        self.systemconfig.set('system', 'root_directory', abs_path)

    def get_root_directory(self):
        return self.systemconfig.get('system', 'root_directory')        
    
    def get_directory(self, dir_key):
        root_directory = self.get_root_directory()
        dir_name = self.systemconfig.get('directories', dir_key)
        return os.path.join(root_directory, dir_name)
        
    def get_directories(self):
        tuples = self.systemconfig.items('directories')
        dir_dict = {key: os.path.join(self.get_root_directory(), dirname) for key, dirname in tuples}
        return dir_dict
        
    def get_imageset_images_list(self, imageset_name):
        mask = self.get_imageset_full_mask(imageset_name)
        return glob(mask)
    
    def get_imageset_full_mask(self, imageset_name):
        imagemask = self.imgconfig.get(imageset_name, 'mask')
        if '/' not in imagemask and '\\' not in imagemask:
            root_dir = self.get_root_directory()
            img_dir = self.systemconfig.get('directories', 'imagesets')
            imagemask = os.path.join(root_dir, img_dir, imageset_name, imagemask)
        return imagemask
        
    
        
        
        
        
        
        
        
        