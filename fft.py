# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 15:40:42 2018

@author: proc1
"""
import numpy as np
import matplotlib.pyplot as plt
import read_3d_segy
from plot_segy import *
from scipy.fftpack import fft,ifft

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
depth = np.linspace(0,-(number_of_sample-1)*sample_intervel,number_of_sample)

one_trace = x.read_int8_data(400,2000)
fft_trace = fft(one_trace)

plt.figure()
plt.subplot(211)
plt.plot(one_trace)
plt.subplot(212)
plt.plot(fft_trace)



#from scipy.fftpack import fft
## Number of sample points
#N = 600
## sample spacing
#T = 1.0 / 800.0
#x = np.linspace(0.0, N*T, N)
#y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
#yf = fft(y)
#xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
#import matplotlib.pyplot as plt
#plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
#plt.grid()
#plt.show()