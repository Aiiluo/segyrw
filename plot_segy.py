# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 23:03:41 2018

@author: Aiiluo
"""
import numpy as np
import matplotlib.pyplot as plt


trace_decimation = 5
gain = 5



def plot_wave(trace,depth,ns,trace_number,inc):
    inc_go = 0
    plt.figure(figsize=(100,60))
    for line in range(0,trace_number,trace_decimation):
        for num in range(0,ns):
            trace[line][num] = trace[line][num] * gain + inc_go
        plt.plot(trace[line],depth,color="black")
        inc_go = inc_go + inc #每一道的间隔
    plt.show()
    # plt.savefig("Line.png", dpi=150) 
    
def plot_wiggle(trace,depth,ns,trace_number,inc):
    inc_go = 0
    wiggle = np.asarray(trace)
    plt.figure(figsize=(100,120))
    for line in range(0,trace_number,trace_decimation):
        for num in range(0,ns):
            trace[line][num] = trace[line][num] * gain + inc_go 
        wiggle = inc_go
        plt.fill_betweenx(depth,trace[line],wiggle,color="black",where=trace[line]>wiggle)
        plt.plot(trace[line],depth,color="black") 
        inc_go = inc_go + inc #每一道的间隔
        print("Ploting:%d%%"%(line*100/trace_number), end='\r', flush=True)

    plt.show() 
    # plt.savefig("Line.png", dpi=150)

