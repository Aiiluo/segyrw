# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 21:28:04 2018

@author: chenp
"""

import struct
import read_segy_header
import numpy as np

class segy3d(read_segy_header.segyheader):
    
    def __init___(self):
        read_segy_header.segyheader.__init__(self)
        self.init_binary_header()
#        (self.inline_start,self.xline_start,self.X_min,self.Y_min) = self.read_control_file(1)
#        (self.inline_end,self.xline_end,self.X_max,self.Y_max) = self.read_last_trace_header()
#        self.inline_lens = self.inline_end - self.inline_start + 1
#        self.xline_lens = self.xline_end - self.xline_start + 1
#        self.trace_count = self.inline_lens * self.xline_lens


        

    def segy_information(self):
        self.read_binary_header()
        
        (self.inline_start,self.xline_start,self.X_min,self.Y_min) = self.read_control_file(1)
        (self.inline_end,self.xline_end,self.X_max,self.Y_max) = self.read_last_trace_header()
        self.inline_lens = self.inline_end - self.inline_start + 1
        self.xline_lens = self.xline_end - self.xline_start + 1
        self.trace_count = self.inline_lens * self.xline_lens
        print("=================== Segy Information =======================")
        print("inline:",self.inline_start," to ",self.inline_end)
        print("xline:",self.xline_start," to ",self.xline_end)
        print("coordinate X:",self.X_min," to ",self.X_max)
        print("coordinate Y:",self.Y_min," to ",self.Y_max)
        print("inline lens:",self.inline_lens)
        print("xline lens:",self.xline_lens)

        return self.inline_start, self.inline_end, self.xline_start, self.xline_end
        
    
    
    def read_3dSegy_data(self,inline,xline):
        
        
        if self.data_fmt == 1:
            self.read_ibmfloat_data(inline,xline)
        elif self.data_fmt == 2:
            self.read_int32_data(inline,xline)
        elif self.data_fmt == 3:
            self.read_int16_data(inline,xline)
        elif self.data_fmt == 5:
            self.read_IEEEfloat_data(inline,xline)
        elif self.data_fmt == 8:
            self.read_int8_data(inline,xline)
        else:
            return "This format is no use now."
    
    def read_int32_data(self, inline, xline):
        return 0

    def read_int16_data(self, inline, xline):
        return 0

    def read_IEEEfloat_data(self, inline, xline):
        return 0

    def read_int8_data(self, inline, xline):
        
        self.init_binary_header()
        (self.inline_start,self.xline_start,self.X_min,self.Y_min) = self.read_control_file(1)
        (self.inline_end,self.xline_end,self.X_max,self.Y_max) = self.read_last_trace_header()
        self.inline_lens = self.inline_end - self.inline_start + 1
        self.xline_lens = self.xline_end - self.xline_start + 1
        self.trace_count = self.inline_lens * self.xline_lens
        
                
        trace_position = (inline-self.inline_start)*self.xline_lens + (xline-self.xline_start)
        start_number = self.text_header_lens+self.bin_header_lens
        data_lens = self.number_of_sample * self.sample_fmt
        trace_lens = data_lens + self.trace_header_lens
        start = start_number+trace_position*trace_lens+self.trace_header_lens
        unpack_fmt = '>' + str(self.number_of_sample) + 'b'
        
        Int8 = np.zeros(self.number_of_sample,dtype=np.int8)
        with open(self.segy_file,'rb') as in_file:
            in_file.seek(start)
            data = in_file.read(data_lens)
            Int8 = np.asarray(struct.unpack(unpack_fmt,data))
            
        return Int8
    
    def IBM2float(self, ibm_float):
        p24 = float(pow(2, 24))
        if ibm_float == 0:
            return 0.0
        sign = ibm_float >> 31 & 0x01
        exponent = ibm_float >> 24 & 0x7f 
        mantissa = (ibm_float & 0x00ffffff)/p24 
        return (1-2*sign)*(mantissa)*pow(16, exponent-64)
#        return pow(-1, sign)*(mantissa)*pow(16, exponent-64)
    
    
    
    def float2IBM(self, float32):
        # This function is for transform pc float to IBM float
        # 符号
        if float32 < 0:
            sign = 1
        else:
            sign = 0
        #abs float32
        float32 = float32*(1-2*sign)
        exp = 0
        floatc = float32
        
        if floatc > 0: #非零值才计算
            if int(floatc) > 0:
                exp = exp + 1
                while int(floatc/16) > 0:
                    exp = exp + 1
                    floatc = floatc/16
            else:
                while int(floatc)*16 == 0:
                    exp = exp - 1
                    floatc = floatc*16
                exp = exp + 1
        exponent = exp + 64
        
        mant = float32 * pow(16, -exp) #去掉float32的整数，把它变成全小数
        mantissa = int(mant * pow(2, 24))#将变成小数的float32左移24位取整
        
        return (sign<<31) | (exponent<<24) | mantissa
                       
        
    
    def read_ibmfloat_data(self, inline, xline):
    # The function is to read trace data of 3D seismic segy data. When you input inline and 
    # xlineinformation, you can get the data of the trace. And then the function can transform 
    # the IBM float to pc float 

        self.init_binary_header() # initail the header information
        (self.inline_start, self.xline_start, self.X_min, self.Y_min) = \
        self.read_control_file(1)
        (self.inline_end, self.xline_end, self.X_max, self.Y_max) =\
         self.read_last_trace_header()
        self.inline_lens = self.inline_end - self.inline_start + 1
        self.xline_lens = self.xline_end - self.xline_start + 1
        self.trace_count = self.inline_lens * self.xline_lens
        
                
        trace_position = (inline-self.inline_start)*self.xline_lens + \
        (xline-self.xline_start)
        start_number = self.text_header_lens+self.bin_header_lens
        data_lens = self.number_of_sample * self.sample_fmt
        trace_lens = data_lens + self.trace_header_lens
        start = start_number+trace_position*trace_lens+self.trace_header_lens
        unpack_fmt = '>' + str(self.number_of_sample) + 'i'
        # IBM_float = [0] * self.number_of_sample       
        IBM_float = np.zeros(self.number_of_sample, dtype=np.int32)
        # PC_float = [0] * self.number_of_sample
        PC_float = np.zeros(self.number_of_sample, dtype=np.float)
        with open(self.segy_file, 'rb') as in_file:
            in_file.seek(start)
            data = in_file.read(data_lens)
#            IBM_float = np.asarray(struct.unpack(unpack_fmt,data))
            IBM_float = list(struct.unpack(unpack_fmt, data))
        
        for i in range(0, self.number_of_sample):
            PC_float[i] = self.IBM2float(IBM_float[i])
            
        return PC_float

        
   
    
            
        