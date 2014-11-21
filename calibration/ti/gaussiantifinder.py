# -*- coding: utf-8 -*-

from flexvi.calibration.ti import tifuncs

class GaussianTrueIntrinsicFinder:
    
    def __init__(self, ce):
        self.dataframes = [ce.df]
        self.outliers = []
        self.means = []
        self.s_deviations = []
        
    def find_ti(self):
        
        donext = True
        while donext:
            m, sd = tifuncs.norm_fit(self.dataframes[-1])
            self.means.append(m)
            self.s_deviations.append(sd)
            outliers_to_remove = tifuncs.find_outliers(self.dataframes[-1], m, sd)
            self.outliers.append(outliers_to_remove)
            if outliers_to_remove == []:
                donext = False
            else:
                self._remove_outliers(outliers_to_remove)
            
                
    def _remove_outliers(self, outliers_to_remove):
        df_last = self.dataframes[-1]
        df_new = df_last.ix[set(df_last.index) - set(outliers_to_remove)]
        self.dataframes.append(df_new)