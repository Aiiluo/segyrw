# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 16:24:06 2018

@author: Judyan
"""
import numpy as np
import matplotlib.pyplot as plt
import read_3d_segy

segy = segy3d()
segy.read_segy_file(r'D:\hj_3d_2015_final_psdm-t_16y03.sgy')
#h.read_segy_file(r'I:\3T3605\weixinan\AT12649.sgy')
segy.trace_header_position(221,4,'i',21,4,'i',73,4,'i',77,4,'i')
segy.segy_information()

inline = np.zeros((2746,3500),dtype=np.int8)
j=0
for i in range(313,2746):
    inline[j] = segy.read_Int8_data(550,i)
    j = j + 1


#segy.read_binary_header    
#x = segy.read_Int8_data(159,313)
#plt.figure()
#plt.plot(x)
 

plt.figure(figsize=(50,100))
plt.subplot(111)
inc = 0
plt_lone = list(range(3500))
for line in range(0,2746,5):
    for num in range(0,3500):
        inline[line][num] += inc
#        x2[line][num] = inc
#    plt.fill_between(plt_lone,inline[line],x2[line],color='grey')
    plt.plot(inline[line],color="black")
    inc += 40 #每一道的间隔
    

plt.savefig("2018114.png", dpi=150) 
