# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 18:45:12 2018

@author: Aiiluo
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import read_3d_segy
import plot_segy 

# From keyboard get segy loacation, trace header location
segy_in = input("Input the segy file(full address):\n")
# start = input("Choose the segy file you want to read, press any key to get start.\n")
# segy_in = os.path.basename

# get types of trace header formation
trace_header_location_fmt = input("What seismic processing company is \
the segy file?\n1.DP;\n2.Western country company;\n3.Petrel;\n4.Others.\n")
if trace_header_location_fmt == '1':
    inline_p=41;xline_p=45;x_cor_p=73;y_cor_p=77;
elif trace_header_location_fmt == '2':
    inline_p=221;xline_p=21;x_cor_p=53;y_cor_p=57;
elif trace_header_location_fmt == '3':
    inline_p=5;xline_p=21;x_cor_p=53;y_cor_p=57;
else:
    inline_p = int(input("Input inline position:"))
    xnline_p = int(input("Input xnline position:"))
    x_cor_p = int(input("Input X cordinate position:"))
    y_cor_p = int(input("Input Y cordinate position:"))
# initial the segy information
x = read_3d_segy.segy3d(inline_p, 4, 'i', xline_p, 4, 'i',\
                             x_cor_p, 4, 'i', y_cor_p, 4, 'i')
x.read_segy_file(segy_in)
(number_of_sample, sample_intervel) = x.init_binary_header()
(inline_start, inline_end, xline_start, xline_end) = x.segy_information()
depth = np.linspace(0,-(number_of_sample-1)*sample_intervel,number_of_sample)

# From keyboard input inline or xline you want to plot
inlineORxline = input("Inline or xline do you want to plot\
(1 for inline, 2 for xline):")
if inlineORxline == '1':
    inline_start = inline_end = int(input("Input number of inline:\n"))
else:
    xline_start = xline_end = int(input("Input number of xline:\n"))

#plot inline or xline
if inline_start == inline_end:
    print("============ PLOT INLINE ",inline_start," ============")
    trace_lens = xline_end - xline_start + 1
    trace = np.ndarray(shape=(trace_lens,number_of_sample))
    for i in range(0,trace_lens):
        trace[i] = x.read_ibmfloat_data(inline_start,xline_start+i)

elif xline_start == xline_end:
    print("============= PLOT XLINE ",xline_start," ==============")
    trace_lens = inline_end - inline_start + 1
    trace = np.ndarray(shape=(trace_lens,number_of_sample))
    for i in range(0,trace_lens):
        trace[i] = x.read_ibmfloat_data(inline_start+i,xline_start)
else:
    print("======= WRONG　INLINE OR XLINE NUMBER =======")

#plot_wave(trace,depth,number_of_sample,trace_lens,20)
plot_segy.plot_wiggle(trace,depth,number_of_sample,trace_lens,20)
