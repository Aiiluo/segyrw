# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 18:45:12 2018

@author: Aiiluo
"""

import numpy as np
import matplotlib.pyplot as plt
import read_3d_segy
from plot_segy import *
import struct
import os

segy_file = r'K:\tp_share\2018年烃源岩评价项目\原始数据\3T3605\weixinan\AT12649.sgy'
x = read_3d_segy.segy3d()
x.read_segy_file(segy_file)
x.segy_information()

number_of_sample = 3072
inline_start = 3031
inline_end = 3201
xline_start = 2270
xline_end = 2271
trace_position = 0

in_file = open(segy_file, 'rb')
in_file.seek(0)
segy_header = in_file.read(3600) #读取文本头和二进制头


with open('wxn_all.sgy', 'wb') as out_file: 
    out_file.write(segy_header) #写入原始文本头和二进制头

for inline in range(inline_start, inline_end):
        for xline in range(xline_start, xline_end):
            trace = [0] * number_of_sample
            trace = x.read_ibmfloat_data(inline, xline)
            trace_header_position = 3600+(240+number_of_sample*4)*\
            trace_position
            with open('wxn_all.sgy', 'ab') as out_file:             
                in_file.seek(trace_header_position)
                trace_header = in_file.read(240)
                out_file.write(trace_header) #读取原始道头写入新文件
            with open('wxn_all.sgy', 'ab') as out_file:  
                for one_trace in trace:
                    one_trace_IBM = x.float2IBM(one_trace)
                    trace_bin = struct.pack('>I', one_trace_IBM)
                    out_file.write(trace_bin) #读取道，转换为float，再转换为IBMfloat
                                              #然后写入文件                    
            trace_position = trace_position + 1
            print('Trace:%d, Inline:%d, Xline:%d' %(trace_position, inline,
                                                    xline))
                
in_file.close

