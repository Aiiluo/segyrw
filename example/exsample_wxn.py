# -*- coding: utf-8 -*-
"""
This modle is creat for plot wxn segy seismic data
Author:Chenp 
"""

import numpy as np
import matplotlib.pyplot as plt
import read_3d_segy
import plot_segy 

x = read_3d_segy.segy3d()
x.read_segy_file(r'F:\AT12649.sgy')

# x.read_segy_file(r'K:\tp_share\2018年烃源岩评价项目\原始数据\3T3605\weixinan\AT12649.sgy')
x.segy_information()
number_of_sample, sample_intervel = x.init_binary_header()
#plot a line or a cross line
trace_lens = 500
inline_start = 3031 
inline_end = 4901
xline_start = 2500
xline_end = 2500

depth = np.linspace(0,-(number_of_sample-1)*sample_intervel,number_of_sample)

#plot inline or xline
if inline_start == inline_end:
    print("============ PLOT INLINE ",inline_start," ============")
    trace_lens = xline_end - xline_start + 1
    trace = np.ndarray(shape=(trace_lens,number_of_sample))
    for i in range(0,trace_lens):
        trace[i] = x.read_ibmfloat_data(inline_start,xline_start+i)
        print("Reading:%d"%i, end='\r', flush=True)

elif xline_start == xline_end:
    print("============ PLOT XLINE ",xline_start," ============")
    trace_lens = inline_end - inline_start + 1
    trace = np.ndarray(shape=(trace_lens,number_of_sample))
    for i in range(0,trace_lens):
        trace[i] = x.read_ibmfloat_data(inline_start+i,xline_start)
        print("Reading:%d"%i, end='\r', flush=True)
else:
    print("======= WRONG　INLINE OR XLINE NUMBER =======")

#plot_wave(trace,depth,number_of_sample,trace_lens,20)
plot_segy.plot_wiggle(trace,depth,number_of_sample,trace_lens,20)



