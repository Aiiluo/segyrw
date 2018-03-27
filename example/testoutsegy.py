import numpy as np
import matplotlib.pyplot as plt
import read_3d_segy
import plot_segy
import struct
import os

segy_file = r'wxn_2270.sgy'
x = read_3d_segy.segy3d()
x.read_segy_file(segy_file)

#初始化地震道头数据
(number_of_sample, sample_intervel) = x.init_binary_header()
(inline_start, inline_end, xline_start, xline_end) = x.segy_information()
inline_lens = inline_end - inline_start
xline_lens = xline_end - xline_start