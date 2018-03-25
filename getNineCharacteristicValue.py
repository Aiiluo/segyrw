# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 12:12:31 2018

@author: proc1
"""

import numpy as np
import matplotlib.pyplot as plt
import read_3d_segy
from plot_segy import *

#x = segy3d()
#x.read_segy_file(r'I:\3T3605\weixinan\AT12649.sgy')
#x.segy_information()
#trace_start = 1
#trace_end = 2997342
#trace_end = 100

def getSampleDepth(depth,sample):
    dif = depth % sample
    if dif == 0:
        return depth
    else:
        if dif >= (sample/2):
            return depth + sample -dif
        else:
            return depth - dif
        
        
print(getSampleDepth(7,4))