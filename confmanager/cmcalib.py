# -*- coding: utf-8 -*-

from flexvi.confmanager.cmbasic import BasicConfigManager
from flexvi.calibration.containers.imageset import CalibrationImageSet
from flexvi.core import chessboard
import os

class CalibrationConfigManager(BasicConfigManager):

    def get_chessboard_imageset(self, imageset_name):
        imagemask = self.get_imageset_full_mask(imageset_name)

        width = self.imgconfig.getint(imageset_name, 'width')
        height = self.imgconfig.getint(imageset_name, 'height')
        pattern_size = (height, width)
        square_size = self.imgconfig.getfloat(imageset_name, 'square')

        imageset = CalibrationImageSet(imageset_name, imagemask, pattern_size, square_size)

        flag_key = self.imgconfig.get(imageset_name, 'findcbc_flags')
        imageset.set_findcbc_flags(chessboard.flags[flag_key])

        return imageset

    def get_calibration_parameters(self):
        res = {}
        res['sample_size'] = self.systemconfig.getint('calibration', 'sample_size')
        res['num_of_samples'] = self.systemconfig.getint('calibration', 'num_of_samples')
        res['imageset'] = self.systemconfig.get('calibration', 'imageset')
        return res

    def get_svs_parameters(self):
        res = {}
        res['imageset_left'] = self.systemconfig.get('svs', 'imageset_left')
        res['imageset_right'] = self.systemconfig.get('svs', 'imageset_right')
        calib_dir = self.get_directory('calibration')
        res['datadir_left'] = os.path.join(calib_dir, self.systemconfig.get('svs', 'datadir_left'))
        res['datadir_right'] = os.path.join(calib_dir, self.systemconfig.get('svs', 'datadir_right'))
        res['name'] = self.systemconfig.get('svs', 'name')
        return res
