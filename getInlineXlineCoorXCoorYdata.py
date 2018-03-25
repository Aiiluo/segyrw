# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 12:45:24 2018

@author: proc1
"""

import numpy as np
import matplotlib.pyplot as plt
import read_3d_segy
from plot_segy import *

x = segy3d()
x.read_segy_file(r'I:\3T3605\weixinan\AT12649.sgy')
x.segy_information()
trace_start = 1
trace_end = 2997340
#trace_end = 100000

inline_index = np.zeros(trace_end-trace_start+1,dtype=np.int16)
xline_index = np.zeros(trace_end-trace_start+1,dtype=np.int16)
coor_X_index = np.zeros(trace_end-trace_start+1)
coor_Y_index = np.zeros(trace_end-trace_start+1)
for i in range(trace_start,trace_end):
    (inline_index[i],xline_index[i],coor_X_index[i],coor_Y_index[i]) = x.read_control_file(i)
    print("Loading Trace:",i)
    print(inline_index[i]," ",xline_index[i]," ",coor_X_index[i]," ",coor_Y_index[i])
    
np.savetxt('inline_index.txt', inline_index,fmt='%s',newline='\n')
np.savetxt('xline_index.txt', xline_index,fmt='%s',newline='\n')
np.savetxt('coor_X_index.txt', coor_X_index,fmt='%s',newline='\n')
np.savetxt('coor_Y_index.txt', coor_Y_index,fmt='%s',newline='\n')