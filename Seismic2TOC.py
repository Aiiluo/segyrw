# -*- coding: utf-8 -*-
"""
This applacation is made for predicting the TOC data from Acoustic Impandence cube or Seismic data.
@author: Aiiluo
"""
print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
import read_3d_segy
import struct
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn import cross_validation, ensemble, metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
from sklearn import tree

# #############################################################################
# Load fit function data
well_data = np.loadtxt('all well.txt')
X = well_data[:, 0:1]
y = well_data[:, 1:2]

# # #############################################################################
# Standardize the input data
# # Stadardize X
# scx = StandardScaler()
# scx.fit(X)
# X_std = scx.transform(X)
# # Stadardize Y
# scy = StandardScaler()
# scx.fit(y)
# y_std = scx.transform(y) 

# #############################################################################
# Random Tree Predict
max_depth = 20
regr_multirf = MultiOutputRegressor(RandomForestRegressor(max_depth=max_depth,
                                                    random_state=0, 
                                                    n_estimators=10))
regr_multirf.fit(X, y)
# #############################################################################
# Use read_3d_segy class to get seismic imformation
# segy_in = r'F:\AT12649.sgy'
# x = read_3d_segy.segy3d()
segy_in = r'K:\tp_share\petrel_bbw\SEGY\WXN_AI_Petrel.sgy'
x = read_3d_segy.segy3d(5,4,'i',21,4,'i',73,4,'i',77,4,'i')
x.read_segy_file(segy_in)
x.read_text_header()
x.segy_information()

# #############################################################################
# From segy information, define the format of seimicdata
number_of_sample = 3072
inline_start = 3031 
inline_end = 4901
xline_start = 2270
xline_end = 2570
trace_position = 0


# #############################################################################
# Read seismic data, compute seismic data and write it in segy formation file
segy_out = 'wxn.sgy'

# Read the fist 3600bytes data of EBCDIC header and binary header, then write it
# to the segy_out file. 
in_file = open(segy_in, 'rb')
in_file.seek(0)
segy_header = in_file.read(3600) #读取文本头和二进制头
with open(segy_out, 'wb') as out_file: 
    out_file.write(segy_header) #写入原始文本头和二进制头

# Read 240bytes of trace header and trace data, then write to segy_out file.
for inline in range(inline_start, inline_end+1):
        for xline in range(xline_start, xline_end+1):
            trace = [0] * number_of_sample # define lens of trace
            trace = np.zeros(number_of_sample, dtype=float)
            trace = x.read_ibmfloat_data(inline, xline) # read a trace of seismic data
            trace_header_position = 3600+(240+number_of_sample*4)*\
            trace_position # seek position increase
            #Write trace header to the segy_out file
            with open(segy_out, 'ab') as out_file:
                in_file.seek(trace_header_position)
                trace_header = in_file.read(240)
                out_file.write(trace_header) 
            #Write trace data to segy_out file
            with open(segy_out, 'ab') as out_file:  
                for one_trace in trace:
                    # one_trace_toc = regr_multirf.predict(one_trace) # RandomForest predict 
                    one_trace_IBM = x.float2IBM(one_trace) # transform float to IBM float 
                    trace_bin = struct.pack('>I', one_trace_IBM) # pack trace data
                    out_file.write(trace_bin) 
                                                                  
            trace_position = trace_position + 1
            print('Trace:%d, Inline:%d, Xline:%d' %(trace_position, inline,
                                                    xline), end='\r')
                
in_file.close

