# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 18:45:12 2018

@author: Aiiluo
"""

import numpy as np
import matplotlib.pyplot as plt
import read_3d_segy
from plot_segy import *

x = segy3d(221,4,'i',21,4,'i',73,4,'i',77,4,'i')
x.read_segy_file(r'D:\hj_3d_2015_final_psdm-t_16y03.sgy')
x.segy_information()


#plot a line or a cross line
number_of_sample = 3500
sample_intervel = 2
trace_lens = 500
inline_start = 500
inline_end = 500
xline_start = 313
xline_end = 3059
#depth = np.arange(0,3500*2,2)
depth = np.linspace(0,-(number_of_sample-1)*sample_intervel,number_of_sample)

if inline_start == inline_end:
    print("============ PLOT INLINE ",inline_start," ============")
    trace_lens = xline_end - xline_start + 1
    trace = np.ndarray(shape=(trace_lens,number_of_sample))
    for i in range(0,trace_lens):
        trace[i] = x.read_int8_data(inline_start,xline_start+i)

elif xline_start == xline_end:
    print("============ PLOT XLINE ",xline_start," ============")
    trace_lens = inline_end - inline_start + 1
    trace = np.ndarray(shape=(trace_lens,number_of_sample))
    for i in range(0,trace_lens):
        trace[i] = x.read_int8_data(inline_start+i,xline_start)
else:
    print("======= WRONG　INLINE OR XLINE NUMBER =======")

plot_wave(trace,depth,number_of_sample,trace_lens,20)



#plot one trace
#one_trace = x.read_int8_data(159,3059)
#y = one_trace[1500:2000]
#
#plt.plot(y)