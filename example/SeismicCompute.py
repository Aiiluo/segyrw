# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 18:45:12 2018

@author: Aiiluo
"""

import numpy as np
import matplotlib.pyplot as plt
import read_3d_segy
import plot_segy
import struct
import os

segy_file = r'K:\tp_share\2018年烃源岩评价项目\原始数据\3T3605\weixinan\AT12649.sgy'
segy_out = 'wxn_2270.sgy'
x = read_3d_segy.segy3d()
x.read_segy_file(segy_file)

#初始化地震道头数据
(number_of_sample, sample_intervel) = x.init_binary_header()
(inline_start, inline_end, xline_start, xline_end) = x.segy_information()
inline_lens = inline_end - inline_start +1
xline_lens = xline_end - xline_start +1

#设定要计算得inline，xline范围
r_inline_start, r_inline_end = 3031, 4901
r_xline_start, r_xline_end = 2270, 2281

in_file = open(segy_file, 'rb')
in_file.seek(0)
segy_header = in_file.read(3600) #读取文本头和二进制头


with open(segy_out, 'wb') as out_file: 
    out_file.write(segy_header) #写入原始文本头和二进制头

for inline in range(r_inline_start, r_inline_end+1):
        for xline in range(r_xline_start, r_xline_end+1):
            trace = np.zeros(number_of_sample, dtype=np.float) 
            trace = x.read_ibmfloat_data(inline, xline)
            #定位240字节道头的起始位置
            trace_header_position = 3600+(240+number_of_sample*4)*((inline-\
                                    inline_start)*xline_lens+(xline-xline_start))
            with open(segy_out, 'ab') as out_file:             
                in_file.seek(trace_header_position)
                trace_header = in_file.read(240)
                out_file.write(trace_header) #读取原始道头写入新文件
            with open(segy_out, 'ab') as out_file:  
                for one_trace in trace:
                    one_trace_IBM = x.float2IBM(one_trace)
                    trace_bin = struct.pack('>I', one_trace_IBM)
                    out_file.write(trace_bin) #读取道，转换为float，再转换为IBMfloat
                                              #然后写入文件   
            print('Writing: Inline:%d, Xline:%d' %(inline,
                                                    xline))
in_file.close

